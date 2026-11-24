"""A single supervised run using the pinned feasibility image and relay."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMAGE = "ase-lab-feasibility:openhands-1.62.0-locked"
DEFAULT_LIMITS = dict(wall_seconds=900, sdk_iterations=25, model_requests=25,
                      memory_mib=2048, cpus=2, pids=128)


def command(argv, **kwargs):
    return subprocess.run(argv, check=True, capture_output=True, **kwargs)


def validate(task):
    fields = {"schema_version", "task_id", "issue", "repository", "revision",
              "allowed_edit_paths", "validation_commands", "model_profile", "limits"}
    if not isinstance(task, dict) or set(task) != fields or type(task["schema_version"]) is not int or task["schema_version"] != 1:
        raise ValueError("Expected exactly the version 1 task fields")
    for key in ("task_id", "issue", "repository", "revision", "model_profile"):
        if not isinstance(task[key], str) or not task[key].strip():
            raise ValueError("Invalid " + key)
    if not re.fullmatch("[0-9a-f]{40}", task["revision"]):
        raise ValueError("revision must be a full commit SHA")
    if task["model_profile"] != "deepseek-flash-relay":
        raise ValueError("Unsupported model profile")
    if not Path(task["repository"]).is_absolute() or not Path(task["repository"]).is_dir():
        raise ValueError("repository must be an existing absolute local directory")
    paths = task["allowed_edit_paths"]
    if not isinstance(paths, list) or not paths or not all(isinstance(p, str) for p in paths):
        raise ValueError("Expected a nonempty list of edit paths")
    for path in paths:
        p = PurePosixPath(path)
        if (not path or p.is_absolute() or str(p) != path or "\\" in path or ":" in path
                or any(part in ("..", ".git") for part in p.parts)):
            raise ValueError("Unsafe edit path")
    if len(paths) != len(set(paths)):
        raise ValueError("Duplicate edit paths")
    limits = task["limits"]
    if not isinstance(limits, dict) or set(limits) != set(DEFAULT_LIMITS):
        raise ValueError("Invalid limit fields")
    for key, maximum in DEFAULT_LIMITS.items():
        if type(limits[key]) is not int or not 1 <= limits[key] <= maximum:
            raise ValueError("Invalid limit " + key)
    checks = task["validation_commands"]
    if not isinstance(checks, list) or not checks:
        raise ValueError("Expected validation commands")
    seen = set()
    for check in checks:
        if not isinstance(check, dict) or set(check) != {"id", "argv", "timeout_seconds", "after"}:
            raise ValueError("Invalid validation fields")
        if not isinstance(check["id"], str) or not re.fullmatch("[a-z][a-z0-9_-]*", check["id"]):
            raise ValueError("Invalid validation id")
        if check["id"] in {"agent", "relay", "setup-error"}:
            raise ValueError("Validation id conflicts with a reserved evidence file")
        if check["after"] is not None and not isinstance(check["after"], str):
            raise ValueError("Validation dependency must be a command id")
        if check["id"] in seen or (check["after"] is not None and check["after"] not in seen):
            raise ValueError("Invalid validation dependency")
        seen.add(check["id"])
        if (not isinstance(check["argv"], list) or not check["argv"]
                or not all(isinstance(a, str) and "\x00" not in a for a in check["argv"])
                or not check["argv"][0]):
            raise ValueError("Invalid command argv")
        if type(check["timeout_seconds"]) is not int or not 1 <= check["timeout_seconds"] <= 900:
            raise ValueError("Invalid validation timeout")
    return task


def git(meta, work, *args):
    return command(["git", "-c", "core.autocrlf=false", "-c", "core.fsmonitor=false",
                    "--git-dir=" + str(meta), "--work-tree=" + str(work), *args]).stdout


def inspect_changes(meta, work, allowed):
    # Index and Git config are outside every agent mount.
    for path in work.rglob("*"):
        if path.is_symlink():
            raise ValueError("Workspace contains a symbolic link")
    if (work / ".git").exists():
        raise ValueError("Agent created repository metadata inside the workspace")
    tracked = git(meta, work, "diff", "--name-only", "-z", "HEAD").decode().split("\0")
    added = git(meta, work, "ls-files", "--others", "-z").decode().split("\0")
    changed = sorted(set(filter(None, tracked + added)))
    violations = []
    for name in changed:
        path = work / name
        if name not in allowed or path.is_symlink() or not path.is_file() or name in added:
            violations.append(name)
    diff = git(meta, work, "diff", "--no-ext-diff", "--no-textconv", "--binary", "HEAD")
    return changed, violations, diff


def container_args(name, image, limits, network, work, writable=False):
    return ["docker", "run", "--name", name, "--network", network,
            "--read-only", "--cap-drop=ALL", "--security-opt=no-new-privileges",
            "--user", "10001:10001", "--memory", str(limits["memory_mib"]) + "m",
            "--cpus", str(limits["cpus"]), "--pids-limit", str(limits["pids"]),
            "--tmpfs", "/tmp:rw,nosuid,size=128m", "-e", "HOME=/tmp",
            "-e", "PYTHONDONTWRITEBYTECODE=1",
            "--mount", "type=bind,src=" + str(work) + ",dst=/work" + ("" if writable else ",readonly")]


def bounded(argv, name, timeout, log):
    start = time.monotonic()
    result = None
    try:
        with log.open("wb") as stream:
            proc = subprocess.run(argv, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
        result = {"status": "passed" if proc.returncode == 0 else "failed",
                  "exit_code": proc.returncode, "seconds": round(time.monotonic() - start, 3)}
        if result["seconds"] > timeout:
            result.update(status="error", reason="timeout", deadline_overrun=True)
            return result
        if proc.returncode in (125, 126, 127):
            result.update(status="error", reason="Container or command could not start")
        return result
    except subprocess.TimeoutExpired:
        result = {"status": "error", "exit_code": None, "reason": "timeout",
                  "seconds": round(time.monotonic() - start, 3)}
        return result
    finally:
        removed = cleanup(["docker", "rm", "-f", name])
        if result is not None and (removed is None or removed.returncode != 0):
            result.update(status="error", cleanup_verified=False)
            result.setdefault("reason", "Container cleanup unverified")


def cleanup(argv):
    try:
        return subprocess.run(argv, capture_output=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None


def collect_evidence(out, result):
    agent_log = out / "agent.log"
    if agent_log.exists():
        for line in agent_log.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if isinstance(event, dict) and event.get("kind") == "MessageEvent" and event.get("source") == "agent":
                message = event.get("llm_message")
                if not isinstance(message, dict) or not isinstance(message.get("content"), list):
                    continue
                content = message["content"]
                result["agent_interpretation"] = "\n".join(
                    part["text"] for part in content if isinstance(part, dict) and isinstance(part.get("text"), str))
    relay_log = out / "relay.log"
    if relay_log.exists():
        for line in relay_log.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                usage = json.loads(line)
            except ValueError:
                continue
            if isinstance(usage, dict) and "total_tokens" in usage:
                result["provider_usage"] = usage


def save_result(out, result):
    collect_evidence(out, result)
    result.setdefault("finished_at", datetime.now(timezone.utc).isoformat())
    temp = out / "result.json.tmp"
    temp.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(out / "result.json")
    lines = ["# ASE-Lab private run report", "", "Status: " + result["run_status"],
             "Outcome: " + result["outcome"], "", "## Independent observations",
             result["reason"], "", json.dumps(result.get("changed_files", [])),
             "", "## Validation"]
    for check in result["validation"]:
        lines.append("- " + check["id"] + ": " + check["status"] +
                     " — " + json.dumps(check["argv"]))
    lines += ["", "## Agent interpretation",
              result.get("agent_interpretation", "No final explanation captured; see private agent.log."),
              "", "## Uncertainty",
              "Model and tool output is untrusted. Human patch review is required.",
              "A passing command is evidence of its exit status, not patch correctness.",
              "Raw logs and patches require content review before publication.",
              "SDK monetary budget enforcement and exhaustive limit behavior are unverified."]
    if result.get("operator_alerts"):
        lines += ["", "## Operator alerts", *["- " + item for item in result["operator_alerts"]]]
    (out / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(task_path, secret, image, output):
    out = output.resolve() / uuid.uuid4().hex
    out.mkdir(parents=True)
    result = dict(schema_version=2, run_id=out.name, started_at=datetime.now(timezone.utc).isoformat(),
                  run_status="not_started", outcome="no_result", reason="", validation=[],
                  sdk_version="1.62.0", model_profile="deepseek-flash-relay")
    network = "ase-" + out.name[:12]
    relay = network + "-relay"
    created_network = False
    created_relay = False
    try:
        task = validate(json.loads(task_path.read_text(encoding="utf-8-sig")))
        result.update(task_id=task["task_id"], revision=task["revision"], limits=task["limits"])
        result["validation"] = [dict(c, status="not_run", reason="Run has not reached validation")
                                for c in task["validation_commands"]]
        if not secret.is_file():
            raise ValueError("Relay secret file is absent")
        if "," in str(out) or "," in str(secret.resolve()) or "," in str(ROOT):
            raise ValueError("Docker bind paths cannot contain commas")
        result["phase"] = "docker_preflight"
        command(["docker", "image", "inspect", image])
        image_id = command(["docker", "image", "inspect", "--format", "{{.Id}}", image]).stdout.decode().strip()
        result["image_id"] = image_id
        result["phase"] = "checkout"
        work, meta = out / "workspace", out / "git-metadata"
        command(["git", "clone", "--no-hardlinks", "--no-checkout", "--", task["repository"], str(work)])
        shutil.move(str(work / ".git"), meta)
        git(meta, work, "checkout", "--detach", task["revision"])
        entries = git(meta, work, "ls-files", "--stage").decode()
        if any(line.startswith(("120000 ", "160000 ")) for line in entries.splitlines()):
            raise ValueError("Symlinks and submodules are outside the initial task contract")
        tracked = git(meta, work, "ls-files", "-z").decode().split("\0")
        if any(p not in tracked or not (work / p).is_file() for p in task["allowed_edit_paths"]):
            raise ValueError("Every permitted edit must name an existing tracked file")
        if git(meta, work, "status", "--porcelain"):
            raise ValueError("Starting checkout is not clean")
        inputs = out / "input"
        inputs.mkdir()
        (inputs / "task.json").write_text(json.dumps(task), encoding="utf-8")
        relay_source = ROOT / "experiments/sdk-feasibility/model_proxy.py"
        # Reuse the observed relay, configuring its request ceiling in a trusted wrapper.
        launcher = ("import runpy; from http.server import HTTPServer; "
                    "p=runpy.run_path('/relay.py'); "
                    "g=p['Handler'].do_POST.__globals__; "
                    "g['KEY']=p['read_key'](); g['remaining']=" +
                    str(task["limits"]["model_requests"]) +
                    "; HTTPServer(('0.0.0.0',8080),p['Handler']).serve_forever()")
        result["phase"] = "relay_setup"
        command(["docker", "network", "create", "--internal", network])
        created_network = True
        command(["docker", "create", "--name", relay, "--network", "bridge",
                 "--read-only", "--cap-drop=ALL", "--security-opt=no-new-privileges",
                 "--user", "10001:10001", "--memory", "256m", "--pids-limit", "32",
                 "--mount", "type=bind,src=" + str(secret.resolve()) + ",dst=/run/secrets/deepseek.env,readonly",
                 "--mount", "type=bind,src=" + str(relay_source) + ",dst=/relay.py,readonly",
                 image_id, "python", "-u", "-c", launcher])
        created_relay = True
        command(["docker", "network", "connect", "--alias", "model-proxy", network, relay])
        command(["docker", "start", relay])
        name = network + "-agent"
        argv = container_args(name, image_id, task["limits"], network, work, writable=True)
        argv += ["--mount", "type=bind,src=" + str(inputs) + ",dst=/input,readonly",
                 "--mount", "type=bind,src=" + str(ROOT / "ase_lab/worker.py") + ",dst=/worker.py,readonly",
                 image_id, "python", "-u", "/worker.py"]
        result["phase"] = "agent"
        result["run_status"] = "error"
        observed = bounded(argv, name, task["limits"]["wall_seconds"], out / "agent.log")
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
        changed, violations, diff = inspect_changes(meta, work, task["allowed_edit_paths"])
        result.update(changed_files=changed, scope_violations=violations)
        if violations:
            result["reason"] = "Rejected changes outside the permitted existing-file scope"
            return out
        if result["run_status"] != "finished":
            result["reason"] = "Agent did not complete; inspect private trace for failure and unfinished work"
            return out
        result["phase"] = "validation"
        frozen = out / "validation-workspace"
        shutil.copytree(work, frozen)
        statuses = {}
        for record in result["validation"]:
            if record["after"] and statuses[record["after"]] != "passed":
                record["reason"] = "Prerequisite validation did not pass"
            else:
                name = network + "-" + record["id"]
                argv = container_args(name, image_id, task["limits"], "none", frozen)
                observed = bounded(argv + [image_id] + record["argv"], name,
                                   record["timeout_seconds"], out / (record["id"] + ".log"))
                record.pop("reason", None)
                record.update(observed, evidence=record["id"] + ".log")
                if observed.get("cleanup_verified") is False:
                    result.setdefault("operator_alerts", []).append("Validation container cleanup unverified: " + name)
            statuses[record["id"]] = record["status"]
        if diff:
            (out / "proposal.patch").write_bytes(diff)
            result.update(outcome="patch_proposal", patch_sha256=hashlib.sha256(diff).hexdigest(),
                          reason="In-scope patch captured; validation results and human review determine acceptance")
        else:
            collect_evidence(out, result)
            if result.get("agent_interpretation", "").strip():
                result["outcome"] = "no_patch"
                result["reason"] = "Agent completed with no repository changes; review its explanation"
            else:
                result.update(run_status="error", reason="No patch or final agent explanation was captured")
    except KeyboardInterrupt:
        result.update(run_status="interrupted", reason="Interrupted by operator")
    except Exception as exc:
        # Exception messages from subprocesses can contain credentials or repository content.
        if result["run_status"] == "finished":
            result["run_status"] = "error"
        if isinstance(exc, subprocess.CalledProcessError):
            (out / "setup-error.log").write_bytes(exc.stderr or b"")
        result["reason"] = type(exc).__name__ + ": " + (str(exc) if isinstance(exc, ValueError) else "See setup and execution prerequisites")
    finally:
        logs = cleanup(["docker", "logs", relay])
        if logs is not None and logs.returncode == 0:
            (out / "relay.log").write_bytes(logs.stdout + logs.stderr)
        if created_relay:
            removed = cleanup(["docker", "rm", "-f", relay])
            if removed is None or removed.returncode != 0:
                result.setdefault("operator_alerts", []).append("Relay container cleanup unverified: " + relay)
        if created_network:
            removed = cleanup(["docker", "network", "rm", network])
            if removed is None or removed.returncode != 0:
                result.setdefault("operator_alerts", []).append("Docker network cleanup unverified: " + network)
        if result.get("operator_alerts"):
            result.update(run_status="error", outcome="no_result")
            result["reason"] += " Operator action required: verify Docker cleanup."
        save_result(out, result)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", type=Path)
    parser.add_argument("--secret-file", required=True, type=Path)
    parser.add_argument("--image", default=DEFAULT_IMAGE)
    parser.add_argument("--output", type=Path, default=ROOT / "runs/first-slice")
    args = parser.parse_args()
    out = run(args.task, args.secret_file, args.image, args.output)
    print(out)
    result = json.loads((out / "result.json").read_text(encoding="utf-8"))
    for alert in result.get("operator_alerts", []):
        print("OPERATOR ALERT: " + alert, file=sys.stderr)
    return 0 if result["run_status"] == "finished" and not result.get("scope_violations") else 1
