"""S04 — Atención: cada palabra decide a qué otras palabras mirar (diapositiva 4).

Frase: «El robot no levantó la caja porque estaba muy pesada». Consulta: «pesada».
Si existe atencion.json (lo escribe datos_atencion.py con BETO), usa esos pesos y quita la etiqueta
«ilustrativo». Si no, usa pesos ilustrativos que suman 1.
manim -r 1920,720 --fps 30 s04_atencion.py Atencion
"""
import json
from pathlib import Path

import numpy as np
from manim import (Scene, VGroup, ArcBetweenPoints, Arrow, Line, Rectangle, FadeIn, FadeOut, Create,
                   GrowFromEdge, LaggedStart, Transform, LEFT, RIGHT, UP, DOWN, BOLD, PI)
from common import *

TOKENS = "El robot no levantó la caja porque estaba muy pesada".split()
QUERY = "pesada"
WEIGHTS = [0.02, 0.14, 0.03, 0.08, 0.05, 0.46, 0.04, 0.07, 0.05, 0.06]   # ilustrativos
SOURCE = None
f = Path(__file__).with_name("atencion.json")
if f.exists():
    d = json.loads(f.read_text(encoding="utf-8"))
    TOKENS, QUERY, WEIGHTS = d["tokens"], d["query"], d["weights"]
    SOURCE = f"{d.get('model', 'modelo')} · capa {d.get('layer', '?')} · promedio de cabezas"
W = np.array(WEIGHTS, float)
W = W / W.sum()
QI = TOKENS.index(QUERY)
TOP = int(np.argmax(np.where(np.arange(len(W)) == QI, -1, W)))


class Atencion(Scene):
    def construct(self):
        chips = VGroup(*[TokenChip(t, color=BORDER, size=27) for t in TOKENS]).arrange(RIGHT, buff=0.16)
        if chips.width > 15.2:
            chips.scale_to_fit_width(15.2)
        chips.move_to([0, 0.05, 0])
        title = T(f"¿a qué palabras mira «{QUERY}»?", size=26, color=MUTED).move_to([-7.6, 2.6, 0], aligned_edge=LEFT)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chips], lag_ratio=0.06), run_time=1.3)
        self.play(FadeIn(title), run_time=0.5)

        # 1. la consulta (Q) y las claves (K)
        q = chips[QI]
        q_tag = T("consulta  Q", size=21, color=Q_COL, font=MONO).next_to(q, DOWN, buff=0.2)
        self.play(q.box.animate.set_stroke(Q_COL, width=4), FadeIn(q_tag), run_time=0.7)
        others = [c for k, c in enumerate(chips) if k != QI]
        k_tag = T("claves  K", size=21, color=K_COL, font=MONO).next_to(chips[0], DOWN, buff=0.2).align_to(chips[0], LEFT)
        self.play(*[c.box.animate.set_stroke(K_COL, width=2.5) for c in others], FadeIn(k_tag), run_time=0.7)
        self.wait(0.3)

        # 2. arcos: grosor y opacidad según el peso
        arcs = VGroup()
        for k, c in enumerate(chips):
            if k == QI:
                continue
            L = abs(q.get_x() - c.get_x())
            h = min(1.55, 0.3 + 0.13 * L)
            ang = 4 * np.arctan(h / (L / 2))
            a = ArcBetweenPoints(q.get_top() + UP * 0.05, c.get_top() + UP * 0.05, angle=ang if c.get_x() < q.get_x() else -ang)
            a.set_stroke(Q_COL, width=1.5 + 22 * W[k], opacity=0.25 + 0.75 * W[k] / W.max())
            arcs.add(a)
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.08), FadeOut(k_tag), run_time=1.6)

        # 3. barras de peso debajo de cada palabra
        base_y = -2.35
        bars, vals = VGroup(), VGroup()
        for k, c in enumerate(chips):
            h = max(0.02, 1.55 * W[k] / W.max())
            col = Q_COL if k == QI else (K_COL if k != TOP else TEXT)
            b = Rectangle(width=min(0.55, c.width * 0.7), height=h, fill_color=col, fill_opacity=0.85 if k == TOP else 0.55,
                          stroke_width=0).move_to([c.get_x(), base_y + h / 2, 0])
            v = T(f"{W[k]:.2f}", size=19, color=TEXT if k == TOP else MUTED, font=MONO).next_to(b, UP, buff=0.06)
            bars.add(b)
            vals.add(v)
        axis = Line([chips.get_left()[0] - 0.1, base_y, 0], [chips.get_right()[0] + 0.1, base_y, 0], stroke_color=AXIS, stroke_width=2)
        q_tag2 = q_tag.copy()
        self.play(FadeOut(q_tag), Create(axis), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), run_time=1.2)
        self.play(FadeIn(vals), run_time=0.5)
        wl = T("pesos de atención (suman 1)", size=20, color=GRAY).next_to(axis, DOWN, buff=0.1).align_to(axis, LEFT)
        self.play(FadeIn(wl), run_time=0.4)

        # 4. la palabra más mirada
        top = chips[TOP]
        self.play(top.box.animate.set_stroke(TEXT, width=4), arcs.animate.set_stroke(opacity=0.15),
                  run_time=0.6)
        best_arc = arcs[TOP if TOP < QI else TOP - 1].copy().set_stroke(Q_COL, opacity=1)
        self.play(Create(best_arc), run_time=0.7)
        msg = T(f"«{QUERY}» mira sobre todo a «{TOKENS[TOP]}»: así resuelve a qué se refiere", size=24, color=TEXT)
        msg.move_to([0, 2.55, 0])
        self.play(FadeOut(title), FadeIn(msg, shift=DOWN * 0.1), run_time=0.7)
        formula = T("atención = softmax(Q·Kᵀ / √d) · V", size=21, color=MUTED, font=MONO).move_to(wl, aligned_edge=LEFT)
        self.play(FadeOut(wl), FadeIn(formula), run_time=0.6)
        if SOURCE:
            self.add(illustrative_label(SOURCE))
        else:
            self.add(illustrative_label("pesos ilustrativos · datos_atencion.py calcula los reales"))
        self.wait(3.5)
