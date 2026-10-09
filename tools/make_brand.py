"""Build the MedMLX brand assets in brand/.

    python tools/make_brand.py
        mark, lockups, avatar, profile banners, org social card

    python tools/make_brand.py social REPO "Description"
        social preview card for one repository

    python tools/make_brand.py social --org MedMLX [--private] [--out DIR]
        social preview cards for every repository listed by `gh repo list`

Requires uharfbuzz, fonttools and cairosvg. IBM Plex (SIL Open Font License) is
downloaded into tools/.fonts/ on first run. All text is converted to outlines,
so the SVGs render the same without the fonts installed.
"""
import argparse
import json
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Literal, TypedDict, cast

import cairosvg

sys.path.insert(0, str(Path(__file__).parent))
import phantom
from textpath import cap_height, text_path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "brand"
FONT_DIR = Path(__file__).parent / ".fonts"
FONT_URLS = {
    "sans": "https://github.com/google/fonts/raw/main/ofl/ibmplexsans/IBMPlexSans%5Bwdth,wght%5D.ttf",
    "mono": "https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-Regular.ttf",
}

# Palette: black, white and neutral grays only.
BLACK = "#0A0A0A"
GRAPHITE = "#262626"
GRAY = "#8E8E93"
SILVER = "#E5E5E5"
WHITE = "#FFFFFF"
MUTED_ON_DARK = "#A1A1A6"
MUTED_ON_LIGHT = "#6E6E73"
CT_LOW = "#141414"  # darkest CT gray on dark
CT_HIGH = "#ADADAD"  # brightest CT gray, kept below white so the mask stands out
PRINT_LOW = "#EDEDED"  # on light, the scan is printed as a negative: PRINT_LOW..PRINT_HIGH
PRINT_HIGH = "#8A8A8A"

type ThemeName = Literal["dark", "light"]
type FontKind = Literal["sans", "mono"]


class Theme(TypedDict):
    bg: str
    fg: str
    muted: str
    accent: str
    on: str
    center: str
    off: str
    air: tuple[str, float]
    scan: tuple[str, str]


class Repository(TypedDict):
    name: str
    description: str | None


class ListedRepository(Repository):
    visibility: str


class Arguments(argparse.Namespace):
    cmd: str | None
    repo: str | None
    description: str
    org: str | None
    private: bool
    out: Path
    footer: str | None


THEMES: dict[ThemeName, Theme] = {
    "dark": Theme(bg=BLACK, fg=WHITE, muted=MUTED_ON_DARK, accent=WHITE,
                 on=WHITE, center=GRAY, off=GRAPHITE, air=(WHITE, 0.05), scan=(CT_LOW, CT_HIGH)),
    "light": Theme(bg=WHITE, fg=BLACK, muted=MUTED_ON_LIGHT, accent=BLACK,
                  on=BLACK, center=GRAY, off=SILVER, air=(BLACK, 0.04), scan=(PRINT_LOW, PRINT_HIGH)),
}

# Mark geometry, in a 100-unit tile: a 3x3 voxel grid whose plus-shaped cells are
# the mask and whose center cell is the voxel in focus.
PAD, GAP, RR = 20.0, 3.5, 2.4
CELL = (100 - 2 * PAD - 2 * GAP) / 3
GRID = 100 - 2 * PAD  # 60


def font(kind: FontKind) -> str:
    path = FONT_DIR / FONT_URLS[kind].rsplit("/", 1)[1].replace("%5B", "[").replace("%5D", "]")
    if not path.exists():
        FONT_DIR.mkdir(exist_ok=True)
        urllib.request.urlretrieve(FONT_URLS[kind], path)
    return str(path)


def num(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


def svg_doc(w: float, h: float, body: str, title: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{num(w)}" height="{num(h)}" viewBox="0 0 {num(w)} {num(h)}" role="img">'
            f"<title>{title}</title>{body}</svg>\n")


def write(name: str, svg: str, png_scale: float | None = None) -> None:
    OUT.mkdir(exist_ok=True)
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if name.endswith(".svg"):
        path.write_text(svg)
    if png_scale:
        png = path.with_suffix(".png")
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(png), scale=png_scale)
    print("wrote", path.relative_to(ROOT) if name.endswith(".svg") else path.with_suffix(".png").relative_to(ROOT))


# Mark and wordmark

def glyph(theme: ThemeName, x: float, y: float, size: float) -> str:
    """The 3x3 voxel grid, drawn into a size x size box at (x, y)."""
    t = THEMES[theme]
    s = size / GRID
    out: list[str] = []
    for i in range(3):
        for j in range(3):
            if i == j == 1:
                fill = t["center"]
            elif i == 1 or j == 1:
                fill = t["on"]
            else:
                fill = t["off"]
            out.append(f'<rect x="{num(x + j * (CELL + GAP) * s)}" y="{num(y + i * (CELL + GAP) * s)}" '
                       f'width="{num(CELL * s)}" height="{num(CELL * s)}" rx="{num(RR * s)}" fill="{fill}"/>')
    return "".join(out)


def wordmark(theme: ThemeName, x: float, baseline: float, cap: float) -> tuple[str, float]:
    sans = font("sans")
    size = cap / cap_height(sans, 1, 600)
    d, w = text_path(sans, "MedMLX", size, wght=600, tracking=-0.01, x=x, y=baseline)
    return f'<path d="{d}" fill="{THEMES[theme]["fg"]}"/>', w


def lockup(theme: ThemeName, x: float, y: float, hm: float) -> tuple[str, float]:
    """Mark plus wordmark. (x, y) is the top left of the mark; returns (svg, width)."""
    cap = hm / 1.45
    gap = 0.34 * hm
    word, w = wordmark(theme, x + hm + gap, y + hm / 2 + cap / 2, cap)
    return glyph(theme, x, y, hm) + word, hm + gap + w


def text(
    s: str, x: float, y: float, size: float, fill: str, kind: FontKind = "sans",
    wght: float = 400, tracking: float = 0.0,
) -> tuple[str, float]:
    d, w = text_path(font(kind), s, size, wght=wght, tracking=tracking, x=x, y=y)
    return f'<path d="{d}" fill="{fill}"/>', w


def wrap(s: str, size: float, max_w: float, wght: float = 400) -> list[str]:
    lines: list[str] = []
    cur = ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and text_path(font("sans"), trial, size, wght=wght)[1] > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


# Voxel CT slice

def _mix(a: str, b: str, t: float) -> str:
    channels_a = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    channels_b = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(p + (q - p) * t):02X}" for p, q in zip(channels_a, channels_b))


def _smooth(e0: float, e1: float, x: float) -> float:
    t = min(1.0, max(0.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def voxel_field(
    theme: ThemeName, w: float, h: float, pitch: float, body_cx: float, body_cy: float,
    body_w: float, air_fade: tuple[float, float, float] | None = None,
) -> str:
    """A grid of voxels covering w x h, with the phantom slice centered at (body_cx, body_cy).

    air_fade, if given, is (x0, x1, floor): empty voxels fade from `floor` opacity
    left of x0 to full opacity right of x1, keeping text areas quiet.
    """
    t = THEMES[theme]
    gap = max(2.0, pitch * 0.16)
    size = pitch - gap
    cols, rows = int(w // pitch) + 1, int(h // pitch) + 1
    x0 = (w - cols * pitch) / 2 + gap / 2
    y0 = (h - rows * pitch) / 2 + gap / 2
    voxel = 1.88 / (body_w / pitch)
    vals, mask = phantom.sample(cols, rows, (body_cx - x0) / pitch, (body_cy - y0) / pitch, voxel)

    mr = [(r, c) for r in range(rows) for c in range(cols) if mask[r][c]]
    focus = (round(sum(r for r, _ in mr) / len(mr)), round(sum(c for _, c in mr) / len(mr))) if mr else None
    arms: set[tuple[int, int]] = {(focus[0] + dr, focus[1] + dc) for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1))} if focus else set()

    groups: dict[tuple[int, str, float], list[tuple[int, int]]] = {}

    def put(fill: str, op: float, r: int, c: int, layer: int = 0) -> None:
        groups.setdefault((layer, fill, op), []).append((c, r))

    air_fill, air_op = t["air"]
    for r in range(rows):
        for c in range(cols):
            v = vals[r][c]
            if v is None:
                op = air_op
                if air_fade:
                    fx0, fx1, floor = air_fade
                    op *= floor + (1 - floor) * _smooth(fx0, fx1, x0 + c * pitch)
                put(air_fill, round(op, 3), r, c)
                continue
            put(_mix(*t["scan"], round(v * 24) / 24), 1, r, c)
            if not mask[r][c]:
                continue
            if (r, c) == focus:
                put(t["center"], 1, r, c, layer=2)
            elif (r, c) in arms:
                put(t["on"], 1, r, c, layer=1)
            else:
                edge = any(not (0 <= r + dr < rows and 0 <= c + dc < cols and mask[r + dr][c + dc])
                           for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)))
                put(t["on"], 0.9 if edge else 0.5, r, c, layer=1)

    out = [f'<defs><rect id="v" width="{num(size)}" height="{num(size)}" rx="{num(size * 0.14)}"/></defs>']
    # scan voxels first, then the mask overlay, then the focus voxel on top
    for key in sorted(groups, key=lambda k: k[0]):
        _, fill, op = key
        uses = "".join(f'<use xlink:href="#v" x="{num(x0 + c * pitch)}" y="{num(y0 + r * pitch)}"/>'
                       for c, r in groups[key])
        opacity = "" if op == 1 else f' fill-opacity="{op}"'
        out.append(f'<g fill="{fill}"{opacity}>{uses}</g>')
    return "".join(out)


# Assets

def build_marks() -> None:
    tile = (f'<rect width="100" height="100" rx="22" fill="{BLACK}"/>' + glyph("dark", PAD, PAD, GRID))
    write("mark.svg", svg_doc(100, 100, tile, "MedMLX"), png_scale=5.12)
    for theme in THEMES:
        write(f"mark-on-{theme}.svg", svg_doc(GRID, GRID, glyph(theme, 0, 0, GRID), "MedMLX"))
    avatar = f'<rect width="100" height="100" fill="{BLACK}"/>' + glyph("dark", PAD, PAD, GRID)
    write("avatar.png", svg_doc(100, 100, avatar, "MedMLX"), png_scale=10.24)
    for theme in THEMES:
        body, w = lockup(theme, 0, 0, 120)
        write(f"lockup-on-{theme}.svg", svg_doc(w, 120, body, "MedMLX"), png_scale=2)


def build_banners() -> None:
    W, H, R = 1600, 480, 28
    for theme, t in THEMES.items():
        body = [f'<clipPath id="r"><rect width="{W}" height="{H}" rx="{R}"/></clipPath>',
                f'<rect width="{W}" height="{H}" rx="{R}" fill="{t["bg"]}"/>',
                f'<g clip-path="url(#r)">{voxel_field(theme, W, H, 18, 1250, 240, 620, air_fade=(640, 980, 0.25))}</g>']
        mark, _ = lockup(theme, 96, 132, 104)
        body.append(mark)
        body.append(text("Native medical imaging models on Apple Silicon", 98, 318, 32, t["muted"])[0])
        body.append(text("segmentation · detection · generation", 98, 372, 19,
                         t["accent"], kind="mono")[0])
        write(f"banner-{theme}.svg", svg_doc(W, H, "".join(body), "MedMLX: native medical imaging models on Apple Silicon"),
              png_scale=1)


def social_card(
    name: str, description: str | None, path: Path, theme: ThemeName = "dark",
    footer: str | None = None,
) -> None:
    W, H = 1280, 640
    t = THEMES[theme]
    body = [f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>',
            voxel_field(theme, W, H, 20, 1135, 330, 660, air_fade=(560, 860, 0.2))]
    if name == "MedMLX":
        mark, _ = lockup(theme, 72, 196, 120)
        body.append(mark)
        body.append(text("Native medical imaging models", 76, 410, 36, t["muted"])[0])
        body.append(text("on Apple Silicon", 76, 456, 36, t["muted"])[0])
        footer = footer or "github.com/MedMLX"
    else:
        mark, _ = lockup(theme, 72, 64, 44)
        body.append(mark)
        size = 80
        while size > 40 and text_path(font("sans"), name, size, wght=600, tracking=-0.01)[1] > 660:
            size -= 2
        body.append(text(name, 70, 300, size, t["fg"], wght=600, tracking=-0.01)[0])
        for k, line in enumerate(wrap(description or "", 30, 640)[:3]):
            body.append(text(line, 72, 300 + 66 + k * 42, 30, t["muted"])[0])
        footer = footer or f"github.com/MedMLX/{name}"
    body.append(text(footer, 72, 572, 22, t["accent"], kind="mono")[0])
    svg = svg_doc(W, H, "".join(body), name)
    path.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(path))
    print("wrote", path)


def build_all() -> None:
    build_marks()
    build_banners()
    social_card("MedMLX", None, OUT / "social" / "MedMLX.png")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("social", help="build repository social preview cards")
    s.add_argument("repo", nargs="?")
    s.add_argument("description", nargs="?", default="")
    s.add_argument("--org", help="build a card for every repository in this GitHub organization")
    s.add_argument("--private", action="store_true", help="include private repositories with --org")
    s.add_argument("--out", type=Path, default=OUT / "social")
    s.add_argument("--footer", help="replace the github.com link at the bottom of the card")
    a = p.parse_args(namespace=Arguments())
    if a.cmd != "social":
        build_all()
        return
    if a.org:
        res = subprocess.run(["gh", "repo", "list", a.org, "--limit", "500", "--json", "name,description,visibility"],
                             capture_output=True, text=True, check=True)
        # gh returns these fields because they are requested explicitly above.
        repos: list[Repository] = [r for r in cast(list[ListedRepository], json.loads(res.stdout))
                 if (a.private or r["visibility"] == "PUBLIC") and not r["name"].startswith(".")]
    elif a.repo:
        repos = [{"name": a.repo, "description": a.description}]
    else:
        p.error("social needs REPO or --org")
    for r in repos:
        social_card(r["name"], r["description"], a.out / f"{r['name']}.png", footer=a.footer)


if __name__ == "__main__":
    main()
