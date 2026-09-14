#!/usr/bin/env python3
"""Create the Astropolis RU spacesuit texture overrides.

The Cosmopolis suit uses the legacy 64x32 humanoid armor atlas.  This script
replaces the opaque helmet with short hair and a small kippah, adds a small
front/back number and an upper-arm tricolour band, and builds a matching icon.
"""

from __future__ import annotations

import binascii
import struct
import zlib
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parent.parent
MEMBER = "assets/cosmopolis/textures/models/armor/space_suit_layer_1.png"
ITEM_MEMBER = "assets/cosmopolis/textures/item/space_suit_helmet.png"
OUTPUT = (
    ROOT
    / "overrides/kubejs/assets/cosmopolis/textures/models/armor/space_suit_layer_1.png"
)
ITEM_OUTPUT = ROOT / "overrides/kubejs/assets/cosmopolis/textures/item/space_suit_helmet.png"


def find_cosmopolis_jar() -> Path:
    for jar in sorted((ROOT / "server/mods").glob("*.jar")):
        try:
            with ZipFile(jar) as archive:
                if MEMBER in archive.namelist():
                    return jar
        except Exception:
            continue
    raise SystemExit("Could not find the Cosmopolis mod jar")


HAIR = (
    (29, 19, 13, 255),
    (43, 28, 18, 255),
    (59, 38, 23, 255),
    (76, 49, 29, 255),
)
KIPPAH_DARK = (10, 18, 45, 255)
KIPPAH = (20, 38, 87, 255)
KIPPAH_LIGHT = (39, 65, 126, 255)
TRANSPARENT = (0, 0, 0, 0)


def paeth(left: int, above: int, upper_left: int) -> int:
    estimate = left + above - upper_left
    dl = abs(estimate - left)
    da = abs(estimate - above)
    dul = abs(estimate - upper_left)
    if dl <= da and dl <= dul:
        return left
    if da <= dul:
        return above
    return upper_left


def decode_rgba(png: bytes) -> tuple[int, int, bytearray]:
    if png[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a PNG")
    cursor = 8
    compressed = bytearray()
    width = height = bit_depth = color_type = -1
    while cursor < len(png):
        length = struct.unpack(">I", png[cursor : cursor + 4])[0]
        kind = png[cursor + 4 : cursor + 8]
        payload = png[cursor + 8 : cursor + 8 + length]
        cursor += 12 + length
        if kind == b"IHDR":
            width, height, bit_depth, color_type, compression, filtering, interlace = struct.unpack(
                ">IIBBBBB", payload
            )
            if (bit_depth, color_type, compression, filtering, interlace) != (8, 6, 0, 0, 0):
                raise ValueError("Expected a non-interlaced 8-bit RGBA PNG")
        elif kind == b"IDAT":
            compressed.extend(payload)
        elif kind == b"IEND":
            break

    channels = 4
    stride = width * channels
    filtered = zlib.decompress(bytes(compressed))
    pixels = bytearray(width * height * channels)
    source = 0
    previous = bytearray(stride)
    for y in range(height):
        filter_type = filtered[source]
        source += 1
        scanline = bytearray(filtered[source : source + stride])
        source += stride
        for x in range(stride):
            left = scanline[x - channels] if x >= channels else 0
            above = previous[x]
            upper_left = previous[x - channels] if x >= channels else 0
            if filter_type == 1:
                scanline[x] = (scanline[x] + left) & 0xFF
            elif filter_type == 2:
                scanline[x] = (scanline[x] + above) & 0xFF
            elif filter_type == 3:
                scanline[x] = (scanline[x] + ((left + above) // 2)) & 0xFF
            elif filter_type == 4:
                scanline[x] = (scanline[x] + paeth(left, above, upper_left)) & 0xFF
            elif filter_type != 0:
                raise ValueError(f"Unsupported PNG filter: {filter_type}")
        pixels[y * stride : (y + 1) * stride] = scanline
        previous = scanline
    return width, height, pixels


def chunk(kind: bytes, payload: bytes) -> bytes:
    return (
        struct.pack(">I", len(payload))
        + kind
        + payload
        + struct.pack(">I", binascii.crc32(kind + payload) & 0xFFFFFFFF)
    )


def encode_rgba(width: int, height: int, pixels: bytearray) -> bytes:
    stride = width * 4
    raw = b"".join(
        b"\x00" + bytes(pixels[y * stride : (y + 1) * stride]) for y in range(height)
    )
    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def set_pixel(pixels: bytearray, width: int, x: int, y: int, rgba: tuple[int, int, int, int]) -> None:
    offset = (y * width + x) * 4
    pixels[offset : offset + 4] = bytes(rgba)


def draw_number(pixels: bytearray, width: int, x: int, y: int) -> None:
    glyphs = {
        "6": ("111", "100", "111", "101", "111"),
        "7": ("111", "001", "010", "010", "010"),
    }
    ink = (20, 54, 65, 255)
    cursor = x
    for digit in "67":
        for row, line in enumerate(glyphs[digit]):
            for column, enabled in enumerate(line):
                if enabled == "1":
                    set_pixel(pixels, width, cursor + column, y + row, ink)
        cursor += 4


def hair_pixel(x: int, y: int, salt: int = 0) -> tuple[int, int, int, int]:
    """Return a deterministic dark-brown pixel-hair colour."""
    value = (x * 17 + y * 29 + x * y * 7 + salt * 13) % 13
    if value in (0, 1):
        return HAIR[0]
    return HAIR[1 + (value % 3)]


def fill_hair(
    pixels: bytearray,
    width: int,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    salt: int = 0,
) -> None:
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            set_pixel(pixels, width, x, y, hair_pixel(x, y, salt))


def draw_hair_and_kippah(pixels: bytearray, width: int) -> None:
    """Replace the legacy helmet UV with short hair and a small skullcap."""
    # Clear the old opaque spacesuit helmet, including its underside and visor.
    for y in range(0, 8):
        for x in range(8, 24):
            set_pixel(pixels, width, x, y, TRANSPARENT)
    for y in range(8, 16):
        for x in range(0, 32):
            set_pixel(pixels, width, x, y, TRANSPARENT)

    # Hair on the top, sides and back of the head.  The central front remains
    # transparent so each player's own face texture is visible through it.
    fill_hair(pixels, width, 8, 0, 15, 7, 1)
    fill_hair(pixels, width, 0, 9, 7, 12, 2)
    fill_hair(pixels, width, 16, 9, 23, 12, 3)
    fill_hair(pixels, width, 24, 9, 31, 13, 4)
    fill_hair(pixels, width, 8, 9, 15, 10, 5)
    for x in (8, 9, 11, 14, 15):
        set_pixel(pixels, width, x, 11, hair_pixel(x, 11, 6))
    for y in range(11, 14):
        set_pixel(pixels, width, 8, y, hair_pixel(8, y, 7))
        set_pixel(pixels, width, 15, y, hair_pixel(15, y, 8))
    for x in (24, 26, 28, 31):
        set_pixel(pixels, width, x, 14, hair_pixel(x, 14, 9))

    # Small rounded dark-navy kippah centred on the top face.
    cap_rows = {
        1: (11, 12),
        2: (10, 13),
        3: (9, 14),
        4: (10, 13),
    }
    for y, (x0, x1) in cap_rows.items():
        for x in range(x0, x1 + 1):
            colour = KIPPAH_LIGHT if (x + y) % 5 == 0 else KIPPAH
            set_pixel(pixels, width, x, y, colour)
    for x in (9, 14):
        set_pixel(pixels, width, x, 3, KIPPAH_DARK)

    # A one-pixel rim makes the cap readable from normal third-person angles.
    for x0 in (0, 8, 16, 24):
        for x in range(x0 + 2, x0 + 6):
            set_pixel(pixels, width, x, 8, KIPPAH_DARK if x in (x0 + 2, x0 + 5) else KIPPAH)


def build_helmet_icon(source: bytes) -> bytes:
    width, height, pixels = decode_rgba(source)
    if (width, height) != (16, 16):
        raise SystemExit(f"Unexpected helmet icon size: {width}x{height}")

    for y in range(height):
        for x in range(width):
            set_pixel(pixels, width, x, y, TRANSPARENT)

    # Compact inventory sprite: a curved kippah with a narrow hair edge.
    icon_rows = {
        4: (7, 8),
        5: (5, 10),
        6: (4, 11),
        7: (3, 12),
        8: (3, 12),
    }
    for y, (x0, x1) in icon_rows.items():
        for x in range(x0, x1 + 1):
            if y == 8 or x in (x0, x1):
                colour = KIPPAH_DARK
            elif (x + y) % 5 == 0:
                colour = KIPPAH_LIGHT
            else:
                colour = KIPPAH
            set_pixel(pixels, width, x, y, colour)
    for x in range(4, 12):
        set_pixel(pixels, width, x, 9, hair_pixel(x, 9, 10))
    return encode_rgba(width, height, pixels)


def main() -> None:
    source_jar = find_cosmopolis_jar()
    with ZipFile(source_jar) as archive:
        width, height, pixels = decode_rgba(archive.read(MEMBER))
    if (width, height) != (64, 32):
        raise SystemExit(f"Unexpected armor atlas size: {width}x{height}")

    draw_hair_and_kippah(pixels, width)

    # Torso front (20..27) and back (32..39), centered vertically.
    draw_number(pixels, width, 20, 23)
    draw_number(pixels, width, 32, 23)

    # Legacy layer-1 maps both arms to x=40..55.  Three rows therefore form a
    # continuous upper-arm band on every visible face of both mirrored arms.
    for x in range(40, 56):
        set_pixel(pixels, width, x, 21, (238, 238, 238, 255))
        set_pixel(pixels, width, x, 22, (25, 67, 160, 255))
        set_pixel(pixels, width, x, 23, (190, 30, 45, 255))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(encode_rgba(width, height, pixels))
    with ZipFile(source_jar) as archive:
        item_png = build_helmet_icon(archive.read(ITEM_MEMBER))
    ITEM_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ITEM_OUTPUT.write_bytes(item_png)
    print(f"Built {OUTPUT.relative_to(ROOT)} from {source_jar.name}")
    print(f"Built {ITEM_OUTPUT.relative_to(ROOT)} from {source_jar.name}")


if __name__ == "__main__":
    main()
