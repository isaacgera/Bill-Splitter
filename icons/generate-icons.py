"""
Generate raster PNG icons for Splitzy from the SVG geometry, using only the
Python standard library (no Pillow / cairosvg / network needed).

Why pure stdlib: the build machine sits behind a TLS-intercepting corporate
proxy, so pip cannot reach PyPI. PNG is a simple format, so we render the icon
geometry into an RGBA pixel buffer and emit valid PNGs via zlib + struct.

Reproduces icons/icon.svg and icons/icon-maskable.svg (512x512 viewBox):
  - rounded-rect background with a diagonal gradient #0ea5e9 -> #0284c7
    (maskable variant: full-bleed square, artwork scaled to the ~80% safe zone)
  - white receipt outline with a zig-zag bottom edge
  - three white horizontal "text" lines

Run:  python icons/generate-icons.py
Outputs (next to this script):
  icon-192.png, icon-512.png, icon-maskable-192.png, icon-maskable-512.png
"""

import os
import zlib
import struct
import math

SS = 3  # supersample factor for anti-aliasing

C0 = (0x0e, 0xa5, 0xe9)   # gradient start
C1 = (0x02, 0x84, 0xc7)   # gradient end
WHITE = (0xff, 0xff, 0xff)


def lerp(a, b, t):
    return a + (b - a) * t


def blend(dst, src, alpha):
    """Alpha-composite src (rgb) over dst (rgba) with coverage alpha [0..1]."""
    sr, sg, sb = src
    dr, dg, db, da = dst
    da_f = da / 255.0
    out_a = alpha + da_f * (1 - alpha)
    if out_a <= 0:
        return (0, 0, 0, 0)
    nr = (sr * alpha + dr * da_f * (1 - alpha)) / out_a
    ng = (sg * alpha + dg * da_f * (1 - alpha)) / out_a
    nb = (sb * alpha + db * da_f * (1 - alpha)) / out_a
    return (int(round(nr)), int(round(ng)), int(round(nb)), int(round(out_a * 255)))


def point_in_rounded_rect(x, y, x0, y0, x1, y1, r):
    if x < x0 or x > x1 or y < y0 or y > y1:
        return False
    # corner checks
    cx = None
    cy = None
    if x < x0 + r and y < y0 + r:
        cx, cy = x0 + r, y0 + r
    elif x > x1 - r and y < y0 + r:
        cx, cy = x1 - r, y0 + r
    elif x < x0 + r and y > y1 - r:
        cx, cy = x0 + r, y1 - r
    elif x > x1 - r and y > y1 - r:
        cx, cy = x1 - r, y1 - r
    if cx is not None:
        return (x - cx) ** 2 + (y - cy) ** 2 <= r * r
    return True


def dist_point_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def build_polyline(pts, closed=False):
    segs = []
    n = len(pts)
    for i in range(n - 1):
        segs.append((pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]))
    if closed:
        segs.append((pts[-1][0], pts[-1][1], pts[0][0], pts[0][1]))
    return segs


def receipt_geometry():
    """Return (outline_segments, line_segments) in 512-space, matching the SVG."""
    # Receipt outline path from the SVG (zig-zag bottom), treated as a closed loop.
    outline = [
        (170, 108), (170, 404),
        (210, 382), (250, 404), (290, 382), (330, 404), (370, 382), (410, 404),
        (410, 108),
        (370, 130), (330, 108), (290, 130), (250, 108), (210, 130),
    ]
    outline_segs = build_polyline(outline, closed=True)
    line_segs = [
        (226, 190, 366, 190),
        (226, 256, 366, 256),
        (226, 322, 310, 322),
    ]
    return outline_segs, line_segs


def render(size, maskable):
    S = size * SS
    # pixel buffer rgba
    buf = [[(0, 0, 0, 0)] * S for _ in range(S)]
    scale = S / 512.0

    # --- background ---
    # Precompute the diagonal gradient as a lookup over (x + y).
    grad = []
    for k in range(2 * S - 1):
        t = k / (2.0 * (S - 1))
        grad.append((int(lerp(C0[0], C1[0], t)),
                     int(lerp(C0[1], C1[1], t)),
                     int(lerp(C0[2], C1[2], t)), 255))

    br = 0 if maskable else int(round(112 * scale))
    for y in range(S):
        rowbuf = buf[y]
        if maskable or br == 0:
            x0, x1 = 0, S
        else:
            # compute the filled x-span for this row given rounded corners
            x0, x1 = 0, S
            if y < br:
                dy = br - y
                dx = br - int(math.sqrt(max(0, br * br - dy * dy)))
                x0, x1 = dx, S - dx
            elif y > (S - 1) - br:
                dy = y - ((S - 1) - br)
                dx = br - int(math.sqrt(max(0, br * br - dy * dy)))
                x0, x1 = dx, S - dx
        for x in range(x0, x1):
            rowbuf[x] = grad[x + y]

    # --- artwork transform ---
    outline_segs, line_segs = receipt_geometry()
    if maskable:
        # SVG: translate(51 51) scale(0.8), stroke-width 22
        def tf(p):
            return (51 + p[0] * 0.8, 51 + p[1] * 0.8)
        stroke_w = 22
    else:
        def tf(p):
            return p
        stroke_w = 26

    def tf_seg(s):
        a = tf((s[0], s[1]))
        b = tf((s[2], s[3]))
        return (a[0] * scale, a[1] * scale, b[0] * scale, b[1] * scale)

    all_segs = [tf_seg(s) for s in outline_segs] + [tf_seg(s) for s in line_segs]
    half = (stroke_w * (0.8 if maskable else 1.0)) * scale / 2.0

    # bounding box of strokes to limit the pixel loop
    xs = [v for s in all_segs for v in (s[0], s[2])]
    ys = [v for s in all_segs for v in (s[1], s[3])]
    pad = half + 2
    minx = max(0, int(min(xs) - pad)); maxx = min(S - 1, int(max(xs) + pad))
    miny = max(0, int(min(ys) - pad)); maxy = min(S - 1, int(max(ys) + pad))

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            d = min(dist_point_seg(x, y, *s) for s in all_segs)
            cov = half - d + 0.5  # 1px soft edge (in supersampled space)
            if cov <= 0:
                continue
            cov = min(1.0, cov)
            buf[y][x] = blend(buf[y][x], WHITE, cov)

    # --- downsample SSxSS -> size ---
    out = bytearray()
    for oy in range(size):
        row = bytearray()
        row.append(0)  # PNG filter type 0 per scanline
        for ox in range(size):
            r = g = b = a = 0
            for dy in range(SS):
                for dx in range(SS):
                    pr, pg, pb, pa = buf[oy * SS + dy][ox * SS + dx]
                    r += pr; g += pg; b += pb; a += pa
            n = SS * SS
            row += bytes((r // n, g // n, b // n, a // n))
        out += row
    return bytes(out)


def write_png(path, size, raw):
    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)  # 8-bit RGBA
    idat = zlib.compress(raw, 9)
    with open(path, "wb") as f:
        f.write(sig)
        f.write(chunk(b"IHDR", ihdr))
        f.write(chunk(b"IDAT", idat))
        f.write(chunk(b"IEND", b""))


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    jobs = [
        ("icon-192.png", 192, False),
        ("icon-512.png", 512, False),
        ("icon-maskable-192.png", 192, True),
        ("icon-maskable-512.png", 512, True),
    ]
    log = []
    for name, size, maskable in jobs:
        raw = render(size, maskable)
        write_png(os.path.join(here, name), size, raw)
        log.append(name + " " + str(size) + "x" + str(size))
    with open(os.path.join(here, "_gen.log"), "w") as f:
        f.write("OK\n" + "\n".join(log) + "\n")


if __name__ == "__main__":
    main()
