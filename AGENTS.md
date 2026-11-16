# Guidance for AI coding assistants

This file guides tools such as AI coding agents when working with **the public ASE-Lab repository**.

1. Keep the project name **ASE-Lab** unchanged unless an explicit decision is recorded.
2. Read [the project vision](docs/overview/vision.md), [scope](docs/overview/scope.md), and [conceptual architecture](docs/architecture/conceptual-architecture.md) before proposing significant changes.
3. Do not imply that an agent runtime, SDK, product feature, or production deployment is already available unless code and tests demonstrate it.
4. Do not select a technology, introduce broad abstractions, or create extensive placeholder modules without a justified task.
5. Respect the [publication policy](docs/governance/publication-policy.md): only intentionally reviewed information belongs in public commits.
6. Never commit tokens, credentials, private datasets, sensitive traces, or private planning material.
7. For implementation changes, explain the design trade-off, add tests where appropriate, and keep documentation consistent.
8. Verify documentation links with `python scripts/check_docs.py`.

All generated or edited material must be reviewed by a human maintainer before publication.
