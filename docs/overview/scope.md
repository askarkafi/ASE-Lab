# Scope and boundaries

**Status:** Preliminary - the first delivery direction is selected; details remain open.

## Long-term product scope

Potential capabilities include task definitions, specialized agent behavior, tool and data integrations, execution/runtime adapters, environment controls, and interfaces that make agent actions reviewable. These are possibilities for the **evolving product**, not a checklist for the first semester.

## Initial academic stage

The initial work is expected to include:

- Analysis and documentation of a coherent architectural direction.
- Initial integration and task-driven validation of the selected OpenHands Software Agent SDK.
- Selection of a **single small, end-to-end implementation slice** with real behavior.
- Automated checks and evidence of what the implemented slice actually does.
- An explanation of the concepts learned and the boundary between reused and project-owned code.

The [selected first delivery direction](../planning/first-slice.md) is repository issue investigation with a reviewable patch proposal or justified no-patch report. Its capability-level acceptance criteria are agreed; task instances, their specific review rubrics, the remaining implementation stack, and architecture require further review and feasibility evidence before implementation.

## Not required in the initial stage

- A complete or production-ready user product.
- A general-purpose multi-agent platform or distributed orchestration layer.
- Support for multiple SDK runtimes in production.
- Full implementation of MCP, A2A, skills, planning, memory, and evaluation all at once.
- New research findings or a publishable paper.
- A fixed timeline before feasibility and SDK analysis.

## Scope control

Features should be added only when they support a defined learning outcome or a concrete product capability. Architectural flexibility is desirable; speculative infrastructure and premature generalization are not.
