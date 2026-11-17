# ASE-Lab

**Agentic Software Engineering Laboratory**

*Design and incremental development of an extensible LLM-based agent platform for software engineering.*

> **Project status:** Foundation stage — architecture and documentation in progress. No operational agent platform is released yet.

## Overview

**ASE-Lab** is a long-term software engineering initiative exploring how LLM-based agents can be designed, integrated, and evolved to support software engineering activities. The goal is to develop a useful, extensible system through small, verifiable increments while making its architecture and engineering decisions understandable and maintainable.

The project connects three complementary perspectives:

- **Product engineering:** building reusable capabilities that can eventually form a practical software product.
- **Education:** learning agent architectures, tool integration, orchestration, and software engineering through hands-on implementation and analysis.
- **Future research:** leaving room for controlled experiments and student-led extensions, without making research infrastructure a prerequisite for the initial work.

## Approach

We have selected the **OpenHands Software Agent SDK** as the initial implementation basis to support hands-on learning and incremental software-agent development rather than reimplementing an entire runtime. Actual integration, the first task, and detailed internal architecture remain to be validated. The selection is revisable if concrete evidence requires it.

The initial academic stage targets **a small but genuine part of the long-term system**, not a complete product, production-ready platform, or multi-agent solution within one semester.

## Current state

| Area | Status |
| --- | --- |
| Project identity and broad direction | Established |
| Project documentation | Initial public foundation |
| SDK selection | OpenHands chosen for initial integration; not yet validated in a running ASE-Lab capability |
| Detailed architecture | Not finalized |
| First implementation slice | Repository issue investigation selected as the initial direction; not implemented |
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
- [Academic foundations and evidence-based rationale](docs/research/academic-foundations.md) ([فارسی](docs/research/academic-foundations.fa.md))
- [University course, project and paper resource index](docs/research/academic-resources.md)
- [Public release policy](docs/governance/publication-policy.md)

## Participation and releases

This public repository is the **curated, published view** of ASE-Lab. Development and exploratory decisions may be carried out separately; reviewed results can be published here in deliberate releases. See [publication policy](docs/governance/publication-policy.md) and [contribution guidance](CONTRIBUTING.md).

## License status

**No project-wide license has been selected yet.** Public visibility does not, by itself, grant permission to reuse or redistribute ASE-Lab's original content. Licenses for external SDKs and dependencies are separate and will be reviewed before adoption. See the [dependency policy](docs/engineering/dependencies-and-forks.md).

## Disclaimer

Architecture diagrams and future features in this repository are **design intentions**, not claims of implemented functionality or release commitments.
