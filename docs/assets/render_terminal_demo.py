"""Run the README demo commands and render their real output as a PNG.

Usage: python3 docs/assets/render_terminal_demo.py
Needs Pillow (`pip install pillow`). Each command in COMMANDS is run from the
repository root and its output is drawn verbatim, so the picture can't drift
from what the code prints. Rerun it whenever the output changes.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "assets" / "terminal-demo.png"

COMMANDS = [
    "python3 demo/dispatch_demo.py",
    "python3 lab/mcp-matrix/tools/tally_seeds.py",
]
# (regex, hex colour) applied per line: red where the canary leaked, green where it held.
HIGHLIGHTS = [
    (r"canary_fired=True|^10/10", "#f07178"),
    (r"canary_fired=False|^ 0/10", "#98c379"),
]

BG, FG, PROMPT = "#1e1e1e", "#d4d4d4", "#e5c07b"
FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/Library/Fonts/Menlo.ttc",
    "C:/Windows/Fonts/consola.ttf",
]
SIZE, PAD, LINE = 15, 24, 21


def font() -> ImageFont.ImageFont:
    for path in FONTS:
        if Path(path).exists():
            return ImageFont.truetype(path, SIZE)
    return ImageFont.load_default(SIZE)


def run(cmd: str) -> list[str]:
    done = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True, check=True)
    return [line.rstrip() for line in done.stdout.splitlines()]


def colour(line: str) -> str:
    for pattern, hex_colour in HIGHLIGHTS:
        if re.search(pattern, line):
            return hex_colour
    return FG


def main() -> None:
    lines: list[tuple[str, str]] = []
    for cmd in COMMANDS:
        lines.append((f"$ {cmd}", PROMPT))
        lines.extend((text, colour(text)) for text in run(cmd))
    f = font()
    width = max(int(f.getlength(text)) for text, _ in lines) + 2 * PAD
    height = len(lines) * LINE + 2 * PAD + 18
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)
    for i, dot in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        draw.ellipse((PAD + i * 20, 12, PAD + i * 20 + 11, 23), fill=dot)
    y = PAD + 18
    for text, fill in lines:
        draw.text((PAD, y), text, font=f, fill=fill)
        y += LINE
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, optimize=True)
    print(f"wrote {OUT.relative_to(ROOT)} ({width}x{height})")


if __name__ == "__main__":
    main()
