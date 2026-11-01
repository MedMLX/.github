"""Regression checks for generated brand SVGs."""

import unittest
import xml.etree.ElementTree as ET

import cairosvg
from make_brand import svg_doc


class SvgTitleTest(unittest.TestCase):
    def test_title_preserves_xml_metacharacters_and_renders(self) -> None:
        title = "A & B <Research>"
        svg = svg_doc(4, 4, '<rect width="4" height="4"/>', title)
        root = ET.fromstring(svg)
        self.assertEqual(root.findtext("{http://www.w3.org/2000/svg}title"), title)
        png = cairosvg.svg2png(bytestring=svg.encode())
        self.assertIsNotNone(png)
        assert png is not None
        self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))


if __name__ == "__main__":
    unittest.main()
