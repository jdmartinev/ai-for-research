"""S18 — ERA y AlphaEvolve escriben código y dejan que un evaluador lo juzgue (diapositiva 18).

Búsqueda evolutiva de juguete, calculada: 12 puntos en un cuadrado unitario; puntaje = distancia
mínima entre pares; mutación gaussiana; se conservan los 4 mejores. Semilla fija.
Cierra con dos resultados publicados: ERA (Aygün et al., Nature 2026) y AlphaEvolve (Novikov et al., 2025).
manim -r 1920,720 --fps 30 s18_evolucion.py Evolucion
"""
import numpy as np
from manim import (Scene, VGroup, Axes, Line, Dot, Square, RoundedRectangle, FadeIn, FadeOut, Create, Transform,
                   LaggedStart, AnimationGroup, ReplacementTransform, LEFT, RIGHT, UP, DOWN, BOLD, rate_functions)
from common import *

RNG = np.random.default_rng(7)
N_PTS, POP, KEEP, GENS = 12, 12, 4, 200


def score(p):
    d = np.sqrt(((p[:, None, :] - p[None, :, :]) ** 2).sum(-1))
    d[np.diag_indices(len(p))] = np.inf
    return d.min()


def evolve():
    pop = [RNG.random((N_PTS, 2)) for _ in range(POP)]
    snaps, best_curve = {}, []
    for g in range(GENS + 1):
        sc = np.array([score(p) for p in pop])
        order = np.argsort(-sc)
        pop = [pop[i] for i in order]
        sc = sc[order]
        best_curve.append(sc[0])
        snaps[g] = ([p.copy() for p in pop], sc.copy())
        sigma = 0.06 * (1 - g / GENS) + 0.006
        parents = pop[:KEEP]
        children = []
        for k in range(POP - KEEP):
            par = parents[k % KEEP]
            children.append(np.clip(par + RNG.normal(0, sigma, par.shape), 0, 1))
        pop = parents + children
    return snaps, np.array(best_curve)


SNAPS, BEST = evolve()
SHOW = [0, 1, 10, 25, 50, 100, 200]


class Evolucion(Scene):
    def card(self, pts, side=1.0):
        sq = Square(side_length=side, stroke_color=BORDER, stroke_width=2, fill_color=PANEL, fill_opacity=1)
        dots = VGroup(*[Dot(sq.get_corner(DOWN + LEFT) + np.array([x * side * 0.86 + side * 0.07,
                                                                     y * side * 0.86 + side * 0.07, 0]),
                            radius=0.032, color=TEXT) for x, y in pts])
        return VGroup(sq, dots)

    def construct(self):
        side, gap, vgap = 0.95, 0.22, 0.5
        origin = np.array([-6.95, 1.75, 0])
        pops, scs = SNAPS[0]
        cards = VGroup()
        for k, p in enumerate(pops):
            c = self.card(p, side)
            r, col = divmod(k, 4)
            c.move_to(origin + np.array([col * (side + gap) + side / 2, -r * (side + vgap) - side / 2, 0]))
            cards.add(c)
        title = T("población de programas", size=23, color=GRAY).next_to(cards, UP, buff=0.18).align_to(cards, LEFT)
        judge = Node("evaluador", judge=True, size=27).move_to([0.55, 0.15, 0])
        rule = T("puntaje = distancia mínima\nentre puntos", size=20, color=MUTED, line_spacing=0.9).next_to(judge, DOWN, buff=0.22)
        gen_lab = T("generación 0", size=24, color=MUTED, font=MONO).next_to(judge, UP, buff=0.35)
        axes = Axes(x_range=[0, GENS, 50], y_range=[0, float(BEST.max()) * 1.15, 0.1], x_length=4.3, y_length=3.4,
                    tips=False, axis_config={"color": AXIS, "stroke_width": 2, "include_ticks": False}).move_to([5.55, 0.25, 0])
        ylab = T("mejor puntaje", size=21, color=MUTED).next_to(axes, UP, buff=0.12).align_to(axes, LEFT)
        xlab = T("generación →", size=21, color=MUTED).next_to(axes, DOWN, buff=0.12).align_to(axes, RIGHT)
        note = illustrative_label("búsqueda evolutiva de juguete, calculada · ERA y AlphaEvolve usan un LLM para proponer código")

        self.play(FadeIn(title), LaggedStart(*[FadeIn(c, scale=0.9) for c in cards], lag_ratio=0.05), run_time=1.4)
        self.play(FadeIn(judge), FadeIn(rule), FadeIn(gen_lab), Create(axes), FadeIn(ylab), FadeIn(xlab), FadeIn(note),
                  run_time=1.0)

        curve_pts = []
        curve = VGroup()

        def judge_round(g, slow):
            pops, scs = SNAPS[g]
            new_cards = VGroup()
            for k, p in enumerate(pops):
                c = self.card(p, side).move_to(cards[k])
                new_cards.add(c)
            labels = VGroup()
            for k in range(POP):
                lab = T(f"{scs[k]:.2f}", size=19, color=AMBER if k < KEEP else MUTED, font=MONO)
                lab.next_to(new_cards[k], DOWN, buff=0.07)
                labels.add(lab)
            return new_cards, labels

        # generación 0 y 1, lentas
        prev_labels = VGroup()
        for g in SHOW:
            slow = g in (0, 1)
            new_cards, labels = judge_round(g, slow)
            gl = T(f"generación {g}", size=24, color=MUTED, font=MONO).move_to(gen_lab)
            x0 = curve_pts[-1][0] if curve_pts else None
            pt = axes.c2p(g, BEST[g])
            seg = None
            if curve_pts:
                # dibujar la curva escalonada desde la última generación mostrada
                gs = list(range(curve_pts[-1][1], g + 1))
                pts = [axes.c2p(x, BEST[x]) for x in gs]
                seg = VGroup(*[Line(pts[i], pts[i + 1], stroke_color=AMBER, stroke_width=4) for i in range(len(pts) - 1)])
            curve_pts.append((pt, g))
            rt = 1.4 if slow else 0.8
            anims = [Transform(cards, new_cards), Transform(gen_lab, gl), FadeOut(prev_labels)]
            if seg is not None:
                anims.append(Create(seg))
            else:
                first_dot = Dot(pt, radius=0.05, color=AMBER)
                curve.add(first_dot)
                anims.append(FadeIn(first_dot))
            self.play(*anims, judge.animate(rate_func=rate_functions.there_and_back).scale(1.08), run_time=rt)
            # el juez marca: 4 conservados (ámbar), el resto gris
            marks = [cards[k][0].animate.set_stroke(AMBER if k < KEEP else BORDER, width=4 if k < KEEP else 2)
                     for k in range(POP)]
            fades = [cards[k][1].animate.set_opacity(1 if k < KEEP else 0.35) for k in range(POP)]
            self.play(*marks, *fades, FadeIn(labels), run_time=0.8 if slow else 0.35)
            if slow:
                self.wait(0.6)
            prev_labels = labels
            if seg is not None:
                curve.add(seg)

        # zoom a la mejor solución
        best = self.card(SNAPS[GENS][0][0], 3.0).move_to([-4.8, 0.0, 0])
        best[0].set_stroke(AMBER, width=5)
        best_lab = T(f"mejor solución · puntaje {SNAPS[GENS][1][0]:.3f}", size=24, color=AMBER).next_to(best, DOWN, buff=0.2)
        self.play(FadeOut(prev_labels), FadeOut(title), ReplacementTransform(cards[0].copy(), best),
                  *[c.animate.set_opacity(0.15) for c in cards], run_time=1.2)
        self.play(FadeIn(best_lab), run_time=0.5)
        self.wait(1.5)

        # resultados publicados
        everything = VGroup(cards, best, best_lab, judge, rule, gen_lab, axes, ylab, xlab, curve)
        era = BigNumber("40 de 87", "métodos generados por ERA superan todo el\nleaderboard de integración single-cell",
                        color=AMBER, size=88, cap_size=26)
        era_src = T("Aygün et al., Nature 2026", size=21, color=GRAY)
        ae = BigNumber("48", "multiplicaciones para multiplicar dos\nmatrices complejas 4×4",
                       color=TEXT, size=88, cap_size=26)
        ae_src = T("AlphaEvolve · Novikov et al., arXiv 2025", size=21, color=GRAY)
        left = VGroup(era, era_src).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-3.6, 0.1, 0])
        right = VGroup(ae, ae_src).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([3.7, 0.1, 0])
        right.align_to(left, UP)
        self.play(FadeOut(everything), FadeOut(note), run_time=0.8)
        self.play(FadeIn(left, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(right, shift=UP * 0.15), run_time=0.8)
        self.wait(3.5)
