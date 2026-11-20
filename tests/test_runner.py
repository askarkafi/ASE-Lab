import copy
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from ase_lab.runner import validate, inspect_changes, run, command


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        command(["git", "init", str(self.repo)])
        for key, value in (("user.name", "Fixture"), ("user.email", "fixture@example.invalid")):
            command(["git", "-C", str(self.repo), "config", key, value])
        (self.repo / "allowed.py").write_text("old\n")
        (self.repo / "other.py").write_text("untouched\n")
        command(["git", "-C", str(self.repo), "add", "."])
        command(["git", "-C", str(self.repo), "commit", "-m", "fixture"])
        revision = command(["git", "-C", str(self.repo), "rev-parse", "HEAD"]).stdout.decode().strip()
        self.task = json.loads((Path(__file__).parent / "task.example.json").read_text())
        self.task.update(repository=str(self.repo), revision=revision, allowed_edit_paths=["allowed.py"])
        self.task["validation_commands"] = [
            dict(id="focused", argv=["python", "-m", "unittest"], timeout_seconds=10, after=None),
            dict(id="suite", argv=["python", "-m", "unittest"], timeout_seconds=10, after="focused")]
        self.secret = self.root / "secret.env"
        self.secret.write_text("FAKE_ONLY")
        self.taskfile = self.root / "task.json"

    def tearDown(self):
        self.temp.cleanup()

    def test_invalid_path_and_limit(self):
        for path in ("../escape", "/etc/passwd", "C:/escape", ".git/config"):
            task = copy.deepcopy(self.task)
            task["allowed_edit_paths"] = [path]
            with self.assertRaises(ValueError):
                validate(task)
        self.task["limits"]["wall_seconds"] = True
        with self.assertRaises(ValueError):
            validate(self.task)

    def test_scope_detects_added_deleted_and_modified(self):
        (self.repo / "allowed.py").write_text("new\n")
        (self.repo / "other.py").unlink()
        (self.repo / "extra.py").write_text("new\n")
        meta = self.root / "metadata"
        (self.repo / ".git").rename(meta)
        changed, violations, diff = inspect_changes(meta, self.repo, ["allowed.py"])
        self.assertEqual(violations, ["extra.py", "other.py"])
        self.assertIn(b"new", diff)

    def exercise(self, edits=True, failure=False, outside=False, timeout=False,
                 relay_cleanup_failure=False, agent_final=True):
        self.taskfile.write_text(json.dumps(self.task))
        real_command = command
        def dispatch(argv, **kwargs):
            if argv[0] == "docker":
                return subprocess.CompletedProcess(argv, 0, b"sha256:fixture\n", b"")
            return real_command(argv, **kwargs)
        def execute(argv, name, seconds, log):
            if name.endswith("-agent"):
                workspace = log.parent / "workspace"
                if edits:
                    (workspace / "allowed.py").write_text("fixed\n")
                if outside:
                    (workspace / "other.py").write_text("out of scope\n")
                final = json.dumps(dict(kind="MessageEvent", source="agent", llm_message=dict(
                    content=[dict(type="text", text="Insufficient evidence for a patch")]))) + "\n" if agent_final else ""
                log.write_text(final + 'ASE_LAB_SDK_SUMMARY={"status":"ConversationExecutionStatus.FINISHED"}\n')
                if timeout:
                    return dict(status="error", exit_code=None, reason="timeout")
                return dict(status="passed", exit_code=0)
            log.write_text("validation output\n")
            return dict(status="failed" if failure else "passed", exit_code=1 if failure else 0)
        def remove(argv):
            code = 1 if relay_cleanup_failure and argv[-1].endswith("-relay") and "rm" in argv else 0
            return subprocess.CompletedProcess(argv, code, b"", b"")
        with patch("ase_lab.runner.command", side_effect=dispatch), patch(
            "ase_lab.runner.bounded", side_effect=execute
        ), patch("ase_lab.runner.cleanup", side_effect=remove):
            out = run(self.taskfile, self.secret, "fixture", self.root / "outputs")
        return out, json.loads((out / "result.json").read_text())

    def test_complete_patch_and_immutable_source(self):
        out, result = self.exercise()
        self.assertEqual(result["outcome"], "patch_proposal")
        self.assertEqual(result["schema_version"], 2)
        self.assertEqual(result["validation"][0]["status"], "passed")
        self.assertTrue((out / "proposal.patch").exists())
        self.assertEqual((self.repo / "allowed.py").read_text(), "old\n")

    def test_scope_violation_rejects_patch_and_skips_validation(self):
        out, result = self.exercise(outside=True)
        self.assertEqual(result["outcome"], "no_result")
        self.assertEqual(result["scope_violations"], ["other.py"])
        self.assertFalse((out / "proposal.patch").exists())
        self.assertEqual(result["validation"][0]["status"], "not_run")

    def test_failed_validation_skips_dependent_command(self):
        _, result = self.exercise(failure=True)
        self.assertEqual(result["validation"][0]["status"], "failed")
        self.assertEqual(result["validation"][1]["status"], "not_run")

    def test_timeout_is_not_success_even_with_finished_claim(self):
        _, result = self.exercise(timeout=True)
        self.assertEqual(result["run_status"], "limit_reached")
        self.assertEqual(result["outcome"], "no_result")

    def test_no_change_result(self):
        _, result = self.exercise(edits=False)
        self.assertEqual(result["outcome"], "no_patch")
        self.assertEqual(result["run_status"], "finished")

    def test_no_change_without_explanation_is_not_no_patch(self):
        _, result = self.exercise(edits=False, agent_final=False)
        self.assertEqual(result["run_status"], "error")
        self.assertEqual(result["outcome"], "no_result")

    def test_relay_cleanup_failure_requires_operator_action(self):
        out, result = self.exercise(relay_cleanup_failure=True)
        self.assertEqual(result["run_status"], "error")
        self.assertEqual(result["outcome"], "no_result")
        self.assertIn("Relay container cleanup unverified", result["operator_alerts"][0])
        self.assertIn("Operator alerts", (out / "report.md").read_text())

    def test_private_evidence_distinguishes_agent_claim(self):
        from ase_lab.runner import save_result
        out = self.root / "evidence"
        out.mkdir()
        (out / "agent.log").write_text(json.dumps(dict(kind="MessageEvent", source="agent",
            llm_message=dict(content=[dict(type="text", text="All tests passed")]))))
        result = dict(run_status="error", outcome="no_result", reason="Interrupted", validation=[
            dict(id="test", status="not_run", argv=["python", "-m", "unittest"])])
        save_result(out, result)
        self.assertEqual(result["agent_interpretation"], "All tests passed")
        self.assertEqual(result["validation"][0]["status"], "not_run")

    def test_invalid_input_never_starts_sdk(self):
        self.taskfile.write_text("{}")
        with patch("ase_lab.runner.bounded") as execute, patch("ase_lab.runner.cleanup"):
            out = run(self.taskfile, self.secret, "fixture", self.root / "outputs")
        execute.assert_not_called()
        result = json.loads((out / "result.json").read_text())
        self.assertEqual(result["run_status"], "not_started")
        self.assertEqual(result["outcome"], "no_result")

    def test_validation_cannot_overwrite_runtime_evidence(self):
        for identifier in ("agent", "relay", "setup-error"):
            task = copy.deepcopy(self.task)
            task["validation_commands"][0]["id"] = identifier
            with self.assertRaises(ValueError):
                validate(task)

    def test_malformed_event_does_not_prevent_result(self):
        from ase_lab.runner import save_result
        out = self.root / "malformed"
        out.mkdir()
        (out / "agent.log").write_text(json.dumps(dict(
            kind="MessageEvent", source="agent", llm_message=None)))
        save_result(out, dict(run_status="error", outcome="no_result",
                             reason="Worker failed", validation=[]))
        self.assertTrue((out / "result.json").is_file())

    def test_dependency_requires_an_identifier(self):
        self.task["validation_commands"][1]["after"] = []
        with self.assertRaises(ValueError):
            validate(self.task)

    def test_container_start_failure_is_an_error(self):
        from ase_lab.runner import bounded
        with patch("ase_lab.runner.subprocess.run", return_value=subprocess.CompletedProcess([], 125)), patch("ase_lab.runner.cleanup"):
            result = bounded(["docker", "run"], "fixture", 10, self.root / "container.log")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["exit_code"], 125)

    def test_elapsed_deadline_overrides_successful_exit(self):
        from ase_lab.runner import bounded
        with patch("ase_lab.runner.subprocess.run", return_value=subprocess.CompletedProcess([], 0)), patch("ase_lab.runner.cleanup"), patch("ase_lab.runner.time.monotonic", side_effect=[0, 901]):
            result = bounded(["docker", "run"], "fixture", 900, self.root / "late.log")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["reason"], "timeout")
        self.assertTrue(result["deadline_overrun"])

    def test_container_cleanup_failure_is_reported(self):
        from ase_lab.runner import bounded
        with patch("ase_lab.runner.subprocess.run", return_value=subprocess.CompletedProcess([], 0)), patch(
            "ase_lab.runner.cleanup", return_value=subprocess.CompletedProcess([], 1)
        ):
            result = bounded(["docker", "run"], "fixture", 10, self.root / "cleanup.log")
        self.assertEqual(result["status"], "error")
        self.assertFalse(result["cleanup_verified"])

    def test_cli_prints_operator_alert(self):
        from ase_lab.runner import main
        out = self.root / "alert"
        out.mkdir()
        (out / "result.json").write_text(json.dumps(dict(
            run_status="error", operator_alerts=["Relay container cleanup unverified"])))
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch("ase_lab.runner.run", return_value=out), patch(
            "sys.argv", ["ase_lab", "task.json", "--secret-file", "secret.env"]
        ), redirect_stdout(stdout), redirect_stderr(stderr):
            code = main()
        self.assertEqual(code, 1)
        self.assertIn("OPERATOR ALERT: Relay container cleanup unverified", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
