# Dependencies, upstream projects, and forks

**Status:** Initial policy for the first supervised source release; review dependencies before each distribution.

## Separate ownership

ASE-Lab distinguishes between (1) original project material, (2) third-party dependencies, and (3) modified copies or forks of upstream projects.

## General policy

- Prefer supported extension APIs over modifying upstream source when that meets the need.
- A fork may be appropriate for learning, experimentation, or functionality unavailable through public extension points.
- Track the upstream repository, base revision, modifications, and relevant notices for each fork.
- Pin or otherwise record the versions required to reproduce executable work.
- Keep third-party license notices and comply with the applicable terms when redistributing code.
- Do not assume that a permissive SDK license automatically licenses ASE-Lab's original code, model access, or other dependencies.
- Keep experimentation and unreviewed upstream patches out of published releases until deliberately reviewed.

## Important distinction

**Legally permitted to modify** is not the same as **technically easy to replace**. Each future component-replacement exercise must first inspect public APIs, internal coupling, tests, and migration costs.

## Current licensing status

ASE-Lab's original published code and documentation use the [MIT License](../../LICENSE). This does not relicense OpenHands, Python, the example `more-itertools` repository, or other third-party components. They retain their own terms. General external code contributions remain paused until contribution terms are clarified.

The first source release records direct component attribution in [THIRD_PARTY.md](../../THIRD_PARTY.md). The Dockerfile pins its base image and top-level SDK packages, but transitive packages are not fully locked; later builds need their own version record before being treated as equivalent to the evaluated image.
