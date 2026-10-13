"""Muestreo: predecir → elegir → agregar → repetir; luego, qué hace la temperatura.

Distribuciones ilustrativas; la de temperatura se calcula: p_T ∝ p^(1/T).
manim -r 1920,720 --fps 30 s_muestreo.py Muestreo
"""
import numpy as np
from manim import (Scene, VGroup, Rectangle, Line, FadeIn, FadeOut, Transform, ReplacementTransform,
                   LaggedStart, Indicate, LEFT, RIGHT, UP, DOWN, BOLD)
from common import *

PROMPT = "Durante la fase de apoyo, la rodilla"
STEPS = [  # (candidatos, probabilidades, índice elegido)
    (["␣se", "␣debe", "␣está", "␣permanece", "␣no", "␣tiene"], [0.34, 0.16, 0.14, 0.12, 0.09, 0.07], 0),
    (["␣flexiona", "␣encuentra", "␣extiende", "␣mantiene", "␣estabiliza", "␣mueve"], [0.41, 0.19, 0.13, 0.11, 0.08, 0.05], 0),
    (["␣ligeramente", "␣para", "␣unos", "␣hasta", ",", "␣y"], [0.29, 0.24, 0.17, 0.12, 0.10, 0.06], 1),
]


def temp(p, t):
    q = np.array(p) ** (1 / t)
    return q / q.sum()


class Muestreo(Scene):
    def bars(self, cands, probs, x0=0.4, y0=1.25, wmax=4.6, pick=None, dy=0.5):
        g = VGroup()
        probs = list(np.array(probs) / np.sum(probs))
        pm = max(probs)
        for k, (c, p) in enumerate(zip(cands, probs)):
            y = y0 - k * dy
            lab = T(c, size=22, color=TEXT if k == pick else MUTED, font=MONO).move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT)
            b = Rectangle(width=max(0.03, wmax * p / pm), height=0.3, stroke_width=0, fill_color=MODEL,
                          fill_opacity=0.95 if k == pick else 0.5).move_to([x0, y, 0], aligned_edge=LEFT)
            v = T(f"{100 * p:.0f}%", size=19, color=MUTED, font=MONO).next_to(b, RIGHT, buff=0.12)
            g.add(VGroup(lab, b, v))
        return g

    def construct(self):
        text = T(PROMPT, size=28, color=TEXT, font=MONO).move_to([-7.6, 2.45, 0], aligned_edge=LEFT)
        self.play(FadeIn(text), run_time=0.6)
        model = Node("modelo", size=24).move_to([-5.6, 0.0, 0])
        self.play(FadeIn(model), run_time=0.5)
        cur = None
        pieces = []
        for s, (cands, probs, pick) in enumerate(STEPS):
            slow = s == 0
            bs = self.bars(cands, probs, pick=None)
            self.play(model.animate(rate_func=lambda t: 1 - abs(2 * t - 1)).scale(1.08),
                      FadeOut(cur) if cur else FadeIn(VGroup()), FadeIn(bs, shift=RIGHT * 0.2), run_time=0.9 if slow else 0.6)
            # elegir: un marcador recorre y se detiene en el elegido
            box = RoundedRectangle(width=bs[0].width + 0.35, height=0.44, corner_radius=0.1, stroke_color=TEXT, stroke_width=2.5,
                                   fill_opacity=0).move_to(bs[0])
            box.align_to(bs[0], LEFT).shift(LEFT * 0.15)
            self.play(FadeIn(box), run_time=0.2)
            seq = [0, 2, 1, 3, pick] if slow else [1, pick]
            for k in seq:
                self.play(box.animate.move_to([box.get_x(), bs[k].get_y(), 0]), run_time=0.18 if slow else 0.14)
            chosen = bs[pick][0]
            piece = cands[pick].replace("␣", " ")
            word_show = T(piece.strip(), size=28, color=MODEL, font=MONO).next_to(text, RIGHT, buff=0.2 if piece.startswith(" ") else 0.04)
            self.play(chosen.animate.set_color(TEXT), bs[pick][1].animate.set_fill(opacity=0.95), run_time=0.3)
            self.play(ReplacementTransform(chosen.copy(), word_show), FadeOut(box), run_time=0.7)
            pieces.append(piece)
            new = T(PROMPT + "".join(pieces), size=28, color=TEXT, font=MONO).move_to([-7.6, 2.45, 0], aligned_edge=LEFT)
            self.remove(text, word_show)
            self.add(new)
            text = new
            if slow:
                lab = T("predecir → elegir → agregar → repetir", size=22, color=MUTED).move_to([-7.6, -0.85, 0], aligned_edge=LEFT)
                self.play(FadeIn(lab), run_time=0.5)
            cur = bs
            self.wait(0.5 if slow else 0.3)

        # temperatura
        self.play(FadeOut(cur), FadeOut(model), FadeOut(lab), run_time=0.5)
        cands, probs, _ = STEPS[0]
        ttl = T("la misma predicción, con distinta temperatura", size=24, color=MUTED).move_to([0, 1.75, 0])
        self.play(FadeIn(ttl), run_time=0.5)
        cols = VGroup()
        for j, t in enumerate([0.3, 1.0, 2.0]):
            q = temp(probs, t)
            g = VGroup()
            x = -5.3 + j * 5.3
            for k, (c, pv) in enumerate(zip(cands, q)):
                y = 0.95 - k * 0.42
                lab = T(c, size=18, color=MUTED, font=MONO).move_to([x - 0.95, y, 0], aligned_edge=RIGHT)
                b = Rectangle(width=max(0.03, 2.6 * pv), height=0.26, stroke_width=0, fill_color=MODEL, fill_opacity=0.75).move_to([x - 0.8, y, 0], aligned_edge=LEFT)
                v = T(f"{100 * pv:.0f}%", size=16, color=GRAY, font=MONO).next_to(b, RIGHT, buff=0.08)
                g.add(lab, b, v)
            head = T(f"T = {t:g}", size=26, color=TEXT, font=MONO, weight=BOLD).move_to([x - 0.2, 1.35, 0])
            sub = T(["casi siempre el más probable", "como predijo el modelo", "más variado, más errores"][j], size=19, color=MUTED).move_to([x - 0.2, -1.65, 0])
            cols.add(VGroup(head, g, sub))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cols], lag_ratio=0.3), run_time=1.8)
        self.add(illustrative_label("probabilidades ilustrativas, renormalizadas sobre los 6 más probables · temperatura: p ∝ p^(1/T)"))
        self.wait(3.5)
