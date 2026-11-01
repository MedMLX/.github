# MedMLX brand assets

## Mark

The mark is a 3×3 grid of voxels. The plus-shaped cells are a segmentation mask and the center cell is the voxel in focus. Keep at least one voxel width of clear space around it, and draw it only in black, white and gray.

| File | Use |
|---|---|
| `avatar.svg`, `avatar.png` | Stacked crimson Med / neutral MLX wordmark on white; PNG is 1024 px square for Hugging Face and PyPI |
| `github-avatar.svg`, `github-avatar.png` | Horizontal MedMLX wordmark on black; PNG is 1024 px square for the GitHub organization |
| `mark.svg`, `mark.png` | Mark on a rounded tile |
| `mark-on-dark.svg`, `mark-on-light.svg` | Mark without a tile |
| `lockup-on-dark.svg`, `lockup-on-light.svg` | Mark and wordmark, with PNGs at 240 px tall |
| `banner-dark.svg`, `banner-light.svg` | Organization profile header with a horizontal wordmark directly on the background, with PNGs at 1600 × 480 |
| `social/` | Repository social preview images, 1280 × 640 |

## Color

| Name | Hex | Use |
|---|---|---|
| Black | `#0A0A0A` | Dark background, text and mask on light |
| White | `#FFFFFF` | Light background, text and mask on dark |
| Crimson | `#A51C30` | Med in the wordmark (Harvard crimson) |
| Gray | `#D5D5D5` | X in the wordmark and center voxel |
| Graphite | `#262626` | Background voxels on dark |
| Silver | `#E5E5E5` | Background voxels on light, rules on light |
| Muted on dark | `#A1A1A6` | Secondary text on Black |
| Muted on light | `#6E6E73` | Secondary text on White |

The wordmark uses crimson for “Med”, black on light or white on dark for “ML”, and
the light gray sampled from the Apple MLX reference for “X”. Keep the mark and
supporting text neutral.

## Avatar

The GitHub organization avatar uses the horizontal wordmark on black, with room
for a circular crop. The stacked wordmark on white remains available for other
services. In both versions “Med” is crimson and “X” is light gray. Keep the voxel
mark for lockups and other icon uses.

## Type

IBM Plex Sans SemiBold for the wordmark and titles, IBM Plex Sans Regular for body text, and IBM Plex Mono for code and labels. All three are under the SIL Open Font License. The SVGs contain text as outlines and render without the fonts installed.

## Banner image

The CT slice in the banner and social cards is synthetic. `tools/phantom.py` draws it from hand-placed ellipses and uses no patient data. The white region (black on light) is a liver mask. Its center voxel and four neighbors repeat the mark. The light version prints the slice as a negative.

## Regenerating

```bash
uv sync --locked
.venv/bin/python tools/make_brand.py                                  # marks, banners and organization card
.venv/bin/python tools/make_brand.py social REPO "Description"        # one repository card
.venv/bin/python tools/make_brand.py social --org MedMLX              # cards for all public repositories
```

The PNG renderer requires the native Cairo library. On macOS, run
`brew install cairo` and `export DYLD_FALLBACK_LIBRARY_PATH="$(brew --prefix cairo)/lib"`
before the generation commands. The first run downloads IBM Plex fonts to
`tools/.fonts/`; subsequent runs use that cache. Generated files are overwritten.
Repository cards default to `brand/social/`; pass `--out DIR` to choose another
directory. The `--org` form requires the GitHub CLI and lists up to 500
repositories; it skips names starting with a dot and excludes private repositories
unless `--private` is supplied.

GitHub has no API for organization avatars or social preview images. Upload the avatar under the organization's Settings → Profile, and each card under the repository's Settings → General → Social preview.
