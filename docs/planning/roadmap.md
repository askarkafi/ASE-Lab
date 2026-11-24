# OpenHands-first, evidence-linked roadmap

**Status:** The first supervised slice completed its bounded delivery cycle and was published as source; later increments remain unscheduled.

**Selected starting point:** [OpenHands Software Agent SDK](https://github.com/OpenHands/software-agent-sdk).

**First vertical slice:** [Repository issue investigation](first-slice.md) was implemented and evaluated privately, and its supervised source is published. See the [public outcome summary](../evaluation/first-slice.md) and [run guide](../../ase_lab/README.md).

The [first-slice delivery plan](first-slice-delivery-plan.md) sets the execution checkpoints and timing of decisions for this increment.

This roadmap connects **hands-on learning**, **incremental product development**, and **published academic foundations**. Each implementation increment should pass through a proportionate cycle of problem definition, design decisions, implementation, validation, human review, and learning. These are practical checkpoints, not a semester calendar, a promise to build the entire platform, or a separate project-management process.

The OpenHands selection is a **working engineering decision** intended to avoid prolonged SDK comparison. It is not a claim that OpenHands is universally superior. Reconsider it only if a concrete blocker or substantial new evidence arises. The [academic rationale](../research/academic-foundations.md) explains the evidence behind the educational approach; the [resource index](../research/academic-resources.md) gives direct access to the linked teaching materials, code, and papers.

## 0 — Foundation and academic grounding (documentation prepared)

**Goal:** Establish a coherent project direction and connect it to existing educational and research practice.

- Keep the product vision, first-stage scope, and selective public publication policy explicit.
- Maintain the evidence-based rationale and a curated link index, without treating external courses as endorsements.
- Record OpenHands as the initial SDK while leaving detailed runtime contracts and the first capability's implementation boundaries open.

**Checkpoint:** A reader can explain why ASE-Lab exists, what it does *not* promise this semester, and which evidence-informed learning path it follows. Public publication depends on a separate reviewed commit.

## 1 - Define the first delivery problem and evidence

**Decide:** Review the agreed behavior, capability-level acceptance criteria, and [delivery plan](first-slice-delivery-plan.md). Identify risks and open decisions. Choose one temporary task and its permitted actions for SDK feasibility; defer the fixed evaluation task set until the execution path is understood.

**Checkpoint:** The temporary task is concrete enough to guide feasibility work, and the slice's purpose and review criteria are clear. The task is not treated as final evaluation evidence.

## 2 - Run and understand the OpenHands execution path

**Study:** [Stanford CS329Z](https://cs329z.stanford.edu/) lectures on agent architecture and tool use; selectively inspect its [agent harness assignment](https://github.com/cs329z/assignment1-harness); [MIT 6.S950 harness lab](https://agencyai.mit.edu/lab5/); [OpenHands SDK paper](https://proceedings.mlsys.org/paper_files/paper/2026/hash/8ae9cf363ea625161f885b798c1f1f78-Abstract-Conference.html).

**Build and inspect:** Set up the selected SDK in a disposable, restricted workspace. Run one minimal task relevant to the agreed problem, then trace the model → agent loop → tool → observation path in both SDK source and actual execution events. Do not require implementing a second complete framework.

**Checkpoint:** One repeatable run, a short explanation of the execution boundary, and recorded non-sensitive traces or test results. No claim that a production agent exists.

## 3 - Design and integrate one ASE-Lab-owned capability

**Study:** [Berkeley's software-development agents lecture](https://rdi.berkeley.edu/llm-agents-mooc/slides/neubig24softwareagents.pdf); [CMU 06-643](https://kitchingroup.cheme.cmu.edu/s26-06643/intro.html) on tests, code quality, and tool extension; the [OpenHands SDK documentation](https://docs.openhands.dev/sdk).

**Design, build, and inspect:** Decide project-owned responsibilities from the agreed task and observed SDK behavior. Invoke OpenHands from ASE-Lab-owned code and implement a small, testable project-owned capability. Add a custom tool or extension only if the task justifies it. Record consequential architecture choices, their alternatives, and trade-offs in an ADR after review. Add a lightweight runtime boundary only for needs observed in this integration; avoid a generic multi-SDK abstraction.

**Checkpoint:** A repeatable invocation from ASE-Lab, tests for the project-owned behavior, and a clear account of which responsibilities belong to ASE-Lab versus OpenHands.

## 4 - Deliver one meaningful software-engineering vertical slice

**Study:** [SWE-agent](https://papers.nips.cc/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html), [SWE-bench](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html), and the [Agentless baseline](https://doi.org/10.1145/3715754).

**Build and evaluate:** Implement the reviewed slice, adjusting scope if SDK feasibility evidence requires it. Complete the flow from task input to a human-reviewable result. Before evaluation, fix a small realistic task set with repository revisions, permitted actions, expected outcomes, validation commands, and human review rubrics. Apply the agreed acceptance criteria and review the resulting code and behavior before broadening scope.

**Checkpoint:** A working, testable end-to-end capability with recorded successes, failures, limitations, and at least a simple baseline when meaningful. This is a suitable academic-stage outcome; a complete platform is not required.

## 5 - Consolidate and publish a reviewed increment

**Study:** [Stanford CS329Z's evaluation assignment](https://github.com/cs329z/assignment2-evals), [Stanford MS&E 203](https://web.stanford.edu/class/msande203/syllabus/), and [AI Agents That Matter](https://mlanthology.org/tmlr/2025/kapoor2025tmlr-ai/).

**Improve:** Add proportionate automated tests, error analysis, execution safeguards, reproducibility notes, and measurements of task outcome, latency, and cost where accessible. Review and selectively publish mature documentation and code from private development to the public repository.

**Checkpoint:** A small, understandable and defensible release; explicitly distinguish demonstrated functionality from intentions.

**Second increment.** Repository Analysis adds read-only, supervised analysis of a fixed Git revision with source citations. Its [laboratory evaluation](../evaluation/repository-analysis.md) records both complete and partial answers, with human review as part of the workflow.

## Boundaries and later directions

- Do **not** delay the next implementation step for another broad SDK comparison.
- Do **not** pre-build multi-agent orchestration, A2A, a large MCP architecture, extensive research infrastructure, or speculative adapters.
- Deep-dive into context management, skills, MCP, and additional agents only where the chosen task or learning objective warrants them.
- A future research study requires its own question, method, controls, and evaluation; citing published research does not itself establish novelty.

See [educational objectives](../education/learning-objectives.md), [conceptual architecture](../architecture/conceptual-architecture.md), and [future extensions](future-extensions.md).
