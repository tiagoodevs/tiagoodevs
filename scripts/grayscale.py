#!/usr/bin/env python3
"""Desaturate the colours in a GitHub stats card SVG.

`github-readme-stats` colours the language dots and progress bar with each
language's brand colour, and there is no option to turn that off. This script
maps those colours to grayscale so the card stays black and white.

Usage: python3 scripts/grayscale.py profile/top-langs.svg
"""

import re
import sys

HEX = re.compile(r"#([0-9a-fA-F]{6})")


def to_gray(match: re.Match) -> str:
    value = match.group(1)
    r, g, b = int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
    # Already neutral: leave the card's own text/border colours alone.
    if max(r, g, b) - min(r, g, b) < 10:
        return match.group(0)
    lum = round(0.2126 * r + 0.7152 * g + 0.0722 * b)
    lum = max(110, min(230, lum))
    gray = f"{lum:02x}"
    return f"#{gray}{gray}{gray}"


def main() -> None:
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as f:
            svg = f.read()
        with open(path, "w", encoding="utf-8") as f:
            f.write(HEX.sub(to_gray, svg))


if __name__ == "__main__":
    main()
