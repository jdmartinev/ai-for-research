"""F03 — Un modelo de lenguaje predice el siguiente token (diapositiva 3, figura fija).

Si existe siguiente_token.json (lo escribe datos_siguiente_token.py con Qwen2.5-0.5B), usa esos datos.
Si no, usa probabilidades ilustrativas y lo dice en la leyenda.
manim -s -r 1920,720 f03_siguiente_token.py SiguienteToken
"""
import json
from pathlib import Path

from manim import Scene, VGroup, Rectangle, Line, LEFT, RIGHT, UP, DOWN, BOLD
from common import *

PROMPT = "Durante la fase de apoyo de la marcha, la rodilla"
DATA = [("␣se", 0.214), ("␣debe", 0.098), ("␣está", 0.087), ("␣es", 0.071),
        ("␣permanece", 0.064), ("␣no", 0.052), ("␣tiene", 0.041), ("␣realiza", 0.033)]
LEGEND = "probabilidades ilustrativas · datos_siguiente_token.py calcula las reales con Qwen2.5-0.5B"
f = Path(__file__).with_name("siguiente_token.json")
if f.exists():
    d = json.loads(f.read_text(encoding="utf-8"))
    PROMPT, DATA = d["prompt"], [(t, p) for t, p in d["top"]]
    LEGEND = f"{d['model']} · una sola pasada · softmax de la última posición"


class SiguienteToken(Scene):
    def construct(self):
        prompt = T(PROMPT, size=26, color=TEXT, font=MONO)
        cursor = Rectangle(width=0.16, height=0.36, fill_color=MODEL, fill_opacity=1, stroke_width=0)
        line = VGroup(prompt, cursor).arrange(RIGHT, buff=0.08).move_to([0, 2.45, 0])
        if line.width > 15:
            line.scale_to_fit_width(15)
        self.add(line)
        x_chip, x_bar, wmax = -3.2, -2.85, 8.4
        pmax = max(p for _, p in DATA)
        for k, (tok, p) in enumerate(DATA):
            y = 1.6 - k * 0.47
            chip = T(tok, size=24, color=TEXT if k == 0 else MUTED, font=MONO).move_to([x_chip, y, 0], aligned_edge=RIGHT)
            w = wmax * p / pmax
            bar = Rectangle(width=w, height=0.3, fill_color=MODEL, fill_opacity=0.95 if k == 0 else 0.6,
                            stroke_width=0).move_to([x_bar, y, 0], aligned_edge=LEFT)
            val = T(f"{100 * p:.1f}%", size=20, color=TEXT if k == 0 else MUTED, font=MONO).next_to(bar, RIGHT, buff=0.15)
            self.add(chip, bar, val)
        axis = Line([x_bar, 1.85, 0], [x_bar, 1.6 - 7 * 0.47 - 0.25, 0], stroke_color=AXIS, stroke_width=2)
        self.add(axis)
        top = sum(p for _, p in DATA)
        foot = T(f"estos 8 suman {100 * top:.1f}%; el resto se reparte entre todo el vocabulario",
                 size=19, color=GRAY).move_to([x_bar, -2.25, 0], aligned_edge=LEFT).shift(DOWN * 0.05)
        self.add(foot, illustrative_label(LEGEND))
