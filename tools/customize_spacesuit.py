#!/usr/bin/env python3
"""Create the Astropolis RU spacesuit texture override.

The Cosmopolis suit uses the legacy 64x32 humanoid armor atlas.  This script
keeps the original atlas byte-for-byte at the pixel level except for a small
front/back number and an upper-arm tricolour band.
"""

from __future__ import annotations

import binascii
import struct
import zlib
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parent.parent
MEMBER = "assets/cosmopolis/textures/models/armor/space_suit_layer_1.png"
OUTPUT = (
    ROOT
    / "overrides/kubejs/assets/cosmopolis/textures/models/armor/space_suit_layer_1.png"
)


def find_cosmopolis_jar() -> Path:
    for jar in sorted((ROOT / "server/mods").glob("*.jar")):
        try:
            with ZipFile(jar) as archive:
                if MEMBER in archive.namelist():
                    return jar
        except Exception:
            continue
    raise SystemExit("Could not find the Cosmopolis mod jar")


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


def main() -> None:
    source_jar = find_cosmopolis_jar()
    with ZipFile(source_jar) as archive:
        width, height, pixels = decode_rgba(archive.read(MEMBER))
    if (width, height) != (64, 32):
        raise SystemExit(f"Unexpected armor atlas size: {width}x{height}")

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
    print(f"Built {OUTPUT.relative_to(ROOT)} from {source_jar.name}")


if __name__ == "__main__":
    main()
