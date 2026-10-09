# Brand tool dependency interfaces

These partial stubs describe the APIs used by the brand scripts. They supply
missing dependency typing without changing drawing, shaping, or rasterization.
Signatures were checked against uharfbuzz 0.56.3 source, FontTools 4.66.1
`pens/svgPathPen.py` and `pens/transformPen.py`, and CairoSVG 2.9.1
`__init__.py` and `surface.py`. HarfBuzz drawing pens use the six contour
methods in `DrawingPen`; component lookup is not used by that boundary.

The bindings remain the real installed libraries at runtime. New library API
usage should be added here from the corresponding implementation, never as an
untyped catch-all.
