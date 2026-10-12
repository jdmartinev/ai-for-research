"""S16 — En autoresearch, tu métrica es el juez y el agente hace el resto (diapositiva 16).

Usa el mismo results.tsv que la escena 1 (o el mismo registro de demostración, semilla 14),
para que las diapositivas 1 y 16 cuenten una sola historia.
manim -r 1920,720 --fps 30 s16_autoresearch.py Autoresearch
"""
import re
import sys
from pathlib import Path

from manim import (Scene, VGroup, Axes, Line, Dot, Rectangle, RoundedRectangle, FadeIn, FadeOut, Create,
                   GrowFromCenter, Transform, LaggedStart, LEFT, RIGHT, UP, DOWN, BOLD, rate_functions)
from common import *

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "escena01"))
sys.path.insert(0, str(HERE.parent / "scene01"))
from scene01_autoresearch_log import demo_log, load_log  # noqa: E402

TSV = HERE / "results.tsv"
if TSV.exists():
    ROWS, METRIC = load_log(TSV)
    DEMO = False
else:
    ROWS, METRIC = demo_log(), "val bpb"
    DEMO = True


def diff_lines(desc):
    """'lr 3e-4 → 6e-4' → ('- lr = 3e-4', '+ lr = 6e-4'); si no hay flecha, una línea agregada."""
    m = re.match(r"\s*(.+?)\s+(\S+)\s*→\s*(\S+.*)$", desc)
    if m:
        k, a, b = m.groups()
        return f"- {k} = {a}", f"+ {k} = {b}"
    return None, f"+ {desc}"


class Autoresearch(Scene):
    def construct(self):
        loop = LoopMotif(["proponer", "correr 5 min", "evaluar", "¿conservar?"], judge_index=2,
                         radius=1.45, size=25, xscale=1.2).shift(LEFT * 4.95 + UP * 0.15)
        term = Terminal("train.py", width=4.3, height=2.5).move_to([0.75, 1.0, 0])
        # barra de progreso de la corrida
        bar_bg = RoundedRectangle(width=4.0, height=0.24, corner_radius=0.12, fill_color=CARD, fill_opacity=1,
                                  stroke_width=0).move_to([0.75, -0.95, 0])
        bar_lab = T("corrida de 5 min", size=21, color=GRAY).next_to(bar_bg, UP, buff=0.12).align_to(bar_bg, LEFT)
        # gráfica del mejor resultado
        losses = [r["loss"] for r in ROWS if r["loss"] is not None]
        lo, hi = min(losses), max(losses)
        pad = (hi - lo) * 0.1 or 0.01
        n = len(ROWS)
        axes = Axes(x_range=[0, n + 1, 10], y_range=[lo - pad, hi + pad, (hi - lo + 2 * pad) / 4],
                    x_length=4.3, y_length=3.5, tips=False,
                    axis_config={"color": AXIS, "stroke_width": 2, "include_ticks": False}).move_to([5.55, 0.3, 0])
        y_lab = T(f"mejor {METRIC}", size=21, color=MUTED).next_to(axes, UP, buff=0.12).align_to(axes, LEFT)
        x_lab = T("experimento →", size=21, color=MUTED).next_to(axes, DOWN, buff=0.12).align_to(axes, RIGHT)
        cap = T("tú escribes program.md; el agente escribe train.py", size=23, color=MUTED).move_to([-2.9, -2.55, 0])

        self.play(LaggedStart(*[FadeIn(nd) for nd in loop.nodes], lag_ratio=0.15), Create(loop.arrows), run_time=1.4)
        self.play(FadeIn(term), FadeIn(bar_bg), FadeIn(bar_lab), Create(axes), FadeIn(y_lab), FadeIn(x_lab),
                  run_time=1.1)
        if DEMO:
            self.add(illustrative_label("datos ilustrativos · mismo registro que la diapositiva 1"))

        best, best_x = None, None
        code = VGroup()
        value_lab = None
        n_slow = 3
        shown = [r for r in ROWS]
        for i, row in enumerate(shown):
            slow = i < n_slow + 1  # la línea base + 3 vueltas lentas
            rt = 1.0 if slow else 0.16
            loss, status = row["loss"], row["status"]
            # 1. proponer: cambia el diff
            old, new = diff_lines(row["desc"]) if i else (None, "+ modelo base")
            lines = VGroup()
            if old:
                lines.add(T(old, size=22, color=GRAY, font=MONO))
            lines.add(T(new, size=22, color=MODEL, font=MONO))
            lines.add(T(f"# experimento {i:02d}", size=20, color=GRAY, font=MONO))
            lines.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            if lines.width > term.frame.width - 0.6:
                lines.scale_to_fit_width(term.frame.width - 0.6)
            lines.move_to([term.frame.get_left()[0] + 0.35, term.body_top - 0.05, 0], aligned_edge=UP + LEFT)
            strike = None
            if old:
                strike = Line(lines[0].get_left(), lines[0].get_right(), stroke_color=GRAY, stroke_width=2)
            # 2. correr: barra
            fill = Rectangle(width=0.01, height=0.24, fill_color=MODEL, fill_opacity=1, stroke_width=0)
            fill.move_to(bar_bg.get_left(), aligned_edge=LEFT)
            # 3. evaluar: valor de la métrica junto al nodo juez
            vtxt = f"{loss:.4f}" if loss is not None else "falló"
            new_val = T(vtxt, size=26, color=AMBER if loss is not None else ERROR, font=MONO, weight=BOLD)
            new_val.next_to(loop.nodes[2], DOWN, buff=0.15)
            # 4. conservar o descartar
            kept = status == "keep"
            word = {"keep": "conservado", "discard": "descartado", "crash": "falló"}[status]
            col = {"keep": AMBER, "discard": GRAY, "crash": ERROR}[status]
            st = stamp(word, col, size=26).next_to(loop.nodes[3], DOWN, buff=0.15)
            # gráfica
            marks = []
            if loss is not None:
                marks.append(Dot(axes.c2p(i + 1, loss), radius=0.05 if kept else 0.04, color=AMBER if kept else GRAY))
            if best is not None:
                marks.append(Line(axes.c2p(best_x, best), axes.c2p(i + 1, best), stroke_color=AMBER, stroke_width=4))
                best_x = i + 1
            if kept and loss is not None:
                if best is None:
                    best, best_x = loss, i + 1
                elif loss < best:
                    marks.append(Line(axes.c2p(i + 1, best), axes.c2p(i + 1, loss), stroke_color=AMBER, stroke_width=4))
                    best = loss

            if slow:
                self.play(loop.pulse(0, run_time=0.5), FadeOut(code, run_time=0.4), FadeIn(lines, shift=RIGHT * 0.1, run_time=0.5))
                if strike:
                    self.play(Create(strike), run_time=0.3)
                self.play(loop.pulse(1, run_time=0.5),
                          fill.animate(run_time=1.0, rate_func=rate_functions.linear).stretch_to_fit_width(4.0).align_to(bar_bg, LEFT))
                anims = [loop.pulse(2, run_time=0.5), FadeIn(new_val, run_time=0.4)]
                if value_lab is not None:
                    anims.append(FadeOut(value_lab, run_time=0.3))
                self.play(*anims)
                self.play(loop.pulse(3, run_time=0.5), GrowFromCenter(st, run_time=0.4),
                          *[Create(m) if isinstance(m, Line) else GrowFromCenter(m) for m in marks])
                self.wait(0.45)
                self.play(FadeOut(st), FadeOut(fill), run_time=0.3)
            else:
                fill.stretch_to_fit_width(4.0).align_to(bar_bg, LEFT)
                anims = [FadeOut(code), FadeIn(lines), FadeIn(new_val)]
                if value_lab is not None:
                    anims.append(FadeOut(value_lab))
                anims += [Create(m) if isinstance(m, Line) else FadeIn(m) for m in marks]
                self.play(*anims, run_time=rt, rate_func=rate_functions.linear)
            code = VGroup(lines, strike) if strike else VGroup(lines)
            if strike and not slow:
                self.add(strike)
            value_lab = new_val

        kept_n = sum(r["status"] == "keep" for r in ROWS)
        summary = T(f"{n} experimentos · {kept_n} conservados", size=23, color=TEXT, weight=BOLD)
        summary.move_to([7.75, -2.2, 0], aligned_edge=RIGHT)
        self.play(FadeIn(cap), FadeIn(summary), run_time=0.8)
        self.wait(3.0)
