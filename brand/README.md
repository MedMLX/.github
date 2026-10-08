# MedMLX brand assets

## Mark

The mark is a 3×3 grid of voxels. The plus-shaped cells are a segmentation mask and the center cell is the voxel in focus. Keep at least one voxel width of clear space around it, and do not draw it in red.

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
| Ink | `#0B1016` | Dark background, text on light |
| Bone | `#ECE8E1` | Text on dark, center voxel on dark |
| Signal | `#36D1B9` | Mask and accent on dark |
| Signal deep | `#0D7F70` | Mask and accent on light (4.5:1 on Paper) |
| Slate | `#1F2933` | Background voxels on dark |
| Mist | `#DDE2E5` | Background voxels on light |
| Paper | `#F7F6F3` | Light background |
| Muted on dark | `#9AA3AD` | Secondary text on Ink |
| Muted on light | `#56606B` | Secondary text on Paper |

## Type

IBM Plex Sans SemiBold for the wordmark and titles, IBM Plex Sans Regular for body text, and IBM Plex Mono for code and labels. All three are under the SIL Open Font License. The SVGs contain text as outlines and render without the fonts installed.

## Banner image

The CT slice in the banner and social cards is synthetic. `tools/phantom.py` draws it from hand-placed ellipses and uses no patient data. The teal region is a liver mask. Its center voxel and four neighbors repeat the mark. The light version prints the slice as a negative.

## Regenerating

```bash
pip install uharfbuzz fonttools cairosvg
python tools/make_brand.py                                  # everything except repository cards
python tools/make_brand.py social REPO "Description"        # one repository card
python tools/make_brand.py social --org MedMLX              # cards for all public repositories
```

GitHub has no API for organization avatars or social preview images. Upload the avatar under the organization's Settings → Profile, and each card under the repository's Settings → General → Social preview.
