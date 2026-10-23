<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../brand/banner-dark.svg">
    <img alt="MedMLX: native medical imaging models on Apple Silicon" src="../brand/banner-light.svg" width="100%">
  </picture>
</p>

# MedMLX

Native medical imaging models on Apple Silicon, built with
[MLX](https://github.com/ml-explore/mlx).

- Local model execution on the Mac's Metal GPU
- Segmentation, detection, generation, and CT reasoning
- Numerical checks against the original model implementations

## Start with medmlx

[`medmlx`](https://github.com/MedMLX/medmlx) provides one Python API, command
and MCP server. From its source checkout on macOS arm64 with Python 3.13:

```sh
git clone https://github.com/MedMLX/medmlx.git
cd medmlx
uv sync --locked --no-dev
uv run --locked --no-sync medmlx models
uv run --locked --no-sync medmlx packages
```

Choose optional extras for the runtimes you need: `segment`, `generate`,
`vision`, or `all` for all three families. Add `mcp` for the MCP server, started
with `medmlx serve --root /path/to/work`. Runtime repositories and checkpoints
have their own availability and access requirements.

Use `medmlx describe <model>` to inspect a runner's arguments,
`medmlx readiness <model>` to check readiness, and
`medmlx run <model> --arguments arguments.json --root /path/to/work` to run it.

## Package repository

| Repository | Purpose |
| --- | --- |
| [medmlx](https://github.com/MedMLX/medmlx) | API, CLI and MCP in `src/medmlx`; shared runtime in `packages/core`; conversion in `conversion`; extraction tools in `tools/extraction` |

## Public model runtimes

Model implementations stay in separate repositories and register runners
through `medmlx.models` entry points. The currently public runtime is:

| Repository | Purpose |
| --- | --- |
| [MLX-Reason-CT](https://github.com/MedMLX/MLX-Reason-CT) | NVIDIA NV-Reason-CT port for 3D CT reports and question answering; runner `mlx-reason-ct` |

Each runtime's README provides requirements, a quick start, supported inputs,
and its validation scope. Model-specific checkpoint instructions and weight
terms are documented with the model.

## Intended use

Research and education. Agreement with an upstream implementation establishes
engineering parity, not clinical validity. Model outputs require human review.
MedMLX is not a medical device and is not affiliated with Apple.

## Licenses

Each repository states its applicable code and dependency licenses and retains
upstream notices. Model weights and datasets have separate terms; follow the
selected model's documentation before use or redistribution.
