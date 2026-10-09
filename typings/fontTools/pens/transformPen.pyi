from fontTools.pens import DrawingPen, Transform

class TransformPen(DrawingPen):
    def __init__(self, outPen: DrawingPen, transformation: Transform) -> None: ...
