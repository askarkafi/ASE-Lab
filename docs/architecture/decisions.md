# Public decision record

This document contains **publicly established project-level decisions**, not exploratory discussion or unapproved technical choices. Accepted implementation decisions may later receive dedicated Architecture Decision Records (ADRs).

| ID | Decision | Status |
| --- | --- | --- |
| P-001 | Preserve the project name **ASE-Lab**. | Established |
| P-002 | Design toward a usable, extensible product while implementing incrementally. | Established |
| P-003 | The first academic stage delivers a **small real part**, not the entire product. | Established |
| P-004 | Practical learning and sound engineering come before building a general research platform. | Established |
| P-005 | Publish reviewed versions of material rather than the complete history of internal exploration. | Established |
| P-006 | Start implementation with **OpenHands Software Agent SDK**; reconsider only if a concrete blocker or compelling new evidence warrants it. | Initial implementation decision |
| P-007 | Use repository issue investigation and a reviewable patch proposal as the first delivery direction; refine its boundaries with task and SDK evidence. | Initial delivery decision |
| P-008 | Follow the [first-slice delivery plan](../planning/first-slice-delivery-plan.md): validate the SDK path before detailed design, test project-owned behavior during implementation, and fix evaluation tasks before evaluation. | Initial delivery approach |

## Decisions not yet made

- Long-term runtime strategy beyond the initial OpenHands integration.
- Detailed module boundaries and integration contracts.
- Task instances, task-specific review rubrics, and detailed execution settings for the [selected first slice](../planning/first-slice.md). Its capability-level acceptance criteria are agreed.
- Programming stack and deployment approach.
- License for ASE-Lab's original code and documentation.

This is a project-level decision, **not** evidence that OpenHands has already been integrated or validated. See [SDK strategy](../engineering/sdk-strategy.md) and the [evidence-linked roadmap](../planning/roadmap.md).

The remaining open decisions are intentional. Public ADRs should be added after a decision is reviewed and ready for publication.

The first-slice direction is a product-scope decision, not an architecture decision. Workspace controls, runtime integration contracts, and module boundaries may warrant ADRs once the first task and SDK execution provide concrete alternatives and trade-offs. No ADR has been accepted for them.
