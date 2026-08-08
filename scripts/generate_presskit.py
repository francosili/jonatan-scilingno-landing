# -*- coding: utf-8 -*-
"""Generates the Jonatan Scilingno press kit / technical rider PDF."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
PRESS = os.path.join(ASSETS, "press")
OUT = os.path.join(PRESS, "Jonatan-Scilingno-PressKit.pdf")

PAGE_W, PAGE_H = A4
MARGIN = 44

BG = (10/255, 10/255, 10/255)
FG = (0.96, 0.95, 0.94)
MUTED = (0.64, 0.64, 0.63)
LINE = (0.24, 0.24, 0.24)

LOGO = os.path.join(ASSETS, "logo-crop.png")
COVER_PHOTO = os.path.join(PRESS, "web-press-04.jpg")
PHOTOS = [
    os.path.join(PRESS, "web-press-01.jpg"),
    os.path.join(PRESS, "web-press-02.jpg"),
    os.path.join(PRESS, "web-press-03.jpg"),
    os.path.join(PRESS, "web-press-04.jpg"),
]

c = canvas.Canvas(OUT, pagesize=A4)


def bg_fill():
    c.setFillColorRGB(*BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


def draw_image_cover(path, x, y, w, h):
    """Draw image covering the given box (crop to fill, like CSS object-fit: cover)."""
    img = ImageReader(path)
    iw, ih = img.getSize()
    box_ratio = w / h
    img_ratio = iw / ih
    if img_ratio > box_ratio:
        draw_h = h
        draw_w = h * img_ratio
        offset_x = x - (draw_w - w) / 2
        offset_y = y
    else:
        draw_w = w
        draw_h = w / img_ratio
        offset_x = x
        offset_y = y - (draw_h - h) / 2
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(img, offset_x, offset_y, draw_w, draw_h)
    c.restoreState()


def eyebrow(text, x, y, color=MUTED, size=9):
    c.setFont("Helvetica-Bold", size)
    c.setFillColorRGB(*color)
    c.drawString(x, y, text.upper())


def footer(page_label):
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(*MUTED)
    c.drawString(MARGIN, 26, "JONATAN SCILINGNO — PRESS KIT")
    c.drawRightString(PAGE_W - MARGIN, 26, page_label)


def header_logo():
    img = ImageReader(LOGO)
    iw, ih = img.getSize()
    target_h = 14
    target_w = target_h * (iw / ih)
    c.drawImage(img, MARGIN, PAGE_H - MARGIN - target_h + 4, target_w, target_h, mask='auto')


def wrap_text(text, font, size, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_paragraph(text, x, y, max_width, size=10.5, leading=16, color=FG, font="Helvetica"):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    lines = wrap_text(text, font, size, max_width)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


# ---------------------------------------------------------------
# PAGE 1 — COVER
# ---------------------------------------------------------------
bg_fill()
photo_h = PAGE_H * 0.62
draw_image_cover(COVER_PHOTO, 0, PAGE_H - photo_h, PAGE_W, photo_h)

# dark gradient-ish scrim at bottom of photo using stacked translucent rects
c.saveState()
steps = 24
scrim_h = 170
for i in range(steps):
    frac = i / steps
    alpha = frac * 0.92
    c.setFillColorRGB(*BG, alpha=alpha)
    yy = PAGE_H - photo_h + scrim_h - (scrim_h / steps) * (i + 1)
    c.rect(0, yy, PAGE_W, scrim_h / steps + 1, fill=1, stroke=0)
c.restoreState()

# lower dark block
c.setFillColorRGB(*BG)
c.rect(0, 0, PAGE_W, PAGE_H - photo_h, fill=1, stroke=0)

# logo
logo_img = ImageReader(LOGO)
iw, ih = logo_img.getSize()
logo_w = PAGE_W - MARGIN * 2
logo_h = logo_w * (ih / iw)
if logo_h > 70:
    logo_h = 70
    logo_w = logo_h * (iw / ih)
c.drawImage(logo_img, MARGIN, PAGE_H - photo_h - 10, logo_w, logo_h, mask='auto')

c.setFont("Helvetica", 12)
c.setFillColorRGB(*FG)
c.drawString(MARGIN, PAGE_H - photo_h - 34, "DJ & Productor — House · Deep House · Dub Techno · Progressive")

c.setFont("Helvetica", 10)
c.setFillColorRGB(*MUTED)
c.drawString(MARGIN, PAGE_H - photo_h - 52, "Rosario, Argentina")

c.setFont("Helvetica-Bold", 10)
c.setFillColorRGB(*MUTED)
c.drawString(MARGIN, 90, "PRESS KIT / EPK")
c.setFont("Helvetica", 9)
c.drawString(MARGIN, 74, "instagram.com/jonatan.es  ·  soundcloud.com/jonatanscilingno  ·  mixcloud.com/jonatanscilingno")

footer("01")
c.showPage()

# ---------------------------------------------------------------
# PAGE 2 — BIO
# ---------------------------------------------------------------
bg_fill()
header_logo()

y = PAGE_H - 130
eyebrow("Sobre mí", MARGIN, y)
y -= 26
c.setFont("Helvetica-Bold", 26)
c.setFillColorRGB(*FG)
c.drawString(MARGIN, y, "Sets que no se")
y -= 30
c.drawString(MARGIN, y, "encasillan en un")
y -= 30
c.drawString(MARGIN, y, "solo género.")

col_x = PAGE_W / 2 - 10
col_w = PAGE_W / 2 - MARGIN - 10
yy = PAGE_H - 130

bio_paragraphs = [
    "Jonatan Scilingno es DJ y productor de Rosario, Argentina, con una marcada influencia de artistas como John Digweed, Dixon y Guy J. Inició su carrera en 2018, formándose en CETEAR, donde consolidó sus habilidades como productor y DJ.",
    "A lo largo de su trayectoria compartió cabina con referentes como Kasper Koman, Blancah, Kevin Di Serna, Alejo González, Brigado Crew, Analog Jungs, Fernando Ferreyra, Marcelo Vasami, Ostil y Joan Retamero, presentándose tanto en distintos espacios de Rosario como fuera de la ciudad.",
    "Se distingue por no encasillarse en un solo género, construyendo sets que fluyen entre distintos estilos con un sello propio y una sensibilidad sonora que atrapa a la audiencia. Su música combina técnica, emotividad y una propuesta versátil que lo posiciona como uno de los talentos destacados de la escena electrónica local.",
]
for para in bio_paragraphs:
    yy = draw_paragraph(para, col_x, yy, col_w, size=10, leading=15)
    yy -= 12

# tags
yy -= 6
tags = ["House", "Deep House", "Dub Techno", "Progressive"]
tx = col_x
c.setFont("Helvetica-Bold", 9)
for tag in tags:
    tw = stringWidth(tag.upper(), "Helvetica-Bold", 9) + 20
    c.setStrokeColorRGB(*LINE)
    c.setFillColorRGB(*BG)
    c.roundRect(tx, yy, tw, 22, 11, fill=1, stroke=1)
    c.setFillColorRGB(*FG)
    c.drawString(tx + 10, yy + 7, tag.upper())
    tx += tw + 8
    if tx > col_x + col_w - 40:
        tx = col_x
        yy -= 30

# shared booth
yy -= 46
c.setStrokeColorRGB(*LINE)
c.line(col_x, yy, col_x + col_w, yy)
yy -= 18
eyebrow("Compartió cabina con", col_x, yy, size=8.5)
yy -= 20
names = ["Kasper Koman", "Blancah", "Kevin Di Serna", "Alejo González", "Brigado Crew",
         "Analog Jungs", "Fernando Ferreyra", "Marcelo Vasami", "Ostil", "Joan Retamero"]
c.setFont("Helvetica-Bold", 10.5)
c.setFillColorRGB(*FG)
nx = col_x
for i, name in enumerate(names):
    nw = stringWidth(name.upper(), "Helvetica-Bold", 10.5)
    if nx + nw > col_x + col_w:
        nx = col_x
        yy -= 18
    c.drawString(nx, yy, name.upper())
    nx += nw + 14
    c.setFillColorRGB(*MUTED)
    c.drawString(nx - 10, yy, "·")
    c.setFillColorRGB(*FG)

footer("02")
c.showPage()

# ---------------------------------------------------------------
# PAGE 3 — FOTOS
# ---------------------------------------------------------------
bg_fill()
header_logo()

y = PAGE_H - 130
eyebrow("Fotos de prensa", MARGIN, y)
y -= 26
c.setFont("Helvetica-Bold", 22)
c.setFillColorRGB(*FG)
c.drawString(MARGIN, y, "Material fotográfico")

grid_top = y - 30
gap = 14
caption_zone = 46  # room for caption + footer below the grid
grid_bottom_limit = 60
available_h = grid_top - grid_bottom_limit - caption_zone
cell_w = (PAGE_W - MARGIN * 2 - gap) / 2
cell_h = (available_h - gap) / 2
positions = [
    (MARGIN, grid_top - cell_h),
    (MARGIN + cell_w + gap, grid_top - cell_h),
    (MARGIN, grid_top - cell_h * 2 - gap),
    (MARGIN + cell_w + gap, grid_top - cell_h * 2 - gap),
]
for path, (px, py) in zip(PHOTOS, positions):
    draw_image_cover(path, px, py, cell_w, cell_h)

bottom_y = positions[-1][1] - 24
c.setFont("Helvetica", 8.5)
c.setFillColorRGB(*MUTED)
c.drawString(MARGIN, bottom_y, "Fotos en alta resolución disponibles a pedido — contacto en la última página.")

footer("03")
c.showPage()

# ---------------------------------------------------------------
# PAGE 4 — RIDER TECNICO
# ---------------------------------------------------------------
bg_fill()
header_logo()

y = PAGE_H - 130
eyebrow("Rider técnico", MARGIN, y)
y -= 26
c.setFont("Helvetica-Bold", 22)
c.setFillColorRGB(*FG)
c.drawString(MARGIN, y, "Especificaciones técnicas")
y -= 44

sections = [
    ("01", "Equipo de cabina (DJ Booth)", [
        "3 o más reproductores CDJ, el modelo más actualizado disponible.",
        "Equipos en perfecto estado y con firmware actualizado.",
    ]),
    ("02", "Mixer", [
        "Preferentemente Pioneer DJM.",
        "Se acepta Allen & Heath (línea Xone / PX5) como alternativa.",
    ]),
    ("03", "Software y formato", [
        "Rekordbox.",
        "Reproducción desde USB — el DJ provee su propio pendrive.",
    ]),
    ("04", "Audio en cabina", [
        "Monitoreo de booth recomendado, con control de volumen accesible desde la cabina.",
        "No se requiere micrófono en cabina.",
    ]),
    ("05", "Alimentación eléctrica", [
        "Estándar 220V / 50Hz — sin requisitos especiales.",
    ]),
    ("06", "Soundcheck", [
        "Se solicita, preferentemente antes del show y sin público presente.",
    ]),
]

for num, title, lines in sections:
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(*MUTED)
    c.drawString(MARGIN, y, num)
    c.setFillColorRGB(*FG)
    c.drawString(MARGIN + 26, y, title.upper())
    y -= 16
    for line in lines:
        c.setFont("Helvetica", 9.5)
        c.setFillColorRGB(*MUTED)
        c.drawString(MARGIN + 26, y, "–  " + line)
        y -= 14
    y -= 12

footer("04")
c.showPage()

# ---------------------------------------------------------------
# PAGE 5 — CONTACTO
# ---------------------------------------------------------------
bg_fill()
header_logo()

y = PAGE_H - 130
eyebrow("Contacto técnico y bookings", MARGIN, y)
y -= 26
c.setFont("Helvetica-Bold", 22)
c.setFillColorRGB(*FG)
c.drawString(MARGIN, y, "Jonatan Scilingno")
y -= 40

contact_lines = [
    ("Email", "Jonatan.sc2726@gmail.com"),
    ("WhatsApp", "+54 9 3413 65-0722"),
    ("Instagram", "@jonatan.es"),
    ("SoundCloud", "soundcloud.com/jonatanscilingno"),
    ("Mixcloud", "mixcloud.com/jonatanscilingno"),
]
for label, value in contact_lines:
    c.setFont("Helvetica-Bold", 9)
    c.setFillColorRGB(*MUTED)
    c.drawString(MARGIN, y, label.upper())
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(*FG)
    c.drawString(MARGIN + 110, y, value)
    y -= 26

y -= 20
c.setStrokeColorRGB(*LINE)
c.line(MARGIN, y, PAGE_W - MARGIN, y)
y -= 24

c.setFont("Helvetica-Bold", 9)
c.setFillColorRGB(*MUTED)
c.drawString(MARGIN, y, "AGENDA")
y -= 18
y = draw_paragraph(
    "Agenda de próximas fechas y disponibilidad actualizada en Instagram @jonatan.es.",
    MARGIN, y, PAGE_W - MARGIN * 2, size=10, leading=15
)

y -= 30
c.setFont("Helvetica-Oblique", 8.5)
c.setFillColorRGB(*MUTED)
c.drawString(MARGIN, y, "Rider sujeto a revisión según las características técnicas de cada evento.")

footer("05")
c.showPage()

c.save()
print("PDF generado en:", OUT)
