#!/usr/bin/env python3
"""Museum of the Year 3000 — one-line museum label entry.

Writes exactly one line (at most 200 characters, no trailing newline)
to /output/entry.txt. Python standard library only.
"""

import os
import sys

ENTRY = "Proof of Humanity, 2024. To enter, visitors named traffic lights for a machine. The machine believed them."

MAX_CHARS = 200
MAX_BYTES = 600  # hard cap on the UTF-8 byte length of the entry


def validate(text):
    """Raise ValueError unless text is a valid single-line entry."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1 to 200 characters")
    if text.strip() != text:
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    if any(0xD800 <= ord(ch) <= 0xDFFF for ch in text):
        raise ValueError("entry must not contain lone surrogates")
    if len(text.encode("utf-8")) > MAX_BYTES:
        raise ValueError("entry must be at most 600 bytes in UTF-8")
    return text


def resolve_output():
    """Return the entry file path, honouring MAKEFUN_OUTPUT."""
    out = os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt")
    if not out.strip():
        raise ValueError("MAKEFUN_OUTPUT must not be empty")
    return out


def write_entry(path, data):
    """Write data to path and verify the round trip byte-for-byte."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(data)
    with open(path, "rb") as f:
        raw = f.read()
    if raw != data.encode("utf-8"):
        raise ValueError("round-trip verification failed")
    return path


def main():
    validate(ENTRY)
    out = resolve_output()
    write_entry(out, ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
