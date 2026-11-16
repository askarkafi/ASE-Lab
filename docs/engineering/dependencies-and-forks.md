# Dependencies, upstream projects, and forks

**Status:** Initial policy; subject to revision before software distribution.

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

ASE-Lab's own license has **not** been selected. This initial public documentation does not grant additional reuse rights beyond applicable law. Before accepting external code contributions or distributing executable components, project licensing and contributor terms need to be clarified.
