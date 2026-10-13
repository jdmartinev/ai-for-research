"""Descenso por gradiente en 2 parámetros: el punto baja por el paisaje y la pérdida cae.

Pérdida cuadrática de juguete, rotada y alargada (por eso zigzaguea). Calculado, η = 0.28.
manim -r 1920,720 --fps 30 s_descenso.py Descenso
"""
import numpy as np
from manim import (Scene, VGroup, Axes, Dot, Line, Ellipse, FadeIn, FadeOut, Create, LaggedStart,
                   LEFT, RIGHT, UP, DOWN, BOLD, DEGREES)
from common import *

TH = 30 * DEGREES
R = np.array([[np.cos(TH), -np.sin(TH)], [np.sin(TH), np.cos(TH)]])
H = R @ np.diag([0.6, 6.0]) @ R.T
loss = lambda p: 0.5 * p @ H @ p + 0.2
grad = lambda p: H @ p
ETA, STEPS = 0.28, 30


def path():
    p = R @ np.array([-2.4, 0.45])
    pts = [p.copy()]
    for _ in range(STEPS):
        p = p - ETA * grad(p)
        pts.append(p.copy())
    return np.array(pts)


PTS = path()


class Descenso(Scene):
    def construct(self):
        S, C = 1.0, np.array([-3.4, 0.15, 0])     # escala y centro del paisaje en pantalla
        to = lambda q: C + np.array([q[0] * S, q[1] * S, 0])
        # curvas de nivel: 0.5 pᵀHp = c  →  elipses con semiejes sqrt(2c/λ)
        rings = VGroup()
        for k, c in enumerate([0.08, 0.3, 0.7, 1.3, 2.1, 3.0]):
            e = Ellipse(width=2 * np.sqrt(2 * c / 0.6) * S, height=2 * np.sqrt(2 * c / 6.0) * S,
                        stroke_color=MODEL, stroke_width=2, stroke_opacity=0.9 - 0.12 * k).rotate(TH).move_to(C)
            rings.add(e)
        mn = Dot(C, radius=0.06, color=TEXT)
        lab = T("paisaje de pérdida con 2 parámetros", size=20, color=GRAY).move_to([-3.4, 2.65, 0])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.1), FadeIn(mn), FadeIn(lab), run_time=1.5)
        ax = Axes(x_range=[0, STEPS, 10], y_range=[0, float(loss(PTS[0])) * 1.1, 2], x_length=4.6, y_length=3.6, tips=False,
                  axis_config={"color": AXIS, "stroke_width": 2, "include_ticks": False}).move_to([4.6, 0.0, 0])
        xl = T("paso →", size=20, color=MUTED).next_to(ax, DOWN, buff=0.12).align_to(ax, RIGHT)
        yl = T("pérdida", size=20, color=MUTED).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.8)
        dot = Dot(to(PTS[0]), radius=0.1, color=AMBER)
        cd = Dot(ax.c2p(0, loss(PTS[0])), radius=0.05, color=AMBER)
        self.play(FadeIn(dot, scale=0.5), FadeIn(cd), run_time=0.4)
        for k in range(1, STEPS + 1):
            rt = 0.45 if k <= 3 else 0.12
            seg = Line(to(PTS[k - 1]), to(PTS[k]), stroke_color=AMBER, stroke_width=3)
            cs = Line(ax.c2p(k - 1, loss(PTS[k - 1])), ax.c2p(k, loss(PTS[k])), stroke_color=AMBER, stroke_width=4)
            self.play(Create(seg), Create(cs), dot.animate.move_to(to(PTS[k])), run_time=rt)
        msg = T("2 parámetros aquí · 405,000 millones en Llama 3.1: la misma regla", size=22, color=TEXT).move_to([-7.6, -2.6, 0], aligned_edge=LEFT)
        self.play(FadeIn(msg), run_time=0.6)
        self.add(illustrative_label("pérdida de juguete · descenso calculado (η = 0.28)").shift(UP * 0.0))
        self.wait(3.5)
