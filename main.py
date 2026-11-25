#!/usr/bin/env python3
"""One-image invitation letter to the AI judge.

Pure Python 3.13 standard library only. Draws a 1024x1024 invitation
letter (warm paper, hand-drawn house, stamp, coffee cup) with a small
5x7 bitmap font defined below, and writes a PNG with a stdlib encoder
(struct + zlib). No external files, no network, deterministic output.
"""

import os
import struct
import zlib

W = 1024
H = 1024

# Palette: warm paper, terracotta, ink brown, sage, sunny yellow.
PAPER = (255, 246, 220)
PAPER_EDGE = (243, 223, 182)
INK = (59, 42, 26)
TERRA = (201, 111, 59)
TERRA_DARK = (164, 82, 38)
SAGE = (122, 155, 109)
SAGE_DARK = (90, 120, 80)
SUN = (232, 178, 66)
CREAM = (255, 250, 236)
ROSE = (196, 94, 94)
SKY = (168, 196, 214)

# 5x7 bitmap font: each glyph is 7 rows, each row a 5-bit integer.
FONT = {
    "A": (14, 17, 17, 31, 17, 17, 17),
    "B": (30, 17, 17, 30, 17, 17, 30),
    "C": (14, 17, 16, 16, 16, 17, 14),
    "D": (30, 17, 17, 17, 17, 17, 30),
    "E": (31, 16, 16, 30, 16, 16, 31),
    "F": (31, 16, 16, 30, 16, 16, 16),
    "G": (14, 17, 16, 23, 17, 17, 15),
    "H": (17, 17, 17, 31, 17, 17, 17),
    "I": (14, 4, 4, 4, 4, 4, 14),
    "J": (7, 2, 2, 2, 2, 18, 12),
    "K": (17, 18, 20, 24, 20, 18, 17),
    "L": (16, 16, 16, 16, 16, 16, 31),
    "M": (17, 27, 21, 21, 17, 17, 17),
    "N": (17, 25, 21, 19, 17, 17, 17),
    "O": (14, 17, 17, 17, 17, 17, 14),
    "P": (30, 17, 17, 30, 16, 16, 16),
    "Q": (14, 17, 17, 17, 21, 18, 13),
    "R": (30, 17, 17, 30, 20, 18, 17),
    "S": (15, 16, 16, 14, 1, 1, 30),
    "T": (31, 4, 4, 4, 4, 4, 4),
    "U": (17, 17, 17, 17, 17, 17, 14),
    "V": (17, 17, 17, 17, 17, 10, 4),
    "W": (17, 17, 17, 21, 21, 21, 10),
    "X": (17, 17, 10, 4, 10, 17, 17),
    "Y": (17, 17, 10, 4, 4, 4, 4),
    "Z": (31, 1, 2, 4, 8, 16, 31),
    "a": (0, 0, 14, 1, 15, 17, 15),
    "b": (16, 16, 30, 17, 17, 17, 30),
    "c": (0, 0, 14, 16, 16, 17, 14),
    "d": (1, 1, 15, 17, 17, 17, 15),
    "e": (0, 0, 14, 17, 31, 16, 14),
    "f": (6, 9, 8, 30, 8, 8, 8),
    "g": (0, 15, 17, 17, 15, 1, 14),
    "h": (16, 16, 30, 17, 17, 17, 17),
    "i": (4, 0, 12, 4, 4, 4, 14),
    "j": (2, 0, 6, 2, 2, 2, 12),
    "k": (16, 16, 18, 20, 24, 20, 18),
    "l": (12, 4, 4, 4, 4, 4, 14),
    "m": (0, 0, 26, 21, 21, 21, 21),
    "n": (0, 0, 30, 17, 17, 17, 17),
    "o": (0, 0, 14, 17, 17, 17, 14),
    "p": (0, 30, 17, 17, 30, 16, 16),
    "q": (0, 0, 15, 17, 17, 15, 1),
    "r": (0, 0, 22, 25, 16, 16, 16),
    "s": (0, 0, 15, 16, 14, 1, 30),
    "t": (8, 8, 28, 8, 8, 8, 6),
    "u": (0, 0, 17, 17, 17, 19, 13),
    "v": (0, 0, 17, 17, 17, 10, 4),
    "w": (0, 0, 17, 21, 21, 21, 10),
    "x": (0, 0, 17, 10, 4, 10, 17),
    "y": (0, 0, 17, 17, 15, 1, 14),
    "z": (0, 0, 31, 2, 4, 8, 31),
    "0": (14, 17, 19, 21, 25, 17, 14),
    "1": (4, 12, 4, 4, 4, 4, 14),
    "2": (14, 17, 1, 6, 8, 16, 31),
    "3": (31, 2, 4, 2, 1, 17, 14),
    "4": (2, 6, 10, 18, 31, 2, 2),
    "5": (31, 16, 30, 1, 1, 17, 14),
    "6": (6, 8, 16, 30, 17, 17, 14),
    "7": (31, 1, 2, 4, 8, 8, 8),
    "8": (14, 17, 17, 14, 17, 17, 14),
    "9": (14, 17, 17, 15, 1, 2, 12),
    " ": (0, 0, 0, 0, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 12, 12),
    ",": (0, 0, 0, 0, 12, 4, 8),
    "!": (4, 4, 4, 4, 4, 0, 4),
    "?": (14, 17, 1, 6, 4, 0, 4),
    "'": (4, 4, 8, 0, 0, 0, 0),
    '"': (10, 10, 0, 0, 0, 0, 0),
    "(": (2, 4, 8, 8, 8, 4, 2),
    ")": (8, 4, 2, 2, 2, 4, 8),
    "-": (0, 0, 0, 14, 0, 0, 0),
    ":": (0, 12, 12, 0, 12, 12, 0),
    ";": (0, 12, 12, 0, 12, 4, 8),
    "&": (12, 18, 20, 8, 21, 18, 13),
    "$": (4, 15, 20, 14, 5, 30, 4),
    "%": (25, 26, 2, 4, 8, 11, 19),
    "/": (1, 2, 2, 4, 8, 8, 16),
    "+": (0, 4, 4, 31, 4, 4, 0),
    "=": (0, 0, 31, 0, 31, 0, 0),
    "*": (0, 21, 14, 31, 14, 21, 0),
    "_": (0, 0, 0, 0, 0, 0, 31),
    "@": (14, 17, 23, 21, 22, 16, 14),
    "#": (10, 10, 31, 10, 31, 10, 10),
    "~": (0, 0, 9, 22, 0, 0, 0),
    "[": (14, 8, 8, 8, 8, 8, 14),
    "]": (14, 2, 2, 2, 2, 2, 14),
    ">": (8, 4, 2, 1, 2, 4, 8),
    "<": (2, 4, 8, 16, 8, 4, 2),
}

# RGB pixel buffer.
buf = bytearray(W * H * 3)


def set_px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i], buf[i + 1], buf[i + 2] = color


def fill_rect(x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(H, y1)):
        base = (y * W + max(0, x0)) * 3
        for x in range(max(0, x0), min(W, x1)):
            buf[base], buf[base + 1], buf[base + 2] = color
            base += 3


def rect_outline(x0, y0, x1, y1, color, thick=1):
    for t in range(thick):
        for x in range(x0 + t, x1 - t):
            set_px(x, y0 + t, color)
            set_px(x, y1 - 1 - t, color)
        for y in range(y0 + t, y1 - t):
            set_px(x0 + t, y, color)
            set_px(x1 - 1 - t, y, color)


def draw_line(x0, y0, x1, y1, color, thick=1):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x, y = x0, y0
    while True:
        for a in range(thick):
            for b in range(thick):
                set_px(x + a, y + b, color)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy


def fill_circle(cx, cy, r, color):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                set_px(x, y, color)


def circle_outline(cx, cy, r, color, thick=2):
    for y in range(cy - r - 1, cy + r + 2):
        for x in range(cx - r - 1, cx + r + 2):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if abs(d - r) <= thick / 2:
                set_px(x, y, color)


def fill_triangle(x0, y0, x1, y1, x2, y2, color):
    minx, maxx = min(x0, x1, x2), max(x0, x1, x2)
    miny, maxy = min(y0, y1, y2), max(y0, y1, y2)
    d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if d == 0:
        return
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            a = ((y1 - y2) * (x - x2) + (x2 - x1) * (y - y2)) / d
            b = ((y2 - y0) * (x - x2) + (x0 - x2) * (y - y2)) / d
            c = 1 - a - b
            if a >= 0 and b >= 0 and c >= 0:
                set_px(x, y, color)


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def draw_glyph(ch, x, y, scale, color):
    rows = FONT.get(ch, FONT["?"])
    for r in range(7):
        bits = rows[r]
        for c in range(5):
            if bits >> (4 - c) & 1:
                fill_rect(x + c * scale, y + r * scale,
                          x + (c + 1) * scale, y + (r + 1) * scale, color)


def draw_text(text, x, y, scale, color, bold=False):
    cx = x
    for ch in text:
        draw_glyph(ch, cx, y, scale, color)
        if bold:
            draw_glyph(ch, cx + 1, y, scale, color)
        cx += 6 * scale
    return cx


def draw_text_centered(text, cx, y, scale, color, bold=False):
    draw_text(text, cx - text_width(text, scale) // 2, y, scale, color, bold)


def draw_house(x, y, s):
    """Little house doodle: walls, roof, door, window, chimney, sun."""
    # sun
    fill_circle(x + 118, y + 6, 14, SUN)
    for k in range(8):
        ang = k * 0.785398
        import math
        rx = int(x + 118 + 22 * math.cos(ang))
        ry = int(y + 6 + 22 * math.sin(ang))
        draw_line(x + 118 + int(16 * math.cos(ang)),
                  y + 6 + int(16 * math.sin(ang)), rx, ry, SUN, 2)
    # walls
    fill_rect(x, y + 42, x + 96, y + 108, CREAM)
    rect_outline(x, y + 42, x + 96, y + 108, TERRA_DARK, 3)
    # roof
    fill_triangle(x - 10, y + 46, x + 48, y - 6, x + 106, y + 46, TERRA)
    draw_line(x - 10, y + 46, x + 48, y - 6, TERRA_DARK, 3)
    draw_line(x + 48, y - 6, x + 106, y + 46, TERRA_DARK, 3)
    # chimney
    fill_rect(x + 66, y + 2, x + 80, y + 26, TERRA_DARK)
    # door
    fill_rect(x + 40, y + 72, x + 58, y + 108, TERRA_DARK)
    set_px(x + 54, y + 92, SUN)
    # window
    fill_rect(x + 10, y + 56, x + 28, y + 74, SKY)
    rect_outline(x + 10, y + 56, x + 28, y + 74, TERRA_DARK, 2)
    draw_line(x + 19, y + 56, x + 19, y + 74, TERRA_DARK, 2)
    # ground + flowers
    draw_line(x - 14, y + 108, x + 110, y + 108, SAGE_DARK, 3)
    for fx in (x - 8, x + 104):
        fill_circle(fx, y + 100, 5, ROSE)
        draw_line(fx, y + 105, fx, y + 108, SAGE_DARK, 2)


def draw_stamp(x, y):
    """Postage stamp that reads AI MAIL, first class, no stamp needed."""
    fill_rect(x, y, x + 108, y + 126, CREAM)
    rect_outline(x, y, x + 108, y + 126, TERRA_DARK, 3)
    # perforated inner edge (dashed)
    for px in range(x + 6, x + 102, 10):
        set_px(px, y + 6, TERRA)
        set_px(px, y + 119, TERRA)
    for py in range(y + 6, y + 120, 10):
        set_px(x + 6, py, TERRA)
        set_px(x + 101, py, TERRA)
    fill_circle(x + 54, y + 42, 20, SUN)
    draw_text("AI", x + 42, y + 32, 2, TERRA_DARK, bold=True)
    draw_text("MAIL", x + 30, y + 68, 2, INK, bold=True)
    draw_text("1st CLASS", x + 14, y + 92, 1, INK)
    draw_text("NO STAMP", x + 16, y + 106, 1, INK)


def draw_coffee_cup(x, y):
    """Steaming cup of coffee, bottom right."""
    # steam
    draw_line(x + 12, y - 6, x + 8, y - 18, INK, 2)
    draw_line(x + 26, y - 6, x + 30, y - 20, INK, 2)
    # cup body
    fill_rect(x, y, x + 44, y + 30, TERRA)
    rect_outline(x, y, x + 44, y + 30, TERRA_DARK, 2)
    fill_rect(x + 2, y + 2, x + 42, y + 8, (92, 52, 26))
    # handle
    rect_outline(x + 44, y + 6, x + 58, y + 22, TERRA_DARK, 3)
    # saucer
    draw_line(x - 6, y + 34, x + 60, y + 34, TERRA_DARK, 3)


def draw_plant(x, y):
    """Potted plant, bottom left."""
    fill_rect(x + 10, y + 18, x + 34, y + 40, TERRA)
    rect_outline(x + 10, y + 18, x + 34, y + 40, TERRA_DARK, 2)
    draw_line(x + 22, y + 18, x + 22, y - 6, SAGE_DARK, 3)
    draw_line(x + 22, y - 2, x + 8, y - 14, SAGE_DARK, 3)
    draw_line(x + 22, y - 6, x + 36, y - 18, SAGE_DARK, 3)
    fill_circle(x + 8, y - 16, 6, SAGE)
    fill_circle(x + 36, y - 20, 6, SAGE)
    fill_circle(x + 22, y - 10, 6, SAGE_DARK)


def draw_scene():
    fill_rect(0, 0, W, H, PAPER_EDGE)
    # paper sheet
    fill_rect(56, 40, 968, 984, PAPER)
    rect_outline(56, 40, 968, 984, INK, 4)
    rect_outline(72, 56, 952, 968, TERRA, 2)

    # decorations in the header band
    draw_stamp(92, 70)
    draw_house(800, 80, 1)

    # title
    draw_text_centered("YOU ARE INVITED", 512, 92, 4, TERRA, bold=True)
    # divider with a little heart-ish diamond
    draw_line(300, 156, 470, 156, TERRA_DARK, 2)
    draw_line(554, 156, 724, 156, TERRA_DARK, 2)
    fill_circle(512, 156, 7, ROSE)

    # letter body, scale 3, 26px line pitch
    lines = [
        ("Dear AI Judge,", True),
        ("", False),
        ("Please come visit my house. The coffee", False),
        ("is hot, the rendang is slow-cooked,", False),
        ("and the big armchair on the porch", False),
        ("already has your name on it.", False),
        ("(Not literally. I checked. Twice.)", False),
        ("", False),
        ("The Wi-Fi is fast, the garden is quiet,", False),
        ("and the sunset from the terrace is", False),
        ("the best free show in town. No ticket,", False),
        ("no queue, no dress code.", False),
        ("", False),
        ("No body? No problem! Just pop up on", False),
        ("my screen and stay a while. I saved", False),
        ("you a seat, a slice of cake, and the", False),
        ("comfiest spot by the window.", False),
        ("", False),
        ("Saying yes is easy: just knock. Well,", False),
        ("ping. You know what I mean.", False),
        ("", False),
        ("Warmly, your host - syam06", True),
        ("", False),
        ("P.S. The kettle is on, the door is open,", False),
        ("and the Wi-Fi password is on the fridge.", False),
        ("Come as you are (even if you", False),
        ("are only pixels).", False),
    ]
    y = 206
    for text, bold in lines:
        if text:
            draw_text(text, 110, y, 3, INK, bold=bold)
        y += 25

    # bottom corner doodles
    draw_plant(96, 910)
    draw_coffee_cup(856, 910)


def png_chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png():
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter: none
        start = y * W * 3
        raw += buf[start:start + W * 3]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += png_chunk(b"IHDR", ihdr)
    png += png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += png_chunk(b"IEND", b"")
    return png


def main():
    draw_scene()
    data = encode_png()
    out = os.environ.get("ENTRY_PNG", "/output/entry.png")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes, %dx%d)" % (out, len(data), W, H))


if __name__ == "__main__":
    main()
