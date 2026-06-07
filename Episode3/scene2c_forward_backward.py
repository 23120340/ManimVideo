"""
Episode 3, Scene 2C: Forward and Backward Simulation
====================================================

Makes differentiable simulation concrete as a computational graph.

Run:
    manim -pql scene2c_forward_backward.py Scene2CForwardBackward
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


class Scene2CForwardBackward(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Differentiable Simulation Is a Graph", font_size=39, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(FadeIn(title, shift=DOWN * 0.10), run_time=0.8)
        self.wait(1.2)

        nodes = VGroup()
        labels = ["state 0", "physics", "state 1", "physics", "state 2", "reward"]
        colors = [BLUE_3B1B, GRAY_MID, BLUE_3B1B, GRAY_MID, BLUE_3B1B, GREEN_3B1B]
        for label, color in zip(labels, colors):
            rect = RoundedRectangle(width=1.55, height=0.85, corner_radius=0.14, color=color, stroke_width=2.0)
            text = Text(label, font_size=18, color=color, weight=BOLD)
            text.move_to(rect)
            nodes.add(VGroup(rect, text))
        nodes.arrange(RIGHT, buff=0.30)
        nodes.move_to(UP * 1.05)

        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arrows.add(Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), color=GRAY_MID, buff=0.06, stroke_width=2.0, max_tip_length_to_length_ratio=0.09))
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.12) for n in nodes], lag_ratio=0.10), run_time=1.4)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=0.9)
        self.wait(4.2)

        forward_label = Text("forward pass: simulate what happens", font_size=25, color=GREEN_3B1B, weight=BOLD)
        forward_label.next_to(nodes, DOWN, buff=0.55)
        self.play(FadeIn(forward_label, shift=UP * 0.12), run_time=0.8)
        self.wait(3.5)
        self.play(FadeOut(forward_label, run_time=0.5))

        back_arrows = VGroup()
        for i in range(len(nodes) - 1, 0, -1):
            back_arrows.add(Arrow(nodes[i].get_bottom(), nodes[i - 1].get_bottom(), color=ORANGE_3B1B, buff=0.10, stroke_width=2.0, max_tip_length_to_length_ratio=0.08).shift(DOWN * 0.65))
        backward_label = Text("backward pass: how should parameters change?", font_size=25, color=ORANGE_3B1B, weight=BOLD)
        backward_label.move_to(DOWN * 1.45)
        self.play(
            FadeIn(backward_label, shift=UP * 0.12),
            LaggedStart(*[GrowArrow(a) for a in back_arrows], lag_ratio=0.08),
            run_time=1.25,
        )
        self.wait(4.8)

        grads = VGroup(
            MathTex(r"\frac{\partial R}{\partial \theta_{\mathrm{ctrl}}}", font_size=31, color=BLUE_3B1B),
            MathTex(r"\frac{\partial R}{\partial \theta_{\mathrm{body}}}", font_size=31, color=PURPLE_3B1B),
            MathTex(r"\frac{\partial R}{\partial \theta_{\mathrm{mat}}}", font_size=31, color=GREEN_3B1B),
            MathTex(r"\frac{\partial R}{\partial \theta_{\mathrm{act}}}", font_size=31, color=ORANGE_3B1B),
        ).arrange(RIGHT, buff=0.38)
        grads.scale_to_fit_width(11.2)
        grads.to_edge(DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.12) for g in grads], lag_ratio=0.16), run_time=1.3)
        self.wait(5.0)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
