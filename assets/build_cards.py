#!/usr/bin/env python3
from pathlib import Path

BG = "#0d0d0d"
STROKE = "#2a2a2a"
TEXT = "#fafafa"
BODY = "#b8b8b8"
MUTED = "#8a8a8a"
ACCENT = "#cfcfcf88"
GLOW = "#ffffff"
PILL_BG = "#161616"
PILL_STROKE = "#333333"
PILL_TEXT = "#e6e6e6"
DOT = "#c7c7c7"

FONT = "Inter, -apple-system, 'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif" # based on system fonts, download if you dont have the font
MARGIN = 12
RADIUS = 20

ABOUT_LINES = [
    "five years building for the web, such as, product features,",
    "discord integrations and a healthy dose of design.",
    "these days i'm shipping, keeping infra alive and",
    "reviewing prs across a few products i care about.",
]
ABOUT_FACTS = [
    ("BASED IN", "🇵🇹"),
    ("EXPERIENCE", "5 years"),
    ("STUDYING", "multimedia"),
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
            f'rx="8" fill="{PILL_BG}" stroke="{PILL_STROKE}"/>'
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
        f'rx="{RADIUS}" fill="{BG}" stroke="{STROKE}"/>'
    )


def spark(cx, cy, r, fill=GLOW, opacity=1.0):
    d = (
        f"M {cx} {cy - r} "
        f"Q {cx + r * 0.16} {cy - r * 0.16} {cx + r} {cy} "
        f"Q {cx + r * 0.16} {cy + r * 0.16} {cx} {cy + r} "
        f"Q {cx - r * 0.16} {cy + r * 0.16} {cx - r} {cy} "
        f"Q {cx - r * 0.16} {cy - r * 0.16} {cx} {cy - r} Z"
    )
    return f'  <path d="{d}" fill="{fill}" opacity="{opacity}"/>'



def decor(cx, cy, radius=132):
    lines = ['  <g clip-path="url(#cardClip)">']
    lines.append(f'    <circle cx="{cx}" cy="{cy}" r="{radius}" fill="url(#glow)"/>')
    lines.extend("  " + line for line in arcs(cx, cy))
    lines.append("  </g>")
    return lines

def about_card():
    w, h = 630, 350
    body = {
        "title": "About Tiago, full-stack developer from Portugal",
        "lines": [
            card_rect(w, h),
            text(44, 92, "👋 I'm Tiago", size=46, fill=TEXT, weight=700, spacing="-0.5"),
            *[text(44, 140 + i * 28, line, size=16.5) for i, line in enumerate(ABOUT_LINES)],
            f'  <line x1="44" y1="240" x2="{w - 44}" y2="240" stroke="{STROKE}"/>',
            *[
                part
                for i, (cap, value) in enumerate(ABOUT_FACTS)
                for part in (
                    label(44 + i * 180, 270, cap),
                    text(44 + i * 180, 300, value, size=19, fill=TEXT, weight=600),
                )
            ],
        ],
    }
    return wrap(w, h, body)



def stack_card():
    w, h = 880, 360
    lines = [
        card_rect(w, h),
        text(44, 62, "Tools I use", 24),
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
    w, h = 450, 350
    lines = [
        card_rect(w, h),
        label(44, 60, "OFF THE CLOCK"),
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
    w, h = 900, 320
    lines = [
        card_rect(w, h),
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
        "card-stack.svg": stack_card,
        "card-offclock.svg": offclock_card,
        "card-talk.svg": talk_card,
    }
    for name, builder in cards.items():
        (out / name).write_text(builder(), encoding="utf-8")
        print(f"wrote assets/{name}")


if __name__ == "__main__":
    main()
