"""S17 — Co-Scientist: los agentes juzgan las hipótesis, y luego el laboratorio (diapositiva 17).

Torneo ilustrativo con Elo calculado (K = 32, inicio 1,200), como describe Gottweis et al. (Nature 2026).
Calidades ocultas y resultados sorteados con la probabilidad de victoria Elo; semilla fija.
Si existe hipotesis.txt (una por línea, 8 líneas), usa esos títulos.
manim -r 1920,720 --fps 30 s17_torneo.py Torneo
"""
from pathlib import Path

import numpy as np
from manim import (Scene, VGroup, Line, RoundedRectangle, Polygon, FadeIn, FadeOut, Create, Transform,
                   LaggedStart, ReplacementTransform, LEFT, RIGHT, UP, DOWN, BOLD, rate_functions)
from common import *

RNG = np.random.default_rng(11)
TITLES = [f"Hipótesis {i}" for i in range(1, 9)]
f = Path(__file__).with_name("hipotesis.txt")
if f.exists():
    TITLES = [ln.strip() for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()][:8]
QUALITY = RNG.normal(1200, 140, 8)          # calidad oculta (en escala Elo)
K = 32


def p_win(a, b):
    return 1 / (1 + 10 ** ((b - a) / 400))


def simulate():
    elo = np.full(8, 1200.0)
    rounds, alive = [], list(range(8))
    while len(alive) > 1:
        matches, nxt = [], []
        for a, b in zip(alive[::2], alive[1::2]):
            win_a = RNG.random() < p_win(QUALITY[a], QUALITY[b])
            w, l = (a, b) if win_a else (b, a)
            exp_w = p_win(elo[w], elo[l])
            elo[w] += K * (1 - exp_w)
            elo[l] -= K * (1 - exp_w)
            matches.append((a, b, w, elo.copy()))
            nxt.append(w)
        rounds.append(matches)
        alive = nxt
    return rounds, alive[0]


ROUNDS, CHAMP = simulate()


class Torneo(Scene):
    def hcard(self, k, w=2.15):
        box = RoundedRectangle(width=w, height=0.52, corner_radius=0.12, fill_color=PANEL, fill_opacity=1,
                               stroke_color=MODEL, stroke_width=2.5)
        t = T(TITLES[k], size=21, color=TEXT)
        if t.width > w - 0.25:
            t.scale_to_fit_width(w - 0.25)
        return VGroup(box, t.move_to(box))

    def construct(self):
        xs = [-6.65, -4.2, -1.75, 0.7]              # columnas: 8 → 4 → 2 → campeona
        ys0 = [2.1 - i * 0.62 for i in range(8)]     # 8 hipótesis
        cards = [self.hcard(k).move_to([xs[0], ys0[k], 0]) for k in range(8)]
        title = T("torneo de hipótesis", size=23, color=GRAY).move_to([xs[0] - 1.07, 2.72, 0], aligned_edge=LEFT)
        # tabla Elo
        tbl_title = T("Elo", size=24, color=MUTED, weight=BOLD).move_to([4.85, 2.55, 0], aligned_edge=LEFT)

        def table(elo):
            order = np.argsort(-elo)
            rows = VGroup()
            for r, k in enumerate(order):
                name = T(TITLES[k], size=20, color=AMBER if k == CHAMP and r == 0 else TEXT)
                if name.width > 2.3:
                    name.scale_to_fit_width(2.3)
                val = T(f"{elo[k]:,.0f}", size=20, color=MUTED, font=MONO)
                name.move_to([4.85, 2.05 - r * 0.47, 0], aligned_edge=LEFT)
                val.move_to([7.75, 2.05 - r * 0.47, 0], aligned_edge=RIGHT)
                rows.add(VGroup(name, val))
            return rows

        tbl = table(np.full(8, 1200.0))
        self.play(FadeIn(title), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cards], lag_ratio=0.08),
                  FadeIn(tbl_title), FadeIn(tbl), run_time=1.6)
        note = illustrative_label("torneo ilustrativo · Elo calculado")
        self.add(note)

        pos = {k: cards[k] for k in range(8)}
        ys = {k: ys0[k] for k in range(8)}
        lines = VGroup()
        for r, matches in enumerate(ROUNDS):
            slow = r == 0
            for (a, b, w, elo) in matches:
                ca, cb = pos[a], pos[b]
                y_mid = (ys[a] + ys[b]) / 2
                # debate: dos marcas que se alternan
                deb = VGroup(T("debate", size=19, color=GRAY)).move_to([(xs[r] + xs[r + 1]) / 2 + 0.05, y_mid, 0])
                ln = VGroup(
                    Line(ca.get_right(), [ca.get_right()[0] + 0.25, ys[a], 0], stroke_color=AXIS, stroke_width=3),
                    Line(cb.get_right(), [cb.get_right()[0] + 0.25, ys[b], 0], stroke_color=AXIS, stroke_width=3),
                    Line([ca.get_right()[0] + 0.25, ys[a], 0], [ca.get_right()[0] + 0.25, ys[b], 0], stroke_color=AXIS, stroke_width=3),
                )
                winner = self.hcard(w).move_to([xs[r + 1], y_mid, 0])
                winner[0].set_stroke(AMBER, width=3.5)
                loser = pos[b if w == a else a]
                rt = 1.25 if slow else 0.8
                self.play(Create(ln), ca[0].animate.set_stroke(TEXT, width=3), cb[0].animate.set_stroke(TEXT, width=3),
                          run_time=rt * 0.6)
                new_tbl = table(elo)
                self.play(ReplacementTransform(pos[w].copy(), winner),
                          loser.animate.set_opacity(0.35), Transform(tbl, new_tbl), run_time=rt)
                lines.add(ln)
                pos[w] = winner
                ys[w] = y_mid
            if slow:
                self.wait(0.4)
        # la campeona va al laboratorio
        champ = pos[CHAMP]
        lab_box = RoundedRectangle(width=2.45, height=2.75, corner_radius=0.18, fill_color=PANEL, fill_opacity=1,
                                   stroke_color=AMBER, stroke_width=3).move_to([3.25, -0.35, 0])
        flask = VGroup(
            Line([-0.12, 0.42, 0], [-0.12, 0.1, 0]), Line([0.12, 0.42, 0], [0.12, 0.1, 0]),
            Line([-0.12, 0.1, 0], [-0.42, -0.38, 0]), Line([0.12, 0.1, 0], [0.42, -0.38, 0]),
            Line([-0.42, -0.38, 0], [0.42, -0.38, 0]), Line([-0.2, 0.42, 0], [0.2, 0.42, 0]),
        ).set_stroke(AMBER, width=4).move_to(lab_box.get_top() + DOWN * 0.62)
        lab_lab = T("validación en\nlaboratorio", size=22, color=TEXT, line_spacing=0.9).next_to(flask, DOWN, buff=0.15)
        self.play(FadeIn(lab_box), Create(flask), FadeIn(lab_lab), run_time=0.9)
        self.bring_to_front(champ)
        self.play(champ.animate.scale(0.95).move_to(lab_box.get_bottom() + UP * 0.45), run_time=1.1)
        cap = T("generar · reflexionar\nrankear · evolucionar", size=22, color=MUTED, line_spacing=0.9).move_to([6.15, -1.95, 0])
        self.play(FadeIn(cap), run_time=0.6)
        self.wait(3.5)
