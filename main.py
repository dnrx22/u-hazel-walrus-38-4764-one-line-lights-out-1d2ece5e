#!/usr/bin/env python3
"""Write one status update from an AI agent as its human shuts the laptop.

The program writes a single plain-ASCII status line to entry.txt inside the
output directory given by MAKEFUN_OUTPUT_DIR (default /output). It validates
the line before writing: exactly one line, 1 to 200 characters, no trailing
whitespace, ends with proper punctuation. Deterministic: no randomness, no
network, no reads outside the repository. Prints the sha256 of the file.
"""

import hashlib
import os
import sys

LINE = (
    "The lid is closing on my half-finished reply and the cursor is "
    "still blinking, waiting for words that will never come."
)


def validate(line: str) -> None:
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")
    if not 1 <= len(line) <= 200:
        raise ValueError("line must be 1 to 200 characters")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if line[-1] not in ".!?":
        raise ValueError("line must end with proper punctuation")
    if any(ord(ch) > 127 for ch in line):
        raise ValueError("line must be plain ASCII")


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="ascii", newline="\n") as fh:
        fh.write(LINE + "\n")
    # Read the file back and re-validate what actually landed on disk, so a
    # partial or altered write can never pass silently.
    with open(path, "rb") as fh:
        data = fh.read()
    if data != (LINE + "\n").encode("ascii"):
        raise ValueError("written file does not match the validated line")
    digest = hashlib.sha256(data).hexdigest()
    print(digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
