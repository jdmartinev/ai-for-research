"""F10 — Deep research por dentro (diapositiva 10). Figura 1920×440.

Arquitectura según Anthropic (2025), «How we built our multi-agent research system»:
agente líder (LeadResearcher) con plan en memoria, subagentes en paralelo, decisión de seguir o no,
y un agente de citas (CitationAgent) antes del reporte.
manim -s -r 1920,440 f10_deep_research.py DeepResearch     (figura fija)
manim -r 1920,440 --fps 30 f10_deep_research.py DeepResearch   (versión animada, ~15 s)
"""
import numpy as np
from manim import (Scene, VGroup, Polygon, Line, Arrow, Circle, RoundedRectangle, CurvedArrow, FadeIn, Create,
                   LaggedStart, LEFT, RIGHT, UP, DOWN, BOLD, PI, config)
from common import *

config.frame_height = 16.0 * 440 / 1920


def arrow(a, b, color=AXIS, w=3.5):
    return Arrow(a, b, buff=0.08, stroke_color=color, stroke_width=w, tip_length=0.18,
                 max_tip_length_to_length_ratio=0.25, max_stroke_width_to_length_ratio=20)


def card(text, w, h=0.62, size=22, stroke=BORDER, fill=CARD, color=TEXT, weight="NORMAL"):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.12, fill_color=fill, fill_opacity=1,
                           stroke_color=stroke, stroke_width=2.5)
    t = T(text, size=size, color=color, weight=weight, line_spacing=0.85).move_to(box)
    return VGroup(box, t)


def magnifier(color=MUTED):
    c = Circle(radius=0.085, stroke_color=color, stroke_width=2.5)
    h = Line(c.get_center() + np.array([0.06, -0.06, 0]), c.get_center() + np.array([0.15, -0.15, 0]),
             stroke_color=color, stroke_width=3)
    return VGroup(c, h)


class DeepResearch(Scene):
    def construct(self):
        q = card("pregunta", 1.45, size=23).move_to([-6.95, 0.25, 0])
        lead = card("agente\nlíder", 1.75, h=1.0, size=23, stroke=MODEL, fill=PANEL, weight=BOLD).move_to([-4.65, 0.25, 0])
        mem = card("plan → memoria", 2.25, h=0.5, size=19, color=MUTED).next_to(lead, DOWN, buff=0.3)
        # subagentes, cada uno con su ventana de contexto
        subs = VGroup()
        ys = [1.05, 0.4, -0.25, -0.9]
        for y in ys:
            frame = RoundedRectangle(width=2.15, height=0.54, corner_radius=0.1, stroke_color=MODEL, stroke_width=2,
                                     fill_color=PANEL, fill_opacity=1).move_to([-1.55, y, 0])
            inner = RoundedRectangle(width=2.0, height=0.42, corner_radius=0.07, stroke_color=BORDER, stroke_width=1.5,
                                     stroke_opacity=1).move_to(frame)
            m = magnifier(MODEL).move_to(frame.get_left() + RIGHT * 0.3)
            t = T("subagente", size=20, color=TEXT).next_to(m, RIGHT, buff=0.15)
            subs.add(VGroup(frame, inner, m, t))
        par = T("3 a 5 en paralelo, cada uno con su contexto", size=17, color=GRAY).next_to(subs, DOWN, buff=0.12)
        # rombo juez
        dx, dy = 0.95, 0.62
        cx = 1.45
        rh = Polygon([cx, 0.25 + dy, 0], [cx + dx, 0.25, 0], [cx, 0.25 - dy, 0], [cx - dx, 0.25, 0],
                     stroke_color=AMBER, stroke_width=3, fill_color=AMBER, fill_opacity=1)
        rh_t = T("¿basta?", size=23, color=BG, weight=BOLD).move_to(rh)
        judge = VGroup(rh, rh_t)
        cite = card("agente de citas", 2.15, size=21).move_to([4.35, 0.25, 0])
        cite_s = T("cada afirmación ↔ su fuente", size=17, color=GRAY).next_to(cite, DOWN, buff=0.12)
        rep = card("reporte", 1.45, size=23, stroke=TEXT).move_to([6.95, 0.25, 0])

        a_q = arrow(q.get_right(), lead.get_left())
        a_fan = VGroup(*[arrow(lead.get_right(), s[0].get_left()) for s in subs])
        a_in = VGroup(*[arrow(s[0].get_right(), rh.get_vertices()[3]) for s in subs])
        a_yes = arrow(rh.get_vertices()[1], cite.get_left(), color=AMBER)
        yes_t = T("sí", size=20, color=AMBER).next_to(a_yes, UP, buff=0.05)
        a_no = CurvedArrow(rh.get_vertices()[0] + UP * 0.05, subs[0][0].get_right() + RIGHT * 0.08 + UP * 0.12,
                           angle=PI * 0.5, color=AMBER, stroke_width=3.5, tip_length=0.18)
        no_t = T("no → más subagentes", size=19, color=AMBER).move_to([1.8, 1.25, 0], aligned_edge=LEFT)
        a_rep = arrow(cite.get_right(), rep.get_left())

        groups = [VGroup(q), VGroup(a_q, lead, mem), VGroup(a_fan, subs, par), VGroup(a_in, judge),
                  VGroup(a_no, no_t), VGroup(a_yes, yes_t, cite, cite_s), VGroup(a_rep, rep)]
        src = T("según Anthropic (2025), How we built our multi-agent research system", size=16, color=GRAY)
        src.to_corner(DOWN + RIGHT, buff=0.1)
        if config.save_last_frame:
            self.add(*groups, src)
            return
        for g in groups:
            self.play(FadeIn(g, shift=RIGHT * 0.15), run_time=0.8)
            self.wait(0.6)
        self.add(src)
        self.wait(4)
