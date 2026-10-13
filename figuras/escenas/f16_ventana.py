"""F16 — La ventana de contexto: todo lo que el modelo ve. Figura fija 1920×720.

Tamaños de los segmentos: ejemplo ilustrativo de una sesión de trabajo, en tokens.
manim -s -r 1920,720 f16_ventana.py Ventana
"""
from manim import Scene, VGroup, Rectangle, RoundedRectangle, Line, Brace, LEFT, RIGHT, UP, DOWN, BOLD
from common import *

TOTAL = 200_000
SEG = [("instrucciones, CLAUDE.md y skills", 9_000, AMBER),
       ("3 papers tuyos", 36_000, MODEL), ("conversación", 22_000, "#8FB8D8"),
       ("resultados de\nherramientas", 61_000, "#4A7FA6")]
OUT = ["tu disco duro", "papers que no le diste", "lo que pasó después\nde su fecha de corte"]


class Ventana(Scene):
    def construct(self):
        W, x0, y = 14.8, -7.4, 0.35
        frame = RoundedRectangle(width=W + 0.16, height=1.36, corner_radius=0.12, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to([x0 + W / 2, y, 0])
        x = x0
        parts = VGroup()
        for name, n, c in SEG:
            w = W * n / TOTAL
            r = Rectangle(width=w, height=1.2, stroke_width=0, fill_color=c, fill_opacity=0.9).move_to([x + w / 2, y, 0])
            lab = T(name, size=19, color=TEXT, line_spacing=0.85)
            num = T(f"{n // 1000}k", size=17, color=MUTED, font=MONO)
            if w > 1.4:
                VGroup(lab, num).arrange(DOWN, buff=0.08).move_to(r).set_color(BG)
                if lab.width > w - 0.15:
                    VGroup(lab, num).scale_to_fit_width(w - 0.2)
            else:
                VGroup(lab, num).arrange(RIGHT, buff=0.15).next_to(r, DOWN, buff=0.25).align_to(r, LEFT)
            parts.add(VGroup(r, lab, num))
            x += w
        free = T("libre", size=20, color=GRAY).move_to([(x + x0 + W) / 2, y, 0])
        title = T("ventana de contexto · 200,000 tokens", size=26, color=TEXT, weight=BOLD).move_to([x0, 2.6, 0], aligned_edge=LEFT)
        sub = T("lo que el modelo ve en este momento", size=21, color=MUTED).next_to(title, DOWN, buff=0.1).align_to(title, LEFT)
        out_t = T("fuera de la ventana: no existe para el modelo", size=21, color=MUTED).move_to([x0, -1.25, 0], aligned_edge=LEFT)
        outs = VGroup(*[RoundedRectangle(width=3.6, height=0.8, corner_radius=0.1, stroke_color=BORDER, stroke_width=1.5, fill_color=PANEL, fill_opacity=1) for _ in OUT]).arrange(RIGHT, buff=0.3)
        outs.next_to(out_t, DOWN, buff=0.18).align_to(out_t, LEFT)
        out_l = VGroup(*[T(t, size=18, color=GRAY, line_spacing=0.85).move_to(b) for t, b in zip(OUT, outs)])
        self.add(title, sub, frame, parts, free, out_t, outs, out_l)
        self.add(illustrative_label("segmentos ilustrativos de una sesión de trabajo · un paper de ~10 páginas ≈ 10-15k tokens"))
