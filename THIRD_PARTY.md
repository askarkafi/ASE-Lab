# Third-party components and examples

ASE-Lab's [MIT License](LICENSE) applies to ASE-Lab's own published material. Third-party projects keep their own licenses.

| Project | Use in this slice | Source and license |
| --- | --- | --- |
| OpenHands Software Agent SDK and tools 1.62.0 | Installed by the Dockerfile; provides the agent loop and tools. No upstream source is copied into this repository. | [Upstream repository](https://github.com/OpenHands/software-agent-sdk) and [MIT license](https://github.com/OpenHands/software-agent-sdk/blob/main/LICENSE) |
| Python 3.12 slim Bookworm image | Pinned base image used to build the local experiment environment. No image layers are distributed in this source repository. | [Official Python image](https://github.com/docker-library/python) |
| more-itertools v10.8.0 | Public repository referenced by the example task and private evaluation. Its source, tests, and generated patches are not bundled. | [Upstream repository](https://github.com/more-itertools/more-itertools) and [license](https://github.com/more-itertools/more-itertools/blob/master/LICENSE) |

The Dockerfile pins its base-image digest and the two top-level OpenHands package versions. It does not lock every transitive Python dependency. Rebuilding at a later date may resolve different transitive versions; record the resulting image digest for a reproducible evaluation. Provider API access and usage costs are separate from software licensing.
