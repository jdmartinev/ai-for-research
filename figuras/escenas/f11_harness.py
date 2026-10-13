"""F11 — El modelo es el motor; el harness es el carro (diapositiva 11). Figura 1920×720.

Seis componentes alrededor del modelo; solo «Verificación» es ámbar (el juez) y cierra el ciclo.
manim -s -r 1920,720 f11_harness.py Harness
"""
import numpy as np
from manim import (Scene, VGroup, Arrow, RoundedRectangle, DashedVMobject, CurvedArrow, LEFT, RIGHT, UP, DOWN, BOLD, PI)
from common import *

PARTS = [("Instrucciones", "CLAUDE.md / AGENTS.md"),
         ("Contexto", "tus archivos, papers y memoria"),
         ("Herramientas", "búsqueda, código, APIs, MCP"),
         ("Skills", "carpetas con SKILL.md"),
         ("Permisos", "qué puede leer, escribir y ejecutar"),
         ("Verificación", "tests, linters, revisor independiente")]


REFS = {"Instrucciones": "Parte 3", "Contexto": "diap. 16", "Herramientas": "Parte 2", "Skills": "Parte 3",
        "Permisos": "Parte 3", "Verificación": "los jueces"}


class Harness(Scene):
    def construct(self):
        model = Node("modelo", size=34, width=2.6).move_to([0, 0, 0])
        model.box.stretch_to_fit_height(1.15)
        cards = VGroup()
        pos = [(-5.0, 1.75), (-5.0, 0.0), (-5.0, -1.75), (5.0, 1.75), (5.0, 0.0), (5.0, -1.75)]
        for (title, ex), (x, y) in zip(PARTS, pos):
            judge = title == "Verificación"
            box = RoundedRectangle(width=4.6, height=1.2, corner_radius=0.14, fill_color=CARD, fill_opacity=1,
                                   stroke_color=AMBER if judge else BORDER, stroke_width=3.5 if judge else 2)
            t = T(title, size=26, color=AMBER if judge else TEXT, weight=BOLD)
            e = T(ex, size=19, color=MUTED, font=MONO if ".md" in ex else FONT)
            VGroup(t, e).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(box).align_to(box.get_left() + RIGHT * 0.3, LEFT)
            ref = T(REFS[title], size=16, color=AMBER if judge else GRAY, font=MONO).move_to(box.get_corner(UP + RIGHT) + LEFT * 0.2 + DOWN * 0.2, aligned_edge=UP + RIGHT)
            cards.add(VGroup(box, t, e, ref).move_to([x, y, 0]))
        arrows = VGroup()
        for c in cards:
            side = c[0].get_right() if c.get_x() < 0 else c[0].get_left()
            target = model.box.get_left() if c.get_x() < 0 else model.box.get_right()
            target = target + UP * (c.get_y() * 0.18)
            judge = c is cards[5]
            arrows.add(Arrow(side, target, buff=0.12, stroke_color=AMBER if judge else AXIS, stroke_width=4 if judge else 3,
                             tip_length=0.2, max_tip_length_to_length_ratio=0.2))
        # retorno: del modelo a la verificación (por abajo)
        back = CurvedArrow(model.box.get_bottom() + DOWN * 0.1, cards[5][0].get_left() + LEFT * 0.12 + DOWN * 0.3,
                           angle=PI * 0.4, color=AMBER, stroke_width=4, tip_length=0.2)
        back_t = T("cada salida pasa por el juez", size=20, color=AMBER).move_to([0.3, -2.4, 0])
        frame = DashedVMobject(RoundedRectangle(width=15.6, height=5.55, corner_radius=0.3, stroke_color=GRAY,
                                                stroke_width=2), num_dashes=90)
        lab = T("harness", size=24, color=MUTED, font=MONO)
        lab.move_to([0, 2.775, 0])
        bg = RoundedRectangle(width=lab.width + 0.4, height=0.4, corner_radius=0.1, fill_color=BG, fill_opacity=1,
                              stroke_width=0).move_to(lab)
        mref = T("Parte 1", size=16, color=GRAY, font=MONO).next_to(model, UP, buff=0.12)
        self.add(frame, bg, lab, arrows, back, back_t, cards, model, mref)
