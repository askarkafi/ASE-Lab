"""OpenHands entry point, mounted read-only inside the agent container."""
import json
from collections import Counter
from pathlib import Path
from openhands.sdk import Agent, Conversation, LLM, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.terminal import TerminalTool


def main():
    task = json.loads(Path("/input/task.json").read_text())
    counts = Counter()
    def observe(event):
        counts[type(event).__name__] += 1
        print(json.dumps(event.model_dump(mode="json")), flush=True)
    agent = Agent(
        llm=LLM(model="openai/deepseek-flash", base_url="http://model-proxy:8080/v1",
                api_key="relay-only-placeholder", api_mode="chat", stream=False,
                max_output_tokens=2048),
        tools=[Tool(name=TerminalTool.name), Tool(name=FileEditorTool.name)])
    conversation = Conversation(agent=agent, workspace="/work",
        max_iteration_per_run=task["limits"]["sdk_iterations"], callbacks=[observe])
    error = None
    try:
        conversation.send_message(
            "Investigate the issue. Explain observations, changes and uncertainty. "
            "Keep behavioral changes limited to the requested issue and preserve unspecified "
            "behavior, including exception types and timing. "
            "Edit only these existing files: " + json.dumps(task["allowed_edit_paths"]) +
            ". Temporary files belong in /tmp. Do not create or delete repository files. "
            "Local commands are permitted in this disposable container. Execution limits: " +
            json.dumps(task["limits"]) +
            ". Keep individual commands and the total investigation within these limits. "
            "Prioritize the supplied validation commands. If the report lacks enough evidence "
            "for a defensible fix, finish with observations and specific missing information. "
            "When no failing input and no invoked function or API are supplied, inspect at most "
            "three plausible code or test locations. Then give a no-patch report with the "
            "observations and the missing details. Avoid broad searches and full-suite runs "
            "for such underspecified reports. ASE-Lab runs the listed validation independently. "
            "Use broad coverage instrumentation only when necessary for the stated issue. Validation: " +
            json.dumps(task["validation_commands"]) + "\nIssue:\n" + task["issue"])
        conversation.run()
    except Exception as exc:
        error = type(exc).__name__
    finally:
        status = str(conversation.state.execution_status)
        conversation.close()
    print("ASE_LAB_SDK_SUMMARY=" + json.dumps(
        {"status": status, "error": error, "event_counts": dict(counts)}), flush=True)
    return 1 if error else 0


if __name__ == "__main__":
    raise SystemExit(main())
