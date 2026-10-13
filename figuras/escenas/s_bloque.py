"""Un bloque transformer: atención (mezcla entre tokens) + MLP (cada token por separado), con residuales.

Valores ilustrativos calculados con matrices aleatorias (semilla fija); colores = valor de cada celda.
manim -r 1920,720 --fps 30 s_bloque.py Bloque
"""
import numpy as np
from manim import (Scene, VGroup, Square, Line, Arrow, CurvedArrow, RoundedRectangle, ArcBetweenPoints, Brace,
                   FadeIn, FadeOut, Create, Transform, LaggedStart, ReplacementTransform, LEFT, RIGHT, UP, DOWN, BOLD, PI,
                   interpolate_color, ManimColor)
from common import *

RNG = np.random.default_rng(5)
WORDS = ["El", "robot", "levantó", "la", "caja"]
X = RNG.normal(0, 1, (5, 6))
A = np.exp(RNG.normal(0, 1.2, (5, 5))); A /= A.sum(1, keepdims=True)
H1 = X + 0.8 * (A @ X)                      # residual + atención
W = RNG.normal(0, 0.7, (6, 6))
H2 = H1 + np.tanh(H1 @ W)                   # residual + MLP


def col(v):
    lo, hi = ManimColor(PANEL), ManimColor(MODEL)
    t = 1 / (1 + np.exp(-v))
    return interpolate_color(lo, hi, float(t))


def vecs(M, x, size=0.22, gap=0.12):
    g = VGroup()
    for i, row in enumerate(M):
        c = VGroup(*[Square(size, stroke_color=BORDER, stroke_width=1, fill_color=col(v), fill_opacity=1) for v in row])
        c.arrange(DOWN, buff=0)
        g.add(c)
    g.arrange(RIGHT, buff=gap).move_to([x, -0.1, 0])
    return g


class Bloque(Scene):
    def construct(self):
        xs = [-6.3, -0.55, 5.2]
        v0 = vecs(X, xs[0])
        words = T("«El robot levantó la caja»", size=18, color=MUTED).next_to(v0, DOWN, buff=0.2)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in v0], lag_ratio=0.1), FadeIn(words), run_time=1.0)
        lab0 = T("un vector por token", size=19, color=GRAY).next_to(v0, UP, buff=0.3)
        self.play(FadeIn(lab0), run_time=0.4)
        # caja de atención
        att = RoundedRectangle(width=2.6, height=2.0, corner_radius=0.16, fill_color=CARD, fill_opacity=1, stroke_color=MODEL, stroke_width=2.5).move_to([-3.45, -0.1, 0])
        att_t = T("atención", size=24, color=TEXT, weight=BOLD).next_to(att, UP, buff=0.12)
        dots = VGroup(*[Dot(radius=0.06, color=MUTED) for _ in range(5)]).arrange(RIGHT, buff=0.38).move_to(att.get_center() + DOWN * 0.45)
        arcs = VGroup()
        for i in range(5):
            for j in range(5):
                if i < j and A[i, j] + A[j, i] > 0.35:
                    a = ArcBetweenPoints(dots[i].get_center(), dots[j].get_center(), angle=-PI * 0.6)
                    a.set_stroke(MODEL, width=1 + 5 * (A[i, j] + A[j, i]), opacity=0.9)
                    arcs.add(a)
        att_s = T("mezcla entre tokens", size=18, color=MUTED).next_to(att, DOWN, buff=0.12)
        self.play(FadeIn(att), FadeIn(att_t), FadeIn(dots), FadeIn(att_s), run_time=0.6)
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.1), run_time=1.0)
        v1 = vecs(H1, xs[1])
        res1 = CurvedArrow(v0.get_top() + UP * 0.55, v1.get_top() + UP * 0.55, angle=-PI * 0.3, color=GRAY, stroke_width=3, tip_length=0.16)
        plus1 = T("+", size=30, color=TEXT, weight=BOLD).next_to(v1, UP, buff=0.2)
        self.play(ReplacementTransform(v0.copy(), v1), run_time=1.2)
        self.play(Create(res1), FadeIn(plus1), FadeOut(lab0), run_time=0.7)
        rl = T("residual: suma una corrección", size=18, color=GRAY).next_to(res1, UP, buff=0.05)
        self.play(FadeIn(rl), run_time=0.4)
        # MLP
        mlp = RoundedRectangle(width=2.6, height=2.0, corner_radius=0.16, fill_color=CARD, fill_opacity=1, stroke_color=MODEL, stroke_width=2.5).move_to([2.3, -0.1, 0])
        mlp_t = T("MLP", size=24, color=TEXT, weight=BOLD).next_to(mlp, UP, buff=0.12)
        cells = VGroup(*[RoundedRectangle(width=0.32, height=0.9, corner_radius=0.06, stroke_color=MUTED, stroke_width=2) for _ in range(5)]).arrange(RIGHT, buff=0.12).move_to(mlp)
        mlp_s = T("cada token por separado", size=18, color=MUTED).next_to(mlp, DOWN, buff=0.12)
        self.play(FadeIn(mlp), FadeIn(mlp_t), FadeIn(cells), FadeIn(mlp_s), run_time=0.6)
        self.play(LaggedStart(*[c.animate(rate_func=lambda t: 1 - abs(2 * t - 1)).set_stroke(MODEL, width=4) for c in cells], lag_ratio=0.2), run_time=1.0)
        v2 = vecs(H2, xs[2])
        res2 = CurvedArrow(v1.get_top() + UP * 0.55, v2.get_top() + UP * 0.55, angle=-PI * 0.3, color=GRAY, stroke_width=3, tip_length=0.16)
        plus2 = T("+", size=30, color=TEXT, weight=BOLD).next_to(v2, UP, buff=0.2)
        self.play(ReplacementTransform(v1.copy(), v2), run_time=1.2)
        self.play(Create(res2), FadeIn(plus2), run_time=0.7)
        br = Brace(VGroup(att, mlp, att_s, mlp_s), DOWN, buff=0.2, color=AXIS)
        bt = T("= 1 bloque transformer", size=24, color=TEXT).next_to(br, DOWN, buff=0.1)
        self.play(FadeIn(br), FadeIn(bt), run_time=0.6)
        self.add(illustrative_label("valores ilustrativos"))
        self.wait(3.5)
