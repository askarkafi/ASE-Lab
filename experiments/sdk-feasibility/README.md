# First-slice runtime support

The [Dockerfile](Dockerfile) builds the pinned Python/OpenHands environment used by the supervised [ASE-Lab runner](../../ase_lab/README.md). [model_proxy.py](model_proxy.py) is the short-lived DeepSeek-only relay used by that runner to keep the real API key outside the agent container. It supports non-streaming chat completions only and has no client authentication; the runner places it on a temporary network and removes it after the run.

These files are runtime support for the first public code slice, not a general provider integration. The relay's token counter is not a monetary spending limit. Do not expose its port publicly or run it as a persistent credential service.

Run the included [offline relay tests](test_model_proxy.py) with `python experiments/sdk-feasibility/test_model_proxy.py` from the repository root.
