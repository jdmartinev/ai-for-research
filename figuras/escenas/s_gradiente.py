"""Gradiente: la pendiente dice hacia dónde mover un parámetro; cada paso baja la pérdida.

Pérdida de juguete L(w) = 0.3 (w − 1)² + 0.5; paso w ← w − η L'(w), η = 0.8. Calculado.
manim -r 1920,720 --fps 30 s_gradiente.py Gradiente
"""
import numpy as np
from manim import (Scene, VGroup, Axes, Dot, Line, Arrow, FadeIn, FadeOut, Create, Transform,
                   LEFT, RIGHT, UP, DOWN, BOLD)
from common import *

L = lambda w: 0.3 * (w - 1) ** 2 + 0.5
dL = lambda w: 0.6 * (w - 1)
ETA, W0, N = 0.8, -2.4, 5


class Gradiente(Scene):
    def construct(self):
        ax = Axes(x_range=[-3, 4, 1], y_range=[0, 5.0, 1], x_length=9.0, y_length=4.4, tips=False,
                  axis_config={"color": AXIS, "stroke_width": 2, "include_ticks": False}).move_to([-2.6, -0.1, 0])
        xl = T("valor de un parámetro  w", size=20, color=MUTED).next_to(ax, DOWN, buff=0.12).align_to(ax, LEFT)
        yl = T("pérdida", size=20, color=MUTED).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        curve = ax.plot(L, x_range=[-2.75, 4], color=MODEL, stroke_width=4)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.8)
        self.play(Create(curve), run_time=1.0)
        rule = T("w  ←  w − η · pendiente", size=30, color=TEXT).move_to([5.1, 1.9, 0])
        rl = T("muévete en contra de la pendiente", size=20, color=MUTED).next_to(rule, DOWN, buff=0.15)
        w = W0
        dot = Dot(ax.c2p(w, L(w)), radius=0.11, color=AMBER)
        self.play(FadeIn(dot, scale=0.5), run_time=0.4)
        info = VGroup()
        for k in range(N):
            s = dL(w)
            x1, x2 = w - 1.1, w + 1.1
            tan = Line(ax.c2p(x1, L(w) + s * (x1 - w)), ax.c2p(x2, L(w) + s * (x2 - w)), stroke_color=TEXT, stroke_width=3)
            new_info = VGroup(T(f"pendiente = {s:+.2f}", size=24, color=TEXT, font=MONO),
                              T(f"pérdida = {L(w):.2f}", size=24, color=AMBER, font=MONO)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([5.1, -0.4, 0])
            wn = w - ETA * s
            arr = Arrow(ax.c2p(w, 0.25), ax.c2p(wn, 0.25), buff=0, stroke_color=AMBER, stroke_width=5, tip_length=0.2,
                        max_tip_length_to_length_ratio=0.3)
            slow = k < 2
            anims = [Create(tan), Transform(info, new_info) if len(info) else FadeIn(new_info)]
            if k == 0:
                anims += [FadeIn(rule), FadeIn(rl)]
            self.play(*anims, run_time=0.8 if slow else 0.45)
            if not len(info):
                info = new_info
            self.play(Create(arr), run_time=0.5 if slow else 0.3)
            self.play(dot.animate.move_to(ax.c2p(wn, L(wn))), FadeOut(tan), FadeOut(arr), run_time=0.8 if slow else 0.45)
            w = wn
        final = VGroup(T(f"pendiente = {dL(w):+.2f}", size=24, color=TEXT, font=MONO),
                       T(f"pérdida = {L(w):.2f}", size=24, color=AMBER, font=MONO)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(info)
        self.play(Transform(info, final), run_time=0.4)
        note = T("con retropropagación se calcula la pendiente\nde todos los parámetros a la vez", size=20, color=MUTED, line_spacing=0.9).move_to([5.1, -1.85, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.add(illustrative_label("pérdida de juguete con un solo parámetro · pasos calculados (η = 0.8)"))
        self.wait(3.5)
