# First private-slice evaluation: public summary

**Status:** Public summary of a maintainer-reviewed private engineering demonstration. Runnable code, raw traces, patches, task inputs, and local configuration are excluded from this documentation release.

ASE-Lab implemented a supervised command-line path for investigating one issue in a fixed repository snapshot. The project-owned runner validates a task, prepares a disposable checkout, invokes OpenHands SDK 1.62.0 in a restricted Docker container, inspects the Git diff, runs specified validation commands independently, and writes a report for human review. A short-lived relay held the model credential outside the agent container. This is a bounded demonstration, not a production service or a general agent platform.

## Evaluation method and observed outcomes

Before model execution, three cases and their review criteria were fixed against the public `more-itertools` v10.8.0 revision `8c1a6ef241b51ff055e89219f050ccf4f15f37f6`: a negative-count defect in `exactly_n`, a requested zero-size behavior for `chunked`, and an underspecified report that should lead to a justified no-patch response. The first case overlapped earlier feasibility work and was familiar to the team. Tests on the clean starting snapshot reproduced the two specified failures.

| Case | Initial attempt | Follow-up evidence |
| --- | --- | --- |
| `exactly_n` | An in-scope patch passed focused, regression, and full-suite validation. | The proposed change met the selected review rubric. |
| `chunked` | A patch passed tests, but the recorded duration exceeded the configured deadline and the patch broadened behavior beyond the requested zero-size case. The attempt was rejected. | A bounded rerun produced a localized patch. Independent checks and review found it met the selected rubric. |
| Insufficient evidence | The agent initially failed without a justified conclusion after the relay token threshold was reached. | A second attempt also failed. A third attempt completed without changes, explained why the report did not identify a defect, and requested the missing reproducer details. It met the no-patch rubric in review. |

All initial failures and reruns were retained in private evidence. For the selected cases, at least one attempt met each rubric in assistant review, and the maintainer accepted the **private bounded demonstration**. Eighteen deterministic tests of ASE-Lab-owned behavior passed after later corrections; those corrections have not been rerun against the live three-case set. The recorded results support a small engineering demonstration, not a success-rate estimate or a claim of reliable general repair.

## Boundaries and remaining risks

- Agent commands ran in a disposable container. Changes outside the named file scope were detected and rejected after execution; the disposable checkout could temporarily contain such changes.
- A completed run can propose a patch or, with a final explanation, a no-patch report. Execution failures are reported separately. Human review determines whether either proposal is justified.
- The model provider returned token counts, but a monetary spending ceiling was not verified. A relay threshold stops subsequent requests and can be crossed by the request already in flight.
- One attempt recorded an elapsed-time overrun whose cause has not been established. The supervisor now rejects a late return, but real-time termination across host suspension is unverified. Supervised runs require an awake host.
- Automatic trace redaction and retention cleanup are not implemented. Raw evidence remains private and requires review before sharing.

Executable components are excluded from this documentation release while the project's own licensing and distribution terms remain unresolved. Any later code release requires a separate file, dependency, license, trace, and history review under the [publication policy](../governance/publication-policy.md).
