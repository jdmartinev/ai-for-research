"""F32 — BrowseComp: exactitud de modelos y agentes. Figura fija 1920×720.

Cifras de Wei et al. (2025), BrowseComp (OpenAI), tal como las presenta Asai (2026), CMU 11-768.
manim -s -r 1920,720 f32_browsecomp.py BrowseComp
"""
from manim import Scene, VGroup, Rectangle, Line, DashedLine, LEFT, RIGHT, UP, DOWN, BOLD
from common import *

ROWS = [("GPT-4o", 0.6, False), ("GPT-4.5", 0.9, False), ("GPT-4o + navegación web", 1.9, False),
        ("o1 (razonamiento)", 9.9, False), ("Deep Research (agente)", 51.5, True)]
HUMAN = 25.3


class BrowseComp(Scene):
    def construct(self):
        x0, wmax, y0 = -2.6, 8.6, 1.75
        scale = wmax / 60
        axis = Line([x0, y0 + 0.45, 0], [x0, y0 - len(ROWS) * 0.78 + 0.25, 0], stroke_color=AXIS, stroke_width=2)
        g = VGroup()
        for k, (name, v, hi) in enumerate(ROWS):
            y = y0 - k * 0.78
            lab = T(name, size=24, color=TEXT if hi else MUTED, weight=BOLD if hi else "NORMAL").move_to([x0 - 0.25, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=max(0.04, v * scale), height=0.46, stroke_width=0, fill_color=MODEL, fill_opacity=0.95 if hi else 0.55).move_to([x0, y, 0], aligned_edge=LEFT)
            num = T(f"{v:.1f}%", size=22, color=TEXT if hi else MUTED, font=MONO).next_to(bar, RIGHT, buff=0.15)
            g.add(lab, bar, num)
        hx = x0 + HUMAN * scale
        hl = DashedLine([hx, y0 + 0.55, 0], [hx, y0 - len(ROWS) * 0.78 + 0.2, 0], stroke_color=TEXT, stroke_width=2.5, dash_length=0.12)
        ht = T(f"referencia humana: {HUMAN}%", size=20, color=TEXT).next_to(hl, UP, buff=0.08)
        title = T("BrowseComp · 1,266 preguntas que exigen muchas búsquedas", size=24, color=MUTED).move_to([-7.6, 2.75, 0], aligned_edge=LEFT)
        foot = T("exactitud: respuesta igual a la de referencia", size=19, color=GRAY).move_to([x0, -2.45, 0], aligned_edge=LEFT)
        self.add(title, axis, g, hl, ht, foot)
