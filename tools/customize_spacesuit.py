#!/usr/bin/env python3
"""Create the Astropolis RU spacesuit texture overrides.

The Cosmopolis suit uses the legacy 64x32 humanoid armor atlas.  This script
adds a fur shtreimel-style helmet with sidelocks, a small front/back number,
an upper-arm tricolour band, and a matching inventory icon.
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


FUR = (
    (31, 20, 14, 255),
    (45, 29, 20, 255),
    (58, 38, 26, 255),
    (72, 47, 31, 255),
    (87, 57, 37, 255),
)
PAYOT = ((25, 17, 12, 255), (49, 31, 21, 255), (72, 46, 30, 255))
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


def fur_pixel(x: int, y: int, salt: int = 0) -> tuple[int, int, int, int]:
    """Return a deterministic, high-contrast pixel-fur colour."""
    value = (x * 17 + y * 29 + x * y * 7 + salt * 13) % 19
    if value in (0, 1):
        return FUR[4]
    if value in (2, 3, 4):
        return FUR[0]
    return FUR[1 + (value % 3)]


def fill_fur(
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
            set_pixel(pixels, width, x, y, fur_pixel(x, y, salt))


def draw_shtreimel(pixels: bytearray, width: int) -> None:
    """Paint the standard legacy helmet UV as a fur hat with visible sidelocks."""
    # Head top and underside.
    fill_fur(pixels, width, 8, 0, 15, 7, 1)
    fill_fur(pixels, width, 16, 0, 23, 7, 2)

    # The upper five pixels of every head face form a thick, continuous fur hat.
    fill_fur(pixels, width, 0, 8, 31, 12, 3)

    # Remove the old spacesuit visor below the brim so the player's face shows.
    for y in range(13, 16):
        for x in range(0, 32):
            set_pixel(pixels, width, x, y, TRANSPARENT)

    # Short curls on the two lower corners of the front head face.
    for index, y in enumerate(range(13, 16)):
        set_pixel(pixels, width, 8 + (index % 2), y, PAYOT[index % len(PAYOT)])
        set_pixel(pixels, width, 15 - (index % 2), y, PAYOT[index % len(PAYOT)])

    # Continue the curls over the two torso side faces.  These columns sit next
    # to the chest front, leaving both front and back "67" markings untouched.
    left_curl = ((19, 20), (18, 21), (19, 22), (18, 23), (19, 24), (18, 25), (19, 26))
    right_curl = ((28, 20), (29, 21), (28, 22), (29, 23), (28, 24), (29, 25), (28, 26))
    for index, ((lx, ly), (rx, ry)) in enumerate(zip(left_curl, right_curl)):
        colour = PAYOT[index % len(PAYOT)]
        set_pixel(pixels, width, lx, ly, colour)
        set_pixel(pixels, width, rx, ry, colour)


def build_helmet_icon(source: bytes) -> bytes:
    width, height, pixels = decode_rgba(source)
    if (width, height) != (16, 16):
        raise SystemExit(f"Unexpected helmet icon size: {width}x{height}")

    for y in range(height):
        for x in range(width):
            set_pixel(pixels, width, x, y, TRANSPARENT)

    # Broad fur crown with slightly rounded corners.
    for y in range(2, 9):
        inset = 1 if y in (2, 8) else 0
        for x in range(2 + inset, 14 - inset):
            set_pixel(pixels, width, x, y, fur_pixel(x, y, 7))
    for x in range(2, 14):
        set_pixel(pixels, width, x, 7, FUR[0 if x % 3 == 0 else 2])

    # Two twisted sidelocks below the hat.
    for index, y in enumerate(range(9, 15)):
        offset = index % 2
        set_pixel(pixels, width, 4 + offset, y, PAYOT[index % len(PAYOT)])
        set_pixel(pixels, width, 11 - offset, y, PAYOT[index % len(PAYOT)])
    return encode_rgba(width, height, pixels)


def main() -> None:
    source_jar = find_cosmopolis_jar()
    with ZipFile(source_jar) as archive:
        width, height, pixels = decode_rgba(archive.read(MEMBER))
    if (width, height) != (64, 32):
        raise SystemExit(f"Unexpected armor atlas size: {width}x{height}")

    draw_shtreimel(pixels, width)

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
