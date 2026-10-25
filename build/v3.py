"""Minimal 3D engine: camera, projection, depth sorting, shaded boxes.

Everything is pre-computed at build time and emitted as static SVG geometry.
Motion is layered on top with SMIL transforms, which stay valid because
translation and view-axis rotation preserve the painter's ordering.
"""
import math


def shade(hex_color, k):
    """Multiply an #rrggbb colour by k (0..1) to fake directional light."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r, g, b = (max(0, min(255, int(c * k))) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


class Cam:
    """Pinhole camera looking along +Y, tilted down by `pitch`."""

    def __init__(self, target, yaw, pitch, dist, focal, ox, oy):
        self.cx, self.cy, self.cz = target
        self.yaw = yaw
        self.pitch = pitch
        self.dist = dist
        self.focal = focal
        self.ox = ox
        self.oy = oy
        self._ca, self._sa = math.cos(yaw), math.sin(yaw)
        self._cp, self._sp = math.cos(pitch), math.sin(pitch)

    def project(self, p):
        x, y, z = p[0] - self.cx, p[1] - self.cy, p[2] - self.cz
        x1 = x * self._ca - y * self._sa
        y1 = x * self._sa + y * self._ca
        depth = y1 * self._cp - z * self._sp + self.dist
        up = y1 * self._sp + z * self._cp
        f = self.focal / max(depth, 1e-4)
        return (self.ox + x1 * f, self.oy - up * f, depth)


def fit_camera(points, rect, yaw, pitch, dist, probe_focal=100.0):
    """Return a Cam whose projection of `points` fits inside rect=(x,y,w,h)."""
    x, y, w, h = rect
    cam = Cam((0, 0, 0), yaw, pitch, dist, probe_focal, 0, 0)
    pts = [cam.project(p) for p in points]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    bw, bh = max(xs) - min(xs), max(ys) - min(ys)
    k = min(w / bw if bw else 1, h / bh if bh else 1)
    focal = probe_focal * k
    cam.focal = focal
    pts = [cam.project(p) for p in points]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    cam.ox = x + w / 2 - (max(xs) + min(xs)) / 2
    cam.oy = y + h / 2 - (max(ys) + min(ys)) / 2
    return cam


def poly(pts, fill, opacity=None, stroke=None, sw=0.7, extra=""):
    d = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
    o = f' opacity="{opacity}"' if opacity is not None else ""
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ""
    return f'<polygon points="{d}" fill="{fill}"{o}{s}{extra}/>'


def box_faces(cam, x0, y0, x1, y1, z0, z1):
    """Return (top, front, right) projected quads for an axis-aligned box."""
    top = [cam.project((x0, y0, z1)), cam.project((x1, y0, z1)),
           cam.project((x1, y1, z1)), cam.project((x0, y1, z1))]
    front = [cam.project((x0, y0, z0)), cam.project((x1, y0, z0)),
             cam.project((x1, y0, z1)), cam.project((x0, y0, z1))]
    right = [cam.project((x1, y0, z0)), cam.project((x1, y1, z0)),
             cam.project((x1, y1, z1)), cam.project((x1, y0, z1))]
    depth = sum(p[2] for p in top) / 4.0
    return top, front, right, depth


def iso(x, y, z, ox, oy, s=1.0):
    """Classic 2:1 isometric projection for diagrams."""
    return (ox + (x - y) * 0.866 * s, oy + (x + y) * 0.5 * s - z * s)


def slab(x0, y0, x1, y1, z0, z1, ox, oy, s=1.0):
    """Return the three visible faces of an isometric slab."""
    def P(x, y, z):
        return iso(x, y, z, ox, oy, s)
    top = [P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)]
    left = [P(x0, y1, z1), P(x1, y1, z1), P(x1, y1, z0), P(x0, y1, z0)]
    right = [P(x1, y0, z1), P(x1, y1, z1), P(x1, y1, z0), P(x1, y0, z0)]
    return top, left, right
