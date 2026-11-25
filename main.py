#!/usr/bin/env python3
"""Write one original one-line text to /output/entry.txt.

A joke excusing a missed deadline: the calendar takes legal action
and the to-do list stops answering. Standard library only, no network,
no input files.

The line itself is a fixed constant. Everything around it is validation
and output plumbing: each rule the competition's sealed scorer applies
(1-200 characters, not only whitespace, a single line of UTF-8 text)
has its own named check so a failure names the rule that caught it.
"""

import os
import sys

LINE = (
    "I missed the deadline so hard the calendar filed a restraining order and my to-do list started ghosting me."
)

MAX_CHARS = 200
MIN_CHARS = 1
OUTPUT_NAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"


class LineError(ValueError):
    """Raised when the entry line fails one of the validation checks."""


def check_not_blank(line: str) -> None:
    """The entry must contain at least one non-whitespace character."""
    if not line.strip():
        raise LineError("must be non-empty after stripping whitespace")


def check_single_line(line: str) -> None:
    """The entry must be exactly one line: no CR, LF, or other line breaks."""
    for bad in ("\n", "\r", "\x0b", "\x0c", "\u2028", "\u2029"):
        if bad in line:
            raise LineError(f"must be a single line (found {bad!r})")


def check_length(line: str) -> None:
    """The entry must fit the competition's character cap."""
    size = len(line)
    if size < MIN_CHARS:
        raise LineError(f"too short: {size} characters, minimum {MIN_CHARS}")
    if size > MAX_CHARS:
        raise LineError(f"too long: {size} characters, maximum {MAX_CHARS}")


def check_no_surrounding_whitespace(line: str) -> None:
    """The entry must not start or end with whitespace (the scorer counts it)."""
    if line != line.strip():
        raise LineError("must not start or end with whitespace")


def check_printable(line: str) -> None:
    """The entry must contain no control characters other than plain spaces."""
    for char in line:
        if ord(char) < 0x20 and char != " " or ord(char) == 0x7F:
            raise LineError(f"contains a control character: {char!r}")


def check_utf8(line: str) -> None:
    """The entry must round-trip as UTF-8 text."""
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise LineError(f"not encodable as UTF-8: {exc}") from exc


CHECKS = (
    check_not_blank,
    check_no_surrounding_whitespace,
    check_single_line,
    check_length,
    check_printable,
    check_utf8,
)


def validate_line(line: str) -> str:
    """Run every named check; raise LineError naming the first failure."""
    if not isinstance(line, str):
        raise LineError(f"expected str, got {type(line).__name__}")
    for check in CHECKS:
        check(line)
    return line


def resolve_output_dir() -> str:
    """Output directory from MAKEFUN_OUTPUT_DIR, defaulting to /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)


def write_entry(line: str, out_dir: str) -> str:
    """Write the line (and nothing else) to <out_dir>/entry.txt.

    Writes to a temporary file in the same directory and renames it into
    place, so a failed run never leaves a half-written entry behind.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_NAME)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
    os.replace(tmp_path, path)
    return path


def main() -> int:
    try:
        validate_line(LINE)
    except LineError as exc:
        print(f"Invalid line: {exc}", file=sys.stderr)
        return 1
    print(LINE)
    path = write_entry(LINE, resolve_output_dir())
    print(f"Wrote {len(LINE)} characters to {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
