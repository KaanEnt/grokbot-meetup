#!/usr/bin/env python3
# Composes the post the way LinkedIn's feed shows it: header, text, the card
# full width, then the action bar. A review image, so no invented counts.
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
WIDTH = 1080
PAD = 32
AVATAR = 96
INK = (0, 0, 0)
MUTED = (102, 102, 102)
LINE = (224, 224, 224)
FEED = (244, 242, 238)
WHITE = (255, 255, 255)


def font(file_name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(HERE / "assets" / file_name), size)


def circle(image: Image.Image, size: int) -> Image.Image:
    fitted = ImageOps.fit(image.convert("RGBA"), (size, size), Image.LANCZOS)
    oversampled = size * 4
    mask = Image.new("L", (oversampled, oversampled), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, oversampled - 1, oversampled - 1), fill=255)
    fitted.putalpha(mask.resize((size, size), Image.LANCZOS))
    return fitted


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    rows: list[str] = []
    for paragraph in text.strip().split("\n"):
        if not paragraph.strip():
            rows.append("")
            continue
        current = ""
        for word in paragraph.split():
            candidate = f"{current} {word}".strip()
            if draw.textlength(candidate, font=fnt) <= max_width:
                current = candidate
            else:
                rows.append(current)
                current = word
        rows.append(current)
    return rows


def action_icon(draw: ImageDraw.ImageDraw, kind: str, x: int, y: int) -> None:
    # Small line icons; close enough to read as the feed's bar.
    w = 3
    if kind == "like":
        draw.rounded_rectangle((x, y + 10, x + 8, y + 26), radius=2, outline=MUTED, width=w)
        draw.line((x + 10, y + 12, x + 16, y + 2, x + 20, y + 4, x + 18, y + 12, x + 26, y + 12, x + 24, y + 26, x + 10, y + 26), fill=MUTED, width=w, joint="curve")
    elif kind == "comment":
        draw.rounded_rectangle((x, y + 2, x + 26, y + 20), radius=6, outline=MUTED, width=w)
        draw.line((x + 6, y + 20, x + 6, y + 27, x + 13, y + 20), fill=MUTED, width=w)
    elif kind == "repost":
        draw.line((x + 2, y + 10, x + 20, y + 10, x + 14, y + 4), fill=MUTED, width=w)
        draw.line((x + 24, y + 18, x + 6, y + 18, x + 12, y + 24), fill=MUTED, width=w)
    elif kind == "share":
        draw.line((x + 2, y + 24, x + 10, y + 10, x + 24, y + 6), fill=MUTED, width=w)
        draw.line((x + 24, y + 6, x + 16, y + 4), fill=MUTED, width=w)
        draw.line((x + 24, y + 6, x + 22, y + 14), fill=MUTED, width=w)


def build(text: str, avatar_path: Path, name: str, headline: str, card_path: Path, out_path: Path) -> None:
    name_font = font("Inter-SemiBold.ttf", 30)
    meta_font = font("Inter-Regular.ttf", 26)
    body_font = font("Inter-Regular.ttf", 28)
    action_font = font("Inter-SemiBold.ttf", 26)
    line_height = 40

    probe = ImageDraw.Draw(Image.new("RGB", (WIDTH, 10)))
    rows = wrap(probe, text, body_font, WIDTH - 2 * PAD)
    card = Image.open(card_path).convert("RGB")
    card = card.resize((WIDTH, round(card.height * WIDTH / card.width)), Image.LANCZOS)

    header_h = PAD + AVATAR + 24
    text_h = len(rows) * line_height + 16
    bar_h = 96
    inner_h = header_h + text_h + card.height + bar_h
    canvas = Image.new("RGB", (WIDTH + 2 * 24, inner_h + 2 * 24), FEED)
    post = Image.new("RGB", (WIDTH, inner_h), WHITE)
    draw = ImageDraw.Draw(post)

    avatar = circle(Image.open(avatar_path), AVATAR)
    post.paste(avatar, (PAD, PAD), avatar)
    x = PAD + AVATAR + 16
    draw.text((x, PAD + 2), name, font=name_font, fill=INK)
    draw.text((x, PAD + 40), headline, font=meta_font, fill=MUTED)
    draw.text((x, PAD + 72), "1h", font=meta_font, fill=MUTED)
    draw.text((WIDTH - PAD - 36, PAD), "···", font=name_font, fill=MUTED)

    y = header_h
    for row in rows:
        if row:
            draw.text((PAD, y), row, font=body_font, fill=INK)
        y += line_height
    y += 16
    post.paste(card, (0, y))
    y += card.height
    draw.line((PAD, y + 1, WIDTH - PAD, y + 1), fill=LINE, width=2)

    slots = [("like", "Like"), ("comment", "Comment"), ("repost", "Repost"), ("share", "Share")]
    slot_w = WIDTH // len(slots)
    for i, (kind, label) in enumerate(slots):
        label_w = draw.textlength(label, font=action_font)
        total = 26 + 12 + label_w
        start = i * slot_w + (slot_w - total) // 2
        action_icon(draw, kind, int(start), y + 34)
        draw.text((start + 38, y + 32), label, font=action_font, fill=MUTED)

    canvas.paste(post, (24, 24))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, "PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview the post as a LinkedIn feed card.")
    parser.add_argument("--post", required=True, help="text file with the post, paragraphs separated by blank lines")
    parser.add_argument("--avatar", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--headline", required=True, help="their LinkedIn headline or the one line on what they build")
    parser.add_argument("--card", required=True, help="the card from make-card.py")
    parser.add_argument("--out", default="preview.png")
    args = parser.parse_args()
    build(Path(args.post).read_text(), Path(args.avatar), args.name, args.headline, Path(args.card), Path(args.out))
    print(args.out)


if __name__ == "__main__":
    main()
