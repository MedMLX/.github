from collections.abc import Callable

from fontTools.pens import DrawingPen

class SVGPathPen(DrawingPen):
    def __init__(self, glyphSet: None, ntos: Callable[[float], str] = str) -> None: ...
    def getCommands(self) -> str: ...
