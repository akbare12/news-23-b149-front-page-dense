#!/usr/bin/env python3
"""news-23 b149 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Validates the PNG header manually with struct: signature,
first chunk must be a 13-byte IHDR of 1024x1024 (bit depth 8, colour type 2/6),
compression/filter/interlace must be 0, IHDR CRC is checked explicitly, every
chunk's CRC is checked during the chunk walk, every IDAT must be non-empty
(total payload >= 1000 bytes), IEND must be the last 0-byte chunk with no
trailing data. Size must be >= 10000 bytes and <= 1 MiB. Writes ONLY to
os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png").
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "160fc4a3972b97b196853074925d0233167079793d113bff795e7dff5fb2a04a"
EXPECTED_SIZE = 173651
SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def validate(data):
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return "bad PNG signature"
    if len(data) < 10_000:
        return "too small (%d bytes)" % len(data)
    if len(data) > 1024 * 1024:
        return "too large (%d bytes)" % len(data)
    # Chunk layout: 8-byte signature, then chunks of
    # 4-byte length, 4-byte type, length bytes data, 4-byte CRC.
    # The CRC covers type+data, not the length field.
    off = 8
    # First chunk must be IHDR: length 13, type IHDR.
    (clen,) = struct.unpack(">I", data[off:off + 4])
    ctype = data[off + 4:off + 8]
    if ctype != b"IHDR" or clen != 13:
        return "first chunk is not a 13-byte IHDR"
    ihdr = data[off + 8:off + 21]
    w, h, depth, ctype2, comp, filt, inter = struct.unpack(">IIBBBBB", ihdr)
    if (w, h) != (1024, 1024):
        return "wrong dimensions %dx%d" % (w, h)
    if depth != 8 or ctype2 not in (2, 6):
        return "unsupported bit depth %d / colour type %d" % (depth, ctype2)
    if comp != 0 or filt != 0 or inter != 0:
        return "unsupported compression/filter/interlace"
    crc_stored, = struct.unpack(">I", data[off + 21:off + 25])
    crc_calc = zlib.crc32(ctype + ihdr) & 0xFFFFFFFF
    if crc_stored != crc_calc:
        return "IHDR CRC mismatch"
    # Walk the remaining chunks. Next chunk starts right after the IHDR
    # chunk: offset 8 + 12 (length+type+CRC) + clen (13) = 33. Note the CRC
    # field is NOT part of the counted chunk body, so the step is 12 + clen,
    # not 12 + clen + 4 — getting this wrong rejects valid PNGs as truncated.
    off = 8 + 12 + clen
    idat_total = 0
    seen_iend = False
    while True:
        if off + 8 > len(data):
            return "truncated chunk header"
        (clen,) = struct.unpack(">I", data[off:off + 4])
        ctype = data[off + 4:off + 8]
        if off + 12 + clen > len(data):
            return "truncated chunk %r" % ctype
        chunk = data[off + 8:off + 8 + clen]
        crc_stored, = struct.unpack(">I", data[off + 8 + clen:off + 12 + clen])
        crc_calc = zlib.crc32(ctype + chunk) & 0xFFFFFFFF
        if crc_stored != crc_calc:
            return "CRC mismatch in chunk %r" % ctype
        if ctype == b"IDAT":
            if clen == 0:
                return "empty IDAT chunk"
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                return "IEND chunk must be empty"
            if off + 12 + clen != len(data):
                return "trailing data after IEND"
            seen_iend = True
            break
        off += 12 + clen
    if not seen_iend:
        return "missing IEND chunk"
    if idat_total < 1000:
        return "IDAT payload too small (%d bytes)" % idat_total
    return None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    repo = os.path.dirname(os.path.abspath(__file__))
    out_dir_abs = os.path.abspath(out_dir)
    if out_dir_abs == repo or out_dir_abs.startswith(repo + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repo")
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(SOURCE):
        return fail("output would overwrite the source image")
    with open(SOURCE, "rb") as f:
        data = f.read()
    err = validate(data)
    if err:
        return fail(err)
    if len(data) != EXPECTED_SIZE:
        return fail("unexpected size %d (expected %d)" % (len(data), EXPECTED_SIZE))
    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SHA256:
        return fail("sha256 mismatch: got %s" % sha)
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        return fail("re-read output does not match source")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main())
