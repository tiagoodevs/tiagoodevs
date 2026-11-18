#!/usr/bin/env python3
import base64
from pathlib import Path

from build_cards import BG_BOTTOM, BG_TOP, MUTED, STROKE, TEXT

HERE = Path(__file__).resolve().parent
FONT_PATH = HERE / "fonts" / "Inter-Regular.woff2"

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
        'font-family="Inter"',
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
        '        font-family: "Inter";',
        "        font-style: normal;",
        "        font-weight: 200 800;",
        f'        src: url(data:font/woff2;base64,{font}) format("woff2");',
        "      }",
        "    ]]></style>",
        '    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">',
        f'      <stop offset="0" stop-color="{BG_TOP}"/>',
        f'      <stop offset="1" stop-color="{BG_BOTTOM}"/>',
        "    </linearGradient>",
        '    <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">',
        '      <circle cx="1.4" cy="1.4" r="1.2" fill="#ffffff" opacity="0.10"/>',
        "    </pattern>",
        "  </defs>",
        '  <g clip-path="url(#clip)">',
        f'    <rect width="{W}" height="{H}" rx="28" fill="url(#bg)"/>',
        f'    <rect width="{W}" height="{H}" fill="url(#dots)" opacity="0.35"/>',
    ]
    lines += [
        f'    <rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="27.5" '
        f'fill="none" stroke="{STROKE}" stroke-width="1.5"/>',
        "  </g>",
        text(74, 268, HEADLINE, 112, TEXT, 600, -4.4),
        text(80, 342, SUBHEAD, 27, SUBTLE, 400, -0.2),
    ]
    return f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title">
  <title id="title">{esc(HEADLINE)} — full-stack developer from 🇵🇹</title>
{chr(10).join(lines)}
</svg>
"""


def main() -> None:
    out = HERE / "banner.svg"
    out.write_text(build(), encoding="utf-8")
    print(f"wrote assets/banner.svg ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
