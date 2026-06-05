"""
SCENE 7 — Minimal outro (Ep1 -> Ep2)
====================================

Keep the transition style consistent with Episode 2 -> Episode 3:
fade to a simple "See you next time." card.

Run:
    manim -pql scene7.py Scene7Outro
"""

from manim import *
from common import *


class Scene7Outro(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        see_you = Text(
            "See you next time.",
            font_size=36,
            color=GRAY_MID,
        )

        self.play(FadeIn(see_you, run_time=1.0, rate_func=smooth))
        self.wait(2.0)
        self.play(FadeOut(see_you, run_time=1.5, rate_func=smooth))
        self.wait(0.3)
