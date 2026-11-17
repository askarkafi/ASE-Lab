# University Course Materials for ASE-Lab — Complete Link Index

> **راهنمای فارسی / Persian guide:** این فایل، فهرست یکپارچهٔ لینک‌های دانشگاهی و پژوهشی مرتبط با ASE-Lab است؛ شامل ۹ دورهٔ دانشگاهی، سیلابس‌ها، فایل‌های ارائه، ویدئوها، تمرین‌ها، Notebookها، پروژه‌های متن‌باز و مقالات منتخب. در بخش دروس، کنار هر لینک توضیح انگلیسی دربارهٔ محتوا و کاربرد آن آمده است؛ بخش‌های تکمیلی پروژه‌ها و مقالات، توضیحات فارسی دارند. همهٔ لینک‌ها به منابع اصلی اشاره می‌کنند و فایل‌های متعلق به دانشگاه‌ها بازنشر نشده‌اند.
>
> **راهنمای استفاده:** برای اسلایدهای PDF روی لینک `PDF` کلیک کنید و در مرورگر ذخیره کنید؛ در صفحات GitHub از **Code → Download ZIP** یا `git clone` استفاده کنید؛ برای ویدئوها صفحهٔ رسمی جلسه را دنبال کنید. در فایل‌های بزرگ یا محدود به سامانهٔ آموزشی ممکن است دانلود نیازمند ورود یا با محدودیت همراه باشد. **آخرین گردآوری: ۱۶ نوامبر ۲۰۲۶.**

## مسیر سریع بر اساس نیاز ASE-Lab

| هدف | منبع پیشنهادی | خروجی مفید |
|---|---|---|
| فهم معماری و حلقهٔ اجرا | [Stanford CS329Z](https://cs329z.stanford.edu/)؛ جلسات 01 و 04–06 | اسلاید + تمرین ساخت Harness |
| شروع Coding Agents | [Graham Neubig — Agents for Software Development](https://rdi.berkeley.edu/llm-agents-mooc/slides/neubig24softwareagents.pdf) | PDF ارائهٔ ۵۳ صفحه‌ای |
| ارزیابی ایجنت | [CS329Z HW2](https://github.com/cs329z/assignment2-evals)؛ [Berkeley Agentic AI](https://rdi.berkeley.edu/agentic-ai/f25) | تمرین ارزیابی + مبانی بنچمارک |
| آزمون، کیفیت کد و CI/CD | [CMU 06-643](https://kitchingroup.cheme.cmu.edu/s26-06643/intro.html) | Notebook و تکالیف عملی |
| یادگیری Harness و مستندسازی دقیق | [MIT 6.S950](https://agencyai.mit.edu/syllabus/) | درس + Lab + اسلاید و کد |
| پیاده‌سازی با SDK | [OpenHands Software Agent SDK](https://github.com/OpenHands/software-agent-sdk) | کد، مستندات، مثال‌ها |

---

**Curated primary-source directory** | **90 unique external links** | **33 direct PDF URLs** | Verified against public official course pages on **16 November 2026**

**Purpose:** Supporting reading and hands-on learning for the *Academic Foundations and Evidence-Based Rationale for ASE-Lab*.

**Scope:** Eight courses cited in the broader ASE-Lab academic research, plus one newly identified MIT supplementary course. Only public links are listed. These links do not imply institutional affiliation or endorsement.

> **Access and copyright note:** This file is an annotated directory of original resources, **not a mirror**. Some PDF decks linked by official websites are large and could not be fetched by the automated browser, though the URLs were traced from the official course pages. Course slide decks, recordings, and datasets may have their own copyrights and access restrictions. Read the licensing terms before copying any content into ASE-Lab. Resources on Canvas/Ed/Gradescope may require enrollment. Fall 2026 courses are ongoing as of this index date, and future-session decks may not yet be posted.

## Quick start: five high-value entries

1. **[Stanford CS329Z — official weekly schedule, slides and video links](https://cs329z.stanford.edu/)** — closest agent-engineering syllabus.
2. **[Stanford HW1 — build an agent harness](https://github.com/cs329z/assignment1-harness)** and **[HW1 PDF](https://github.com/cs329z/assignment1-harness/blob/main/cs329z_assignment1_harness.pdf)** — starter code, tests, design constraints.
3. **[Stanford HW2 — evaluate an agent](https://github.com/cs329z/assignment2-evals)** and **[HW2 PDF](https://github.com/cs329z/assignment2-evals/blob/main/cs329z_assignment2_evaluation.pdf)** — task specification, code, evaluators and reporting templates.
4. **[Berkeley — Agents for Software Development (Graham Neubig, PDF)](https://rdi.berkeley.edu/llm-agents-mooc/slides/neubig24softwareagents.pdf)** · **[public lecture video](https://www.youtube.com/live/f9L9Fkq-8K4)** — direct connection to SWE-agent and OpenHands.
5. **[CMU 06-643 — full notebook-based teaching site](https://kitchingroup.cheme.cmu.edu/s26-06643/intro.html)** · **[source repository](https://github.com/jkitchin/s26-06643)** — testing, packaging, AI-assisted workflows and extensibility.

## 1. Stanford University — CS329Z: Engineering AI Agents (Fall 2026)

- **[Course overview, detailed lecture schedule, readings, slide links and selected lecture videos](https://cs329z.stanford.edu/)**
- **[Logistics, assessed coursework and learning policies](https://cs329z.stanford.edu/logistics.html)**
- **[HW1 repository (agent harness)](https://github.com/cs329z/assignment1-harness)** · **[HW1 handout (PDF)](https://github.com/cs329z/assignment1-harness/blob/main/cs329z_assignment1_harness.pdf)**
- **[HW2 repository (agent evaluation)](https://github.com/cs329z/assignment2-evals)** · **[HW2 handout (PDF)](https://github.com/cs329z/assignment2-evals/blob/main/cs329z_assignment2_evaluation.pdf)**
- **[Lecture 5 companion code (frameworks)](https://github.com/cs329z/lecture5-frameworks)**
- **[Student paper-video assignment handout (PDF)](https://web.stanford.edu/class/cs329z/assignments/paper_video.pdf)**

**Officially linked lecture PDF decks** (public URLs as shown in the course schedule; some are large):

| Lecture | Subject | Direct slides |
|---|---|---|
| 01 | Introduction, agent architecture, compound AI systems | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture01.pdf) |
| 02 | LLMs for builders, context engineering | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture02.pdf) |
| 03 | RAG and agentic retrieval | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture03.pdf) |
| 04 | Tool use and function calling | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture04.pdf) |
| 05 | Frameworks, orchestration and OpenHands | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture05.pdf) |
| 06 | Design patterns, scaffolds, context handling | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture06.pdf) |
| 07 | Agent memory | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture07.pdf) |
| 08 | Multi-agent systems | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture08.pdf) |
| 09 | Agent optimization | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture09.pdf) |
| 10 | Terminal-Bench and terminal agent evaluation | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture10.pdf) |
| 11 | Data for agentic systems | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture11.pdf) |
| 12 | Data selection and quality | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture12.pdf) |
| 13 | Agent evaluations and benchmark design | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture13.pdf) |
| 15 | LLM-as-judge and evaluation infrastructure | [PDF](https://web.stanford.edu/class/cs329z/slides/lecture15.pdf) |

**Public video example:** [Lecture 1 — What Are AI Agents?](https://www.youtube.com/watch?v=DGI4vucR71w). Further lecture video links are adjacent to each posted deck on the official schedule. The course also notes that some class recordings are available to enrolled students via Canvas, so public video coverage should not be assumed complete.

**Suggested ASE-Lab focus:** HW1, HW2, lectures 01, 04–06 and 13–15. The course's **Coding & Software Agents** session is scheduled for **30 November 2026** and has no slide link as of 16 November 2026; check the course schedule later.

## 2. UC Berkeley — CS294/194-196: Large Language Model Agents (Fall 2024)

- **[Official course, full syllabus, readings and linked videos](https://rdi.berkeley.edu/llm-agents/f24)**
- **[Department's public course collection](https://rdi.berkeley.edu/publicCourses)** — includes a video playlist entry.

**High-value lecture files and recordings:**

| Lecture | Resources |
|---|---|
| Agents for Software Development — Graham Neubig, 14 Oct | [PDF slides](https://rdi.berkeley.edu/llm-agents-mooc/slides/neubig24softwareagents.pdf) · [Video](https://www.youtube.com/live/f9L9Fkq-8K4) |
| LLM agents: history and overview — Shunyu Yao | [PDF](https://rdi.berkeley.edu/llm-agents/assets/llm_agent_history.pdf) · [Video and references on course page](https://rdi.berkeley.edu/llm-agents/f24) |
| Compound AI Systems and DSPy — Omar Khattab | [PDF](https://rdi.berkeley.edu/llm-agents-mooc/slides/dspy_lec.pdf) · [Video on course page](https://rdi.berkeley.edu/llm-agents/f24) |
| Agentic AI Frameworks and AutoGen — Chi Wang | [PDF](https://rdi.berkeley.edu/llm-agents-mooc/slides/autogen.pdf) |
| Multimodal knowledge assistants — Jerry Liu | [PDF](https://rdi.berkeley.edu/llm-agents-mooc/slides/MKA.pdf) (large file) |

**Project information:** the official syllabus contains project pathways, labs, proposal and implementation requirements. Some submissions and original recordings are not public and/or require institutional access.

**Suggested ASE-Lab focus:** software development agents, AutoGen as an architectural counterexample, DSPy and reliability discussions.

## 3. UC Berkeley — CS294/194-280: Advanced Large Language Model Agents (Spring 2025)

- **[Official syllabus, slides, weekly recordings, reading links and project tracks](https://rdi.berkeley.edu/adv-llm-agents/sp25)**.
- [Coding Agents and AI for Vulnerability Detection — Charles Sutton (PDF)](https://rdi.berkeley.edu/adv-llm-agents/slides/Code%20Agents%20and%20AI%20for%20Vulnerability%20Detection.pdf)
- [Reasoning, Memory, and Planning of Language Agents — Yu Su (PDF)](https://rdi.berkeley.edu/adv-llm-agents/slides/language_agents_YuSu_Berkeley.pdf)
- [Reasoning and Alignment — Jason Weston (PDF)](https://rdi.berkeley.edu/adv-llm-agents/slides/Jason-Weston-Reasoning-Alignment-Berkeley-Talk.pdf) (large file)

**Project structure:** application track and research track, with proposal, milestone, lab, poster, final presentation and report; the official page describes the distinction between applied work and novel research.

**Suggested ASE-Lab focus:** coding agent tool use, verification and memory/planning; read selectively.

## 4. UC Berkeley — CS294/194-196: Agentic AI (Fall 2025)

- **[Official syllabus, slides, recordings and project rubric](https://rdi.berkeley.edu/agentic-ai/f25)**.
- [Introduction (PDF)](https://rdi.berkeley.edu/agentic-ai/slides/introduction_25.pdf)
- [Overview of LLM Agents (PDF)](https://rdi.berkeley.edu/agentic-ai/slides/lecture1.pdf)
- [Agent Evaluations and Project Overview (PDF)](https://rdi.berkeley.edu/agentic-ai/slides/LLM%20Agent%20Evaluations%20%26%20Project%20Overview.pdf)
- [Multi-Agent AI (PDF)](https://rdi.berkeley.edu/agentic-ai/slides/multiagent_berkeley_2025.pptx.pdf)
- [Lessons from Training Agentic Models (PDF)](https://rdi.berkeley.edu/agentic-ai/slides/weizhu.pdf)

**Project structure:** Green Agent evaluator development and White Agent implementation, with demos and reports; the official page includes specific assessment weights and deliverable dates.

**Suggested ASE-Lab focus:** evaluation architecture and the boundary between the agent being evaluated and the evaluator.

## 5. Stanford University — MS&E 203: Building and Evaluating AI Products and Agents (Fall 2026)

- **[Official course page](https://web.stanford.edu/class/msande203/)**.
- **[Ten-week syllabus with assigned readings and deliverables](https://web.stanford.edu/class/msande203/syllabus/)**.

**Relevant topics:** evaluation design and metrics; multi-turn agents and simulation; qualitative failure investigation; responsible AI; proposal, midterm and final milestones. Public syllabus/readings are available, but a comprehensive open lecture-slide archive was **not verified**. Some onboarding and submissions are hosted in Canvas or shared documents.

**Suggested ASE-Lab focus:** measurable success criteria, error analysis and milestone discipline without importing the full course-management overhead.

## 6. Carnegie Mellon University — 06-643: Creating Scientific Software with AI Coding Agents (Spring 2026)

- **[Official course website](https://kitchingroup.cheme.cmu.edu/s26-06643/intro.html)**
- **[Syllabus, schedule, grading and project specification](https://kitchingroup.cheme.cmu.edu/s26-06643/syllabus.html)**
- **[All assignments, technical tasks and reflection requirements](https://kitchingroup.cheme.cmu.edu/s26-06643/assignments/index.html)**
- **[Public source repository with notebooks](https://github.com/jkitchin/s26-06643)**

**Fully readable lecture modules and notebook sources:**

- [Module 05 — Testing with AI](https://kitchingroup.cheme.cmu.edu/s26-06643/05-testing-with-ai/05-testing-with-ai.html)
- [Module 06 — Code Quality](https://kitchingroup.cheme.cmu.edu/s26-06643/06-code-quality/06-code-quality.html)
- [Module 08 — GitHub Collaboration](https://kitchingroup.cheme.cmu.edu/s26-06643/08-github-collaboration/08-github-collaboration.html)
- [Module 11 — Configuring & Extending AI Agents (skills, MCP and custom tools)](https://kitchingroup.cheme.cmu.edu/s26-06643/11-advanced-mcp/11-advanced-mcp.html)

**Assignment samples:**

- [A1 — AI + Terminal Foundations](https://kitchingroup.cheme.cmu.edu/s26-06643/assignments/a1-ai-exploration.html)
- [A2 — Git + API Exploration](https://kitchingroup.cheme.cmu.edu/s26-06643/assignments/a2-api-package.html)
- [A3 — Package + Test](https://kitchingroup.cheme.cmu.edu/s26-06643/assignments/a3-testing-quality.html)

**Suggested ASE-Lab focus:** tests, code quality, traceable development, tool extension, safe scripting. This course is largely about *using* coding agents, not building an agent runtime.

## 7. Stanford University — CS224G: Building and Scaling LLM Applications (Winter 2026)

- **[Course site](https://web.stanford.edu/class/cs224g/index.html)**
- **[Detailed 10-week schedule with linked lecture notes](https://web.stanford.edu/class/cs224g/schedule.html)**
- [Agent Orchestration & Workflow Design (PDF)](https://web.stanford.edu/class/cs224g/lectures/CS%20224G%202026%20Lecture%207%20-%20Agent%20Orchestration%20%26%20Workflow%20Design.pdf)
- [Code Generation with LLMs (PDF)](https://web.stanford.edu/class/cs224g/lectures/CS%20224G%202026%20Lecture%2011%20-%20Code%20Generation%20with%20LLMs.pdf) (linked from schedule; automated fetch timed out)
- [Agentic Orchestration with PydanticAI (PDF)](https://web.stanford.edu/class/cs224g/lectures/CS%20224G%202026%20Lecture%2014%20-%20Agentic%20Orchestration%20with%20PydanticAI.pdf)
- [PydanticAI base-agent teaching repository](https://github.com/LeonieFreisinger/pydanticai-base-agent)

The schedule also links a Colab notebook for the agent-design session, lecture notes for context engineering, RAG, evaluation and code generation, plus Demo Day recordings and student project pages.

**Suggested ASE-Lab focus:** implementation cadence, context engineering and applied orchestration.

## 8. MIT — 6.S192: Agentic Web / Networked AI Agents (January 2026)

- **[Official MIT EECS course listing and full ten-session outline](https://eecsis.mit.edu/plugins/IAP2026.html)**.
- Workshop themes: agent protocols (MCP, A2A), discovery, identity and security, sandboxing, coordination and deployment.
- **Public slide decks, recordings and full workshop repository for this exact IAP offering were not verified.** Do not equate the official course description with a public lecture archive.

## Additional newly identified course (not among the original eight)

### MIT — 6.S950: Agency with AI, Fall 2026

This is an **additional independently verified** resource. It was not cited in the original justification document, but is strongly aligned with its educational aims.

- **[Course homepage](https://agencyai.mit.edu/)**
- **[Official syllabus, lectures and labs](https://agencyai.mit.edu/syllabus/)**
- **[Public GitHub repository of released slide decks and labs](https://github.com/agency-with-ai/materials)**
- **[Lecture 5 — The Harness](https://agencyai.mit.edu/w5/)** · [presentation](https://slides.com/shensquared/agencyai-f26-lec05/embed?byline=hidden&style=light)
- **[Lab 5 — Inspect and experiment on a small agent harness](https://agencyai.mit.edu/lab5/)**

Topics: source-checked literature review, spec-driven agent building, harness design, context management, evaluation methodology, delegated work and provenance. The authors explicitly label course materials **CC BY-SA 4.0**, subject to separate rights for embedded third-party content. This provides a particularly reusable learning resource, distinct from the older MIT 6.S192 offering.

## Suggested minimum study sequence for ASE-Lab

| Learning objective | First source | Practical follow-up |
|---|---|---|
| Agent loop and architecture | Stanford CS329Z lectures 01, 04–06 | CS329Z HW1 starter code |
| Coding-agent architectures | Berkeley 2024: Graham Neubig lecture | Inspect mini-SWE-agent / OpenHands SDK |
| Evaluation and replicability | Stanford CS329Z lectures 13–15; HW2 | Create a small ASE-Lab eval set |
| Good software engineering | CMU modules 05, 06, 11 | Tests, code quality and an extension prototype |
| Project and reporting discipline | Stanford MS&E 203 syllabus | Define milestones, acceptance tests and failure reports |
| Critical evaluation of tool use | MIT 6.S950 lecture 5 and lab 5 | Trace the execution loop and compare model/harness changes |

**Boundary:** These suggestions are ASE-Lab's interpretation and study plan, not a claim that universities endorse the project or its choice of SDK.

## Source citations for maintainers

When citing courses in a public rationale, cite **the official syllabus/course page** rather than a copy of its slide decks. Cite individual decks with lecturer, lecture title, semester and URL where relevant. For permission to mirror or adapt files, consult each author's/license notice rather than assuming public accessibility is equivalent to open licensing.

---

# Additional sources — research projects, academic papers and documentation

این بخش به نسخهٔ پیشین افزوده شده تا لینک‌های *Academic Foundations and Evidence-Based Rationale for ASE-Lab* و منابع پژوهشی مرتبط نیز همگی در **همین فایل واحد** در دسترس باشند. پیوندهای زیر، مگر جایی که خلاف آن ذکر شده، به مخزن رسمی یا صفحهٔ انتشار مقاله می‌روند؛ وجود لینک، به معنی دسترسی آزاد به تمام داده‌ها یا مجوز بازنشر نیست.

## 9. پروژه‌های متن‌باز و زیرساخت‌های مرتبط

| پروژه | لینک مستقیم | نوع / کاربرد برای ASE-Lab |
|---|---|---|
| OpenHands Software Agent SDK | [مخزن رسمی GitHub](https://github.com/OpenHands/software-agent-sdk) | **کد**؛ زیرساخت اولیهٔ انتخابی برای ساخت ایجنت، ابزارها و محیط اجرا |
| OpenHands SDK documentation | [مستندات رسمی SDK](https://docs.openhands.dev/sdk) | **Documentation**؛ API، نمونهٔ استفاده و دستورالعمل‌های نصب/اجرا |
| SWE-agent | [مخزن پروژه](https://github.com/SWE-agent/SWE-agent) | **کد و آموزش**؛ حل مسئلهٔ نرم‌افزاری با تعامل با Repository و Terminal |
| mini-SWE-agent | [مخزن پروژه](https://github.com/SWE-agent/mini-swe-agent) | **کد کم‌حجم**؛ مطالعهٔ معماری حلقهٔ ایجنت و اقدامات خط فرمان |
| SWE-bench | [مخزن بنچمارک](https://github.com/SWE-bench/SWE-bench) · [معرفی رسمی](https://www.swebench.com/original) | **Benchmark / کد و داده**؛ مسائل واقعی GitHub و ارزیابی Patch |
| Agentless | [مخزن GitHub](https://github.com/OpenAutoCoder/Agentless) | **Baseline**؛ مسیر سادهٔ Localization–Repair–Validation برای مقایسه با Agent |
| AgentBeats | [صفحهٔ پژوهشی Berkeley](https://rdi.berkeley.edu/agentx-agentbeats) · [مخزن GitHub](https://github.com/agentbeats/agentbeats) | **ارزیابی**؛ جداکردن ارزیاب از ایجنت تحت آزمون (Green/White Agent) |
| Stanford CS329Z — HW1 | [کد تکلیف](https://github.com/cs329z/assignment1-harness) · [صورت تکلیف PDF](https://github.com/cs329z/assignment1-harness/blob/main/cs329z_assignment1_harness.pdf) | **تمرین عملی**؛ ساخت Agent Harness، ابزارها و آزمون‌ها |
| Stanford CS329Z — HW2 | [کد تکلیف](https://github.com/cs329z/assignment2-evals) · [صورت تکلیف PDF](https://github.com/cs329z/assignment2-evals/blob/main/cs329z_assignment2_evaluation.pdf) | **تمرین عملی**؛ طراحی Evaluation و تحلیل خطا |
| MIT 6.S950 course materials | [مخزن رسمی تمرین و ارائه](https://github.com/agency-with-ai/materials) | **اسلاید و Lab**؛ Harness، Spec، ارزیابی و تمرین‌های علمی |

## 10. مقالات بنیادی و کلیدی

**راهنما:** در عنوان هر ردیف، نام و سال مقاله آمده؛ لینک معمولاً به صفحهٔ رسمی کنفرانس/مجله یا متن مقاله می‌رود. مقاله‌های منتشرشده در کنفرانس/مجله از گزارش‌های فنی و Preprintها تفکیک شده‌اند. در همهٔ موارد برای نوشتن گزارش علمی، ارجاع کتاب‌شناختیِ واقعی مقاله را از صفحهٔ اصلی بردارید.

| عنوان مقاله (انتشار) | لینک | دلیل مطالعه / ارتباط با ASE-Lab |
|---|---|---|
| ReAct: Synergizing Reasoning and Acting in Language Models (ICLR 2023) | [OpenReview](https://openreview.net/forum?id=WE_vluYUL-X) · [arXiv](https://arxiv.org/abs/2210.03629) | **Agent Loop**؛ ترکیب استدلال، اقدام و مشاهده |
| Reflexion: Language Agents with Verbal Reinforcement Learning (NeurIPS 2023) | [مقالهٔ کنفرانس](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html) | **Feedback / Memory**؛ ثبت بازخورد و اصلاح تلاش‌ها |
| Executable Code Actions Elicit Better LLM Agents — CodeAct (ICML 2024) | [PMLR](https://proceedings.mlr.press/v235/wang24h.html) | **Tool/Action Design**؛ کد اجرایی به‌عنوان واسط اقدام |
| SWE-bench: Can Language Models Resolve Real-world GitHub Issues? (ICLR 2024) | [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html) | **Benchmark**؛ ارزیابی تعمیر نرم‌افزار با Issue واقعی و تست |
| SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering (NeurIPS 2024) | [NeurIPS proceedings](https://papers.nips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html) | **Coding Agent Interface**؛ طراحی ابزارهای مناسب خواندن/ویرایش/تست کد |
| OpenHands: An Open Platform for AI Software Developers as Generalist Agents (ICLR 2025) | [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/a4b6ad6b48850c0c331d1259fc66a69c-Abstract-Conference.html) | **پلتفرم و محیط اجرا**؛ مبانی OpenHands اولیه |
| The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents (MLSys 2026) | [MLSys proceedings](https://proceedings.mlsys.org/paper_files/paper/2026/hash/8ae9cf363ea625161f885b798c1f1f78-Abstract-Conference.html) | **مبنای انتخاب SDK**؛ توسعه‌پذیری، چرخهٔ حیات و اجرای ایجنت |
| Demystifying LLM-based Software Engineering Agents — Agentless (FSE 2025) | [DOI](https://doi.org/10.1145/3715754) | **Baseline ساده**؛ ارزیابی اینکه کجا Workflow محدود کافی است |
| Training Software Engineering Agents and Verifiers with SWE-Gym (ICML 2025) | [PMLR](https://proceedings.mlr.press/v267/pan25g.html) | **محیط آموزش و ارزیابی**؛ مربوط به مراحل پژوهشی بعدی |
| AgentBench: Evaluating LLMs as Agents (ICLR 2024) | [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html) | **ارزیابی تعاملی**؛ تحلیل توانایی و شکست ایجنت |
| Lost in the Middle: How Language Models Use Long Contexts (TACL 2024) | [ACL Anthology](https://aclanthology.org/2024.tacl-1.9/) | **Context Engineering**؛ محدودیت استفادهٔ مدل از متن طولانی |
| AI Agents That Matter (TMLR 2025) | [ML Anthology](https://mlanthology.org/tmlr/2025/kapoor2025tmlr-ai/) | **روش‌شناسی ارزیابی**؛ هزینه، تکرارپذیری و اعتبار معیار |
| Toolformer: Language Models Can Teach Themselves to Use Tools (NeurIPS 2023) | [arXiv](https://arxiv.org/abs/2302.04761) | **مبانی Tool Use**؛ برای مطالعهٔ تکمیلی |

## 11. فایل‌ها و منابع پیشنهادی برای دانلود در اولویت

| اولویت | نوع | دانلود / مشاهده | استفادهٔ مشخص |
|---|---|---|---|
| 1 | PDF اسلاید | [Stanford Lecture 01](https://web.stanford.edu/class/cs329z/slides/lecture01.pdf) | فهم اجزای Agent و Agent Loop |
| 2 | PDF اسلاید | [Stanford Lecture 04](https://web.stanford.edu/class/cs329z/slides/lecture04.pdf) | Tool Use و Function Calling |
| 3 | PDF اسلاید | [Stanford Lecture 05](https://web.stanford.edu/class/cs329z/slides/lecture05.pdf) | Frameworks، Orchestration، آشنایی با OpenHands |
| 4 | PDF اسلاید | [Stanford Lecture 06](https://web.stanford.edu/class/cs329z/slides/lecture06.pdf) | طراحی Scaffolds و Context Management |
| 5 | PDF اسلاید | [Berkeley — Agents for Software Development](https://rdi.berkeley.edu/llm-agents-mooc/slides/neubig24softwareagents.pdf) | ارتباط مستقیم درس دانشگاهی با SWE-agent و OpenHands |
| 6 | PDF تکلیف | [Stanford — HW1 Harness](https://github.com/cs329z/assignment1-harness/blob/main/cs329z_assignment1_harness.pdf) | تمرین ساخت ایجنت مستقل از Framework |
| 7 | PDF تکلیف | [Stanford — HW2 Evaluation](https://github.com/cs329z/assignment2-evals/blob/main/cs329z_assignment2_evaluation.pdf) | تمرین طراحی سنجش و اعتبارسنجی |
| 8 | PDF اسلاید | [Stanford Lecture 13](https://web.stanford.edu/class/cs329z/slides/lecture13.pdf) | مبانی Evaluation و طراحی بنچمارک |
| 9 | PDF اسلاید | [Berkeley — Coding Agents and Vulnerability Detection](https://rdi.berkeley.edu/adv-llm-agents/slides/Code%20Agents%20and%20AI%20for%20Vulnerability%20Detection.pdf) | تحلیل نقش ابزارهای تعاملی در مسائل کدنویسی |
| 10 | منبع عملی | [CMU — Notebook repository](https://github.com/jkitchin/s26-06643) | تست، CI/CD، کیفیت کد و توسعهٔ ابزار |
| 11 | منبع عملی | [MIT — Harness Lab 5](https://agencyai.mit.edu/lab5/) | مطالعه و آزمایش Harness کوچک |
| 12 | مقاله | [OpenHands SDK (MLSys 2026)](https://proceedings.mlsys.org/paper_files/paper/2026/hash/8ae9cf363ea625161f885b798c1f1f78-Abstract-Conference.html) | آشنایی با معماری SDK و استدلال برای انتخاب آن |

## 12. وضعیت راستی‌آزمایی و نکات دسترسی

- صفحات رسمی ۹ دورهٔ معرفی‌شده، لینک‌های کلیدی GitHub و نمونه‌های منتخب اسلاید، هنگام تهیهٔ این فهرست در **۱۶ نوامبر ۲۰۲۶** در وب مشاهده شدند.
- اسلایدهای Stanford Lecture 01، ارائهٔ Berkeley *Agents for Software Development* و ارائهٔ *Coding Agents and AI for Vulnerability Detection* مستقیماً قابل باز کردن بودند. فایل‌های Stanford Lecture 13 و 15 از صفحهٔ رسمی دانشگاه لینک شده‌اند، اما دریافت خودکار آن‌ها به دلیل بزرگی فایل ناموفق بود؛ **این مورد به معنای خراب‌بودن لینک نیست**.
- دربارهٔ MIT 6.S192، سیلابس/شرح دوره تأیید شده ولی **آرشیو عمومی کامل فایل‌های ارائه و تمرین‌ها تأیید نشده** است. دربارهٔ Stanford MS&E 203 نیز سیلابس عمومی است اما آرشیو کامل اسلایدها تأیید نشده.
- برای بعضی دوره‌ها و تکالیف، Canvas، Ed، Gradescope یا سامانهٔ داخلی دانشگاه ممکن است نیازمند ثبت‌نام باشد. پیوندهای عمومی را از منابع دارای محدودیت تفکیک کنید.
- انتشار عمومی محتوا به‌معنای آزاد بودن کپی یا بازنشر نیست؛ هنگام اقتباس، مجوز **همان فایل/مخزن** را بررسی کنید. مخزن MIT 6.S950 شرایط CC BY-SA 4.0 را برای مواد منتشرشده توضیح می‌دهد، اما آثار اشخاص ثالث ممکن است جداگانه محدودیت داشته باشند.
- این فهرست «دایرکتوری لینک» است، نه آرشیو باینری فایل‌ها و نه ادعای تأیید یا وابستگی رسمی ASE-Lab به دانشگاه‌ها.
