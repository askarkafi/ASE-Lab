# First delivery slice: repository issue investigation

**Status:** A supervised private implementation and selected three-case evaluation were accepted as a bounded engineering demonstration. Executable code has not been published. See the [public evaluation summary](../evaluation/first-slice.md).

**Purpose:** Define one complete, testable software-engineering delivery cycle before choosing detailed implementation contracts.

## Problem and intended user

A software engineer investigating a bounded repository issue needs a reviewable account of the relevant code, a proposed change, and evidence that the change addresses the issue. ASE-Lab should help produce that account while leaving acceptance and application of the change to a human maintainer.

This is the **selected direction for the first delivery slice**. One repository task can exercise task definition, agent execution, tool use, workspace control, tests, and human review without requiring a general multi-agent platform. Feasibility findings may justify revising its boundaries.

## Required workflow

1. A maintainer supplies an issue description, a specific repository revision, permitted files and actions, validation commands, and execution limits. Missing required inputs are identified before agent execution.
2. ASE-Lab prepares a reproducible, disposable or appropriately restricted workspace without exposing credentials. Tool, time, and resource limits are fixed before the run.
3. The agent examines relevant code and tests, supports its diagnosis with observations, and distinguishes evidence from interpretation.
4. A completed run ends with either a reviewable patch and rationale or an explicit no-patch report explaining why a defensible change could not be proposed. An execution failure is reported separately.
5. Permitted validation commands are run where possible. The report records commands actually executed, their observed results, commands not run, uncertainty, and incomplete work. Tool failures and limit exhaustion are reported as outcomes, not hidden.
6. A maintainer reviews the report and any patch before a change is accepted or published.

The private demonstration uses a versioned JSON task, a supervised command-line runner, and a small OpenHands worker adapter. These choices do not settle the long-term product interface.

## Scope for the first delivery

- One local repository snapshot and one bounded issue per run.
- A proposed patch or a clear explanation of why no defensible patch was produced.
- A reviewable record of relevant actions and test outcomes, with sensitive content removed before publication.
- A repeatable demonstration on a small set of representative tasks.

Out of scope: automatically merging or publishing changes, unattended access to private repositories, production deployment, multi-agent coordination, and support for multiple runtimes.

## Acceptance criteria for every run

- A completed run produces one of the two task outcomes above. A run that cannot complete reports an explicit error, limit, or interruption status; it is not counted as a justified no-patch conclusion.
- For an approved disposable repository snapshot, local commands run in a restricted container. Changes outside the named file scope are detected and rejected after execution; temporary out-of-scope changes can occur inside that disposable checkout. Credentials remain outside the agent container.
- A reviewer can distinguish observed facts, the agent's interpretation, and unresolved uncertainty.
- Reported test commands and results match execution evidence. A test not run is never reported as passed.
- Any patch is inspectable and is not automatically merged or published.
- Relevant actions and failures are traceable without requiring publication of sensitive raw traces.

For a patch to be accepted, a human reviewer must also judge that it addresses the issue, stays within the justified change scope, meets ordinary code and test quality expectations, and has no evident adverse effect. Passing tests alone do not establish patch quality. A no-patch result is acceptable when it explains the evidence examined, the blocking uncertainty, and what further information is needed.

## Evaluation tasks and delivery decision

For SDK feasibility, one temporary task is sufficient. Before evaluation, select and freeze a small task set containing at least: (a) a reproducible issue with a relevant test, (b) an issue requiring investigation across related code and tests, and (c) a report for which the evidence is insufficient to justify a patch. The second case need not require a multi-file patch. Use only tasks and data approved for the intended workspace and publication context.

For each task, record the starting revision, issue statement, permitted actions, expected outcome, validation commands, and human review rubric before running the agent. Keep the reference solution, if one exists, out of the agent's task input. Record every attempt, including failures and reruns, rather than selecting only successful runs.

The first slice is ready for delivery when the complete path from input to reviewable result works; deterministic tests of ASE-Lab-owned behavior pass; execution boundaries hold for all selected tasks; the solvable tasks yield patches that pass validation and human review; and the insufficient-evidence task yields a justified no-patch report. If a condition fails, improve the slice or explicitly narrow its claimed capability and acceptance scope before delivery.

Report successes, failures, latency, and model or tool cost where available. A few tasks establish an engineering demonstration, not a general success rate or superiority claim. Compare with a simple human or non-agent baseline only when the tasks and measurement make the comparison meaningful.

## Engineering and decision gates

1. **Scope gate:** The maintainer has selected the problem direction, capability-level acceptance criteria, and [delivery plan](first-slice-delivery-plan.md). Choose one temporary task and its permitted execution settings for SDK feasibility; confirm the final task instances and review rubrics before evaluation.
2. **Feasibility gate:** Run and inspect a minimal OpenHands task in a disposable environment. Record the SDK version, execution path, usable extension points, and blockers.
3. **Design gate:** Decide the smallest ASE-Lab-owned task, policy, and integration responsibilities supported by that evidence. Record an ADR if a consequential architectural choice has real alternatives and lasting trade-offs.
4. **Delivery gate:** Implement the slice with focused tests, human review, and evidence from representative runs.
5. **Publication gate:** Review the exact code, documentation, dependencies, license notices, traces, and history under the [publication policy](../governance/publication-policy.md).

The first two gates may refine or change this slice. A concrete blocker should trigger a documented scope or SDK decision rather than speculative infrastructure.

## Remaining decisions beyond the private demonstration

- Which additional issue types and repositories justify expanding beyond the selected evaluation set?
- What monetary cost ceiling and host-level stopping behavior can be verified for broader operation?
- When would a different provider, SDK extension, or interface be justified by a concrete task?

See the [scope](../overview/scope.md), [conceptual architecture](../architecture/conceptual-architecture.md), [delivery plan](first-slice-delivery-plan.md), [roadmap](roadmap.md), and [evaluation summary](../evaluation/first-slice.md). Resolve remaining questions with maintainer review and implementation evidence.
