# MedMLX organization profile

The GitHub organization profile and shared brand assets for
[MedMLX](https://github.com/MedMLX), native medical imaging models on Apple Silicon.

- Organization overview and public package links
- Light and dark banners, marks, lockups, and social images
- Reproducible Python tools for the brand assets

[Profile](#profile) · [Brand](#brand) · [Development](#development) · [License](#license)

## Profile

Edit [profile/README.md](profile/README.md) to update the organization landing
page. Keep its package list limited to public repositories. GitHub renders that
file as the organization profile.

## Brand

The [brand guide](brand/README.md) documents the palette and asset usage.
Existing SVG and PNG assets live in [brand/](brand/).
Generation tools live in [tools/](tools/).

The [Hugging Face organization card](huggingface/README.md) uses the generated
light and dark banners from `brand/`. Its static renderer is
[`huggingface/index.html`](huggingface/index.html).

## Development

The Python tools use Python 3.12 and the dependency lock in `uv.lock`.
Prepare or update the environment explicitly with `uv sync --locked`.
`make qa` runs Ruff and Pyright in the existing environment without syncing it.
`make typecheck` runs strict Pyright and the Ruff annotation/import checks.
MedMLX repositories share this typing
policy: explicit dynamic types are prohibited, type-ignore comments are disabled,
unnecessary ignores are errors, and Pyright uses the maintained host Node.
Each repository keeps its supported Python version and declared source scope.
Profile Markdown and existing assets do not require a model runtime.

The common targets are `env`, `lint`, `typecheck`, `test`, `qa`, `loc`, and `clean`.
There is no automated test suite here, so `make test` fails with that explanation;
exercise a changed tool against a small local input.

[SECURITY.md](SECURITY.md) provides the default private vulnerability-reporting
route for repositories without their own security policy.

## License

See [LICENSE](LICENSE) for the repository's code and asset terms. Model packages
retain their own code, checkpoint, and dependency licenses.

Use `LICENSE` at each Git or independently packaged project root. Keep
attribution and complete applicable upstream code-license texts together in
`THIRD_PARTY_NOTICES.md`, preserving their original terms and notices. Separate
folders for simple copied code licenses were rejected because they scatter the
terms without adding information. Varying notice filenames and loose legal
files in `src/` likewise make attribution and packaging harder to verify.

Genuine vendored source and bundled assets retain their source-local licenses.
Operational model-license manifests and publisher records retain their declared
paths and separate code, weight and data terms. Independently packaged components
keep their own root legal files; retain installed legal resource paths only when
actually consumed. This layout does not relicense upstream materials.

## Implementation mapping

[Central implementation map](https://github.com/MedMLX/Med-MLX/blob/main/implementation-maps/.github.json) records upstream-to-native changes, source references and qualification scope.
