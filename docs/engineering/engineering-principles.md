# Engineering principles

ASE-Lab aims to follow ordinary good software engineering practices while recognizing the specific uncertainty of LLM-based systems.

## Guiding principles

1. **Build vertically, not broadly.** Prefer an executable end-to-end capability over many disconnected placeholders.
2. **Reuse intentionally.** Adopt existing open-source SDKs and tools where they solve established problems; study their architecture rather than treating them as black boxes.
3. **Keep boundaries explicit.** Make the responsibilities of project code, external SDKs, models, and execution environments understandable.
4. **Avoid premature abstraction.** Introduce interfaces when a real use case or test justifies them.
5. **Make behavior observable.** Collect enough logs, events, and outcomes to debug and evaluate the implemented slice.
6. **Test project-owned contracts.** Use focused unit and integration tests, and note where model outputs are non-deterministic.
7. **Protect execution environments.** Model-generated code and commands must be subject to validation, permissions, limits, and appropriate isolation.
8. **Document uncertainty.** Distinguish assumptions, proposals, accepted decisions, and verified capabilities.
9. **Preserve reproducibility.** Record external dependencies and versions used in executable examples.
10. **Review AI-generated contributions.** AI coding tools may help produce code, but the project retains responsibility for design, validation, and security.

## Definition of a useful implementation slice

A slice should have a documented purpose, a minimal working path, a repeatable demonstration, basic automated checks, and an explanation of what ASE-Lab implements versus what it reuses.
