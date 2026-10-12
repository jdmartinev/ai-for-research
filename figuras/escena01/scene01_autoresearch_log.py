"""
Scene 1 - "An AI agent can now run a research loop overnight, without us"
AI for Research talk, slide 1.

An autoresearch-style log scrolls in a terminal. Each experiment is stamped
kept (amber) or discarded (gray), a loss chart fills in beside it, and the
scene ends on a counter: N experiments · H hours · 0 humans.

Data
----
Reads ``results.tsv`` next to this file (the log Karpathy's autoresearch writes).
Accepted columns (header row, tab-separated, case-insensitive):
  - metric:      val_bpb | val_loss | loss          (required)
  - description: description | change | desc        (optional)
  - status:      status  (keep / discard / crash)   (optional; computed if absent)
If no results.tsv exists, an illustrative demo log is generated and the video
carries a small "illustrative data" label. Replace it with your overnight run.

Render (output is 1920x720, 8:3, to sit inside the slide's evidence box):
  manim -r 1920,720 --fps 30 scene01_autoresearch_log.py AutoresearchLog
Quick preview:
  manim -ql -r 960,360 scene01_autoresearch_log.py AutoresearchLog

Options (environment variables):
  MINUTES_PER_RUN   minutes per experiment incl. overhead (default 6.5)
  HIDE_DEMO_LABEL   set to 1 to hide the "illustrative data" label
"""

from __future__ import annotations

import csv
import os
import random
from pathlib import Path

from manim import (
    AnimationGroup, Axes, Circle, Create, Dot, FadeIn, FadeOut, GrowFromCenter,
    LaggedStart, Line, Rectangle, RoundedRectangle, Scene, Text, VGroup, Write,
    config, DOWN, LEFT, RIGHT, UP, UL, UR, DR, BOLD, rate_functions,
)

# ---------------------------------------------------------------- canvas
config.frame_height = 6.0
config.frame_width = 16.0
config.background_color = "#0F1626"

# ---------------------------------------------------------------- palette (matches the deck)
BG = "#0F1626"
PANEL = "#141D2F"
BORDER = "#2A3550"
AXIS = "#3A475C"
TEXT = "#ECEEF0"
MUTED = "#B9C3CF"
GRAY = "#5B6678"
AMBER = "#F2A541"
CRASH = "#C97B63"
FONT = "JetBrains Mono"

HERE = Path(__file__).resolve().parent
MINUTES_PER_RUN = float(os.environ.get("MINUTES_PER_RUN", "6.5"))
HIDE_DEMO_LABEL = os.environ.get("HIDE_DEMO_LABEL") == "1"


# ---------------------------------------------------------------- data
DEMO_CHANGES = [
    "lr 3e-4 → 6e-4", "warmup 100 → 300 steps", "RMSNorm before attn",
    "GELU → SwiGLU", "batch 32 → 48", "weight decay 0.1 → 0.05",
    "rotary base 10k → 50k", "depth 8 → 10 layers", "width 512 → 640",
    "dropout 0.1 → 0.0", "cosine → linear decay", "grad clip 1.0 → 0.5",
    "add QK-norm", "tie embeddings", "Muon for matrices",
    "AdamW β2 0.95 → 0.98", "seq len 512 → 1024", "head dim 64 → 128",
    "zero-init out proj", "z-loss 1e-4", "ReLU² MLP", "value residual",
    "softcap logits 30", "init std 0.02 → 0.01", "EMA of weights",
    "remove biases", "parallel attn + MLP", "GQA, 4 groups",
    "WSD lr schedule", "batch 48 → 64", "MLP ratio 4 → 3",
    "embedding lr ×2", "untie lm head", "lr 6e-4 → 8e-4",
    "warmdown 20% → 35%", "depth 10 → 12 layers",
]


def demo_log(n: int = 72, seed: int = 14) -> list[dict]:
    """Illustrative log: a baseline, then edits that are kept only if they beat the best."""
    rng = random.Random(seed)
    rows = [{"desc": "baseline", "loss": 1.0000, "status": "keep"}]
    best = 1.0000
    crash_at = {23, 51}
    for i in range(1, n):
        desc = DEMO_CHANGES[(i * 7 + rng.randrange(5)) % len(DEMO_CHANGES)]
        if i in crash_at:
            rows.append({"desc": desc, "loss": None, "status": "crash"})
            continue
        # most edits hurt a little; some help; gains shrink as the model improves
        gain_scale = 0.012 * (1.0 - i / (1.5 * n))
        loss = best + abs(rng.gauss(0.0035, 0.004)) - (rng.uniform(0.4, 1.0) * gain_scale if rng.random() < 0.3 else 0.0)
        loss = round(loss, 4)
        status = "keep" if loss < best else "discard"
        best = min(best, loss)
        rows.append({"desc": desc, "loss": loss, "status": status})
    return rows


def load_log(path: Path) -> tuple[list[dict], str]:
    """Load results.tsv. Returns (rows, metric_name)."""
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        cols = {c.lower().strip(): c for c in (reader.fieldnames or [])}
        metric = next((m for m in ("val_bpb", "val_loss", "loss") if m in cols), None)
        if metric is None:
            raise ValueError(f"{path.name}: needs a val_bpb, val_loss or loss column")
        desc_col = next((cols[d] for d in ("description", "change", "desc") if d in cols), None)
        status_col = cols.get("status")
        rows, best = [], float("inf")
        for i, r in enumerate(reader):
            raw = (r.get(cols[metric]) or "").strip()
            try:
                loss = float(raw)
            except ValueError:
                loss = None
            status = (r.get(status_col) or "").strip().lower() if status_col else ""
            if status not in ("keep", "discard", "crash"):
                status = "crash" if loss is None or loss == 0 else ("keep" if loss < best else "discard")
            if loss is None or loss == 0:
                loss, status = None, "crash"
            if status == "keep" and loss is not None:
                best = min(best, loss)
            desc = (r.get(desc_col) or "").strip() if desc_col else ""
            rows.append({"desc": desc or ("baseline" if i == 0 else f"experiment {i}"),
                         "loss": loss, "status": status})
    if not rows:
        raise ValueError(f"{path.name} has no rows")
    return rows, metric.replace("_", " ")


# ---------------------------------------------------------------- scene
class AutoresearchLog(Scene):
    VISIBLE = 11          # log lines visible in the terminal
    SLOW = 6              # experiments shown at reading speed
    SPACING = 0.40        # vertical distance between log lines (units)

    def construct(self):
        log_path = HERE / "results.tsv"
        if log_path.exists():
            rows, metric = load_log(log_path)
            demo = False
        else:
            rows, metric = demo_log(), "val bpb"
            demo = True

        n = len(rows)
        losses = [r["loss"] for r in rows if r["loss"] is not None]
        lo, hi = min(losses), max(losses)
        pad = (hi - lo) * 0.12 or 0.01
        y_min, y_max = lo - pad, hi + pad

        # ---------- terminal
        term = RoundedRectangle(width=9.3, height=5.7, corner_radius=0.18,
                                fill_color=PANEL, fill_opacity=1,
                                stroke_color=BORDER, stroke_width=2).move_to([-3.25, 0, 0])
        bar_y = term.get_top()[1] - 0.26
        dots = VGroup(*[Circle(radius=0.065, fill_color=c, fill_opacity=1, stroke_width=0)
                        for c in (GRAY, GRAY, GRAY)]).arrange(RIGHT, buff=0.12)
        dots.move_to([term.get_left()[0] + 0.45, bar_y, 0])
        title = Text("results.tsv  ·  autoresearch", font=FONT, font_size=18, color=MUTED)
        title.move_to([term.get_center()[0], bar_y, 0])
        divider = Line([term.get_left()[0], bar_y - 0.26, 0], [term.get_right()[0], bar_y - 0.26, 0],
                       stroke_color=BORDER, stroke_width=2)

        # character width -> font size so a 52-char line fits the terminal
        probe = Text("0" * 40, font=FONT, font_size=20)
        fs = 20 * (8.6 / 52) / (probe.width / 40)
        x_text = term.get_left()[0] + 0.32
        x_tag = term.get_right()[0] - 0.32
        y_first = divider.get_y() - 0.42
        y_status = term.get_bottom()[1] + 0.32

        status_line = self._status(f"▶ waiting for first run", fs, x_text, y_status)

        # ---------- chart
        axes = Axes(x_range=[0, n + 1, 10], y_range=[y_min, y_max, (y_max - y_min) / 4],
                    x_length=5.5, y_length=4.5, tips=False,
                    axis_config={"color": AXIS, "stroke_width": 2, "include_ticks": False})
        axes.move_to([4.95, 0.15, 0])
        y_lab = Text(metric, font=FONT, font_size=18, color=MUTED)
        y_lab.next_to(axes.y_axis.get_top(), UP, buff=0.12).align_to(axes.y_axis, LEFT)
        x_lab = Text("experiment →", font=FONT, font_size=18, color=MUTED)
        x_lab.next_to(axes.x_axis.get_right(), DOWN, buff=0.14).align_to(axes.x_axis.get_right(), RIGHT)
        hi_lab = Text(f"{hi:.3f}", font=FONT, font_size=16, color=GRAY)
        hi_lab.next_to(axes.c2p(0, hi), LEFT, buff=0.1)
        lo_lab = Text(f"{lo:.3f}", font=FONT, font_size=16, color=GRAY)
        lo_lab.next_to(axes.c2p(0, lo), LEFT, buff=0.1)
        legend = VGroup(
            Dot(radius=0.06, color=AMBER), Text("kept", font=FONT, font_size=16, color=AMBER),
            Dot(radius=0.06, color=GRAY), Text("discarded", font=FONT, font_size=16, color=GRAY),
        ).arrange(RIGHT, buff=0.12)
        legend[2].shift(RIGHT * 0.2)
        legend[3].shift(RIGHT * 0.2)
        legend.next_to(axes, DOWN, buff=0.18).align_to(axes.x_axis, LEFT)

        demo_label = None
        if demo and not HIDE_DEMO_LABEL:
            demo_label = Text("illustrative data", font=FONT, font_size=14, color=GRAY)
            demo_label.move_to([axes.x_axis.get_right()[0], legend.get_y() - 0.34, 0], aligned_edge=RIGHT)

        # ---------- intro
        intro = [FadeIn(term), FadeIn(dots), FadeIn(title), Create(divider),
                 Create(axes), FadeIn(y_lab), FadeIn(x_lab), FadeIn(hi_lab), FadeIn(lo_lab),
                 FadeIn(legend), FadeIn(status_line)]
        if demo_label:
            intro.append(FadeIn(demo_label))
        self.play(*intro, run_time=1.2)
        self.wait(0.4)

        lines: list[VGroup] = []
        best = None
        best_x = None
        kept = 0
        first_loss = None
        chart_marks = VGroup()

        for i, row in enumerate(rows):
            slow = i < self.SLOW
            # speed ramps from reading pace to a blur
            t = 1.0 if slow else max(0.07, 0.34 * (1 - (i - self.SLOW) / max(1, n - self.SLOW)) + 0.07)

            loss, status = row["loss"], row["status"]
            loss_txt = f"{loss:.4f}" if loss is not None else "  —   "
            main = Text(f"#{i:02d}  {row['desc'][:27]:<27}  {loss_txt}",
                        font=FONT, font_size=fs, color=TEXT)
            tag_word = {"keep": "kept", "discard": "discarded", "crash": "crash"}[status]
            tag_col = {"keep": AMBER, "discard": GRAY, "crash": CRASH}[status]
            tag = Text(tag_word, font=FONT, font_size=fs, color=tag_col, weight=BOLD)
            y = y_first - min(i, self.VISIBLE - 1) * self.SPACING
            main.move_to([x_text, y, 0], aligned_edge=LEFT)
            tag.move_to([x_tag, y, 0], aligned_edge=RIGHT)
            line = VGroup(main, tag)

            # scroll once the terminal is full
            scroll = []
            if i >= self.VISIBLE:
                old = lines[i - self.VISIBLE]
                scroll = [FadeOut(old, shift=UP * self.SPACING)] + [
                    lines[j].animate.shift(UP * self.SPACING) for j in range(i - self.VISIBLE + 1, i)
                ]

            new_status = self._status(f"▶ running #{i:02d} · 5:00 training budget", fs, x_text, y_status)

            # chart marks for this experiment
            marks = []
            if loss is not None:
                dot = Dot(axes.c2p(i + 1, loss), radius=0.055 if status == "keep" else 0.045,
                          color=AMBER if status == "keep" else GRAY)
                marks.append(dot)
            if best is not None:
                seg = Line(axes.c2p(best_x, best), axes.c2p(i + 1, best), stroke_color=AMBER, stroke_width=4)
                marks.append(seg)
                best_x = i + 1
            if status == "keep" and loss is not None:
                if best is None:
                    first_loss, best, best_x = loss, loss, i + 1
                elif loss < best:
                    drop = Line(axes.c2p(i + 1, best), axes.c2p(i + 1, loss), stroke_color=AMBER, stroke_width=4)
                    marks.append(drop)
                    best = loss
                kept += 1

            if slow:
                # 1. the agent starts a run
                self.play(*scroll, FadeOut(status_line), FadeIn(new_status), run_time=0.35)
                status_line = new_status
                # 2. the result line appears
                self.play(FadeIn(main, shift=RIGHT * 0.15), run_time=0.45)
                self.wait(0.25)
                # 3. verdict: stamp and recolor, mark on chart
                verdict = [GrowFromCenter(tag)]
                if status == "keep":
                    verdict.append(main.animate.set_color(AMBER))
                else:
                    verdict.append(main.animate.set_color(GRAY))
                verdict += [Create(m) if isinstance(m, Line) else GrowFromCenter(m) for m in marks]
                self.play(*verdict, run_time=0.5)
                # regroup so the line scrolls and fades as one object later
                self.remove(main, tag)
                self.add(line)
                self.wait(0.35)
            else:
                main.set_color(AMBER if status == "keep" else GRAY)
                anims = scroll + [FadeOut(status_line), FadeIn(new_status), FadeIn(line)]
                anims += [Create(m) if isinstance(m, Line) else FadeIn(m) for m in marks]
                self.play(*anims, run_time=t, rate_func=rate_functions.linear)
                status_line = new_status

            lines.append(line)
            chart_marks.add(*marks)

        done = self._status(f"■ queue empty · {n} runs logged", fs, x_text, y_status)
        self.play(FadeOut(status_line), FadeIn(done), run_time=0.3)
        self.wait(0.6)

        # ---------- finale: dim the evidence, show the counter
        hours = n * MINUTES_PER_RUN / 60
        hours_txt = f"{hours:.0f} hours" if hours >= 1.5 else f"{hours * 60:.0f} minutes"
        counter = Text(f"{n} experiments · {hours_txt} · 0 humans", font=FONT,
                       font_size=46, color=TEXT, weight=BOLD)
        sub = Text(f"{metric}  {first_loss:.4f} → {best:.4f}   ·   {kept} changes kept",
                   font=FONT, font_size=24, color=AMBER)
        card = VGroup(counter, sub).arrange(DOWN, buff=0.3)
        backing = Rectangle(width=config.frame_width, height=config.frame_height,
                            fill_color=BG, fill_opacity=0.78, stroke_width=0)
        self.play(FadeIn(backing), run_time=0.6)
        self.play(Write(counter), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.6)
        self.wait(3.0)

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def _status(msg: str, fs: float, x: float, y: float) -> Text:
        t = Text(msg, font=FONT, font_size=fs * 0.9, color=MUTED)
        t.move_to([x, y, 0], aligned_edge=LEFT)
        return t
