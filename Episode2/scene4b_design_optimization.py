"""
Episode 2, Scene 4B: Why Joint Optimization Is Needed
=====================================================

Adds a slower, explicit explanation of the optimization problem before the
existing bi-level trick scene.

Run:
    manim -pql scene4b_design_optimization.py Scene4BDesignOptimization
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def process_box(text, color, width=2.15, height=0.78):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.16,
        color=color,
        stroke_width=1.8,
        fill_color=color,
        fill_opacity=0.12,
    )
    label = Text(text, font_size=16, color=GRAY_LIGHT, weight=BOLD)
    if label.width > width - 0.25:
        label.scale_to_fit_width(width - 0.25)
    label.move_to(box)
    return VGroup(box, label)


def arrow_between(left, right, color=GRAY_MID):
    return Arrow(
        left.get_right(),
        right.get_left(),
        buff=0.12,
        color=color,
        stroke_width=1.55,
        tip_length=0.085,
        max_tip_length_to_length_ratio=0.055,
    )


class Scene4BDesignOptimization(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text(
            "Why Sensor Design Is Expensive",
            font_size=40,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.0))
        self.wait(0.35)

        naive_title = Text("Naive black-box search", font_size=23, color=RED_BRAIN, weight=BOLD)
        joint_title = Text("Joint design-control learning", font_size=23, color=GREEN_3B1B, weight=BOLD)
        naive_title.move_to(LEFT * 3.35 + UP * 2.05)
        joint_title.move_to(RIGHT * 3.25 + UP * 2.05)

        divider = DashedLine(UP * 2.2, DOWN * 2.55, color=GRAY_DIM, stroke_width=2.0, dash_length=0.16).shift(LEFT * 0.12)

        self.play(Create(divider), FadeIn(naive_title), FadeIn(joint_title), run_time=0.75)

        n1 = process_box("choose layout", BLUE_3B1B, width=2.05, height=0.66)
        n2 = process_box("train policy", ORANGE_3B1B, width=2.05, height=0.66)
        n3 = process_box("simulate", PURPLE_3B1B, width=2.05, height=0.66)
        n4 = process_box("score", RED_BRAIN, width=2.05, height=0.66)
        naive = VGroup(n1, n2, n3, n4).arrange(DOWN, buff=0.30)
        naive.move_to(LEFT * 3.35 + DOWN * 0.10)

        naive_arrows = VGroup()
        for a, b in zip(naive[:-1], naive[1:]):
            naive_arrows.add(Arrow(a.get_bottom(), b.get_top(), buff=0.08, color=GRAY_MID, stroke_width=1.45, tip_length=0.075, max_tip_length_to_length_ratio=0.055))
        loop_back = CurvedArrow(
            n4.get_left() + LEFT * 0.28 + DOWN * 0.03,
            n1.get_left() + LEFT * 0.28 + UP * 0.03,
            angle=-TAU / 4.2,
            color=RED_BRAIN,
            stroke_width=1.8,
            tip_length=0.11,
        )
        slow = Text("new layout means retrain", font_size=15, color=RED_BRAIN, weight=BOLD)
        slow.scale_to_fit_width(2.55)
        slow.next_to(n4, DOWN, buff=0.16)

        self.play(LaggedStart(*[FadeIn(box, shift=UP * 0.12) for box in naive], lag_ratio=0.12), run_time=1.2)
        self.play(LaggedStart(*[GrowArrow(a) for a in naive_arrows], lag_ratio=0.10), run_time=0.7)
        self.play(Create(loop_back), FadeIn(slow, shift=UP * 0.1), run_time=0.85)
        self.wait(0.8)

        j1 = process_box("design policy", BLUE_3B1B, width=1.85, height=0.66)
        j2 = process_box("control policy", GREEN_3B1B, width=1.90, height=0.66)
        j3 = process_box("one rollout", PURPLE_3B1B, width=1.65, height=0.66)
        joint_top = VGroup(j1, j2, j3).arrange(RIGHT, buff=0.38)
        joint_top.move_to(RIGHT * 3.42 + UP * 0.52)
        joint_arrows = VGroup(arrow_between(j1, j2), arrow_between(j2, j3))

        reward = process_box("reward", YELLOW_3B1B, width=1.35, height=0.56)
        reward.move_to(RIGHT * 3.42 + DOWN * 0.58)
        r_arrow = Arrow(j3.get_bottom(), reward.get_top(), buff=0.09, color=YELLOW_3B1B, stroke_width=1.55, tip_length=0.085, max_tip_length_to_length_ratio=0.055)

        grad_theta = CurvedArrow(
            reward.get_left() + LEFT * 0.05,
            j1.get_bottom() + DOWN * 0.05,
            angle=-TAU / 7.5,
            color=BLUE_3B1B,
            stroke_width=1.65,
            tip_length=0.10,
        )
        grad_phi = CurvedArrow(
            reward.get_right() + RIGHT * 0.05,
            j2.get_bottom() + DOWN * 0.05,
            angle=TAU / 7.5,
            color=GREEN_3B1B,
            stroke_width=1.65,
            tip_length=0.10,
        )
        generalist = Text(
            "The control policy learns to act\nwith a given sensor design.",
            font_size=16,
            color=GRAY_LIGHT,
            line_spacing=1.20,
        )
        generalist.move_to(RIGHT * 3.42 + DOWN * 1.85)

        self.play(LaggedStart(*[FadeIn(box, scale=0.92) for box in joint_top], lag_ratio=0.15), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in joint_arrows], lag_ratio=0.12), run_time=0.55)
        self.play(GrowArrow(r_arrow), FadeIn(reward, scale=0.9), run_time=0.65)
        self.play(
            Create(grad_theta),
            Create(grad_phi),
            run_time=0.9,
        )
        self.play(FadeIn(generalist, shift=UP * 0.1), run_time=0.65)
        self.wait(0.8)

        takeaway = Text(
            "The method optimizes the eye and the behavior together.",
            font_size=25,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        takeaway.scale_to_fit_width(11.2)
        takeaway.to_edge(DOWN, buff=0.52)
        self.play(Write(takeaway, run_time=1.1))
        self.wait(2.2)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
