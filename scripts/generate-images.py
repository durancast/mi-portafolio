#!/usr/bin/env python3
"""
Genera las imágenes estáticas del portafolio con la paleta Witcher:
negro cálido (#0a0908), oro antiguo (#c9973f / #e3b45a) y vino tinto (#a13333).

- public/avatar.png  → placeholder circular del medallón (reemplazar por foto/memoji)
- public/og.png      → tarjeta Open Graph 1200×630

Uso: python3 scripts/generate-images.py
Requiere: pillow (pip install pillow)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

# Paleta (debe coincidir con @theme en src/styles/global.css)
INK = (10, 9, 8)  # zinc-950
LEATHER = (22, 19, 15)  # zinc-900
GOLD = (227, 180, 90)  # lumbre (gold-400)
CRIMSON = (200, 55, 45)  # carmesí de marca (accent-500)
CRIMSON_LIGHT = (224, 101, 90)  # accent-400
BONE = (233, 226, 211)  # hueso/pergamino (bone-100)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def radial(size, inner, outer, cx=0.5, cy=0.42):
    """Fondo con degradado radial (inner → outer)."""
    img = Image.new("RGB", size, outer)
    w, h = size
    glow = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(glow)
    radius = int(max(w, h) * 0.75)
    d.ellipse(
        (int(w * cx) - radius, int(h * cy) - radius,
         int(w * cx) + radius, int(h * cy) + radius),
        fill=255,
    )
    glow = glow.filter(ImageFilter.GaussianBlur(radius * 0.45))
    layer = Image.new("RGB", size, inner)
    img = Image.composite(layer, img, glow)
    return img


def grain(img, amount=6):
    """Grano sutil para romper el degradado plano."""
    import random

    random.seed(7)
    noise = Image.effect_noise(img.size, 24).convert("L")
    noise = noise.point(lambda v: 128 + (v - 128) * amount // 10)
    return Image.composite(
        img.point(lambda v: min(255, v + 6)),
        img,
        noise.point(lambda v: max(0, v - 128) * 2),
    )


def monogram(draw, cx, cy, size, font_path, text, color):
    font = ImageFont.truetype(font_path, size)
    box = draw.textbbox((0, 0), text, font=font)
    x = cx - (box[2] - box[0]) / 2 - box[0]
    y = cy - (box[3] - box[1]) / 2 - box[1]
    draw.text((x, y), text, font=font, fill=color)


def make_avatar():
    """Placeholder 512×512 del medallón (el CSS lo recorta en círculo)."""
    s = 512
    img = radial((s, s), (34, 28, 21), INK)
    img = grain(img)
    d = ImageDraw.Draw(img)

    # Anillo doble dorado (medallón)
    for inset, alpha, width in ((36, 90, 3), (52, 45, 1)):
        ring = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        rd = ImageDraw.Draw(ring)
        rd.ellipse((inset, inset, s - inset, s - inset), outline=GOLD + (alpha,), width=width)
        img.paste(ring, (0, 0), ring)

    # Monograma AD en hueso
    monogram(d, s // 2, s // 2 + 8, 190, FONT_BOLD, "AD", BONE)

    # Filo de espada carmesí bajo el monograma
    d.line((s * 0.36, s * 0.70, s * 0.64, s * 0.70), fill=CRIMSON_LIGHT + (200,), width=3)
    d.polygon(
        [(s * 0.485, s * 0.735), (s * 0.515, s * 0.735), (s * 0.5, s * 0.765)],
        fill=CRIMSON_LIGHT + (200,),
    )

    img.save(PUBLIC / "avatar.png", optimize=True)
    print("✓ public/avatar.png")


def make_og():
    """Tarjeta Open Graph 1200×630."""
    w, h = 1200, 630
    img = radial((w, h), (30, 25, 18), INK, cy=0.3)
    img = grain(img, amount=4)
    d = ImageDraw.Draw(img)

    # Rejilla técnica tenue
    grid = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    step = 56
    for x in range(0, w, step):
        gd.line((x, 0, x, h), fill=(63, 54, 45, 55), width=1)
    for y in range(0, h, step):
        gd.line((0, y, w, y), fill=(63, 54, 45, 55), width=1)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rectangle((0, 0, w, h * 0.85), fill=140)
    mask = mask.filter(ImageFilter.GaussianBlur(60))
    img.paste(Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB"), (0, 0), mask)
    d = ImageDraw.Draw(img)

    # Badge de estado (carmesí de marca)
    badge_font = ImageFont.truetype(FONT_MONO, 24)
    badge_text = "● Disponible para incorporación inmediata"
    bx, by = 96, 150
    box = d.textbbox((0, 0), badge_text, font=badge_font)
    bw, bh = box[2] - box[0] + 44, box[3] - box[1] + 26
    d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=999,
                        outline=CRIMSON + (200,), width=2, fill=(10, 9, 8, 220))
    d.text((bx + 22, by + 11), badge_text, font=badge_font, fill=CRIMSON_LIGHT)

    # Nombre (hueso)
    name_font = ImageFont.truetype(FONT_BOLD, 96)
    d.text((96, 226), "Alejandro Duran", font=name_font, fill=BONE)

    # Rol en mono carmesí
    role_font = ImageFont.truetype(FONT_MONO, 40)
    d.text((98, 356), "// Full-Stack Software Engineer", font=role_font, fill=CRIMSON_LIGHT)

    # Pitch corto
    pitch_font = ImageFont.truetype(FONT_MONO, 26)
    d.text((98, 424), "Arquitectura limpia · APIs tipadas · Producto con criterio",
           font=pitch_font, fill=(168, 158, 144))

    # Fila inferior: dominio + email
    foot_font = ImageFont.truetype(FONT_MONO, 28)
    d.text((98, 530), "durancast.dev", font=foot_font, fill=CRIMSON_LIGHT)
    dw = d.textbbox((0, 0), "durancast.dev", font=foot_font)[2]
    d.text((98 + dw + 28, 530), "· info@durancast.dev", font=foot_font, fill=(168, 158, 144))

    # Monograma medallón a la derecha (anillo ámbar, texto hueso)
    cx, cy, r = 990, 330, 150
    for inset, alpha, width in ((0, 90, 4), (26, 45, 2)):
        d.ellipse((cx - r + inset, cy - r + inset, cx + r - inset, cy + r - inset),
                  outline=GOLD + (alpha,), width=width)
    monogram(d, cx, cy + 10, 150, FONT_BOLD, "AD", BONE)

    img.save(PUBLIC / "og.png", optimize=True)
    print("✓ public/og.png")


if __name__ == "__main__":
    make_avatar()
    make_og()
