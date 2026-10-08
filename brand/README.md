# MedMLX brand assets

## Mark

The mark is a 3×3 grid of voxels. The plus-shaped cells are a segmentation mask and the center cell is the voxel in focus. Keep at least one voxel width of clear space around it, and draw it only in black, white and gray.

| File | Use |
|---|---|
| `avatar.png` | 1024 px square avatar for GitHub, Hugging Face, and PyPI |
| `mark.svg`, `mark.png` | Mark on a rounded tile |
| `mark-on-dark.svg`, `mark-on-light.svg` | Mark without a tile |
| `lockup-on-dark.svg`, `lockup-on-light.svg` | Mark and wordmark, with PNGs at 240 px tall |
| `banner-dark.svg`, `banner-light.svg` | Organization profile header, with PNGs at 1600 × 480 |
| `social/` | Repository social preview images, 1280 × 640 |

## Color

| Name | Hex | Use |
|---|---|---|
| Black | `#0A0A0A` | Dark background, text and mask on light |
| White | `#FFFFFF` | Light background, text and mask on dark |
| Gray | `#8E8E93` | Center voxel |
| Graphite | `#262626` | Background voxels on dark |
| Silver | `#E5E5E5` | Background voxels on light, rules on light |
| Muted on dark | `#A1A1A6` | Secondary text on Black |
| Muted on light | `#6E6E73` | Secondary text on White |

There is no accent color.

## Type

IBM Plex Sans SemiBold for the wordmark and titles, IBM Plex Sans Regular for body text, and IBM Plex Mono for code and labels. All three are under the SIL Open Font License. The SVGs contain text as outlines and render without the fonts installed.

## Banner image

The CT slice in the banner and social cards is synthetic. `tools/phantom.py` draws it from hand-placed ellipses and uses no patient data. The white region (black on light) is a liver mask. Its center voxel and four neighbors repeat the mark. The light version prints the slice as a negative.

## Regenerating

```bash
pip install uharfbuzz fonttools cairosvg
python tools/make_brand.py                                  # everything except repository cards
python tools/make_brand.py social REPO "Description"        # one repository card
python tools/make_brand.py social --org MedMLX              # cards for all public repositories
```

GitHub has no API for organization avatars or social preview images. Upload the avatar under the organization's Settings → Profile, and each card under the repository's Settings → General → Social preview.
