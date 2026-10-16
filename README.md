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

## Development

The Python tools use Python 3.12 and the dependency lock in `uv.lock`.
`make typecheck` runs the repository's type checks through uv.
Profile Markdown and existing assets do not require a model runtime.

## License

See [LICENSE](LICENSE) for the repository's code and asset terms. Model packages
retain their own code, checkpoint, and dependency licenses.

## Implementation mapping

[implementation-map.json](implementation-map.json) records upstream-to-native changes, source references and qualification scope.
