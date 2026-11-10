<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../brand/banner-dark.svg">
    <img alt="MedMLX: native medical imaging models on Apple Silicon" src="../brand/banner-light.svg" width="100%">
  </picture>
</p>

Native medical imaging on Apple Silicon, built with [MLX](https://github.com/ml-explore/mlx).
Segmentation, detection, synthesis and CT reasoning, running locally on your Mac.

[Website](https://medmlx.org) · [Hugging Face](https://huggingface.co/MedMLX) · [Python API, CLI & MCP](https://github.com/MedMLX/medmlx)

## Get started

Requires Apple Silicon, Metal, Python 3.13 and [uv](https://docs.astral.sh/uv/).
Install MedMLX, then segment a CT scan in a working folder:

```sh
uv tool install --python 3.13 "medmlx[all,mcp]"
mkdir -p ~/medmlx-work && cp /path/to/ct.nii.gz ~/medmlx-work/
echo '{"image_path": "ct.nii.gz", "output_dir": "segment-ct"}' > ~/medmlx-work/arguments.json
medmlx run mlx-segment-ct --arguments arguments.json --root ~/medmlx-work
```

The mask is written to `~/medmlx-work/segment-ct/`. Weights download on first use.
`medmlx models` lists every model and `medmlx describe <model>` shows its inputs;
the [setup guide](https://github.com/MedMLX/medmlx/blob/main/docs/setup.md) covers
offline weights.

<img alt="MedMLX outputs across CT, PET/CT, radiographs, endoscopy and MRI" src="https://raw.githubusercontent.com/MedMLX/medmlx/main/docs/gallery.jpg" width="100%">

## Models

### Segmentation

| Repository | Task | Input |
| :--- | :--- | :--- |
| [totalsegmentator-mlx](https://github.com/MedMLX/totalsegmentator-mlx) | Whole-body anatomy (TotalSegmentator v2) | CT |
| [mlx-segment-ct](https://github.com/MedMLX/mlx-segment-ct) | Automatic and point-prompted anatomy (VISTA-3D) | CT, MRI |
| [nnunet-mlx](https://github.com/MedMLX/nnunet-mlx) | Organs, lesions and brain tumors (nnU-Net v2) | CT, PET/CT, brain MRI |
| [synthseg-mlx](https://github.com/MedMLX/synthseg-mlx) | Brain segmentation and parcellation | Brain MRI, CT |
| [swin-unetr-mlx](https://github.com/MedMLX/swin-unetr-mlx) | 13 abdominal organs | Contrast CT |
| [segresnet-mlx](https://github.com/MedMLX/segresnet-mlx) | Brain tumors and renal structures | Brain MRI, CT |
| [unest-mlx](https://github.com/MedMLX/unest-mlx) | Kidney cortex, medulla and collecting system | CT |
| [flexray-mlx](https://github.com/MedMLX/flexray-mlx) | Radiograph anatomy | X-ray |
| [flexible-unet-mlx](https://github.com/MedMLX/flexible-unet-mlx) | Surgical tools | Endoscopy |

### Prompted segmentation

| Repository | Task | Input |
| :--- | :--- | :--- |
| [medsam2-mlx](https://github.com/MedMLX/medsam2-mlx) | Box, point or mask prompts with propagation (MedSAM2) | 3D volumes, video frames |
| [biomedparse-mlx](https://github.com/MedMLX/biomedparse-mlx) | Text prompts (BiomedParse v2) | 3D volumes, 2D images |
| [sam3-mlx](https://github.com/MedMLX/sam3-mlx) | Text, box or point prompts (SAM 3) | 2D images, video frames |

### Detection, reasoning and language

| Repository | Task | Input |
| :--- | :--- | :--- |
| [lung-nodule-mlx](https://github.com/MedMLX/lung-nodule-mlx) | Lung nodule detection (MONAI RetinaNet) | Chest CT |
| [mlx-reason-ct](https://github.com/MedMLX/mlx-reason-ct) | CT reports and question answering (NV-Reason-CT) | CT |
| [med-vlm-mlx](https://github.com/MedMLX/med-vlm-mlx) | Image-to-text (MedGemma) | 2D images |

### Synthesis

| Repository | Task | Input |
| :--- | :--- | :--- |
| [mlx-generate-ctmr](https://github.com/MedMLX/mlx-generate-ctmr) | Synthetic 3D CT and MRI (NV-Generate) | Label maps |
| [lesiondiffusion-mlx](https://github.com/MedMLX/lesiondiffusion-mlx) | Synthetic lesions | CT and organ mask |
| [fdg-pet-ct-mlx](https://github.com/MedMLX/fdg-pet-ct-mlx) | Synthetic FDG PET | CT and organ labels |

### Features

| Repository | Task | Input |
| :--- | :--- | :--- |
| [radimagenet-mlx](https://github.com/MedMLX/radimagenet-mlx) | Radiology image embeddings (RadImageNet) | 2D images |
| [mlx-radiomics](https://github.com/MedMLX/mlx-radiomics) | Radiomics features and voxel maps | Image and label mask |

Code, model weights and datasets retain their own licenses; see each repository’s notices.

## Community

- [Request a model](https://github.com/MedMLX/.github/issues/new?template=model-request.yml) to run on your Mac.
- [Ask a question](https://github.com/MedMLX/.github/discussions/categories/q-a) about installation, model selection or usage.
- [Report a bug](https://github.com/MedMLX/.github/blob/main/SUPPORT.md#report-a-bug) in the affected package.
- [Share your work](https://github.com/MedMLX/.github/discussions/categories/show-and-tell) with MedMLX.
