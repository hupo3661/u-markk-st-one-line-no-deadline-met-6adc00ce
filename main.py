#!/usr/bin/env python3
"""Write one original one-line text to /output/entry.txt.

a joke excusing a missed deadline: the calendar takes legal action and the to-do list stops answering. Standard library only, no network, no input files.
"""

import os

LINE = (
    "I missed the deadline so hard the calendar filed a restraining order and my to-do list started ghosting me."
)


def main() -> None:
    if not LINE.strip():
        raise SystemExit("Invalid line: must be non-empty after stripping.")
    if "\n" in LINE or "\r" in LINE:
        raise SystemExit("Invalid line: must be a single line with no newline characters.")
    if len(LINE) > 200:
        raise SystemExit("Invalid line: exceeds the competition's character limit.")
    print(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)


if __name__ == "__main__":
    main()
