from manim import Scene, VGroup, LEFT, RIGHT, UP, DOWN
from common import *


class ComponentSheet(Scene):
    def construct(self):
        loop = LoopMotif(["proponer", "correr 5 min", "evaluar", "¿conservar?"], judge_index=2).shift(LEFT * 4.6)
        term = Terminal("train.py", width=4.6, height=2.4).shift(RIGHT * 1.2 + UP * 1.2)
        chips = VGroup(TokenChip("El"), TokenChip("␣robot"), TokenChip("␣levantó", color=K_COL)).arrange(RIGHT, buff=0.15)
        chips.next_to(term, DOWN, buff=0.4)
        st = VGroup(stamp("conservado", AMBER), stamp("descartado", GRAY), stamp("falló", ERROR)).arrange(RIGHT, buff=0.4)
        st.next_to(chips, DOWN, buff=0.35)
        bn = BigNumber("74%", "un LLM como juez", color=AMBER).shift(RIGHT * 6 + UP * 0.6)
        self.add(loop, term, chips, st, bn, illustrative_label())
