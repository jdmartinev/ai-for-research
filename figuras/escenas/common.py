"""Componentes compartidos para las escenas de la charla «¿Quién decide qué cuenta como mejor?».

Lienzo 1920×720 (8:3) → 16 × 6 unidades de Manim (1 unidad = 120 px).
El juez siempre es ámbar. Todo texto en pantalla va en español.
"""
from __future__ import annotations

import numpy as np
from manim import (
    ArcBetweenPoints, Arrow, Circle, Create, CurvedArrow, Dot, FadeIn, Indicate, Line,
    Rectangle, RoundedRectangle, Text, VGroup, config, DOWN, LEFT, RIGHT, UP, BOLD, PI,
    AnimationGroup, Succession, rate_functions,
)

# ---------------------------------------------------------------- lienzo
config.frame_width = 16.0
config.frame_height = 6.0
config.background_color = "#0F1626"

# ---------------------------------------------------------------- paleta
BG = "#0F1626"
PANEL = "#141D2F"
CARD = "#1E2A40"
BORDER = "#2A3550"
AXIS = "#3A475C"
TEXT = "#ECEEF0"
MUTED = "#B9C3CF"
GRAY = "#5B6678"
AMBER = "#F2A541"
MODEL = "#5FA8D3"
Q_COL = "#5FA8D3"
K_COL = "#B39DDB"
V_COL = "#6FC2A5"
ERROR = "#C97B63"

FONT = "IBM Plex Sans"
MONO = "JetBrains Mono"
DISPLAY = "Space Grotesk"


def T(s, size=30, color=TEXT, font=FONT, weight="NORMAL", **kw):
    return Text(s, font=font, font_size=size, color=color, weight=weight, **kw)


def illustrative_label(text="ilustrativo"):
    lab = T(text, size=19, color=GRAY)
    lab.to_corner(DOWN + RIGHT, buff=0.15)
    return lab


# ---------------------------------------------------------------- piezas
class Node(VGroup):
    """Rectángulo redondeado con etiqueta. judge=True → relleno ámbar."""

    def __init__(self, label, judge=False, width=None, size=28, color=MODEL):
        super().__init__()
        self.judge = judge
        txt = T(label, size=size, color=BG if judge else TEXT, weight=BOLD if judge else "NORMAL")
        w = width or max(1.9, txt.width + 0.5)
        box = RoundedRectangle(width=w, height=max(0.72, txt.height + 0.38), corner_radius=0.16,
                               stroke_color=AMBER if judge else color, stroke_width=3,
                               fill_color=AMBER if judge else PANEL, fill_opacity=1)
        txt.move_to(box)
        self.box, self.txt = box, txt
        self.add(box, txt)

    def relabel(self, label, size=28):
        new = T(label, size=size, color=BG if self.judge else TEXT, weight=BOLD if self.judge else "NORMAL")
        new.move_to(self.box)
        return new


class LoopMotif(VGroup):
    """Ciclo de 3 o 4 nodos en sentido horario; el nodo juez va en ámbar."""

    def __init__(self, labels, judge_index, radius=1.7, size=27, node_width=None, xscale=1.25):
        super().__init__()
        n = len(labels)
        self.nodes = VGroup()
        angles = [PI / 2 - 2 * PI * k / n for k in range(n)]  # arriba, luego horario
        for k, (lab, ang) in enumerate(zip(labels, angles)):
            nd = Node(lab, judge=(k == judge_index), size=size, width=node_width)
            nd.move_to(radius * np.array([np.cos(ang) * xscale, np.sin(ang), 0]))
            self.nodes.add(nd)
        self.arrows = VGroup()
        for k in range(n):
            a, b = self.nodes[k], self.nodes[(k + 1) % n]
            start = a.get_center() + 0.0
            end = b.get_center() + 0.0
            arc = ArcBetweenPoints(start, end, angle=-2 * PI / n * 0.9, stroke_color=AXIS, stroke_width=4)
            # recortar los extremos para que no toquen los nodos
            pts = arc.get_all_points()
            arr = CurvedArrow(self._edge(a, end, start), self._edge(b, start, end), angle=-2 * PI / n * 0.55,
                              color=AXIS, stroke_width=4, tip_length=0.22)
            self.arrows.add(arr)
        self.add(self.arrows, self.nodes)

    @staticmethod
    def _edge(node, toward, center_ref):
        c = node.get_center()
        d = toward - c
        d = d / (np.linalg.norm(d) + 1e-9)
        w, h = node.box.width / 2 + 0.08, node.box.height / 2 + 0.08
        t = min(w / (abs(d[0]) + 1e-9), h / (abs(d[1]) + 1e-9))
        return c + d * t

    def pulse(self, i, run_time=0.6):
        nd, ar = self.nodes[i], self.arrows[i]
        anims = [nd.animate(rate_func=rate_functions.there_and_back).scale(1.1),
                 ar.animate(rate_func=rate_functions.there_and_back).set_color(AMBER if nd.judge else MODEL)]
        return AnimationGroup(*anims, run_time=run_time)


class Terminal(VGroup):
    def __init__(self, title, width=6.0, height=3.4):
        super().__init__()
        self.frame = RoundedRectangle(width=width, height=height, corner_radius=0.16,
                                      fill_color=PANEL, fill_opacity=1, stroke_color=BORDER, stroke_width=2)
        top = self.frame.get_top()[1] - 0.28
        dots = VGroup(*[Circle(radius=0.06, fill_color=GRAY, fill_opacity=1, stroke_width=0) for _ in range(3)])
        dots.arrange(RIGHT, buff=0.12).move_to([self.frame.get_left()[0] + 0.4, top, 0])
        ttl = T(title, size=22, color=MUTED, font=MONO).move_to([self.frame.get_center()[0], top, 0])
        div = Line([self.frame.get_left()[0], top - 0.27, 0], [self.frame.get_right()[0], top - 0.27, 0],
                   stroke_color=BORDER, stroke_width=2)
        self.add(self.frame, dots, ttl, div)

    @property
    def body_top(self):
        """Primera línea útil bajo la barra de título (se calcula después de mover la terminal)."""
        return self.frame.get_top()[1] - 0.83


class TokenChip(VGroup):
    def __init__(self, text, color=MODEL, size=28, fill=PANEL):
        super().__init__()
        t = T(text, size=size, color=TEXT, font=MONO)
        box = RoundedRectangle(width=t.width + 0.32, height=t.height + 0.3, corner_radius=0.12,
                               stroke_color=color, stroke_width=2.5, fill_color=fill, fill_opacity=1)
        t.move_to(box)
        self.box, self.txt = box, t
        self.add(box, t)


def stamp(word, color, size=28):
    return T(word, size=size, color=color, weight=BOLD)


class BigNumber(VGroup):
    def __init__(self, value, caption, color=TEXT, size=96, cap_size=28, cap_width=None):
        super().__init__()
        v = T(value, size=size, color=color, font=DISPLAY, weight=BOLD)
        c = T(caption, size=cap_size, color=MUTED)
        if cap_width and c.width > cap_width:
            c = Text(caption, font=FONT, font_size=cap_size, color=MUTED).scale_to_fit_width(cap_width)
        VGroup(v, c).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        self.value, self.caption = v, c
        self.add(v, c)


def wrap(text, n):
    """Parte un texto en líneas de como máximo n caracteres (por palabras)."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return "\n".join(lines)
