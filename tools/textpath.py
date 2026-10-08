"""Convert text to SVG path data with HarfBuzz shaping, so wordmarks need no installed fonts."""
import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

_cache = {}


def _font(path):
    if path not in _cache:
        blob = hb.Blob.from_file_path(str(path))
        face = hb.Face(blob)
        _cache[path] = (face, face.upem)
    return _cache[path]


def text_path(font_path, text, size, wght=400, tracking=0.0, x=0.0, y=0.0, features=None, extra_axes=None):
    """Return (d, advance_width) for `text` with its baseline-left at (x, y).

    tracking is in em units (0.01 = 1% of the font size between letters).
    """
    face, upem = _font(font_path)
    font = hb.Font(face)
    axes = {"wght": wght}
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
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gx = x + (cx + pos.x_offset) * scale
        gy = y - pos.y_offset * scale
        tpen = TransformPen(pen, (scale, 0, 0, -scale, gx, gy))
        font.draw_glyph_with_pen(info.codepoint, tpen)
        cx += pos.x_advance + tracking * upem
    width = (cx - tracking * upem) * scale
    return pen.getCommands(), width


def cap_height(font_path, size, wght=400):
    face, upem = _font(font_path)
    font = hb.Font(face)
    font.set_variations({"wght": wght})
    ext = font.get_glyph_extents(font.get_nominal_glyph(ord("H")))
    return ext.y_bearing * size / upem
