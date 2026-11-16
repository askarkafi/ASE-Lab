# SDK evaluation strategy

**Status:** Evaluation planned; no SDK selected.

## Why evaluate existing SDKs?

The project intends to investigate whether an existing agent SDK can provide the execution loop, model integration, state handling, and tooling needed for an initial capability. This may preserve development effort for project-specific engineering and educational work.

## Initial technologies to investigate

- [OpenHands Software Agent SDK](https://github.com/OpenHands/software-agent-sdk), with a software engineering focus.
- [OpenAI Agents SDK (Python)](https://github.com/openai/openai-agents-python), a general agent development toolkit.
- [LangGraph](https://github.com/langchain-ai/langgraph), potentially relevant when explicit workflow and state orchestration are required.

These technologies are not exact substitutes in every respect. Listing them does not imply a decision or a plan to combine all three.

## Evaluation criteria

| Dimension | Questions |
| --- | --- |
| Runtime boundary | What execution-loop and state responsibilities does the SDK own? |
| Extensibility | Can tools, context handling, skills, and policies be changed through stable APIs? |
| Software engineering fit | Can the SDK work safely with repositories, files, commands, and tests? |
| Observability | Are events, logs, traces, and results available for inspection? |
| Protocols | What MCP or multi-agent capabilities exist, and how are they exposed? |
| Ownership | How much project-specific code is required for a meaningful slice? |
| Maintenance | Are dependencies, versioning, documentation, and licenses manageable? |
| Educational value | Can concepts be learned and demonstrated beyond merely running examples? |

## Evidence before adoption

A small controlled prototype and review of public extension APIs should inform the decision. A comparison does **not** require two full product implementations. Results and accepted decisions will be published when they are ready for release.
