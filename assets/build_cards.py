#!/usr/bin/env python3
"""Generates the bento cards in this folder.

GitHub strips CSS from READMEs, so the cards are plain SVG images that get
committed and referenced from README.md. Edit the CONTENT below and run:

    python3 assets/build_cards.py

The README expects these exact filenames.
"""

from pathlib import Path

# ---------------------------------------------------------------- design tokens

BG_TOP = "#1e2c24"
BG_BOTTOM = "#16211b"
STROKE = "#2f4a3b"
TEXT = "#f4f8f4"
BODY = "#b9ccbd"
MUTED = "#8fa798"
ACCENT = "#7fb08f"
WARM = "#e3c493"
PILL_BG = "#22322a"
PILL_STROKE = "#385545"
PILL_TEXT = "#dbe8dd"
DOT = "#6f9b7d"

FONT = "-apple-system, 'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MARGIN = 12
RADIUS = 20

# --------------------------------------------------------------------- content

ABOUT_LINES = [
    "five years building for the web — product features,",
    "discord integrations and a healthy dose of design.",
    "these days i'm shipping, keeping infra alive and",
    "reviewing prs across a few products i care about.",
]
ABOUT_FACTS = [
    ("BASED IN", "portugal"),
    ("EXPERIENCE", "5 years"),
    ("STUDYING", "multimedia"),
]

LEADING = [
    ("Paddlewheel", "COO"),
    ("Monitry", "Director"),
    ("Delivr", "Director"),
]
BUILDING = [
    ("Orbit", "HR SaaS"),
    ("Usercue", "feedback"),
    ("Boostify", "discord bot"),
]

STACK = [
    ("LANGUAGES", ["TypeScript", "JavaScript", "Python", "Go", "Rust", "PHP"]),
    ("FRONTEND", ["React", "Next.js", "Tailwind", "Angular"]),
    ("BACKEND & DATA", ["Node.js", "Prisma", "Postgres", "Supabase", "MongoDB", "Docker"]),
    ("TOOLING", ["Git", "GitHub", "VS Code", "Bun", "pnpm", "Arch"]),
]

OFF_CLOCK = [
    ("camera", "behind the lens", "if it's sunny, i'm outside"),
    ("headphones", "headphones on", "rainy days, code and music"),
    ("moon", "asleep by midnight", "non-negotiable"),
]

# --------------------------------------------------------------------- helpers


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def text(x, y, value, size=16, fill=BODY, weight=400, spacing=None, anchor=None, opacity=None):
    attrs = [
        f'x="{x}"',
        f'y="{y}"',
        f'font-family="{FONT}"',
        f'font-size="{size}"',
        f'font-weight="{weight}"',
        f'fill="{fill}"',
    ]
    if spacing is not None:
        attrs.append(f'letter-spacing="{spacing}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    return f"  <text {' '.join(attrs)}>{esc(value)}</text>"


def pill_width(label: str) -> float:
    return round(len(label) * 7.1 + 30, 1)


def pills(x, center_y, labels, gap=10):
    out = []
    cx = x
    for label in labels:
        w = pill_width(label)
        out.append(
            f'  <rect x="{cx}" y="{center_y - 16}" width="{w}" height="32" '
            f'rx="16" fill="{PILL_BG}" stroke="{PILL_STROKE}"/>'
        )
        out.append(
            text(cx + w / 2, center_y + 4.5, label, size=13, fill=PILL_TEXT, weight=500, anchor="middle")
        )
        cx += w + gap
    return out


def label(x, y, value, anchor=None):
    return text(x, y, value, size=10.5, fill=ACCENT, weight=700, spacing="1.8", anchor=anchor)


def wrap(width, height, body):
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title">
  <title id="title">{esc(body.pop('title'))}</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{BG_TOP}"/>
      <stop offset="1" stop-color="{BG_BOTTOM}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{WARM}" stop-opacity="0.16"/>
      <stop offset="1" stop-color="{WARM}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="cardClip">
      <rect x="{MARGIN}" y="{MARGIN}" width="{width - 2 * MARGIN}" height="{height - 2 * MARGIN}" rx="{RADIUS}"/>
    </clipPath>
  </defs>
{chr(10).join(body['lines'])}
</svg>
"""


def card_rect(w, h):
    return (
        f'  <rect x="{MARGIN}" y="{MARGIN}" width="{w - 2 * MARGIN}" height="{h - 2 * MARGIN}" '
        f'rx="{RADIUS}" fill="url(#bg)" stroke="{STROKE}"/>'
    )


def spark(cx, cy, r, fill=WARM, opacity=1.0):
    d = (
        f"M {cx} {cy - r} "
        f"Q {cx + r * 0.16} {cy - r * 0.16} {cx + r} {cy} "
        f"Q {cx + r * 0.16} {cy + r * 0.16} {cx} {cy + r} "
        f"Q {cx - r * 0.16} {cy + r * 0.16} {cx - r} {cy} "
        f"Q {cx - r * 0.16} {cy - r * 0.16} {cx} {cy - r} Z"
    )
    return f'  <path d="{d}" fill="{fill}" opacity="{opacity}"/>'


def arcs(cx, cy):
    out = []
    for i, r in enumerate((58, 86, 114)):
        out.append(
            f'  <path d="M {cx - r} {cy} A {r} {r} 0 0 1 {cx} {cy - r}" '
            f'stroke="{WARM}" stroke-opacity="{0.20 - i * 0.05:.2f}" stroke-width="1.2" fill="none"/>'
        )
    return out


def decor(cx, cy, radius=132):
    lines = ['  <g clip-path="url(#cardClip)">']
    lines.append(f'    <circle cx="{cx}" cy="{cy}" r="{radius}" fill="url(#glow)"/>')
    lines.extend("  " + line for line in arcs(cx, cy))
    lines.append("  </g>")
    return lines


# ----------------------------------------------------------------------- cards


def about_card():
    w, h = 630, 420
    body = {
        "title": "About Tiago, full-stack developer from Portugal",
        "lines": [
            card_rect(w, h),
            *decor(556, 76),
            label(44, 64, "FULL-STACK DEVELOPER"),
            label(w - 44, 64, "PORTUGAL", anchor="end"),
            text(44, 138, "hey, i'm tiago", size=46, fill=TEXT, weight=700, spacing="-0.5"),
            spark(378, 118, 12),
            *[text(44, 188 + i * 28, line, size=16.5) for i, line in enumerate(ABOUT_LINES)],
            f'  <line x1="44" y1="308" x2="{w - 44}" y2="308" stroke="{STROKE}"/>',
            *[
                part
                for i, (cap, value) in enumerate(ABOUT_FACTS)
                for part in (
                    label(44 + i * 190, 340, cap),
                    text(44 + i * 190, 370, value, size=19, fill=TEXT, weight=600),
                )
            ],
        ],
    }
    return wrap(w, h, body)


def currently_card():
    w, h = 420, 420
    lines = [
        card_rect(w, h),
        label(44, 64, "CURRENTLY"),
        text(44, 112, "wearing a few hats", size=25, fill=TEXT, weight=600, spacing="-0.3"),
        label(44, 154, "LEADING"),
    ]
    y = 186
    for name, role in LEADING:
        lines.append(f'  <circle cx="48" cy="{y - 5}" r="3" fill="{DOT}"/>')
        lines.append(text(62, y, name, size=16, fill=TEXT, weight=600))
        lines.append(text(w - 44, y, role, size=12, fill=MUTED, anchor="end"))
        y += 34
    lines.append(f'  <line x1="44" y1="284" x2="{w - 44}" y2="284" stroke="{STROKE}"/>')
    lines.append(label(44, 312, "BUILDING"))
    y = 344
    for name, role in BUILDING:
        lines.append(f'  <circle cx="48" cy="{y - 5}" r="3" fill="{DOT}" opacity="0.55"/>')
        lines.append(text(62, y, name, size=15.5, fill=TEXT, weight=600))
        lines.append(text(w - 44, y, role, size=12, fill=MUTED, anchor="end"))
        y += 30
    body = {"title": "What Tiago is working on", "lines": lines}
    return wrap(w, h, body)


def stack_card():
    w, h = 880, 320
    lines = [
        card_rect(w, h),
        label(44, 62, "STACK"),
        text(w - 44, 62, "the short list", size=12.5, fill=MUTED, anchor="end"),
    ]
    centers = (116, 172, 228, 284)
    for (cap, items), cy in zip(STACK, centers):
        lines.append(label(44, cy + 4, cap))
        lines.extend(pills(196, cy, items))
    body = {"title": "Tiago's tech stack", "lines": lines}
    return wrap(w, h, body)


def icon(kind, cx, cy):
    if kind == "camera":
        return [
            f'  <rect x="{cx - 9}" y="{cy - 5}" width="18" height="13" rx="3" stroke="{ACCENT}" stroke-width="1.6"/>',
            f'  <path d="M {cx - 4} {cy - 5} l 1.6 -2.6 h 4.8 l 1.6 2.6" stroke="{ACCENT}" stroke-width="1.6" fill="none"/>',
            f'  <circle cx="{cx}" cy="{cy + 1.5}" r="3.4" stroke="{ACCENT}" stroke-width="1.6"/>',
        ]
    if kind == "headphones":
        return [
            f'  <path d="M {cx - 8} {cy + 3} v -3 a 8 8 0 0 1 16 0 v 3" stroke="{ACCENT}" stroke-width="1.6" fill="none"/>',
            f'  <rect x="{cx - 10}" y="{cy + 2}" width="4.6" height="7.5" rx="2.2" stroke="{ACCENT}" stroke-width="1.6"/>',
            f'  <rect x="{cx + 5.4}" y="{cy + 2}" width="4.6" height="7.5" rx="2.2" stroke="{ACCENT}" stroke-width="1.6"/>',
        ]
    return [
        f'  <path d="M {cx + 3.9} {cy - 7} A 8 8 0 1 0 {cx + 3.9} {cy + 7} A 7 7 0 0 1 {cx + 3.9} {cy - 7} Z" fill="{ACCENT}" stroke="{ACCENT}" stroke-width="1.2" stroke-linejoin="round"/>',
    ]


def offclock_card():
    w, h = 400, 320
    lines = [
        card_rect(w, h),
        label(44, 60, "OFF THE CLOCK"),
        *decor(w - 40, 70, 120),
    ]
    y = 120
    for kind, title, sub in OFF_CLOCK:
        lines.append(
            f'  <circle cx="62" cy="{y - 6}" r="20" fill="{PILL_BG}" stroke="{PILL_STROKE}"/>'
        )
        lines.extend(icon(kind, 62, y - 6))
        lines.append(text(100, y - 2, title, size=15.5, fill=TEXT, weight=600))
        lines.append(text(100, y + 20, sub, size=12.5, fill=MUTED))
        y += 70
    body = {"title": "Tiago outside of work", "lines": lines}
    return wrap(w, h, body)


def talk_card():
    w, h = 600, 320
    lines = [
        card_rect(w, h),
        *decor(516, 80, 130),
        label(44, 60, "LET'S BUILD SOMETHING"),
        text(44, 132, "got an idea, a bug,", size=32, fill=TEXT, weight=700, spacing="-0.4"),
        text(44, 172, "or just want to talk shop?", size=32, fill=TEXT, weight=700, spacing="-0.4"),
        text(44, 214, "collabs, products and infra chats are always welcome.", size=14),
        f'  <line x1="44" y1="248" x2="{w - 44}" y2="248" stroke="{STROKE}"/>',
        text(44, 284, "tiagodevs.net", size=18, fill=ACCENT, weight=600),
        f'  <path d="M 178 278 h 30 m -8 -6 l 8 6 l -8 6" stroke="{ACCENT}" stroke-width="1.6" fill="none"/>',
        text(w - 44, 284, "discord · email", size=12.5, fill=MUTED, anchor="end"),
    ]
    body = {"title": "Get in touch with Tiago", "lines": lines}
    return wrap(w, h, body)


def main():
    out = Path(__file__).resolve().parent
    cards = {
        "card-about.svg": about_card,
        "card-currently.svg": currently_card,
        "card-stack.svg": stack_card,
        "card-offclock.svg": offclock_card,
        "card-talk.svg": talk_card,
    }
    for name, builder in cards.items():
        (out / name).write_text(builder(), encoding="utf-8")
        print(f"wrote assets/{name}")


if __name__ == "__main__":
    main()
