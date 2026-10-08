"""Synthetic axial abdominal CT slice used as the MedMLX banner image.

Every structure is an ellipse placed by hand. Nothing here comes from patient data.
Coordinates: u runs left to right on the image (patient right is image left),
v runs top (anterior) to bottom (posterior). The body spans about u in [-0.94, 0.94].
"""
import math


def _ell(u, v, cx, cy, a, b, rot=0.0):
    c, s = math.cos(rot), math.sin(rot)
    x, y = u - cx, v - cy
    xr, yr = c * x + s * y, -s * x + c * y
    return (xr / a) ** 2 + (yr / b) ** 2


def tissue(u, v):
    """Return (intensity in 0..1, in_liver_mask), or (None, False) outside the body."""
    body = _ell(u, v, 0, 0, 0.94, 0.64)
    if body > 1:
        return None, False
    val = 0.20  # subcutaneous fat
    if body > 0.91:
        val = 0.46  # skin
    liver = False
    if _ell(u, v, 0, 0.01, 0.84, 0.54) <= 1:
        val = 0.42  # abdominal wall muscle
        if _ell(u, v, 0, 0.0, 0.78, 0.49) <= 1:
            val = 0.28  # mesenteric fat
            for bx, by, ba, bb, bv in ((0.12, -0.30, 0.13, 0.08, 0.50), (0.30, 0.02, 0.10, 0.08, 0.46),
                                       (0.02, -0.10, 0.09, 0.07, 0.54), (0.17, -0.13, 0.06, 0.05, 0.08),
                                       (-0.02, 0.05, 0.07, 0.06, 0.48)):
                if _ell(u, v, bx, by, ba, bb) <= 1:
                    val = bv  # bowel loops, one with gas
            if _ell(u, v, 0.43, -0.22, 0.22, 0.14, 0.3) <= 1:
                val = 0.05 if v < -0.28 else 0.40  # stomach, gas over fluid
            if _ell(u, v, 0.63, 0.07, 0.11, 0.2, -0.5) <= 1:
                val = 0.56  # spleen
            for kx in (-0.30, 0.30):
                if _ell(u, v, kx, 0.24, 0.09, 0.12, 0.35 if kx > 0 else -0.35) <= 1:
                    val = 0.72  # kidneys
            if _ell(u, v, -0.09, 0.16, 0.05, 0.05) <= 1:
                val = 0.62  # IVC
            if _ell(u, v, 0.05, 0.18, 0.05, 0.05) <= 1:
                val = 0.88  # aorta
            if u < 0.02 and _ell(u, v, -0.42, -0.08, 0.36, 0.34, 0.25) <= 1:
                val, liver = 0.56, True
        for px in (-0.16, 0.16):
            if _ell(u, v, px, 0.43, 0.11, 0.08) <= 1:
                val = 0.44  # paraspinal muscles
        if _ell(u, v, 0, 0.31, 0.10, 0.08) <= 1:
            val = 0.97  # vertebral body
        if abs(u) < 0.03 and 0.37 < v < 0.52:
            val = 0.90  # posterior elements
        for ang in (200, 215, 232, 308, 325, 340):
            t = math.radians(ang)
            if _ell(u, v, 0.81 * math.cos(t), -0.51 * math.sin(t), 0.04, 0.04) <= 1:
                val = 0.93  # ribs
    return val, liver


def _noise(r, c, seed):
    h = (r * 73856093) ^ (c * 19349663) ^ (seed * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h / 0xFFFFFFFF - 0.5) * 2  # -1..1


def sample(cols, rows, center_col, center_row, voxel, seed=7, jitter=0.03):
    """Sample the phantom on a cols x rows grid.

    center_col/center_row place the body center on the grid; voxel is the size of
    one grid cell in phantom units. Returns (values, mask) as nested lists, with
    None for air.
    """
    vals = [[None] * cols for _ in range(rows)]
    mask = [[False] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            u = (c + 0.5 - center_col) * voxel
            v = (r + 0.5 - center_row) * voxel
            val, liver = tissue(u, v)
            if val is None:
                continue
            vals[r][c] = min(1.0, max(0.03, val + jitter * _noise(r, c, seed)))
            mask[r][c] = liver
    return vals, mask
