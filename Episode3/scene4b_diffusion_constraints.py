"""
Episode 3, Scene 4B: Generative Design Needs Constraints
========================================================

Expands DiffuseBot into a constraint-aware design pipeline.

Run:
    manim -pql scene4b_diffusion_constraints.py Scene4BDiffusionConstraints
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def pipeline_box(label, color, width=1.75):
    rect = RoundedRectangle(
        width=width,
        height=0.80,
        corner_radius=0.16,
        color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=0.10,
    )
    text = Text(label, font_size=16, color=color, weight=BOLD, line_spacing=1.0)
    if text.width > width - 0.20:
        text.scale_to_fit_width(width - 0.20)
    text.move_to(rect)
    return VGroup(rect, text)


class Scene4BDiffusionConstraints(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Generative Design Needs Physics and Constraints", font_size=35, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.0))
        self.wait(0.35)

        boxes = VGroup(
            pipeline_box("noisy\nshape", GRAY_MID),
            pipeline_box("diffusion\nproposal", PURPLE_3B1B, 1.95),
            pipeline_box("robotize", BLUE_3B1B, 1.55),
            pipeline_box("simulate", ORANGE_3B1B, 1.55),
            pipeline_box("utility\ngradient", GREEN_3B1B, 1.85),
            pipeline_box("guided\ndesign", TEAL_EP2, 1.75),
        ).arrange(RIGHT, buff=0.20)
        boxes.scale_to_fit_width(11.6)
        boxes.move_to(UP * 1.25)

        arrows = VGroup()
        for left, right in zip(boxes[:-1], boxes[1:]):
            arrows.add(Arrow(left[0].get_right(), right[0].get_left(), color=GRAY_MID, buff=0.06, stroke_width=2.0))

        self.play(LaggedStart(*[FadeIn(b, scale=0.92) for b in boxes], lag_ratio=0.11), run_time=1.2)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), run_time=0.8)
        self.wait(0.55)

        divider = DashedLine(LEFT * 5.5 + DOWN * 0.30, RIGHT * 5.5 + DOWN * 0.30, color=GRAY_DIM, stroke_width=1.6, dash_length=0.16)
        self.play(Create(divider), run_time=0.5)

        left_title = Text("Looks plausible", font_size=26, color=PURPLE_3B1B, weight=BOLD)
        right_title = Text("Can actually work", font_size=26, color=GREEN_3B1B, weight=BOLD)
        left_title.move_to(LEFT * 3.15 + DOWN * 0.85)
        right_title.move_to(RIGHT * 3.15 + DOWN * 0.85)

        left_bad = VGroup(
            Text("thin limbs", font_size=19, color=RED_BRAIN),
            Text("no actuators", font_size=19, color=RED_BRAIN),
            Text("unstable", font_size=19, color=RED_BRAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        left_bad.next_to(left_title, DOWN, buff=0.32)

        right_good = VGroup(
            Text("stable support", font_size=19, color=GREEN_3B1B),
            Text("actuation possible", font_size=19, color=GREEN_3B1B),
            Text("fabrication-aware", font_size=19, color=GREEN_3B1B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        right_good.next_to(right_title, DOWN, buff=0.32)

        cross = Text("x", font_size=36, color=RED_BRAIN, weight=BOLD)
        check = Text("OK", font_size=30, color=GREEN_3B1B, weight=BOLD)
        cross.next_to(left_bad, LEFT, buff=0.28)
        check.next_to(right_good, LEFT, buff=0.28)

        self.play(FadeIn(left_title), FadeIn(right_title), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.10) for t in left_bad], lag_ratio=0.12), FadeIn(cross), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.10) for t in right_good], lag_ratio=0.12), FadeIn(check), run_time=0.8)
        self.wait(0.7)

        bottom = Text(
            "DiffuseBot is best read as generative search guided by physics feedback.",
            font_size=24,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        bottom.scale_to_fit_width(11.5)
        bottom.to_edge(DOWN, buff=0.42)
        self.play(Write(bottom, run_time=1.2))
        self.wait(2.2)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
