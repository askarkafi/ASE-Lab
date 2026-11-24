"""Supervised, read-only repository analysis on a fixed Git revision."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import uuid

from . import runner


UNCERTAINTY_FIELDS = {
    "scope": "Scope inspected (agent report)",
    "unresolved": "What remains unresolved",
    "needed_evidence": "Evidence needed",
}
INCONCLUSIVE_MESSAGE = "The inspected evidence was insufficient to answer the question."
EVIDENCE_LABELS = {
    "diagnostic_output": "Relevant logs, error output, or a stack trace",
    "reproduction": "A failing input or reproduction steps",
    "affected_component": "The affected API, command, or component",
    "expected_behavior": "Expected behavior or acceptance criteria",
    "source_context": "Additional source, tests, or documentation",
}


def validate(task):
    fields = {"schema_version", "task_id", "capability", "question", "repository",
              "revision", "model_profile", "limits"}
    if (not isinstance(task, dict) or set(task) != fields or
            type(task["schema_version"]) is not int or task["schema_version"] != 1):
        raise ValueError("Expected exactly the version 1 analysis task fields")
    if task["capability"] != "repository_analysis":
        raise ValueError("Unsupported capability")
    for key in ("task_id", "question", "repository", "revision", "model_profile"):
        if not isinstance(task[key], str) or not task[key].strip():
            raise ValueError("Invalid " + key)
    if not re.fullmatch(r"[0-9a-f]{40}", task["revision"]):
        raise ValueError("revision must be a full commit SHA")
    if not Path(task["repository"]).is_absolute() or not Path(task["repository"]).is_dir():
        raise ValueError("repository must be an existing absolute local directory")
    if task["model_profile"] != "deepseek-flash-relay":
        raise ValueError("Unsupported model profile")
    limits = task["limits"]
    if not isinstance(limits, dict) or set(limits) != set(runner.DEFAULT_LIMITS):
        raise ValueError("Invalid limit fields")
    for key, maximum in runner.DEFAULT_LIMITS.items():
        if type(limits[key]) is not int or not 1 <= limits[key] <= maximum:
            raise ValueError("Invalid limit " + key)
    return task


def snapshot(work):
    """Capture every file, directory and mode, including ignored and untracked paths."""
    records = {}
    def fail_walk(exc):
        raise exc

    for base, dirs, files in os.walk(work, followlinks=False, onerror=fail_walk):
        for name in dirs + files:
            path = Path(base) / name
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode) or not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                raise ValueError("Workspace contains an unsupported file type")
            rel = path.relative_to(work).as_posix()
            digest = hashlib.sha256(path.read_bytes()).hexdigest() if stat.S_ISREG(mode) else None
            records[rel] = (stat.S_IMODE(mode), digest)
    return records


def final_message(log):
    final = None
    finish = None
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict) or event.get("source") != "agent":
            continue
        if event.get("kind") == "ActionEvent" and event.get("tool_name") == "finish":
            action = event.get("action")
            if isinstance(action, dict) and action.get("kind") == "FinishAction" and isinstance(action.get("message"), str):
                finish = action["message"]
            continue
        if event.get("kind") != "MessageEvent":
            continue
        message = event.get("llm_message")
        if isinstance(message, dict) and isinstance(message.get("content"), list):
            final = "\n".join(part["text"] for part in message["content"]
                              if isinstance(part, dict) and isinstance(part.get("text"), str))
    return finish if finish is not None else final


def collect_usage(out, result):
    log = out / "relay.log"
    if not log.exists():
        return
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            record = json.loads(line)
        except ValueError:
            continue
        if isinstance(record, dict) and record.get("event") == "upstream_transport_error":
            result.setdefault("relay_errors", []).append(record)
            result["provider_usage_incomplete"] = True
        if isinstance(record, dict) and "total_tokens" in record and record.get("event") != "upstream_transport_error":
            result["provider_usage"] = record


def verify_answer(message, meta, work):
    try:
        candidate = message.strip()
        fenced = re.fullmatch(r"```(?:json)?\s*\n(.*?)\n```", candidate, re.DOTALL)
        answer = json.loads(fenced.group(1) if fenced else candidate)
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("Final answer is not a JSON object") from exc
    if not isinstance(answer, dict) or set(answer) != {"observations", "interpretation", "uncertainty"}:
        raise ValueError("Invalid answer fields")
    if not isinstance(answer["observations"], list) or len(answer["observations"]) > 20:
        raise ValueError("Expected at most 20 cited observations")
    interpretation, uncertainty = answer["interpretation"], answer["uncertainty"]
    if not isinstance(interpretation, str) or len(interpretation) > 12000:
        raise ValueError("Invalid interpretation")
    if not isinstance(uncertainty, dict) or uncertainty.keys() != UNCERTAINTY_FIELDS.keys():
        raise ValueError("Invalid structured uncertainty")
    if not answer["observations"]:
        rationale = (uncertainty["scope"], uncertainty["unresolved"])
        if interpretation.strip() or any(not isinstance(v, str) or not v.strip() or len(v) > 4000 for v in rationale):
            raise ValueError("Inconclusive answer needs scope and rationale, with empty interpretation")
        needed = uncertainty["needed_evidence"]
        if (not isinstance(needed, list) or not 1 <= len(needed) <= len(EVIDENCE_LABELS)
                or any(not isinstance(kind, str) or kind not in EVIDENCE_LABELS for kind in needed)
                or len(set(needed)) != len(needed)):
            raise ValueError("Inconclusive answer needs distinct evidence categories")
        # The original narrative is available in the finish trace for review.
        answer["uncertainty"] = {
            "scope": "",
            "unresolved": INCONCLUSIVE_MESSAGE,
            "needed_evidence": "\n".join("- " + EVIDENCE_LABELS[kind] for kind in needed),
        }
        return answer
    if any(not isinstance(value, str) or len(value) > 4000 for value in uncertainty.values()):
        raise ValueError("Invalid structured uncertainty")
    tracked = set(filter(None, runner.git(meta, work, "ls-files", "-z").decode().split("\0")))
    for item in answer["observations"]:
        if not isinstance(item, dict) or set(item) != {"path", "start_line", "end_line", "finding"}:
            raise ValueError("Invalid observation fields")
        name = item["path"]
        if (not isinstance(name, str) or name not in tracked or "\\" in name or ":" in name
                or PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts):
            raise ValueError("Citation does not name a tracked file")
        start, end = item["start_line"], item["end_line"]
        if type(start) is not int or type(end) is not int or not 1 <= start <= end <= start + 39:
            raise ValueError("Invalid citation line range")
        if not isinstance(item["finding"], str) or not item["finding"].strip() or len(item["finding"]) > 4000:
            raise ValueError("Invalid finding")
        path = work / name
        if path.is_symlink() or not path.is_file():
            raise ValueError("Citation does not name a regular file")
        try:
            lines = path.read_text(encoding="utf-8").removesuffix("\n").split("\n")
        except UnicodeDecodeError as exc:
            raise ValueError("Citation is not UTF-8 text") from exc
        if end > len(lines):
            raise ValueError("Citation line range exceeds file length")
        quote = "\n".join(lines[start - 1:end])
        if not quote.strip() or len(quote) > 8000 or "\0" in quote:
            raise ValueError("Invalid source excerpt")
        item["quote"] = quote
    return answer


def save_result(out, result):
    result.setdefault("finished_at", datetime.now(timezone.utc).isoformat())
    temporary = out / "result.json.tmp"
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(out / "result.json")
    lines = ["# ASE-Lab repository analysis", "", "Status: " + result["run_status"],
             "Outcome: " + result["outcome"], "", "## Independent observations",
             "- Revision: " + result.get("revision", "unknown"),
             "- Workspace unchanged: " + str(result.get("workspace_unchanged", "unverified")),
             "- Changed workspace paths: " + json.dumps(result.get("changed_files", [])),
             "- " + result["reason"]]
    if result.get("provider_usage"):
        lines.append("- Provider-reported usage: " + json.dumps(result["provider_usage"]))
    if result.get("provider_usage_incomplete"):
        lines.append("- Provider usage incomplete: at least one upstream request had no usage response")
        lines.append("- Relay transport errors: " + json.dumps(result["relay_errors"]))
    answer = result.get("answer")
    if answer:
        lines += ["", "## Agent observations with verified excerpts"]
        if not answer["observations"]:
            lines.append("No positive finding was supported by a verified excerpt.")
        for item in answer["observations"]:
            lines += ["", "### " + item["path"] + ":" + str(item["start_line"]) +
                      "-" + str(item["end_line"]), item["finding"], ""]
            lines += ["    " + line for line in item["quote"].split("\n")]
        if answer["interpretation"].strip():
            lines += ["", "## Agent interpretation", answer["interpretation"]]
        lines += ["", "## Uncertainty"]
        for key, label in UNCERTAINTY_FIELDS.items():
            value = answer["uncertainty"][key]
            if value.strip():
                lines += ["", "### " + label, value]
    else:
        lines += ["", "## Uncertainty", "No verified answer was produced. Review private execution evidence."]
    if result.get("operator_alerts"):
        lines += ["", "## Operator alerts", *["- " + x for x in result["operator_alerts"]]]
    (out / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(task_path, secret, image, output):
    out = output.resolve() / uuid.uuid4().hex
    out.mkdir(parents=True)
    result = dict(schema_version=2, run_id=out.name, started_at=datetime.now(timezone.utc).isoformat(),
                  run_status="not_started", outcome="no_result", reason="", sdk_version="1.62.0",
                  model_profile="deepseek-flash-relay")
    network = "ase-" + out.name[:12]
    relay = network + "-relay"
    created_network = created_relay = False
    try:
        task = validate(json.loads(task_path.read_text(encoding="utf-8-sig")))
        result.update(task_id=task["task_id"], revision=task["revision"], limits=task["limits"])
        if not secret.is_file():
            raise ValueError("Relay secret file is absent")
        if any("," in str(p.resolve()) for p in (out, secret, runner.ROOT)):
            raise ValueError("Docker bind paths cannot contain commas")
        result["phase"] = "docker_preflight"
        runner.command(["docker", "image", "inspect", image])
        image_id = runner.command(["docker", "image", "inspect", "--format", "{{.Id}}", image]).stdout.decode().strip()
        result["image_id"] = image_id
        result["phase"] = "checkout"
        work, meta = out / "workspace", out / "git-metadata"
        runner.command(["git", "clone", "--no-hardlinks", "--no-checkout", "--", task["repository"], str(work)])
        shutil.move(str(work / ".git"), meta)
        runner.git(meta, work, "checkout", "--detach", task["revision"])
        entries = runner.git(meta, work, "ls-files", "--stage").decode()
        if any(line.startswith(("120000 ", "160000 ")) for line in entries.splitlines()):
            raise ValueError("Symlinks and submodules are outside the analysis contract")
        if runner.git(meta, work, "status", "--porcelain"):
            raise ValueError("Starting checkout is not clean")
        before = snapshot(work)
        inputs = out / "input"
        inputs.mkdir()
        worker_task = {key: task[key] for key in ("capability", "question", "revision", "limits")}
        (inputs / "task.json").write_text(json.dumps(worker_task), encoding="utf-8")
        launcher = ("import runpy; from http.server import HTTPServer; "
                    "p=runpy.run_path('/relay.py'); g=p['Handler'].do_POST.__globals__; "
                    "g['KEY']=p['read_key'](); g['remaining']=" +
                    str(min(task["limits"]["model_requests"], task["limits"]["sdk_iterations"])) +
                    "; g['analysis_budget']=True"
                    "; HTTPServer(('0.0.0.0',8080),p['Handler']).serve_forever()")
        result["phase"] = "relay_setup"
        runner.command(["docker", "network", "create", "--internal", network])
        created_network = True
        runner.command(["docker", "create", "--name", relay, "--network", "bridge",
                        "--read-only", "--cap-drop=ALL", "--security-opt=no-new-privileges",
                        "--user", "10001:10001", "--memory", "256m", "--pids-limit", "32",
                        "--mount", "type=bind,src=" + str(secret.resolve()) + ",dst=/run/secrets/deepseek.env,readonly",
                        "--mount", "type=bind,src=" + str(runner.ROOT / "experiments/sdk-feasibility/model_proxy.py") + ",dst=/relay.py,readonly",
                        image_id, "python", "-u", "-c", launcher])
        created_relay = True
        runner.command(["docker", "network", "connect", "--alias", "model-proxy", network, relay])
        runner.command(["docker", "start", relay])
        name = network + "-agent"
        argv = runner.container_args(name, image_id, task["limits"], network, work)
        argv += ["--mount", "type=bind,src=" + str(inputs) + ",dst=/input,readonly",
                 "--mount", "type=bind,src=" + str(runner.ROOT / "ase_lab/worker.py") + ",dst=/worker.py,readonly",
                 image_id, "python", "-u", "/worker.py"]
        result.update(phase="agent", run_status="error")
        observed = runner.bounded(argv, name, task["limits"]["wall_seconds"], out / "agent.log")
        result["agent_process"] = observed
        if observed.get("cleanup_verified") is False:
            result.setdefault("operator_alerts", []).append("Agent container cleanup unverified: " + name)
        result["run_status"] = "limit_reached" if observed.get("reason") == "timeout" else "error"
        trace = (out / "agent.log").read_text(encoding="utf-8", errors="replace")
        summaries = [line.partition("=")[2] for line in trace.splitlines() if line.startswith("ASE_LAB_SDK_SUMMARY=")]
        if summaries:
            result["sdk_reported"] = json.loads(summaries[-1])
        if observed["status"] == "passed" and result.get("sdk_reported", {}).get("status", "").endswith("FINISHED"):
            result["run_status"] = "finished"
        result["phase"] = "inspection"
        after = snapshot(work)
        result["changed_files"] = sorted(name for name in before.keys() | after.keys()
                                         if before.get(name) != after.get(name))
        result["workspace_unchanged"] = not result["changed_files"]
        if not result["workspace_unchanged"]:
            result.update(run_status="error", reason="Repository workspace changed during analysis")
            return out
        if result["run_status"] != "finished":
            result["reason"] = "Agent did not complete; inspect private trace"
            return out
        result["phase"] = "verification"
        result["answer"] = verify_answer(final_message(out / "agent.log"), meta, work)
        if result["answer"]["observations"]:
            result.update(outcome="analysis_report", reason="Cited excerpts verified against the fixed checkout")
        else:
            result.update(outcome="inconclusive", reason="Agent completed without a supported positive finding")
    except KeyboardInterrupt:
        result.update(run_status="interrupted", reason="Interrupted by operator")
    except Exception as exc:
        if result["run_status"] == "finished":
            result["run_status"] = "error"
        if isinstance(exc, subprocess.CalledProcessError):
            (out / "setup-error.log").write_bytes(exc.stderr or b"")
        result["reason"] = type(exc).__name__ + ": " + (str(exc) if isinstance(exc, ValueError) else "See setup and execution prerequisites")
    finally:
        logs = runner.cleanup(["docker", "logs", relay])
        if logs is not None and logs.returncode == 0:
            (out / "relay.log").write_bytes(logs.stdout + logs.stderr)
        if created_relay:
            removed = runner.cleanup(["docker", "rm", "-f", relay])
            if removed is None or removed.returncode != 0:
                result.setdefault("operator_alerts", []).append("Relay container cleanup unverified: " + relay)
        if created_network:
            removed = runner.cleanup(["docker", "network", "rm", network])
            if removed is None or removed.returncode != 0:
                result.setdefault("operator_alerts", []).append("Docker network cleanup unverified: " + network)
        if result.get("operator_alerts"):
            result.update(run_status="error", outcome="no_result")
            result["reason"] += " Operator action required: verify Docker cleanup."
        collect_usage(out, result)
        save_result(out, result)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", type=Path)
    parser.add_argument("--secret-file", required=True, type=Path)
    parser.add_argument("--image", default=runner.DEFAULT_IMAGE)
    parser.add_argument("--output", type=Path, default=runner.ROOT / "runs/analysis")
    args = parser.parse_args()
    out = run(args.task, args.secret_file, args.image, args.output)
    print(out)
    result = json.loads((out / "result.json").read_text(encoding="utf-8"))
    for alert in result.get("operator_alerts", []):
        print("OPERATOR ALERT: " + alert, file=sys.stderr)
    return 0 if result["run_status"] == "finished" and result["outcome"] in {"analysis_report", "inconclusive"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
