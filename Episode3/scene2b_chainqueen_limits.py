"""
Episode 3, Scene 2B: Why ChainQueen-Style Differentiable Physics Matters
========================================================================

Deepens the differentiable simulation section with soft-robot difficulties,
a particle/grid mental model, and important caveats.

Run:
    manim -pql scene2b_chainqueen_limits.py Scene2BChainQueenLimits
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def info_card(title, lines, color, width=3.55):
    frame = RoundedRectangle(
        width=width,
        height=2.28,
        corner_radius=0.18,
        color=color,
        stroke_width=2,
        fill_color=GRAY_DARKER,
        fill_opacity=0.16,
    )
    head = Text(title, font_size=22, color=color, weight=BOLD)
    head.move_to(frame.get_top() + DOWN * 0.35)
    body = VGroup(*[Text(line, font_size=20, color=GRAY_LIGHT) for line in lines])
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    body.move_to(frame.get_center() + DOWN * 0.22)
    return VGroup(frame, head, body)


class Scene2BChainQueenLimits(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Why Soft-Robot Physics Is Hard", font_size=40, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.0))
        self.wait(0.35)

        cards = VGroup(
            info_card("Deformation", ["flex", "many states"], BLUE_3B1B),
            info_card("Contact", ["ground force", "friction"], ORANGE_3B1B),
            info_card("Materials", ["stiffness", "elasticity", "actuators"], GREEN_3B1B),
        ).arrange(RIGHT, buff=0.32)
        cards.scale_to_fit_width(11.2)
        cards.move_to(UP * 0.72)

        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.14), run_time=1.3)
        self.wait(0.8)

        self.play(cards.animate.scale(0.78).to_edge(UP, buff=1.42), run_time=0.8)

        grid = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5.7,
            y_length=2.7,
            background_line_style={"stroke_color": GRAY_DIM, "stroke_width": 1, "stroke_opacity": 0.35},
            axis_config={"stroke_opacity": 0},
        )
        grid.move_to(LEFT * 3.0 + DOWN * 1.05)
        particles = VGroup()
        for i in range(7):
            for j in range(4):
                particles.add(Dot(grid.c2p(-2.2 + i * 0.34, -0.55 + j * 0.28), radius=0.035, color=TEAL_EP2))
        soft_label = Text("soft body as particles", font_size=18, color=TEAL_EP2)
        soft_label.next_to(grid, DOWN, buff=0.12)

        graph = VGroup()
        steps = ["state", "physics", "reward"]
        colors = [BLUE_3B1B, ORANGE_3B1B, GREEN_3B1B]
        for step, color in zip(steps, colors):
            box = RoundedRectangle(width=1.35, height=0.68, corner_radius=0.14, color=color, stroke_width=2)
            text = Text(step, font_size=18, color=color, weight=BOLD).move_to(box)
            graph.add(VGroup(box, text))
        graph.arrange(RIGHT, buff=0.38)
        graph.move_to(RIGHT * 3.15 + DOWN * 0.76)
        graph_arrows = VGroup(
            Arrow(graph[0][0].get_right(), graph[1][0].get_left(), color=GRAY_MID, buff=0.08, stroke_width=2.0, max_tip_length_to_length_ratio=0.09),
            Arrow(graph[1][0].get_right(), graph[2][0].get_left(), color=GRAY_MID, buff=0.08, stroke_width=2.0, max_tip_length_to_length_ratio=0.09),
        )
        back_arrow = CurvedArrow(
            graph[2][0].get_top(),
            graph[0][0].get_top(),
            angle=-TAU / 4,
            color=RED_BRAIN,
            stroke_width=2.2,
            tip_length=0.14,
        )
        back_label = Text("gradient", font_size=18, color=RED_BRAIN, weight=BOLD)
        back_label.next_to(back_arrow, UP, buff=0.08)

        self.play(Create(grid), FadeIn(soft_label), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in particles], lag_ratio=0.01), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(g, scale=0.9) for g in graph], lag_ratio=0.13), run_time=0.85)
        self.play(GrowArrow(graph_arrows[0]), GrowArrow(graph_arrows[1]), run_time=0.55)
        self.play(Create(back_arrow), FadeIn(back_label), run_time=0.8)
        self.wait(0.8)

        caveat = Text(
            "A gradient is a direction under a model, not a guarantee of global truth.",
            font_size=23,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        caveat.scale_to_fit_width(11.5)
        caveat.to_edge(DOWN, buff=0.42)
        self.play(Write(caveat, run_time=1.2))
        self.wait(2.2)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
