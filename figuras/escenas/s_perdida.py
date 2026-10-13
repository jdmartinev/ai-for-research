"""Pérdida: el texto real es el juez; −log p(correcto) mide la sorpresa. Probabilidades ilustrativas.

manim -r 1920,720 --fps 30 s_perdida.py Perdida
"""
import numpy as np
from manim import (Scene, VGroup, Axes, Dot, Line, Rectangle, RoundedRectangle, FadeIn, FadeOut, Create,
                   Transform, ReplacementTransform, LEFT, RIGHT, UP, DOWN, BOLD)
from common import *

CANDS = ["␣extiende", "␣mueve", "␣bloquea", "␣flexiona", "␣rota", "␣apoya"]
P0 = [0.31, 0.22, 0.15, 0.05, 0.04, 0.03]
P1 = [0.12, 0.07, 0.04, 0.62, 0.02, 0.03]
CI = 3


class Perdida(Scene):
    def bars(self, probs):
        g = VGroup()
        for k, (c, p) in enumerate(zip(CANDS, probs)):
            y = 1.05 - k * 0.47
            lab = T(c, size=21, color=TEXT if k == CI else MUTED, font=MONO, weight=BOLD if k == CI else "NORMAL").move_to([-4.0, y, 0], aligned_edge=RIGHT)
            b = Rectangle(width=max(0.03, 5.5 * p), height=0.3, stroke_width=0, fill_color=TEXT if k == CI else MODEL,
                          fill_opacity=0.85 if k == CI else 0.5).move_to([-3.8, y, 0], aligned_edge=LEFT)
            v = T(f"{100 * p:.0f}%", size=19, color=TEXT if k == CI else MUTED, font=MONO).next_to(b, RIGHT, buff=0.12)
            g.add(VGroup(lab, b, v))
        return g

    def construct(self):
        ctx = T("…en la fase de apoyo, la rodilla se", size=26, color=TEXT, font=MONO).move_to([-7.6, 2.45, 0], aligned_edge=LEFT)
        blank = RoundedRectangle(width=1.9, height=0.45, corner_radius=0.08, fill_color=CARD, fill_opacity=1, stroke_color=BORDER).next_to(ctx, RIGHT, buff=0.2)
        q = T("?", size=26, color=GRAY, font=MONO).move_to(blank)
        self.play(FadeIn(ctx), FadeIn(blank), FadeIn(q), run_time=0.8)
        model_lab = T("lo que predice el modelo", size=20, color=GRAY).move_to([-7.6, 1.6, 0], aligned_edge=LEFT)
        bs = self.bars(P0)
        self.play(FadeIn(model_lab), FadeIn(bs, shift=RIGHT * 0.2), run_time=1.0)
        self.wait(0.5)
        # el juez: el texto real
        real = T("flexiona", size=26, color=AMBER, font=MONO, weight=BOLD).move_to(blank)
        jl = T("el texto real (el juez)", size=20, color=AMBER).next_to(blank, RIGHT, buff=0.3)
        self.play(FadeOut(q), FadeIn(real), FadeIn(jl), run_time=0.7)
        self.play(bs[CI][0].animate.scale(1.12), run_time=0.4)
        # curva −log p
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 4, 1], x_length=4.0, y_length=3.0, tips=False,
                  axis_config={"color": AXIS, "stroke_width": 2, "include_ticks": False}).move_to([5.45, 0.15, 0])
        curve = ax.plot(lambda x: -np.log(x), x_range=[0.018, 1], color=AXIS, stroke_width=3)
        xl = T("probabilidad del token correcto", size=18, color=MUTED).next_to(ax, DOWN, buff=0.12)
        yl = T("pérdida", size=18, color=MUTED).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        f = T("pérdida = −log p", size=22, color=MUTED, font=MONO).move_to([5.45, -2.2, 0])
        self.play(Create(ax), Create(curve), FadeIn(xl), FadeIn(yl), FadeIn(f), run_time=1.0)
        p0, p1 = P0[CI], P1[CI]
        dot = Dot(ax.c2p(p0, -np.log(p0)), radius=0.09, color=AMBER)
        big = T(f"{-np.log(p0):.2f}", size=64, color=AMBER, font=DISPLAY, weight=BOLD).move_to([1.5, 1.0, 0])
        bl = T("pérdida", size=20, color=AMBER).next_to(big, DOWN, buff=0.05)
        self.play(FadeIn(dot, scale=0.5), FadeIn(big), FadeIn(bl), run_time=0.7)
        sub = T("le dio 5%: mucha sorpresa", size=20, color=MUTED).next_to(bl, DOWN, buff=0.15)
        self.play(FadeIn(sub), run_time=0.4)
        self.wait(1.0)
        # actualizar
        upd = T("actualizar los parámetros", size=22, color=TEXT).move_to([-5.0, -2.05, 0])
        self.play(FadeIn(upd), run_time=0.4)
        bs2 = self.bars(P1)
        big2 = T(f"{-np.log(p1):.2f}", size=64, color=AMBER, font=DISPLAY, weight=BOLD).move_to(big)
        sub2 = T("ahora le da 62%: poca sorpresa", size=20, color=MUTED).move_to(sub)
        self.play(Transform(bs, bs2), dot.animate.move_to(ax.c2p(p1, -np.log(p1))), Transform(big, big2), Transform(sub, sub2), run_time=1.6)
        self.add(illustrative_label("probabilidades ilustrativas · pérdida calculada"))
        self.wait(3.5)
