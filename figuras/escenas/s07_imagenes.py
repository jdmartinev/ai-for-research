"""S07 — Multimodal: una imagen se vuelve una frase de parches (diapositiva 7).

La imagen se recorta a 448 × 448 y se parte en 14 × 14 = 196 parches de 32 px (como un ViT).
Cada parche se dibuja con su color promedio y entra a la misma secuencia que el texto.
Si existe input.jpg (o input.png) se usa esa imagen; si no, se genera una figura sintética de marcha.
manim -r 1920,720 --fps 30 s07_imagenes.py Imagenes
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from manim import (Arrow, Scene, VGroup, ImageMobject, Square, Line, Rectangle, Brace, FadeIn, FadeOut, Create,
                   LaggedStart, Group, LEFT, RIGHT, UP, DOWN, BOLD)
from common import *

HERE = Path(__file__).resolve().parent
N, PX = 14, 448


def synthetic_gait():
    """Cuatro fases de la marcha dibujadas a mano (piernas en dos tonos), fondo claro."""
    im = Image.new("RGB", (PX, PX), "#D9E0E8")
    d = ImageDraw.Draw(im)
    for y in range(PX):  # degradado suave
        c = int(226 - 28 * y / PX)
        d.line([(0, y), (PX, y)], fill=(c, c + 4, c + 10))
    ground = 372
    d.rectangle([0, ground, PX, PX], fill="#8E9AA8")
    # (ángulo cadera-rodilla, rodilla-tobillo) de cada pierna, en grados desde la vertical
    phases = [((25, 5), (-20, -35)), ((5, 0), (-5, -60)), ((-15, -10), (30, 10)), ((-25, -40), (20, 5))]
    for k, (front, back) in enumerate(phases):
        cx, hip = 78 + k * 100, 230
        thigh, shin = 70, 70
        for (a1, a2), col in ((back, "#3C5F86"), (front, "#1F3550")):
            a1r, a2r = np.radians(a1), np.radians(a2)
            knee = (cx + thigh * np.sin(a1r), hip + thigh * np.cos(a1r))
            ank = (knee[0] + shin * np.sin(a2r), knee[1] + shin * np.cos(a2r))
            d.line([(cx, hip), knee, ank], fill=col, width=11, joint="curve")
            d.line([ank, (ank[0] + 22, ank[1] + 2)], fill=col, width=9)
        d.line([(cx, hip), (cx + 4, hip - 92)], fill="#1F3550", width=13)
        d.ellipse([cx - 16, hip - 140, cx + 22, hip - 102], fill="#1F3550")
        sw = [(-20, 25), (10, -10), (25, -20), (-10, 15)][k]
        for s, col in ((sw[0], "#3C5F86"), (sw[1], "#1F3550")):
            sr = np.radians(s)
            d.line([(cx + 3, hip - 82), (cx + 3 + 62 * np.sin(sr), hip - 82 + 62 * np.cos(sr))], fill=col, width=9)
    return im


src = next((HERE / n for n in ("input.jpg", "input.png") if (HERE / n).exists()), None)
if src:
    im = Image.open(src).convert("RGB")
    s = min(im.size)
    im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2)).resize((PX, PX))
    LABEL = f"imagen: {src.name} · 14 × 14 parches"
else:
    im = synthetic_gait()
    LABEL = "imagen sintética · 448 px, parches de 32 px"
IMG = np.array(im)
MEANS = IMG.reshape(N, PX // N, N, PX // N, 3).mean(axis=(1, 3)).astype(int)   # (14, 14, 3)


def hexcol(rgb):
    return "#%02X%02X%02X" % tuple(int(v) for v in rgb)


class Imagenes(Scene):
    def construct(self):
        side = 4.4
        pic = ImageMobject(IMG).set(height=side).move_to([-5.35, 0.1, 0])
        frame = Square(side, stroke_color=BORDER, stroke_width=2).move_to(pic)
        self.play(FadeIn(pic), Create(frame), run_time=1.0)
        self.add(illustrative_label(LABEL))

        # cuadrícula
        cell = side / N
        ul = pic.get_corner(UP + LEFT)
        grid = VGroup(*[Line(ul + RIGHT * cell * i, ul + RIGHT * cell * i + DOWN * side) for i in range(1, N)],
                      *[Line(ul + DOWN * cell * i, ul + DOWN * cell * i + RIGHT * side) for i in range(1, N)])
        grid.set_stroke(BG, width=2, opacity=0.9)
        cnt = T("14 × 14 = 196 parches", size=24, color=MUTED, font=MONO).next_to(frame, UP, buff=0.15)
        self.play(LaggedStart(*[Create(g) for g in grid], lag_ratio=0.03), FadeIn(cnt), run_time=1.4)
        self.wait(0.4)

        # parches con su color promedio
        patches = VGroup()
        for r in range(N):
            for c in range(N):
                sq = Square(cell * 0.96, stroke_width=0, fill_color=hexcol(MEANS[r, c]), fill_opacity=1)
                sq.move_to(ul + RIGHT * cell * (c + 0.5) + DOWN * cell * (r + 0.5))
                patches.add(sq)
        self.play(FadeIn(patches), FadeOut(grid), pic.animate.set_opacity(0.25), run_time=0.8)

        # destino: secuencia de 4 filas × 49 + el texto
        seq_t = T("la secuencia que lee el modelo", size=23, color=GRAY).move_to([-1.75, 2.45, 0], aligned_edge=LEFT)
        tok, gap, per_row = 0.16, 0.025, 49
        x0, y0 = -1.75 + tok / 2, 1.85
        targets = [np.array([x0 + (k % per_row) * (tok + gap), y0 - (k // per_row) * (tok + gap * 3), 0]) for k in range(N * N)]
        self.play(FadeIn(seq_t), run_time=0.4)
        self.play(LaggedStart(*[p.animate.set(width=tok).move_to(t) for p, t in zip(patches, targets)], lag_ratio=0.012),
                  run_time=3.2)
        ribbon_right = targets[per_row - 1][0] + tok / 2
        img_br = Brace(VGroup(*patches[-per_row:]), DOWN, buff=0.1, color=MODEL)
        img_lab = T("196 tokens de imagen", size=21, color=MODEL).next_to(img_br, DOWN, buff=0.08)
        self.play(FadeIn(img_br), FadeIn(img_lab), pic.animate.set_opacity(1), run_time=0.6)

        words = ["Describe", "este", "ciclo", "de", "marcha:"]
        chips = VGroup(*[TokenChip(w, color=MUTED, size=24) for w in words]).arrange(RIGHT, buff=0.12)
        chips.move_to([-1.75, -0.65, 0], aligned_edge=LEFT)
        txt_lab = T("+ el texto, en la misma secuencia", size=21, color=MUTED).next_to(chips, DOWN, buff=0.15).align_to(chips, LEFT)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in chips], lag_ratio=0.1), run_time=1.0)
        self.play(FadeIn(txt_lab), run_time=0.4)

        model = Node("modelo", size=27).move_to([ribbon_right - 1.1, -1.75, 0])
        arr = Arrow([ribbon_right - 1.1, chips.get_y(), 0] + LEFT * 0.0, model.get_top(), buff=0.0, stroke_color=AXIS,
                    stroke_width=4, max_tip_length_to_length_ratio=0.35)
        arr.put_start_and_end_on(np.array([chips.get_right()[0] + 0.15, chips.get_y(), 0]), model.get_top() + UP * 0.08)
        self.play(FadeIn(model), Create(arr), run_time=0.7)
        cap = T("para el modelo, una imagen es otra frase", size=24, color=TEXT).move_to([-7.6, -2.55, 0], aligned_edge=LEFT)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.6)
        self.wait(3.5)
