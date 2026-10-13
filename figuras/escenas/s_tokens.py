"""Tokens: la frase se parte en pedazos con número (tokenizador real, Tekken de Mistral).

Lee tokens.json (lo escribe datos_tokens.py).
manim -r 1920,720 --fps 30 s_tokens.py Tokens
"""
import json
from pathlib import Path

from manim import (Scene, VGroup, FadeIn, FadeOut, Transform, LaggedStart, ReplacementTransform,
                   LEFT, RIGHT, UP, DOWN, BOLD)
from common import *

D = json.loads(Path(__file__).with_name("tokens.json").read_text(encoding="utf-8"))
COLS = [MODEL, "#8FB8D8", "#4A7FA6"]


def show(piece):
    return piece.replace(" ", "␣")


class Tokens(Scene):
    def chips(self, toks, size=24):
        g = VGroup()
        for k, (p, i) in enumerate(toks):
            c = TokenChip(show(p), color=COLS[k % 3], size=size)
            n = T(str(i), size=15, color=GRAY, font=MONO).next_to(c, DOWN, buff=0.08)
            g.add(VGroup(c, n))
        return g.arrange(RIGHT, buff=0.1, aligned_edge=UP)

    def construct(self):
        main = D["frases"][0]
        sent = T(main["texto"], size=34, color=TEXT).move_to([0, 2.2, 0])
        self.play(FadeIn(sent), run_time=0.8)
        self.wait(0.6)
        row = self.chips(main["tokens"])
        if row.width > 15.4:
            row.scale_to_fit_width(15.4)
        row.move_to([0, 1.05, 0])
        self.play(ReplacementTransform(sent.copy(), VGroup(*[r[0] for r in row])), sent.animate.set_opacity(0.35), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(r[1], shift=UP * 0.1) for r in row], lag_ratio=0.06), run_time=1.2)
        cnt = T(f"{len(main['tokens'])} tokens · cada uno es un número del vocabulario", size=22, color=MUTED).next_to(row, DOWN, buff=0.35)
        self.play(FadeIn(cnt), run_time=0.5)
        self.wait(1.2)

        # palabras técnicas
        lab = T("palabras de tu campo:", size=22, color=GRAY).move_to([-7.6, -0.85, 0], aligned_edge=LEFT)
        self.play(FadeIn(lab), run_time=0.4)
        x = -7.6
        groups = []
        for f in D["frases"][1:]:
            w = T(f["texto"], size=26, color=TEXT).move_to([x, -1.45, 0], aligned_edge=LEFT)
            ch = self.chips(f["tokens"], size=22).move_to(w, aligned_edge=LEFT)
            n = T(f"{len(f['tokens'])} tokens", size=20, color=MUTED).next_to(ch, DOWN, buff=0.12).align_to(ch, LEFT)
            self.play(FadeIn(w), run_time=0.35)
            self.play(ReplacementTransform(w, VGroup(*[c[0] for c in ch])), run_time=0.7)
            self.play(FadeIn(VGroup(*[c[1] for c in ch])), FadeIn(n), run_time=0.4)
            x = ch.get_right()[0] + 0.6
            groups.append(ch)
        self.add(illustrative_label(f"tokenizador real: {D['tokenizer']} · vocabulario de {D['vocab']:,} tokens".replace(",", ",")))
        self.wait(3.5)
