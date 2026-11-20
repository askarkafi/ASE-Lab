# ASE-Lab

**Agentic Software Engineering Laboratory**

*Design and incremental development of an extensible LLM-based agent platform for software engineering.*

> **Project status:** A first supervised software slice was built and evaluated privately. No executable ASE-Lab capability or production platform has been published yet.

## Overview

**ASE-Lab** is a long-term software engineering initiative exploring how LLM-based agents can be designed, integrated, and evolved to support software engineering activities. The goal is to develop a useful, extensible system through small, verifiable increments while making its architecture and engineering decisions understandable and maintainable.

The project connects three complementary perspectives:

- **Product engineering:** building reusable capabilities that can eventually form a practical software product.
- **Education:** learning agent architectures, tool integration, orchestration, and software engineering through hands-on implementation and analysis.
- **Future research:** leaving room for controlled experiments and student-led extensions, without making research infrastructure a prerequisite for the initial work.

## Approach

We selected the **OpenHands Software Agent SDK** as the initial implementation basis. A private command-line integration and a selected three-case evaluation have been completed; the maintainer accepted the bounded engineering demonstration. The selection remains revisable if concrete evidence requires it. See the [public evaluation summary](docs/evaluation/first-slice.md) for outcomes and limits.

The initial academic stage targets **a small but genuine part of the long-term system**, not a complete product, production-ready platform, or multi-agent solution within one semester.

## Current state

| Area | Status |
| --- | --- |
| Project identity and broad direction | Established |
| Project documentation | Initial public foundation |
| SDK selection | OpenHands 1.62.0 exercised in a private ASE-Lab command-line integration |
| Detailed architecture | Not finalized |
| First implementation slice | Supervised repository issue investigation implemented and evaluated privately; code publication pending |
| Functional product release | Not available |

## Documentation

Start with the [documentation index](docs/README.md). Key documents include:

- [Vision and goals](docs/overview/vision.md)
- [Scope and non-goals](docs/overview/scope.md)
- [Conceptual architecture](docs/architecture/conceptual-architecture.md)
- [Engineering principles](docs/engineering/engineering-principles.md)
- [SDK selection approach](docs/engineering/sdk-strategy.md)
- [Educational objectives](docs/education/learning-objectives.md)
- [OpenHands-first, evidence-linked roadmap](docs/planning/roadmap.md)
- [First-slice evaluation summary](docs/evaluation/first-slice.md)
- [Academic foundations and evidence-based rationale](docs/research/academic-foundations.md) ([فارسی](docs/research/academic-foundations.fa.md))
- [University course, project and paper resource index](docs/research/academic-resources.md)
- [Public release policy](docs/governance/publication-policy.md)

## Participation and releases

This public repository is the **curated, published view** of ASE-Lab. Development and exploratory decisions may be carried out separately; reviewed results can be published here in deliberate releases. See [publication policy](docs/governance/publication-policy.md) and [contribution guidance](CONTRIBUTING.md).

## License status

**No project-wide license has been selected yet.** Public visibility does not, by itself, grant permission to reuse or redistribute ASE-Lab's original content. Licenses for external SDKs and dependencies are separate and will be reviewed before adoption. See the [dependency policy](docs/engineering/dependencies-and-forks.md).

## Disclaimer

Architecture diagrams and future features remain **design intentions**. The private first-slice evidence supports only the bounded behavior described in the evaluation summary; it is not a release commitment for other features.
