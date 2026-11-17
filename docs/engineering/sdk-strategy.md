# SDK strategy — OpenHands-first

**Status:** OpenHands Software Agent SDK selected as the **initial implementation basis**; integration and suitability remain to be validated in actual ASE-Lab tasks.

## Decision and rationale

ASE-Lab will begin with the [OpenHands Software Agent SDK](https://github.com/OpenHands/software-agent-sdk), which provides software-engineering-oriented agent, tool, and workspace concepts. Its direct connection to software agents and the availability of its source code offer an appropriate foundation for hands-on learning and incremental product work. The [OpenHands SDK paper](https://proceedings.mlsys.org/paper_files/paper/2026/hash/8ae9cf363ea625161f885b798c1f1f78-Abstract-Conference.html) is a primary research reference; it does not prove that every SDK release will meet ASE-Lab's requirements.

An initial documentary evaluation considered OpenHands, the more general [OpenAI Agents SDK](https://github.com/openai/openai-agents-python), and [LangGraph](https://github.com/langchain-ai/langgraph) for stateful orchestration. Those options are not interchangeable in all respects. Further broad comparison is **not** a prerequisite for beginning implementation; selection may be revisited if a material blocker is demonstrated.

## Practical integration principles

1. **Use the SDK before abstracting it.** Read the relevant source code while running a small repository task, and understand the agent loop, events, tool execution, state, and workspace boundary.
2. **Keep ASE-Lab ownership clear.** Project-owned tasks, tools, tests, and policies should be identifiable; add only the integration interfaces needed by a real use case.
3. **Validate safety and behavior.** Execute agent-driven commands in a disposable or appropriately isolated workspace; test extension points and permissions before relying on them.
4. **Prefer supported extension points to a fork.** Record concrete incompatibilities before considering internal modifications or a maintained fork.
5. **Do not overclaim.** An SDK choice is not an implemented agent, a benchmark result, or a promise of future multi-runtime support.

## Minimum validation in the roadmap

The [OpenHands-first roadmap](../planning/roadmap.md) starts with one minimal, repeatable SDK run, then tested ASE-Lab-owned behavior and a bounded software-engineering capability. Add a custom extension only if the task justifies it. Inspect execution events, task results, failures, version compatibility, and the effort of integration as these steps unfold.

See [academic foundations](../research/academic-foundations.md) for the educational and research rationale, and [academic resource index](../research/academic-resources.md) for official course assignments and paper links.
