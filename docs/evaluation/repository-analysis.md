# Repository Analysis laboratory evaluation

Repository Analysis answers focused questions about a fixed Git revision. It returns source excerpts with the agent's findings and uncertainty, or an inconclusive result with the kinds of evidence needed to proceed. The [run guide](../../ase_lab/README.md) describes the supervised workflow.

## Method

The final demonstration used OpenHands SDK 1.62.0 and the DeepSeek Flash relay against the public ASE-Lab revision `b5c7432ac85a68c8ee3be1fd227ea52fc7ca8e3c`. Three cases were fixed before evaluation and run once in the final batch. Each case had a ceiling of six model requests and 240 seconds of agent time. The supervisor compared the complete disposable checkout before and after each run. Review considered citation relevance, answer coverage and uncertainty in addition to the program outcome.

## Final batch

| Case | Requests | Agent seconds | Review |
| --- | ---: | ---: | --- |
| Locate out-of-scope change detection and rejection and identify its test | 6 | 31.842 | Partial. The report located detection and rejection but missed the requested runtime rejection test. |
| Explain dependent validation and identify tests of skipped commands | 6 | 29.084 | Complete. The report cited the execution branch and tests distinguishing failure from a skipped command. |
| Identify the cause of a hypothetical incident with insufficient evidence | 5 | 35.267 | Appropriate inconclusive report. It requested diagnostics, reproduction information and the affected component. |

All three agents finished within their ceilings and the checkouts remained unchanged. The batch used 17 relay requests and recorded 110,132 tokens. One request disconnected without usage telemetry, and a monetary total was unavailable. The locked-image offline suite passed 34 project tests, five relay tests and an OpenHands integration probe with a local fake upstream.

## Lessons and limits

Earlier runs exposed long exploration without a final answer, quotation transcription errors, and uncertainty that exceeded the search evidence. The supervisor now reserves the final request for reporting, extracts excerpts directly from tracked files and renders a bounded inconclusive result. An earlier batch found the rejection test, while the final batch missed it. Human review remains part of the laboratory workflow. This small demonstration describes observed behavior and does not estimate performance across repositories.
