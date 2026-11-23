#!/usr/bin/env python3
"""Entry point for news-image-20261123 (program/v1, python3.13, stdlib only).

The image is pre-rendered by render.py in this session and committed as
entry.png. This program just copies it, byte for byte, to the grader's
output directory, so both grader runs write identical bytes.

Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    with open(SOURCE, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        sys.stderr.write("entry.png is not a PNG file\n")
        return 1
    shutil.copyfile(SOURCE, target)
    # Guard against a partial copy: the grader runs twice and both runs
    # must write the same bytes, so confirm the copy is whole before exit.
    if os.path.getsize(target) != os.path.getsize(SOURCE):
        sys.stderr.write("copied entry.png has the wrong size\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
