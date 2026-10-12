"""S09 — Un agente cierra el ciclo con el mundo: las herramientas le responden (diapositiva 9).

Traza ilustrativa (se reemplaza con trace.json si existe: [{"pensar","herramienta","resultado"}]).
manim -r 1920,720 --fps 30 s09_agente.py Agente
"""
import json
from pathlib import Path

from manim import (Scene, VGroup, Line, Circle, RoundedRectangle, Rectangle, FadeIn, FadeOut, Create,
                   Write, Transform, ReplacementTransform, LaggedStart, AnimationGroup, LEFT, RIGHT, UP, DOWN,
                   BOLD, rate_functions)
from common import *

TRACE = [
    {"pensar": "buscar estudios en humanos", "herramienta": "búsqueda",
     "resultado": "4 de 12 con humanos"},
    {"pensar": "comparar sus efectos", "herramienta": "código",
     "resultado": "tabla de efectos lista"},
    {"pensar": "guardar reporte con fuentes", "herramienta": "archivos",
     "resultado": "reporte.md escrito"},
]
f = Path(__file__).with_name("trace.json")
REAL = f.exists()
if REAL:
    TRACE = json.loads(f.read_text(encoding="utf-8"))[:3]


def icon(kind, color):
    """Íconos de línea simples, sin marcas."""
    if kind == "búsqueda":
        c = Circle(radius=0.17, stroke_color=color, stroke_width=4)
        h = Line(c.get_center() + [0.12, -0.12, 0], c.get_center() + [0.3, -0.3, 0], stroke_color=color, stroke_width=5)
        return VGroup(c, h)
    if kind == "código":
        return T("</>", size=30, color=color, font=MONO, weight=BOLD)
    if kind == "archivos":
        r = RoundedRectangle(width=0.36, height=0.46, corner_radius=0.05, stroke_color=color, stroke_width=4)
        l1 = Line(r.get_left() + [0.08, 0.06, 0], r.get_right() + [-0.08, 0.06, 0], stroke_color=color, stroke_width=3)
        l2 = Line(r.get_left() + [0.08, -0.08, 0], r.get_right() + [-0.08, -0.08, 0], stroke_color=color, stroke_width=3)
        return VGroup(r, l1, l2)
    return T("{ }", size=30, color=color, font=MONO, weight=BOLD)


class Agente(Scene):
    def construct(self):
        loop = LoopMotif(["observar", "pensar", "actuar", "resultado"], judge_index=3, radius=1.6, xscale=1.42).shift(LEFT * 4.35)
        # herramientas
        names = ["búsqueda", "código", "archivos", "API"]
        tools = VGroup()
        for nm in names:
            card = RoundedRectangle(width=2.7, height=0.82, corner_radius=0.14, fill_color=PANEL, fill_opacity=1,
                                    stroke_color=BORDER, stroke_width=2)
            ic = icon(nm, MUTED).scale_to_fit_height(0.4)
            lab = T(nm, size=27, color=MUTED)
            VGroup(ic, lab).arrange(RIGHT, buff=0.25).move_to(card)
            tools.add(VGroup(card, ic, lab))
        tools.arrange(DOWN, buff=0.22).move_to([0.55, -0.1, 0])
        tools_title = T("herramientas", size=24, color=GRAY).next_to(tools, UP, buff=0.25)
        term = Terminal("traza del agente", width=5.75, height=4.9).move_to([4.95, -0.05, 0])

        self.play(LaggedStart(*[FadeIn(n) for n in loop.nodes], lag_ratio=0.15), run_time=1.2)
        self.play(Create(loop.arrows), run_time=1.0)
        self.play(FadeIn(tools_title), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in tools], lag_ratio=0.12),
                  FadeIn(term), run_time=1.2)

        y = term.body_top
        lines = VGroup()
        x_left = term.frame.get_left()[0] + 0.3
        for lap, step in enumerate(TRACE):
            slow = lap == 0
            rt = 1.5 if slow else 0.95
            k = names.index(step["herramienta"]) if step["herramienta"] in names else 3
            # observar
            self.play(loop.pulse(0, run_time=rt * 0.6))
            # pensar
            th = T(wrap("pensar: " + step["pensar"], 40), size=18, color=TEXT, font=MONO, line_spacing=0.9)
            th.move_to([x_left, y, 0], aligned_edge=UP + LEFT)
            self.play(loop.pulse(1, run_time=rt * 0.6), FadeIn(th, shift=RIGHT * 0.1, run_time=rt * 0.6))
            y -= th.height + 0.12
            # actuar → se enciende la herramienta
            act = T(f"actuar: {step['herramienta']}(…)", size=18, color=MODEL, font=MONO)
            act.move_to([x_left, y, 0], aligned_edge=UP + LEFT)
            card = tools[k][0]
            self.play(loop.pulse(2, run_time=rt * 0.6), card.animate(run_time=rt * 0.5).set_stroke(MODEL, width=4),
                      tools[k][2].animate(run_time=rt * 0.5).set_color(TEXT), FadeIn(act, run_time=rt * 0.5))
            y -= act.height + 0.12
            # la herramienta responde → resultado (juez)
            res_txt = T(step["resultado"], size=21, color=BG, weight=BOLD)
            res_card = RoundedRectangle(width=res_txt.width + 0.4, height=0.55, corner_radius=0.12, fill_color=AMBER,
                                        fill_opacity=1, stroke_width=0).move_to(card)
            res_txt.move_to(res_card)
            res = VGroup(res_card, res_txt)
            self.play(FadeIn(res, run_time=rt * 0.35))
            self.play(res.animate(run_time=rt * 0.8).scale(0.8).move_to(loop.nodes[3].get_center() + DOWN * 0.75 + RIGHT * 0.4),
                      card.animate(run_time=rt * 0.5).set_stroke(BORDER, width=2),
                      tools[k][2].animate(run_time=rt * 0.5).set_color(MUTED))
            out = T(f"resultado: {step['resultado']}", size=18, color=AMBER, font=MONO)
            out.move_to([x_left, y, 0], aligned_edge=UP + LEFT)
            self.play(loop.pulse(3, run_time=rt * 0.6), FadeOut(res, run_time=rt * 0.5), FadeIn(out, run_time=rt * 0.5))
            y -= out.height + 0.32
            lines.add(th, act, out)
            if slow:
                self.wait(0.6)

        # respuesta final
        ans_txt = T("respuesta", size=25, color=TEXT, weight=BOLD)
        ans_box = RoundedRectangle(width=ans_txt.width + 0.45, height=0.7, corner_radius=0.14, fill_color=PANEL,
                                   fill_opacity=1, stroke_color=AMBER, stroke_width=3)
        ans = VGroup(ans_box, ans_txt.move_to(ans_box)).move_to(loop.get_center())
        self.play(FadeIn(ans, scale=0.7), run_time=0.8)
        cap = T("cada resultado es el juez de la vuelta siguiente", size=23, color=MUTED)
        cap.move_to([loop.get_center()[0], -2.72, 0])
        if not REAL:
            self.add(illustrative_label("traza ilustrativa"))
        self.play(FadeIn(cap), run_time=0.6)
        self.wait(3.0)
