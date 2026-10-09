from os import PathLike
from typing import BinaryIO

def svg2png(
    bytestring: bytes | None = None, *, file_obj: BinaryIO | None = None,
    url: str | None = None, dpi: float = 96, parent_width: float | None = None,
    parent_height: float | None = None, scale: float = 1, unsafe: bool = False,
    background_color: str | None = None, negate_colors: bool = False,
    invert_images: bool = False, write_to: str | PathLike[str] | BinaryIO | None = None,
    output_width: float | None = None, output_height: float | None = None,
) -> bytes | None: ...
