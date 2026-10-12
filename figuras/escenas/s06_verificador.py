"""S06 — Un verificador como juez: refuerzo con recompensas verificables (diapositiva 6).

Juguete calculado: una política softmax sobre 6 respuestas candidatas a «17 × 24 = ?».
Cada paso muestrea 8 respuestas; el verificador da 1 si es 408 y 0 si no; REINFORCE con línea base
(promedio del lote) actualiza los logits. Semilla fija. Nadie le muestra al modelo cómo multiplicar.
manim -r 1920,720 --fps 30 s06_verificador.py Verificador
"""
import numpy as np
from manim import (Scene, VGroup, Line, Rectangle, Arrow, CurvedArrow, FadeIn, FadeOut, Create, Transform,
                   GrowFromCenter, LaggedStart, LEFT, RIGHT, UP, DOWN, BOLD, PI, rate_functions)
from common import *

CANDS = [398, 408, 418, 308, 428, 388]
CORRECT = 408
P0 = np.array([0.30, 0.12, 0.22, 0.14, 0.12, 0.10])
BATCH, STEPS, LR = 8, 30, 1.0
RNG = np.random.default_rng(3)


def train():
    logits = np.log(P0)
    hist, samples = [], []
    for _ in range(STEPS + 1):
        p = np.exp(logits - logits.max())
        p /= p.sum()
        hist.append(p.copy())
        idx = RNG.choice(len(CANDS), size=BATCH, p=p)
        r = np.array([CANDS[i] == CORRECT for i in idx], float)
        samples.append((idx, r))
        adv = r - r.mean()
        grad = np.zeros_like(logits)
        for i, A in zip(idx, adv):
            oh = np.zeros_like(logits)
            oh[i] = 1
            grad += A * (oh - p)
        logits = logits + LR * grad / BATCH
    return hist, samples


HIST, SAMPLES = train()
CI = CANDS.index(CORRECT)


class Verificador(Scene):
    def construct(self):
        prompt = TokenChip("17 × 24 = ?", color=MUTED, size=30).move_to([-5.9, 2.1, 0])
        model = Node("modelo", size=27).move_to([-5.9, 0.55, 0])
        samp_lab = T("8 respuestas muestreadas", size=20, color=GRAY).move_to([-2.35, 2.3, 0])
        a1 = Arrow(prompt.get_bottom(), model.get_top(), buff=0.1, stroke_color=AXIS, stroke_width=4,
                   max_tip_length_to_length_ratio=0.3)
        judge = Node("verificador", judge=True, size=27).move_to([1.65, 0.55, 0])
        rule = T("1 si es 408\n0 si no", size=20, color=MUTED, font=MONO, line_spacing=0.9).next_to(judge, UP, buff=0.2)
        # posiciones de las 8 muestras: 2 columnas × 4 filas
        slots = [np.array([-3.65 + 2.35 * (k // 4), 1.65 - 0.66 * (k % 4), 0]) for k in range(BATCH)]

        # gráfica de probabilidades
        base_y, hmax, x0, dx = -1.85, 3.15, 3.9, 0.74
        axis = Line([x0 - 0.45, base_y, 0], [x0 + dx * 5 + 0.45, base_y, 0], stroke_color=AXIS, stroke_width=2)
        names = VGroup(*[T(str(c), size=21, color=TEXT if c == CORRECT else MUTED, font=MONO,
                           weight=BOLD if c == CORRECT else "NORMAL").move_to([x0 + dx * i, base_y - 0.25, 0])
                         for i, c in enumerate(CANDS)])

        def bars(p):
            return VGroup(*[Rectangle(width=0.52, height=max(0.02, hmax * p[i]), stroke_width=0,
                                      fill_color=V_COL if i == CI else MODEL, fill_opacity=0.9 if i == CI else 0.55)
                            .move_to([x0 + dx * i, base_y + max(0.02, hmax * p[i]) / 2, 0]) for i in range(len(CANDS))])

        def ptxt(p, step):
            return VGroup(T(f"P(408) = {p[CI]:.2f}", size=24, color=TEXT, font=MONO, weight=BOLD),
                          T(f"paso {step}", size=21, color=GRAY, font=MONO)).arrange(RIGHT, buff=0.4) \
                .move_to([x0 + dx * 2.5, 2.55, 0])

        chart_t = T("probabilidad de cada respuesta", size=20, color=GRAY).move_to([x0 + dx * 2.5, 2.05, 0])
        bb = bars(HIST[0])
        pt = ptxt(HIST[0], 0)

        self.play(FadeIn(prompt), run_time=0.6)
        self.play(Create(a1), FadeIn(model), FadeIn(samp_lab), run_time=0.7)
        self.play(FadeIn(judge), FadeIn(rule), Create(axis), FadeIn(names), FadeIn(bb), FadeIn(pt), FadeIn(chart_t),
                  run_time=1.0)
        self.add(illustrative_label("refuerzo de juguete, calculado"))

        back = CurvedArrow(judge.get_bottom() + DOWN * 0.1, model.get_bottom() + DOWN * 0.1 + RIGHT * 0.4, angle=-PI * 0.42,
                           color=AMBER, stroke_width=4, tip_length=0.22)
        back_lab = T("actualizar pesos (REINFORCE)", size=20, color=AMBER).next_to(back, DOWN, buff=0.08)
        chips = VGroup()
        for s in range(STEPS):
            idx, r = SAMPLES[s]
            slow = s < 2
            new_chips = VGroup()
            for k, (i, ok) in enumerate(zip(idx, r)):
                c = TokenChip(str(CANDS[i]), color=BORDER, size=22).move_to(slots[k] + LEFT * 0.4)
                w = stamp("correcta" if ok else "incorrecta", AMBER if ok else GRAY, size=17).next_to(c, RIGHT, buff=0.12)
                new_chips.add(VGroup(c, w))
            if slow:
                self.play(FadeOut(chips), LaggedStart(*[FadeIn(nc[0], shift=RIGHT * 0.3) for nc in new_chips], lag_ratio=0.1),
                          model.animate(rate_func=rate_functions.there_and_back).scale(1.08), run_time=1.2)
                self.play(judge.animate(rate_func=rate_functions.there_and_back).scale(1.1), run_time=0.5)
                self.play(LaggedStart(*[GrowFromCenter(nc[1]) for nc in new_chips], lag_ratio=0.08),
                          *[nc[0].box.animate.set_stroke(AMBER if ok else BORDER, width=3 if ok else 2.5)
                            for nc, ok in zip(new_chips, r)], run_time=1.0)
                self.wait(0.4)
                anims = [Transform(bb, bars(HIST[s + 1])), Transform(pt, ptxt(HIST[s + 1], s + 1))]
                if s == 0:
                    self.play(Create(back), FadeIn(back_lab), run_time=0.7)
                self.play(*anims, back.animate(rate_func=rate_functions.there_and_back).set_stroke(width=7), run_time=1.0)
                self.wait(0.3)
            else:
                for nc, ok in zip(new_chips, r):
                    nc[0].box.set_stroke(AMBER if ok else BORDER, width=3 if ok else 2.5)
                rt = 0.5 if s < 8 else 0.3
                self.play(FadeOut(chips), FadeIn(new_chips), Transform(bb, bars(HIST[s + 1])),
                          Transform(pt, ptxt(HIST[s + 1], s + 1)), run_time=rt, rate_func=rate_functions.linear)
            chips = new_chips
        self.wait(0.6)
        cap = T("nadie le mostró cómo multiplicar: solo un verificador que dice sí o no",
                size=23, color=TEXT).move_to([-7.6, -2.55, 0], aligned_edge=LEFT)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.7)
        self.wait(3.5)
