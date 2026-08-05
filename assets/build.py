from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

HERE = Path(__file__).parent

VERDE = "#2d717c"
AMBAR = "#f2c728"
ROJO = "#fe6565"
NAVY = "#0a132d"
WHITE = "#ffffff"

BARS = [(4, 18, 8, 8, VERDE), (12, 12, 8, 14, AMBAR), (20, 6, 8, 20, ROJO)]
DISPLAY_FONT = "C:/Windows/Fonts/georgiab.ttf"
BODY_FONT = "C:/Windows/Fonts/arial.ttf"
WORDMARK = "PreventIA"


def draw_mark(draw, origin_x, origin_y, scale):
    for x, y, w, h, colour in BARS:
        draw.rectangle(
            [origin_x + x * scale, origin_y + y * scale,
             origin_x + (x + w) * scale - 1, origin_y + (y + h) * scale - 1],
            fill=colour,
        )


def canvas(width, height, background):
    mode = "RGB" if background else "RGBA"
    fill = background or (0, 0, 0, 0)
    return Image.new(mode, (width, height), fill)


def mark_png(path, size, background, coverage=0.75):
    image = canvas(size, size, background)
    scale = size * coverage / 32
    offset = (size - 32 * scale) / 2
    draw_mark(ImageDraw.Draw(image), offset, offset, scale)
    image.save(HERE / path)
    return image


def lockup_layout(unit):
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    font = ImageFont.truetype(DISPLAY_FONT, max(1, int(unit * 18)))
    box = probe.textbbox((0, 0), WORDMARK, font=font)
    mark_scale = unit * 2.2
    mark_w = 32 * mark_scale
    gap, pad = unit * 6, unit * 6
    width = pad * 2 + mark_w + gap + (box[2] - box[0])
    height = max(mark_w, box[3] - box[1]) + pad * 2
    return font, box, mark_scale, mark_w, gap, pad, width, height


def lockup_image(target_width, background, ink):
    _, _, _, _, _, _, natural, _ = lockup_layout(100)
    unit = 100 * target_width / natural
    font, box, mark_scale, mark_w, gap, pad, width, height = lockup_layout(unit)
    text_h = box[3] - box[1]

    image = canvas(round(width), round(height), background)
    draw = ImageDraw.Draw(image)
    draw_mark(draw, pad, (height - 32 * mark_scale) / 2, mark_scale)
    draw.text((pad + mark_w + gap - box[0], (height - text_h) / 2 - box[1]),
              WORDMARK, font=font, fill=ink)
    return image, unit


def lockup_png(path, target_width, background, ink):
    image, _ = lockup_image(target_width, background, ink)
    image.save(HERE / path)
    return image


def card_png(path, width, height, background, ink):
    image = canvas(width, height, background)
    draw = ImageDraw.Draw(image)

    lockup, _ = lockup_image(round(width * 0.52), None, ink)
    sub = "Seguimiento entre controles"
    sub_font = ImageFont.truetype(BODY_FONT, round(width * 0.028))
    sub_box = draw.textbbox((0, 0), sub, font=sub_font)
    sub_w, sub_h = sub_box[2] - sub_box[0], sub_box[3] - sub_box[1]

    spacing = round(height * 0.05)
    block_h = lockup.height + spacing + sub_h
    top = round((height - block_h) / 2)

    image.paste(lockup, (round((width - lockup.width) / 2), top), lockup)
    draw.text(((width - sub_w) / 2 - sub_box[0], top + lockup.height + spacing - sub_box[1]),
              sub, font=sub_font, fill=ink)
    image.save(HERE / path)
    return image


def main():
    mark_png("whatsapp-profile.png", 640, NAVY, coverage=0.72)
    mark_png("icon-192.png", 192, WHITE)
    mark_png("icon-512.png", 512, WHITE)
    mark_png("icon-mask.png", 512, NAVY, coverage=0.78)
    mark_png("apple-touch-icon.png", 180, NAVY, coverage=0.68)

    master = Image.new("RGB", (48, 48), WHITE)
    scale = 48 * 0.96 / 32
    offset = (48 - 32 * scale) / 2
    draw_mark(ImageDraw.Draw(master), offset, offset, scale)
    master.save(HERE / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    lockup_png("logo-readme.png", 600, None, NAVY)
    lockup_png("logo-readme-dark.png", 600, None, WHITE)
    lockup_png("logo-1080.png", 1920, None, NAVY)
    lockup_png("logo-corner-1080.png", 600, None, NAVY)
    lockup_png("logo-4k.png", 3840, None, NAVY)
    lockup_png("logo-corner-4k.png", 1200, None, NAVY)

    card_png("og-image.png", 1200, 630, WHITE, NAVY)
    card_png("github-social-preview.png", 1280, 640, WHITE, NAVY)

    for f in sorted(HERE.glob("*.png")) + sorted(HERE.glob("*.ico")):
        with Image.open(f) as im:
            print(f"{f.name:32s} {im.size[0]:5d}x{im.size[1]:<5d} {f.stat().st_size / 1024:8.1f} KB")


if __name__ == "__main__":
    main()
