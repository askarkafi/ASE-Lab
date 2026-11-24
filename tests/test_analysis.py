import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from ase_lab import analysis
from ase_lab.runner import command, DEFAULT_LIMITS


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        command(["git", "init", str(self.repo)])
        for key, value in (("user.name", "Fixture"), ("user.email", "fixture@example.invalid")):
            command(["git", "-C", str(self.repo), "config", key, value])
        (self.repo / "feature.py").write_text("def feature():\n    return 42\n", encoding="utf-8")
        command(["git", "-C", str(self.repo), "add", "."])
        command(["git", "-C", str(self.repo), "commit", "-m", "fixture"])
        revision = command(["git", "-C", str(self.repo), "rev-parse", "HEAD"]).stdout.decode().strip()
        self.task = dict(schema_version=1, task_id="feature-location", capability="repository_analysis",
                         question="Where is feature implemented?", repository=str(self.repo),
                         revision=revision, model_profile="deepseek-flash-relay", limits=DEFAULT_LIMITS)
        self.taskfile = self.root / "task.json"
        self.secret = self.root / "secret.env"
        self.secret.write_text("FAKE_ONLY")

    def answer(self):
        return dict(observations=[dict(path="feature.py", start_line=1, end_line=2,
                                       finding="The function is here.")],
                    interpretation="This is the implementation.", uncertainty=self.uncertainty())

    def uncertainty(self):
        return dict(scope="Inspected feature.py.", unresolved="Callers were not checked.",
                    needed_evidence="A call site or a test invoking feature().")

    def inconclusive(self):
        return dict(observations=[], interpretation="", uncertainty=dict(
            scope="Searched for diagnostic files.",
            unresolved="No incident artifacts exist anywhere in the repository.",
            needed_evidence=["diagnostic_output", "reproduction"]))

    def exercise(self, answer=None, edit=False, tracked_edit=False, status="FINISHED", cleanup_failure=False,
                 fenced=False, prefix=""):
        self.taskfile.write_text(json.dumps(self.task))
        real_command = command
        calls = []

        def dispatch(argv, **kwargs):
            if argv[0] == "docker":
                calls.append(argv)
                return subprocess.CompletedProcess(argv, 0, b"sha256:fixture\n", b"")
            return real_command(argv, **kwargs)

        def execute(argv, name, seconds, log):
            calls.append(argv)
            work = log.parent / "workspace"
            if edit:
                (work / "ignored.tmp").write_text("injected")
            if tracked_edit:
                (work / "feature.py").write_text("tampered\n")
            message = json.dumps(answer or self.answer())
            if fenced:
                message = "```json\n" + message + "\n```"
            text = json.dumps(dict(kind="MessageEvent", source="agent", llm_message=dict(
                content=[dict(type="text", text=prefix + message)])))
            log.write_text(text + "\nASE_LAB_SDK_SUMMARY=" + json.dumps(dict(status=status)) + "\n")
            return dict(status="passed", exit_code=0)

        def cleanup(argv):
            failed = cleanup_failure and "rm" in argv and argv[-1].endswith("-relay")
            return subprocess.CompletedProcess(argv, 1 if failed else 0, b"", b"")

        with patch("ase_lab.analysis.runner.command", side_effect=dispatch), patch(
            "ase_lab.analysis.runner.bounded", side_effect=execute
        ), patch("ase_lab.analysis.runner.cleanup", side_effect=cleanup):
            out = analysis.run(self.taskfile, self.secret, "fixture", self.root / "outputs")
        return json.loads((out / "result.json").read_text()), calls, out

    def test_verified_report_and_read_only_mount(self):
        result, calls, out = self.exercise()
        self.assertEqual((result["run_status"], result["outcome"]), ("finished", "analysis_report"))
        self.assertEqual(result["schema_version"], 2)
        self.assertEqual(result["answer"]["observations"][0]["quote"], "def feature():\n    return 42")
        self.assertTrue(result["workspace_unchanged"])
        agent_argv = next(argv for argv in calls if "--name" in argv and argv[argv.index("--name") + 1].endswith("-agent"))
        self.assertIn("type=bind,src=" + str(out / "workspace") + ",dst=/work,readonly", agent_argv)
        self.assertIn("--read-only", agent_argv)
        self.assertEqual((self.repo / "feature.py").read_text(), "def feature():\n    return 42\n")
        self.assertIn("feature.py:1-2", (out / "report.md").read_text())
        worker_task = json.loads((out / "input/task.json").read_text())
        self.assertEqual(set(worker_task), {"capability", "question", "revision", "limits"})

    def test_rejects_agent_supplied_quote(self):
        answer = self.answer()
        answer["observations"][0]["quote"] = "invented line"
        result, _, _ = self.exercise(answer=answer)
        self.assertEqual((result["run_status"], result["outcome"]), ("error", "no_result"))
        self.assertIn("Invalid observation fields", result["reason"])

    def test_rejects_range_past_end_of_file(self):
        answer = self.answer()
        answer["observations"][0]["end_line"] = 3
        result, _, _ = self.exercise(answer=answer)
        self.assertEqual(result["outcome"], "no_result")
        self.assertIn("exceeds file length", result["reason"])

    def test_rejects_untracked_or_escaping_citation(self):
        for name in ("../feature.py", "missing.py"):
            answer = self.answer()
            answer["observations"][0]["path"] = name
            result, _, _ = self.exercise(answer=answer)
            self.assertEqual(result["outcome"], "no_result")
            self.assertIn("tracked file", result["reason"])

    def test_rejects_workspace_change_even_if_ignored(self):
        result, _, _ = self.exercise(edit=True)
        self.assertFalse(result["workspace_unchanged"])
        self.assertEqual(result["changed_files"], ["ignored.tmp"])
        self.assertEqual(result["outcome"], "no_result")

    def test_rejects_tracked_change(self):
        result, _, _ = self.exercise(tracked_edit=True)
        self.assertFalse(result["workspace_unchanged"])
        self.assertEqual(result["changed_files"], ["feature.py"])
        self.assertEqual(result["outcome"], "no_result")

    def test_collects_provider_reported_usage_without_claiming_cost(self):
        out = self.root / "usage"
        out.mkdir()
        (out / "relay.log").write_text('not json\n{"total_tokens": 12, "requests_used": 1}\n')
        result = {}
        analysis.collect_usage(out, result)
        self.assertEqual(result["provider_usage"]["total_tokens"], 12)

    def test_marks_usage_incomplete_after_upstream_disconnect(self):
        out = self.root / "usage-error"
        out.mkdir()
        (out / "relay.log").write_text('\n'.join([
            '{"total_tokens": 12, "requests_used": 1}',
            '{"event": "upstream_transport_error", "requests_used": 2, "total_tokens": 12, "usage_unknown_for_request": true}',
        ]))
        result = {}
        analysis.collect_usage(out, result)
        self.assertEqual(result["provider_usage"]["requests_used"], 1)
        self.assertTrue(result["provider_usage_incomplete"])
        self.assertEqual(result["relay_errors"][0]["requests_used"], 2)

    def test_extracts_openhands_finish_action(self):
        log = self.root / "agent.log"
        log.write_text(json.dumps(dict(kind="ActionEvent", source="agent", tool_name="finish",
            action=dict(kind="FinishAction", message=json.dumps(self.answer())))) + "\n")
        self.assertEqual(json.loads(analysis.final_message(log)), self.answer())

    def test_completed_inconclusive_answer(self):
        answer = self.inconclusive()
        result, _, out = self.exercise(answer=answer)
        self.assertEqual((result["run_status"], result["outcome"]), ("finished", "inconclusive"))
        report = (out / "report.md").read_text()
        self.assertIn("No positive finding", report)
        self.assertIn(analysis.INCONCLUSIVE_MESSAGE, report)
        self.assertIn("Relevant logs", report)
        for artifact in ("report.md", "result.json"):
            self.assertNotIn(answer["uncertainty"]["unresolved"], (out / artifact).read_text())
        self.assertIn(answer["uncertainty"]["unresolved"], (out / "agent.log").read_text())

    def test_inconclusive_requires_all_uncertainty_fields(self):
        answer = self.inconclusive()
        answer["uncertainty"]["needed_evidence"] = ["No incident artifacts exist anywhere"]
        result, _, _ = self.exercise(answer=answer)
        self.assertEqual(result["outcome"], "no_result")

    def test_single_fenced_json_is_accepted_but_extra_prose_is_not(self):
        answer = self.inconclusive()
        result, _, _ = self.exercise(answer=answer, fenced=True)
        self.assertEqual((result["run_status"], result["outcome"]), ("finished", "inconclusive"))
        result, _, _ = self.exercise(answer=answer, fenced=True, prefix="Here is the answer:\n")
        self.assertEqual((result["run_status"], result["outcome"]), ("error", "no_result"))

    def test_inconclusive_cannot_make_unsupported_claim(self):
        answer = self.inconclusive()
        answer["interpretation"] = "Feature X is absent"
        result, _, _ = self.exercise(answer=answer)
        self.assertEqual((result["run_status"], result["outcome"]), ("error", "no_result"))

    def test_cleanup_failure_overrides_report(self):
        result, _, _ = self.exercise(cleanup_failure=True)
        self.assertEqual((result["run_status"], result["outcome"]), ("error", "no_result"))
        self.assertIn("Relay container cleanup unverified", result["operator_alerts"][0])

    def test_unfinished_is_not_analysis(self):
        result, _, _ = self.exercise(status="STOPPED")
        self.assertEqual(result["outcome"], "no_result")

    def test_invalid_input_rejected_before_container(self):
        self.task["schema_version"] = True
        self.taskfile.write_text(json.dumps(self.task))
        with patch("ase_lab.analysis.runner.command") as execute, patch("ase_lab.analysis.runner.cleanup"):
            out = analysis.run(self.taskfile, self.secret, "fixture", self.root / "outputs")
        execute.assert_not_called()
        self.assertEqual(json.loads((out / "result.json").read_text())["run_status"], "not_started")


if __name__ == "__main__":
    unittest.main()
