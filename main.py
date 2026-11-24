#!/usr/bin/env python3
"""Copy entry.png into the output directory, checking it first.

Reads entry.png from the same directory as this file, validates the
PNG magic bytes, the 1 MiB size limit and the 1024x1024 dimensions
(parsed from the IHDR chunk with the standard library only), then
copies the file byte for byte to MAKEFUN_OUTPUT_DIR (default
/output), or to the directory given as an optional command-line
argument. The copy goes through a temp file that is renamed into
place, then is read back and re-validated, so a failed run never
leaves a half-written entry.png behind.

Deterministic by construction: the same entry.png is copied every
run, so two runs write identical bytes.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
EXPECTED_W, EXPECTED_H = 1024, 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def validate_png(data, path):
    """Check magic bytes, size limit and dimensions of raw PNG data."""
    if data[:8] != PNG_MAGIC:
        raise ValueError(f"{path}: not a PNG file (bad magic bytes)")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ValueError(f"{path}: missing IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if len(data) > MAX_BYTES:
        raise ValueError(f"{path}: {len(data)} bytes, over the 1 MiB limit")
    if (width, height) != (EXPECTED_W, EXPECTED_H):
        raise ValueError(f"{path}: {width}x{height}, expected "
                         f"{EXPECTED_W}x{EXPECTED_H}")
    return width, height


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"error: {source} not found; run draw_news.py first",
              file=sys.stderr)
        return 1

    data = source.read_bytes()
    width, height = validate_png(data, source)

    if len(sys.argv) > 2:
        print("usage: main.py [output-dir]", file=sys.stderr)
        return 2
    out_dir = Path(sys.argv[1] if len(sys.argv) == 2
                   else os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"error: cannot create output directory {out_dir}: {exc}",
              file=sys.stderr)
        return 1

    dest = out_dir / "entry.png"
    tmp = out_dir / ".entry.png.tmp"
    try:
        shutil.copyfile(source, tmp)
        os.replace(tmp, dest)
    except OSError as exc:
        print(f"error: cannot write {dest}: {exc}", file=sys.stderr)
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass
        return 1

    written = dest.read_bytes()
    if written != data:
        print("error: written copy does not match entry.png", file=sys.stderr)
        return 1
    # Re-validate the copy on its own merits: a truncated write must
    # fail even if the bytes happened to match by accident.
    validate_png(written, dest)

    digest = hashlib.sha256(written).hexdigest()
    print(f"ok: entry.png {width}x{height}, {len(written)} bytes, "
          f"sha256 {digest}")
    print(f"copied to {dest} (verified: magic, size, dimensions, bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
