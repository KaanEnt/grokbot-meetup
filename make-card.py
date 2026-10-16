#!/usr/bin/env python3
# Builds the LinkedIn card: the event cover on top, a strip below with the
# person's picture, name and one line, the way the Traction cards are laid out.
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
WIDTH = 1254
STRIP = 314
PAD = 72
AVATAR = 170
GAP = 40
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (140, 140, 140)


def font(file_name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(HERE / "assets" / file_name), size)


def circle(image: Image.Image, size: int) -> Image.Image:
    fitted = ImageOps.fit(image.convert("RGBA"), (size, size), Image.LANCZOS)
    oversampled = size * 4
    mask = Image.new("L", (oversampled, oversampled), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, oversampled - 1, oversampled - 1), fill=255)
    fitted.putalpha(mask.resize((size, size), Image.LANCZOS))
    return fitted


def shorten(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> str:
    if draw.textlength(text, font=fnt) <= max_width:
        return text
    while text and draw.textlength(text + "...", font=fnt) > max_width:
        text = text[:-1].rstrip()
    return text + "..."


# The one line gets two rows at most; anything longer is cut, not squeezed.
def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int, max_rows: int = 2) -> list[str]:
    rows: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=fnt) <= max_width:
            current = candidate
            continue
        if current:
            rows.append(current)
        current = word
        if len(rows) == max_rows - 1:
            rest = " ".join(text.split()[len(" ".join(rows).split()):])
            return rows + [shorten(draw, rest, fnt, max_width)]
    if current:
        rows.append(current)
    return rows[:max_rows]


def build(cover_path: Path, avatar_path: Path, name: str, line: str, out_path: Path) -> None:
    cover = ImageOps.fit(Image.open(cover_path).convert("RGB"), (WIDTH, WIDTH), Image.LANCZOS)
    card = Image.new("RGB", (WIDTH, WIDTH + STRIP), BLACK)
    card.paste(cover, (0, 0))

    avatar = circle(Image.open(avatar_path), AVATAR)
    avatar_y = WIDTH + (STRIP - AVATAR) // 2
    card.paste(avatar, (PAD, avatar_y), avatar)

    draw = ImageDraw.Draw(card)
    name_font = font("Inter-SemiBold.ttf", 60)
    line_font = font("Inter-Regular.ttf", 40)
    text_x = PAD + AVATAR + GAP
    max_width = WIDTH - text_x - PAD
    name_text = shorten(draw, name, name_font, max_width)
    line_rows = wrap(draw, line, line_font, max_width)
    name_height = name_font.getbbox(name_text)[3]
    row_height = line_font.getbbox("Ag")[3] + 8
    block_height = name_height + 16 + row_height * len(line_rows)
    top = WIDTH + (STRIP - block_height) // 2
    draw.text((text_x, top), name_text, font=name_font, fill=WHITE)
    y = top + name_height + 16
    for row in line_rows:
        draw.text((text_x, y), row, font=line_font, fill=GREY)
        y += row_height

    out_path.parent.mkdir(parents=True, exist_ok=True)
    card.save(out_path, "PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the event post card.")
    parser.add_argument("--cover", default=str(HERE / "assets" / "event-cover.png"))
    parser.add_argument("--avatar", required=True, help="the person's picture (GitHub avatar or X profile image)")
    parser.add_argument("--name", required=True)
    parser.add_argument("--line", required=True, help="one line on what they build")
    parser.add_argument("--out", default="card.png")
    args = parser.parse_args()
    build(Path(args.cover), Path(args.avatar), args.name, args.line, Path(args.out))
    print(args.out)


if __name__ == "__main__":
    main()
