#!/usr/bin/env python3
"""Generates the monochrome profile banner.

The banner is an SVG so it stays crisp at any width, which means the typeface
has to travel with it: Plus Jakarta Sans is embedded as a base64 woff2 in an
@font-face rule (browsers will not fetch external files from an SVG used as an
image). Edit the copy below and run:

    python3 assets/build_banner.py

The font is licensed under the SIL Open Font License; see assets/fonts/OFL.txt.
"""

import base64
from pathlib import Path

from build_cards import BG_BOTTOM, BG_TOP, MUTED, STROKE, TEXT

HERE = Path(__file__).resolve().parent
FONT_PATH = HERE / "fonts" / "PlusJakartaSans.woff2"

W, H = 1600, 420
KICKER = "#bdbdbd"
SUBTLE = "#9a9a9a"
FAINT = "#8a8a8a"

HEADLINE = "build, test, and ship."
SUBHEAD = "web apps, discord integrations and the infra in between."


def esc(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, value, size, fill, weight=400, spacing=0, anchor=None):
    attrs = [
        f'x="{x}"',
        f'y="{y}"',
        'font-family="Plus Jakarta Sans"',
        f'font-size="{size}"',
        f'font-weight="{weight}"',
        f'fill="{fill}"',
    ]
    if spacing:
        attrs.append(f'letter-spacing="{spacing}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    return f'  <text {" ".join(attrs)}>{esc(value)}</text>'


def build():
    font = base64.b64encode(FONT_PATH.read_bytes()).decode()
    lines = [
        "  <defs>",
        '    <style type="text/css"><![CDATA[',
        "      @font-face {",
        '        font-family: "Plus Jakarta Sans";',
        "        font-style: normal;",
        "        font-weight: 200 800;",
        f'        src: url(data:font/woff2;base64,{font}) format("woff2");',
        "      }",
        "    ]]></style>",
        '    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">',
        f'      <stop offset="0" stop-color="{BG_TOP}"/>',
        f'      <stop offset="1" stop-color="{BG_BOTTOM}"/>',
        "    </linearGradient>",
        '    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">',
        '      <stop offset="0" stop-color="#ffffff" stop-opacity="0.09"/>',
        '      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>',
        "    </radialGradient>",
        f'    <clipPath id="clip"><rect width="{W}" height="{H}" rx="28"/></clipPath>',
        '    <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">',
        '      <circle cx="1.4" cy="1.4" r="1.2" fill="#ffffff" opacity="0.10"/>',
        "    </pattern>",
        "  </defs>",
        '  <g clip-path="url(#clip)">',
        f'    <rect width="{W}" height="{H}" rx="28" fill="url(#bg)"/>',
        f'    <rect width="{W}" height="{H}" fill="url(#dots)" opacity="0.35"/>',
        '    <circle cx="1420" cy="70" r="300" fill="url(#glow)"/>',
    ]
    for i, r in enumerate((120, 190, 260, 330)):
        lines.append(
            f'    <path d="M {1500 - r} 60 A {r} {r} 0 0 1 1500 {60 - r}" '
            f'stroke="#ffffff" stroke-opacity="{0.16 - i * 0.03:.2f}" stroke-width="1.3" fill="none"/>'
        )
    lines += [
        f'    <rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="27.5" '
        f'fill="none" stroke="{STROKE}" stroke-width="1.5"/>',
        "  </g>",
        text(80, 96, "FULL-STACK DEVELOPER", 19, KICKER, 700, 3.4),
        text(W - 80, 96, "PORTO, PORTUGAL", 19, MUTED, 600, 2.4, "end"),
        text(74, 268, HEADLINE, 112, TEXT, 800, -4.4),
        text(80, 342, SUBHEAD, 27, SUBTLE, 400, -0.2),
        f'  <line x1="80" y1="372" x2="{W - 80}" y2="372" stroke="#242424"/>',
        text(80, 402, "5 years experience", 19, FAINT, 500, 0.9),
        text(W / 2, 402, "41.16° N · 8.63° W", 19, FAINT, 500, 1.0, "middle"),
        text(W - 80, 402, "tiagodevs.net", 18, SUBTLE, 600, 0.6, "end"),
    ]
    return f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title">
  <title id="title">{esc(HEADLINE)} — full-stack developer from Porto, Portugal</title>
{chr(10).join(lines)}
</svg>
"""


def main() -> None:
    out = HERE / "banner.svg"
    out.write_text(build(), encoding="utf-8")
    print(f"wrote assets/banner.svg ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
