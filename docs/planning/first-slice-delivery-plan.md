# Delivery plan for the first vertical slice

**Status:** The private first-slice engineering demonstration was accepted by the maintainer. This plan remains the record of its delivery checkpoints; publication is a separate review gate. See the [evaluation summary](../evaluation/first-slice.md).

**Scope:** The [first delivery slice](first-slice.md), from a bounded repository issue to a human-reviewable patch or justified no-patch report.

This plan identifies the evidence needed to move from the agreed behavior and acceptance criteria to a tested capability. It refines the [project roadmap](roadmap.md); it is not a separate project-management process or a fixed calendar. Findings may change the scope or order, provided the decision and its reason are recorded.

## 1. Confirm the delivery baseline

**Work:** Use the existing slice definition as the statement of user problem, intended result, scope, and capability-level acceptance criteria. Identify the main risks: unsafe command execution, sensitive data exposure, inaccurate test reporting, and unjustified patches. Record which decisions depend on SDK evidence.

**Exit evidence:** A maintainer can explain what the slice promises, what it excludes, how a result will be reviewed, and which decisions are still open. This baseline does not require choosing a final evaluation repository or task set.

## 2. Validate the OpenHands execution path

**Work:** Use a temporary repository task to test the execution path and controls, not to score product performance. Follow this bounded protocol:

1. **Preflight:** Confirm an isolated, disposable execution environment before enabling agent-driven commands. Pin the SDK and Python versions, verify model access without exposing credentials, and set time, step, and cost limits before the run. A local workspace path alone is not an isolation boundary.
2. **Task baseline:** Prepare one small issue with a known starting revision, a permitted file scope, and a test that independently reproduces the issue. Record the baseline result before giving the task to the agent. Keep any reference fix out of the task input.
3. **SDK run:** Start with the smallest supported agent and tool configuration that can inspect the repository, propose a bounded change, and run the permitted test. Observe the request, agent loop, tool calls, observations, status transitions, and final result through supported SDK facilities.
4. **Independent inspection:** Compare the actual workspace diff and test output with the agent's report. Verify how the installed SDK exposes termination, tool errors, and configured limits. Exercise a controlled failure or limit path when safe and inexpensive; record any untested control as unknown.
5. **Feasibility decision:** Record the environment and versions, task input, limits, non-sensitive observations, and blockers. State whether the SDK path is usable as proposed, usable after a bounded change, or blocked by a concrete incompatibility.

Keep experimental code and traces out of public commits until reviewed. This task is deliberately simpler than the final evaluation cases.

**Exit evidence:** A reproducible failing baseline, at least one repeatable SDK run, independently checked file and test outcomes, and a short account of which SDK facilities support the required workflow and controls. An unsupported or unverified control remains an explicit open risk. If a material blocker appears, document it before changing the slice or SDK decision. The temporary task is not the final evaluation set.

## 3. Make the necessary design decisions

**Work:** Define the smallest ASE-Lab-owned responsibilities for task intake, execution policy, SDK invocation, and reviewable reporting. Decide the first interface and output representation from the observed SDK behavior. A local command-line entry point using the SDK's Python API is the initial proposal because it can demonstrate a repository task without a web service; it is not an accepted technology or interface decision until feasibility confirms it. Add a custom tool, extension, or integration boundary only when the task or tests justify it.

**Exit evidence:** A design sufficient to implement and test the slice, with project-owned and SDK-owned responsibilities distinguished. Record an ADR only for a consequential architectural choice with real alternatives and lasting trade-offs. Keep the [conceptual architecture](../architecture/conceptual-architecture.md) consistent with accepted findings.

## 4. Build the complete path

**Work:** Implement task intake, bounded execution, and a human-reviewable patch or no-patch report. Test deterministic ASE-Lab behavior as it is built, including invalid input, limits, result recording, failure reporting, and truthful test status. Exercise the complete path on one task before broadening it.

**Exit evidence:** A repeatable end-to-end run, focused automated tests for project-owned behavior, and a reviewer who can inspect the output and distinguish observed facts from agent interpretation. This is still a development checkpoint, not a product release.

## 5. Evaluate and refine

**Work:** Before evaluation, fix a small task set with repository revisions, issue statements, permitted actions, expected outcomes, validation commands, and human review rubrics. Include a reproducible issue, a task requiring investigation across related code and tests, and a case with insufficient evidence for a patch. Record all attempts, failures, reruns, latency, and cost where available. Review proposed patches as code, not only as passing tests.

**Exit evidence:** The [slice acceptance criteria](first-slice.md#evaluation-tasks-and-delivery-decision) hold for the selected tasks, or the implementation and claimed capability are revised explicitly. A few tasks support an engineering demonstration, not a general performance claim.

## 6. Review and publish a deliberate increment

**Work:** A human maintainer reviews code, tests, documentation, dependencies, license notices, generated outputs, sensitive traces, and the exact Git history intended for publication. Document observed behavior and limitations separately from future plans.

**Exit evidence:** A small, reproducible and defensible increment is approved under the [publication policy](../governance/publication-policy.md). Publication is a separate reviewed action.

## Timing of tests and open decisions

Acceptance criteria and the method of review are defined before coding. One temporary task is enough for SDK feasibility. Deterministic tests accompany implementation. The final task set and repository revisions are frozen before evaluation, after the execution path is understood.

For the private demonstration, the task set, initial CLI/JSON interface, and numerical limits were fixed and evaluated. The [public summary](../evaluation/first-slice.md) records the outcome and remaining limits. Broader provider support, monetary cost controls, and product interfaces remain future decisions. No production deployment, general multi-agent architecture, or multi-SDK compatibility is required for this slice.
