"""F17 — Leyes de escala: pérdida contra cómputo para varios tamaños, con el ajuste de Chinchilla.

L(N, D) = E + A/N^α + B/D^β, con E = 1.69, A = 406.4, B = 410.7, α = 0.34, β = 0.28
(Hoffmann et al., 2022, ecuación 10). Cómputo C ≈ 6·N·D. Curvas calculadas, no datos medidos.
manim -s -r 1920,720 f17_escala.py Escala
"""
import numpy as np
from manim import Scene, VGroup, Axes, Line, DashedLine, Dot, LEFT, RIGHT, UP, DOWN, BOLD
from common import *

E, A, B, a, b = 1.69, 406.4, 410.7, 0.34, 0.28
Lf = lambda N, D: E + A / N ** a + B / D ** b
SIZES = [(1e8, "100 M"), (1e9, "1,000 M"), (1e10, "10,000 M"), (1e11, "100,000 M")]


class Escala(Scene):
    def construct(self):
        lc = np.linspace(18, 25, 300)                       # log10 C
        ax = Axes(x_range=[18, 25, 1], y_range=[1.6, 4.2, 0.5], x_length=10.5, y_length=4.4, tips=False,
                  axis_config={"color": AXIS, "stroke_width": 2, "include_ticks": False}).move_to([-1.6, -0.05, 0])
        xl = T("cómputo de entrenamiento (FLOPs) →", size=19, color=MUTED).next_to(ax, DOWN, buff=0.35).align_to(ax, LEFT)
        yl = T("pérdida", size=19, color=MUTED).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        ticks = VGroup()
        for e in [18, 20, 22, 24]:
            ticks.add(T(f"10^{e}", size=16, color=GRAY, font=MONO).next_to(ax.c2p(e, 1.6), DOWN, buff=0.08))
        for v in [2, 3, 4]:
            ticks.add(T(f"{v:.1f}", size=16, color=GRAY, font=MONO).next_to(ax.c2p(18, v), LEFT, buff=0.1))
        curves, labs = VGroup(), VGroup()
        cols = [GRAY, "#4A7FA6", MODEL, "#8FB8D8"]
        for (N, name), c in zip(SIZES, cols):
            pts = []
            for x in lc:
                D = 10 ** x / (6 * N)
                if D < N:            # menos de 1 token por parámetro: fuera de rango útil
                    continue
                y = Lf(N, D)
                if y <= 4.2:
                    pts.append(ax.c2p(x, y))
            g = VGroup(*[Line(pts[i], pts[i + 1], stroke_color=c, stroke_width=3) for i in range(len(pts) - 1)])
            curves.add(g)
            labs.add(T(f"{name}", size=17, color=c).next_to(pts[0], UP + RIGHT, buff=0.06))
        # envolvente óptima: para cada C, el mínimo sobre N
        Ns = np.logspace(7, 13, 400)
        env = []
        for x in lc:
            C = 10 ** x
            y = min(Lf(N, C / (6 * N)) for N in Ns)
            if y <= 4.2:
                env.append(ax.c2p(x, y))
        envg = VGroup(*[Line(env[i], env[i + 1], stroke_color=TEXT, stroke_width=5) for i in range(len(env) - 1)])
        el = T("el mejor modelo para cada presupuesto", size=20, color=TEXT, weight=BOLD).move_to(ax.c2p(18.25, 1.98), aligned_edge=LEFT)
        pl = T("cada curva: un tamaño de modelo (parámetros)", size=18, color=MUTED).move_to(ax.c2p(18.25, 1.74), aligned_edge=LEFT)
        note = VGroup(T("Chinchilla: conviene crecer", size=21, color=MUTED),
                      T("parámetros y datos a la par,", size=21, color=MUTED),
                      T("unos 20 tokens por parámetro", size=21, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([6.0, 1.5, 0])
        self.add(ax, xl, yl, ticks, curves, labs, envg, el, pl, note)
        self.add(illustrative_label("curvas calculadas con el ajuste de Hoffmann et al. (2022) · C ≈ 6ND"))
