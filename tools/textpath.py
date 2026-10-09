"""Convert text to SVG path data with HarfBuzz shaping, so wordmarks need no installed fonts."""
from collections.abc import Mapping
from os import PathLike
from typing import cast

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

_cache: dict[str | PathLike[str], tuple[hb.Face, int]] = {}


def _font(path: str | PathLike[str]) -> tuple[hb.Face, int]:
    if path not in _cache:
        blob = hb.Blob.from_file_path(str(path))
        face = hb.Face(blob)
        _cache[path] = (face, face.upem)
    return _cache[path]


def text_path(
    font_path: str | PathLike[str], text: str, size: float, wght: float = 400,
    tracking: float = 0.0, x: float = 0.0, y: float = 0.0,
    features: dict[str, bool | int] | None = None,
    extra_axes: Mapping[str, float] | None = None,
) -> tuple[str, float]:
    """Return (d, advance_width) for `text` with its baseline-left at (x, y).

    tracking is in em units (0.01 = 1% of the font size between letters).
    """
    face, upem = _font(font_path)
    font = hb.Font(face)
    axes: dict[str, float] = {"wght": wght}
    if extra_axes:
        axes.update(extra_axes)
    font.set_variations(axes)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features or {"kern": True, "liga": True})
    scale = size / upem
    pen = SVGPathPen(None, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    cx = 0.0
    for info, pos in zip(buf.glyph_infos, cast(list[hb.GlyphPosition], buf.glyph_positions)):
        gx = x + (cx + pos.x_offset) * scale
        gy = y - pos.y_offset * scale
        tpen = TransformPen(pen, (scale, 0, 0, -scale, gx, gy))
        font.draw_glyph_with_pen(info.codepoint, tpen)
        cx += pos.x_advance + tracking * upem
    width = (cx - tracking * upem) * scale
    return pen.getCommands(), width


def cap_height(font_path: str | PathLike[str], size: float, wght: float = 400) -> float:
    face, upem = _font(font_path)
    font = hb.Font(face)
    font.set_variations({"wght": wght})
    # IBM Plex contains H and its outline; the brand assets depend on that glyph.
    ext = cast(hb.GlyphExtents, font.get_glyph_extents(cast(int, font.get_nominal_glyph(ord("H")))))
    return ext.y_bearing * size / upem
