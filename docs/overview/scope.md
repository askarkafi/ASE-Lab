# Scope and boundaries

**Status:** A first bounded engineering demonstration was accepted privately; broader product scope remains open.

## Long-term product scope

Potential capabilities include task definitions, specialized agent behavior, tool and data integrations, execution/runtime adapters, environment controls, and interfaces that make agent actions reviewable. These are possibilities for the **evolving product**, not a checklist for the first semester.

## Initial academic stage

The initial work is expected to include:

- Analysis and documentation of a coherent architectural direction.
- Initial integration and task-driven validation of the selected OpenHands Software Agent SDK.
- Selection of a **single small, end-to-end implementation slice** with real behavior.
- Automated checks and evidence of what the implemented slice actually does.
- An explanation of the concepts learned and the boundary between reused and project-owned code.

The [first delivery slice](../planning/first-slice.md) investigates repository issues and proposes a reviewable patch or justified no-patch report. A private supervised implementation and selected [three-case evaluation](../evaluation/first-slice.md) were completed. This is evidence for a bounded workflow, not production readiness or a general success rate.

## Not required in the initial stage

- A complete or production-ready user product.
- A general-purpose multi-agent platform or distributed orchestration layer.
- Support for multiple SDK runtimes in production.
- Full implementation of MCP, A2A, skills, planning, memory, and evaluation all at once.
- New research findings or a publishable paper.
- A fixed timeline before feasibility and SDK analysis.

## Scope control

Features should be added only when they support a defined learning outcome or a concrete product capability. Architectural flexibility is desirable; speculative infrastructure and premature generalization are not.
