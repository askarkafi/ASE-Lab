# Academic Foundations and Evidence-Based Rationale for ASE-Lab

**ASE-Lab — Agentic Software Engineering Laboratory**

**Document type:** Academic and engineering rationale

**Evidence reviewed:** 16 November 2026

**Status:** Draft for public project documentation

## 1. Purpose and scope

Recent university courses and peer-reviewed research treat LLM-based agents not merely as prompting applications, but as engineered systems requiring tool interfaces, execution environments, feedback loops, evaluation, and explicit trade-offs. This document examines a selected body of such evidence and draws out a proportionate educational and engineering direction for **ASE-Lab**: an independent initiative for learning, building, and empirically evaluating agents for software engineering.

The argument proceeds **from documented educational practices and research findings to a project design rationale**. It is an assessment of how the project can be grounded, not a claim about the chronology of every internal decision or an assertion that the cited institutions have endorsed ASE-Lab.

## 2. Evidence from university courses

Several publicly documented courses provide especially relevant examples:

- **Stanford CS329Z — Engineering AI Agents (Fall 2026)** teaches agent components and design trade-offs through applied work. Students build an agentic harness without an agent framework, then construct evaluations for an existing agent, alongside a quarter-long project. This supports an educational approach in which learners first understand the underlying mechanisms and then use higher-level abstractions. [C1]
- **UC Berkeley CS294/194-196 — Large Language Model Agents (Fall 2024)** covers reasoning, planning, tools, infrastructure, evaluation, and applications including software development. Its syllabus explicitly includes a lecture on software-development agents and offers labs and implementation-based project pathways. This connects general agent engineering to repository-level software tasks. [C2]
- **Stanford MS&E 203 — Building and Evaluating AI Products and Agents (Fall 2026)** places problem selection, measurable success criteria, failure analysis, quality, latency, and cost within a project-based development cycle. This is evidence for evaluating useful systems rather than treating a working demonstration as sufficient validation. [C3]
- **Carnegie Mellon 06-643 — Creating Scientific Software with AI Coding Agents (Spring 2026)** combines AI-assisted development with testing, packaging, code quality, documentation, and CI/CD. Its emphasis on understanding and reviewing AI-generated work reinforces the need to preserve software-engineering discipline when agents are involved. [C4]

**Educational inference.** These courses differ in scope, but collectively motivate a learning-by-building model: understand core mechanisms, implement a bounded capability, assess it rigorously, and improve it through evidence. They do not prescribe one universal architecture or require a complete agent platform as a course deliverable.

## 3. Evidence from research and open projects

The research literature supplies a complementary technical rationale:

- **ReAct** describes the interleaving of model reasoning, actions, and observations, providing a conceptual basis for studying agent execution loops. [R1]
- **SWE-bench** frames repository-level issue resolution as a testable software-engineering task; **SWE-agent** demonstrates the importance of designing interfaces through which agents inspect and modify code and run tests. Together, they justify using realistic, reproducible tasks to study coding agents. [R2, R3]
- **OpenHands** documents a general-purpose software-agent platform, while the **OpenHands Software Agent SDK** paper describes a more composable foundation with extensible tools, execution environments, and lifecycle control. These works make reusing an existing agent infrastructure a credible engineering option, rather than reimplementing every subsystem. [R4, R5]
- **Agentless** demonstrates that a comparatively simple, staged workflow can be competitive on certain software-repair benchmarks. **AI Agents That Matter** identifies weaknesses in agent evaluation, including excessive emphasis on accuracy, insufficient cost accounting, and limited reproducibility. These findings argue against unnecessary complexity and for explicit baselines and measurement. [R6, R7]

The open-source **mini-SWE-agent** project offers an additional example of a deliberately small coding-agent implementation useful for understanding the fundamentals. [P1]

**Research inference.** The evidence supports *studying and experimentally comparing* agent designs; it does not establish that greater autonomy, more agents, or a larger platform will necessarily improve outcomes. Architectural choices should remain proportional to the problem and subject to revision.

## 4. Implications for ASE-Lab

From these educational and research patterns, a coherent project direction follows:

1. **Deep learning through implementation.** Study agent loops, tools, context, execution, and evaluation through focused readings and small exercises; avoid treating SDK usage as a substitute for architectural understanding.
2. **An incremental, modular software artifact.** Develop real, reusable capabilities for software-engineering agents, with clear boundaries that can accommodate later extensions without requiring them upfront.
3. **A bounded first vertical slice.** Begin with one demonstrable and testable capability rather than attempting a complete multi-agent platform within one academic term. [Repository issue investigation](../planning/first-slice.md) is now the selected first direction; its detailed task instances and implementation remain to be validated.
4. **Evaluation from the outset.** Record task outcomes, test results, failures, execution traces, latency, and model cost where available. Compare against simple or non-agentic baselines when informative.
5. **Research capacity as a consequence, not a presumption.** Once the system and evaluation process are stable, questions about tool-interface design, context management, reliability, or agent-versus-workflow trade-offs may be developed into controlled studies.

### Role of OpenHands

The **OpenHands Software Agent SDK** is a practical *initial implementation basis*, not an irreversible choice or a claim of proven superiority over all alternatives. Its documented architecture is relevant to ASE-Lab's modular ambitions. The project should still evaluate SDK behavior, version compatibility, execution safety, integration effort, and fitness for its own tasks. [R5, P2]

## 5. Conclusion and limits of the argument

The selected courses establish credible precedents for **project-based agent education**, while peer-reviewed research establishes a substantive technical domain centered on **software-agent interfaces, execution, and evaluation**. Taken together, they support pursuing ASE-Lab as a **small-first, modular, evidence-oriented engineering laboratory** that unites practical learning, reusable software development, and potential later research.

This is a **reasoned project rationale**, not proof that ASE-Lab is scientifically novel, the best possible implementation, or guaranteed to succeed. The sources are selected for relevance, not presented as an exhaustive systematic review. Course descriptions and public assignments may change; benchmark results are setting-dependent; and published work on OpenHands does not validate every subsequent SDK release. ASE-Lab is independent of the cited universities and research groups, and no institutional affiliation or endorsement is implied.

## References

### University courses

- **[C1]** Stanford University. *CS329Z: Engineering AI Agents*. Fall 2026. [Course](https://cs329z.stanford.edu/) · [Coursework and assignments](https://cs329z.stanford.edu/logistics.html).
- **[C2]** University of California, Berkeley. *CS294/194-196: Large Language Model Agents*. Fall 2024. [Official syllabus and project requirements](https://rdi.berkeley.edu/llm-agents/f24).
- **[C3]** Stanford University. *MS&E 203: Building and Evaluating AI Products and Agents*. Fall 2026. [Course](https://web.stanford.edu/class/msande203/) · [Syllabus](https://web.stanford.edu/class/msande203/syllabus/).
- **[C4]** Carnegie Mellon University. *06-643: Creating Scientific Software with AI Coding Agents*. Spring 2026. [Course](https://kitchingroup.cheme.cmu.edu/s26-06643/intro.html) · [Syllabus](https://kitchingroup.cheme.cmu.edu/s26-06643/syllabus.html).

### Peer-reviewed research

- **[R1]** Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR. [Paper](https://openreview.net/forum?id=WE_vluYUL-X).
- **[R2]** Jimenez, C. E., et al. (2024). *SWE-bench: Can Language Models Resolve Real-world Github Issues?* ICLR. [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html).
- **[R3]** Yang, J., et al. (2024). *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*. NeurIPS. [Proceedings](https://papers.nips.cc/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html).
- **[R4]** Wang, X., et al. (2025). *OpenHands: An Open Platform for AI Software Developers as Generalist Agents*. ICLR. [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/a4b6ad6b48850c0c331d1259fc66a69c-Abstract-Conference.html).
- **[R5]** Wang, X., et al. (2026). *The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents*. MLSys. [Proceedings](https://proceedings.mlsys.org/paper_files/paper/2026/hash/8ae9cf363ea625161f885b798c1f1f78-Abstract-Conference.html).
- **[R6]** Xia, C. S., Deng, Y., Dunn, S., & Zhang, L. (2025). *Demystifying LLM-Based Software Engineering Agents*. *Proceedings of the ACM on Software Engineering*, FSE. [DOI](https://doi.org/10.1145/3715754).
- **[R7]** Kapoor, S., Stroebl, B., Siegel, Z. S., Nadgir, N., & Narayanan, A. (2025). *AI Agents That Matter*. *Transactions on Machine Learning Research*. [Article](https://mlanthology.org/tmlr/2025/kapoor2025tmlr-ai/).

### Open-source project references

- **[P1]** SWE-agent contributors. *mini-SWE-agent*. [Source repository](https://github.com/SWE-agent/mini-swe-agent).
- **[P2]** OpenHands contributors. *OpenHands Software Agent SDK*. [Source repository](https://github.com/OpenHands/software-agent-sdk) · [Documentation](https://docs.openhands.dev/sdk).
