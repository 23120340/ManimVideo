"""
Episode 3, Scene 4C: Diffusion Basics
=====================================

Explains the generative half before adding physics guidance.

Run:
    manim -pql scene4c_diffusion_basics.py Scene4CDiffusionBasics
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


class Scene4CDiffusionBasics(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Diffusion First Makes a Plausible Shape", font_size=38, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.1))
        self.wait(1.2)

        steps = VGroup()
        names = ["noise", "rough blob", "candidate", "robot-like shape"]
        colors = [GRAY_MID, PURPLE_3B1B, BLUE_3B1B, GREEN_3B1B]
        for i, (name, color) in enumerate(zip(names, colors)):
            frame = RoundedRectangle(width=2.25, height=1.85, corner_radius=0.18, color=color, stroke_width=2.0)
            dots = VGroup()
            if i == 0:
                for r in range(4):
                    for c in range(5):
                        dots.add(Dot(radius=0.025 + 0.008 * ((r + c) % 2), color=GRAY_MID).move_to(frame.get_center() + LEFT * 0.55 + RIGHT * c * 0.28 + UP * 0.35 + DOWN * r * 0.22))
            else:
                body = RoundedRectangle(width=0.75 + 0.18 * i, height=0.55 + 0.12 * i, corner_radius=0.16, color=color, stroke_width=2)
                body.move_to(frame.get_center())
                limb1 = Line(body.get_left(), body.get_left() + LEFT * (0.25 + 0.08 * i) + DOWN * 0.35, color=color, stroke_width=2)
                limb2 = Line(body.get_right(), body.get_right() + RIGHT * (0.25 + 0.08 * i) + DOWN * 0.35, color=color, stroke_width=2)
                dots.add(body, limb1, limb2)
            label = Text(name, font_size=18, color=color, weight=BOLD).next_to(frame, DOWN, buff=0.20)
            steps.add(VGroup(frame, dots, label))
        steps.arrange(RIGHT, buff=0.48)
        steps.move_to(UP * 0.35)
        arrows = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), color=GRAY_MID, buff=0.08, stroke_width=2.0, max_tip_length_to_length_ratio=0.09) for i in range(3)])

        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.12) for s in steps], lag_ratio=0.18), run_time=1.8)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.20), run_time=0.9)
        self.wait(5.0)

        callouts = VGroup(
            Text("The model learns a distribution of shapes.", font_size=24, color=GRAY_LIGHT),
            Text("But plausible geometry is not the same as useful physics.", font_size=24, color=ORANGE_3B1B, weight=BOLD),
        ).arrange(DOWN, buff=0.32)
        callouts.move_to(DOWN * 1.55)
        self.play(FadeIn(callouts[0], shift=UP * 0.12), run_time=0.8)
        self.wait(3.2)
        self.play(FadeIn(callouts[1], shift=UP * 0.12), run_time=0.8)
        self.wait(5.0)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
