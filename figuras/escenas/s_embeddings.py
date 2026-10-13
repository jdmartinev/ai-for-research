"""Embeddings: cada token es un vector; lo parecido queda cerca. Posiciones ilustrativas en 2D.

manim -r 1920,720 --fps 30 s_embeddings.py Embeddings
"""
import numpy as np
from manim import (Scene, VGroup, Dot, Line, DashedLine, Ellipse, FadeIn, FadeOut, Create, LaggedStart,
                   Transform, LEFT, RIGHT, UP, DOWN, BOLD)
from common import *

GROUPS = {
    "articulaciones": [("rodilla", -4.6, 1.0), ("cadera", -5.5, 0.45), ("tobillo", -3.9, 0.25), ("codo", -4.9, -0.3)],
    "movimiento": [("marcha", 0.0, 1.55), ("carrera", 0.95, 1.1), ("salto", -0.2, 0.7), ("zancada", 0.85, 1.95)],
    "dispositivos": [("exoesqueleto", -1.9, -1.25), ("prótesis", -0.9, -1.75), ("órtesis", -2.4, -1.95)],
    "bioquímica": [("proteína", 4.2, -0.8), ("enzima", 5.0, -0.25), ("aminoácido", 4.3, -1.55)],
}
VEC = [0.12, -0.48, 0.91, 0.03, -0.27, 0.66, -0.15, 0.38]


class Embeddings(Scene):
    def construct(self):
        dots, labels, by_word = VGroup(), VGroup(), {}
        order = []
        for g, items in GROUPS.items():
            for w, x, y in items:
                d = Dot([x, y + 0.35, 0], radius=0.07, color=MODEL)
                l = T(w, size=21, color=TEXT).next_to(d, RIGHT, buff=0.1)
                by_word[w] = (d, l)
                order.append((d, l))
        rng = np.random.default_rng(2)
        perm = rng.permutation(len(order))
        self.play(LaggedStart(*[FadeIn(VGroup(*order[i]), scale=0.7) for i in perm], lag_ratio=0.12), run_time=2.6)
        self.wait(0.5)
        # grupos
        rings = VGroup()
        for g, items in GROUPS.items():
            pts = np.array([by_word[w][0].get_center() for w, _, _ in items])
            lab_pts = np.array([by_word[w][1].get_right() for w, _, _ in items])
            lo = np.minimum(pts.min(0), lab_pts.min(0)); hi = np.maximum(pts.max(0), lab_pts.max(0))
            c = (lo + hi) / 2
            e = Ellipse(width=hi[0] - lo[0] + 0.9, height=hi[1] - lo[1] + 0.8, stroke_color=AXIS, stroke_width=2).move_to(c)
            t = T(g, size=19, color=GRAY).next_to(e, DOWN, buff=0.05)
            rings.add(VGroup(e, t))
        self.play(LaggedStart(*[Create(r[0]) for r in rings], lag_ratio=0.2), FadeIn(VGroup(*[r[1] for r in rings])), run_time=1.6)
        self.wait(0.8)
        # cerca y lejos
        rd, rl = by_word["rodilla"]
        cd, _ = by_word["cadera"]
        ed, _ = by_word["enzima"]
        self.play(rd.animate.set_color(TEXT).scale(1.5), rl.animate.set_color(TEXT), run_time=0.4)
        near = Line(rd.get_center(), cd.get_center(), stroke_color=MODEL, stroke_width=4)
        far = DashedLine(rd.get_center(), ed.get_center(), stroke_color=GRAY, stroke_width=3, dash_length=0.12)
        nl = T("cerca", size=20, color=MODEL).next_to(near.get_center(), UP + LEFT, buff=0.08)
        fl = T("lejos", size=20, color=GRAY).move_to(rd.get_center() * 0.22 + ed.get_center() * 0.78 + DOWN * 0.28)
        self.play(Create(near), FadeIn(nl), run_time=0.7)
        self.play(Create(far), FadeIn(fl), run_time=0.9)
        self.wait(0.6)
        # el vector
        vec = T("rodilla → [" + ", ".join(f"{v:+.2f}" for v in VEC[:5]) + ", …]", size=20, color=TEXT, font=MONO)
        vec.move_to([7.75, 2.65, 0], aligned_edge=RIGHT)
        sub = T("miles de números por token", size=19, color=MUTED).next_to(vec, DOWN, buff=0.12).align_to(vec, RIGHT)
        self.play(FadeIn(vec, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(sub), run_time=0.4)
        self.add(illustrative_label("posiciones y números ilustrativos · los reales tienen miles de dimensiones"))
        self.wait(3.5)
