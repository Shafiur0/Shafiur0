"""Typography engine: instantiates OFL variable fonts and converts text to SVG paths."""
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "fonts")


class Face:
    def __init__(self, filename, weight=400):
        path = os.path.join(FONT_DIR, filename)
        font = TTFont(path)
        try:
            font = instantiateVariableFont(font, {"wght": weight}, inplace=False)
        except Exception:
            pass
        self.font = font
        self.cmap = font.getBestCmap()
        self.glyphset = font.getGlyphSet()
        self.upem = font["head"].unitsPerEm
        self.hmtx = font["hmtx"]

    def _adv(self, gname):
        return self.hmtx[gname][0]

    def width(self, text, size, tracking=0.0):
        """Advance width in user units, including per-character tracking."""
        if not text:
            return 0.0
        s = size / self.upem
        total = 0.0
        for ch in text:
            g = self.cmap.get(ord(ch))
            if g is None:
                total += self._adv(self.cmap.get(ord("n"))) * s
            else:
                total += self._adv(g) * s
        total += tracking * (len(text) - 1)
        return total

    def path(self, text, x, y, size, tracking=0.0):
        """Return concatenated path data for `text`, baseline at y, left edge at x."""
        s = size / self.upem
        cx = x
        parts = []
        for ch in text:
            g = self.cmap.get(ord(ch))
            if g is None:
                cx += self._adv(self.cmap.get(ord("n"))) * s + tracking
                continue
            pen = SVGPathPen(self.glyphset, ntos=lambda v: f"{v:.2f}")
            tpen = TransformPen(pen, Transform(s, 0, 0, -s, cx, y))
            self.glyphset[g].draw(tpen)
            d = pen.getCommands()
            if d:
                parts.append(d)
            cx += self._adv(g) * s + tracking
        return " ".join(parts)

    def path_center(self, text, cx, y, size, tracking=0.0):
        w = self.width(text, size, tracking)
        return self.path(text, cx - w / 2.0, y, size, tracking)

    def path_right(self, text, rx, y, size, tracking=0.0):
        w = self.width(text, size, tracking)
        return self.path(text, rx - w, y, size, tracking)


def fmt(v):
    """Compact number formatting for path coordinates."""
    if isinstance(v, float):
        r = round(v, 2)
        if r == int(r):
            return str(int(r))
        return f"{r:g}"
    return str(v)
