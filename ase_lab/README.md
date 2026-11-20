# Run the supervised first slice

ASE-Lab's first executable slice investigates one issue in an approved local Git repository snapshot. It uses OpenHands SDK 1.62.0 for the agent loop and a project-owned supervisor for task validation, workspace preparation, execution bounds, diff inspection, independent validation, and reviewable output. It is a supervised engineering demonstration, not a production service.

## Prerequisites

- Python 3.12 or later, Git, and Docker with Linux containers.
- An approved local repository clone and a fixed 40-character commit SHA.
- A DeepSeek API key and approval to send the issue and relevant repository content to that provider. Provider use incurs cost. The only tested model profile is `deepseek-flash-relay`.

Build the pinned feasibility image from the included [Dockerfile](../experiments/sdk-feasibility/Dockerfile):

```powershell
docker build -t ase-lab-feasibility:openhands-1.62.0 experiments/sdk-feasibility
```

Copy the [example task](../tests/task.example.json) to a local file under ignored `runs/`, replace its `repository` value with an absolute path to the approved clone, and review its issue, allowed files, validation commands, and limits. The example references a public `more-itertools` revision; ASE-Lab does not bundle that project's source.

```powershell
New-Item -ItemType Directory -Force runs/local
Copy-Item tests/task.example.json runs/local/task.json
```

Create `runs/local/deepseek.env` containing one line in the form `DEEPSEEK_API_KEY=<your key>`. Keep the file private; `runs/` is ignored by Git. The key is mounted read-only only in a short-lived model relay container, not in the agent container.

```powershell
python -m ase_lab runs/local/task.json --secret-file runs/local/deepseek.env
python -m unittest discover -s tests -v
python experiments/sdk-feasibility/test_model_proxy.py
python scripts/check_docs.py
```

The command prints an ignored attempt directory containing `result.json`, `report.md`, private logs, and, for a completed in-scope patch proposal, `proposal.patch`. Review the result and patch before using them. No patch is automatically applied to the source repository, merged, or published. A nonzero CLI exit indicates that the run did not complete within its accepted execution scope.

## Result contract and limits

Task input uses schema version 1. Result JSON uses schema version 2. `run_status` records completion, error, limit, or interruption. `outcome` is `patch_proposal`, `no_patch`, or `no_result`; the last denotes a run that did not produce a defensible task result. A completed no-change run needs a captured agent explanation before it can be a `no_patch` candidate. Human review still judges whether that explanation or any patch is justified.

The initial policy permits modifications to named existing tracked files. Agent commands run in a disposable container. The supervisor checks the resulting Git diff and rejects additions, deletions, symlinks, and out-of-scope modifications. An agent can temporarily change other files inside the disposable checkout; this is detected after execution. Independent validation runs without network access against a read-only copy. The source repository remains unchanged.

The task can lower ceilings of 900 agent seconds, 25 SDK iterations, 25 model requests including retries, 2048 MiB memory, 2 CPUs, and 128 processes. The relay has a reported-token threshold, but monetary cost enforcement is unverified and one request can cross the token threshold. Real-time termination across host suspension is also unverified; keep the host awake and supervise runs. If Docker cleanup cannot be verified, the CLI prints an operator alert and returns an error. Raw traces may contain sensitive material, are not automatically redacted, and must be reviewed before sharing. Retention cleanup is manual.

The [public evaluation summary](../docs/evaluation/first-slice.md) describes the selected cases, initial failures, follow-ups, and evidence limits. The included runner and relay tests use temporary Git repositories, simulated Docker/SDK execution, and fake provider responses; they do not make a live provider call.
