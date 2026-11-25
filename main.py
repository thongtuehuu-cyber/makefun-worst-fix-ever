"""Worst Fix Ever entry: writes one commit-message line to entry.txt.

Deterministic: no network, no randomness, no reading outside this repo.
The line is embedded below; validate() enforces the gate (1-100 chars,
single line, not whitespace-only) and main() writes it with no trailing
newline to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
"""

import os
import sys

LINE = "fix: patch the race condition by making every request wait for all the others"
MAX_CHARS = 100


def validate(line):
    """Enforce the entry gate; raises ValueError on any invalid line."""
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not line.strip():
        raise ValueError("entry must not be empty or whitespace-only")
    if len(line) > MAX_CHARS:
        raise ValueError("entry exceeds 100 characters")
    return line


def main():
    line = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read-back gate: what landed on disk must be exactly the line.
    with open(path, "rb") as f:
        assert f.read() == data, "read-back mismatch"
    return 0


if __name__ == "__main__":
    sys.exit(main())
