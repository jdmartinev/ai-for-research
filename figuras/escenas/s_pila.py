"""La pila: los vectores suben por decenas de bloques; el del último token da las probabilidades.

Llama 3.1 405B tiene 126 bloques. Colores de los vectores calculados al azar (semilla fija);
las probabilidades finales son las ilustrativas de la figura F03.
manim -r 1920,720 --fps 30 s_pila.py Pila
"""
import numpy as np
from manim import (Scene, VGroup, Square, Rectangle, RoundedRectangle, Arrow, FadeIn, FadeOut, Create, Transform,
                   LaggedStart, ReplacementTransform, LEFT, RIGHT, UP, DOWN, BOLD, interpolate_color, ManimColor)
from common import *

RNG = np.random.default_rng(9)
TOKS = ["Durante", "␣la", "␣fase", "…", "␣la", "␣rod", "illa"]
TOP = [("␣se", 0.214), ("␣debe", 0.098), ("␣está", 0.087), ("␣es", 0.071), ("␣permanece", 0.064)]
LAYERS = ["bloque 1", "bloque 2", "bloque 3", "⋮", "bloque 126"]


def col(v):
    return interpolate_color(ManimColor(PANEL), ManimColor(MODEL), float(1 / (1 + np.exp(-v))))


def row(vals, x0, y, w=0.36, gap=0.66):
    g = VGroup()
    for k, v in enumerate(vals):
        s = Square(w, stroke_color=BORDER, stroke_width=1, fill_color=col(v), fill_opacity=1).move_to([x0 + k * (w + gap), y, 0])
        g.add(s)
    return g


class Pila(Scene):
    def construct(self):
        n = len(TOKS)
        x0 = -6.6
        chips = VGroup(*[TokenChip(t, color=BORDER, size=19) for t in TOKS])
        for k, c in enumerate(chips):
            c.move_to([x0 + k * 1.02, -2.55, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.08), run_time=0.9)
        ys = [-1.75, -0.95, -0.25, 0.35, 0.95, 1.75]   # embedding, bloques 1..3, ⋮, 126
        slabs = VGroup()
        for i, name in enumerate(LAYERS):
            y = ys[i + 1]
            if name == "⋮":
                slabs.add(T("⋮", size=34, color=GRAY).move_to([x0 + 3.06, y, 0]))
                continue
            sl = RoundedRectangle(width=7.4, height=0.46, corner_radius=0.1, fill_color=CARD, fill_opacity=1, stroke_color=BORDER, stroke_width=1.5).move_to([x0 + 3.06, y, 0])
            lab = T(name, size=18, color=MUTED).next_to(sl, RIGHT, buff=0.2)
            slabs.add(VGroup(sl, lab))
        self.play(LaggedStart(*[FadeIn(s) for s in slabs], lag_ratio=0.12), run_time=1.0)
        cur = row(RNG.normal(0, 1, n), x0, ys[0])
        el = T("embeddings", size=18, color=MUTED).next_to(cur, RIGHT, buff=0.35)
        self.play(ReplacementTransform(chips.copy(), cur), FadeIn(el), run_time=0.9)
        for i in range(len(LAYERS)):
            if LAYERS[i] == "⋮":
                continue
            new = row(RNG.normal(0, 1.2, n), x0, ys[i + 1])
            slab = slabs[i][0]
            self.play(slab.animate(rate_func=lambda t: 1 - abs(2 * t - 1)).set_stroke(MODEL, width=3),
                      ReplacementTransform(cur.copy(), new), run_time=0.7)
            cur = new
        last = cur[-1]
        self.play(last.animate.set_stroke(TEXT, width=3).scale(1.3), run_time=0.4)
        # salida: probabilidades
        arr = Arrow(slabs[-1][1].get_right(), [3.0, 1.75, 0], buff=0.12, stroke_color=AXIS, stroke_width=4, tip_length=0.2)
        out_t = T("vector del último token → probabilidades", size=19, color=GRAY).move_to([5.3, 2.55, 0])
        bars = VGroup()
        for k, (tk, p) in enumerate(TOP):
            y = 1.75 - k * 0.48
            lab = T(tk, size=20, color=TEXT if k == 0 else MUTED, font=MONO).move_to([4.55, y, 0], aligned_edge=RIGHT)
            b = Rectangle(width=10 * p, height=0.28, stroke_width=0, fill_color=MODEL, fill_opacity=0.95 if k == 0 else 0.55).move_to([4.7, y, 0], aligned_edge=LEFT)
            v = T(f"{100 * p:.1f}%", size=17, color=MUTED, font=MONO).next_to(b, RIGHT, buff=0.1)
            bars.add(VGroup(lab, b, v))
        self.play(Create(arr), FadeIn(out_t), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in bars], lag_ratio=0.1), run_time=1.0)
        note = T("Llama 3.1 405B apila 126 bloques", size=22, color=TEXT).move_to([5.3, -1.2, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.add(illustrative_label("colores y probabilidades ilustrativos"))
        self.wait(3.5)
