"""
Episode 2, Scene 4C: Joint Training
===================================

Explains the generalist controller idea behind efficient sensor search.

Run:
    manim -pql scene4c_joint_training.py Scene4CJointTraining
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


class Scene4CJointTraining(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("The Trick: One Controller, Many Sensor Layouts", font_size=36, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.1))
        self.wait(1.2)

        design_box = RoundedRectangle(width=3.3, height=1.35, corner_radius=0.18, color=GREEN_3B1B, stroke_width=2.2)
        design_box.move_to(LEFT * 3.8 + UP * 1.15)
        design_text = VGroup(
            Text("design policy", font_size=23, color=GREEN_3B1B, weight=BOLD),
            VGroup(
                Text("proposes", font_size=19, color=GRAY_LIGHT),
                MathTex(r"\theta_{\mathrm{eye}}", font_size=24, color=GRAY_LIGHT),
            ).arrange(RIGHT, buff=0.08),
        ).arrange(DOWN, buff=0.12).move_to(design_box)

        controller_box = RoundedRectangle(width=3.55, height=1.35, corner_radius=0.18, color=BLUE_3B1B, stroke_width=2.2)
        controller_box.move_to(ORIGIN + UP * 1.15)
        controller_text = VGroup(
            Text("control policy", font_size=23, color=BLUE_3B1B, weight=BOLD),
            Text("acts from observations", font_size=19, color=GRAY_LIGHT),
        ).arrange(DOWN, buff=0.12).move_to(controller_box)

        task_box = RoundedRectangle(width=3.0, height=1.35, corner_radius=0.18, color=ORANGE_3B1B, stroke_width=2.2)
        task_box.move_to(RIGHT * 3.75 + UP * 1.15)
        task_text = VGroup(
            Text("task score", font_size=23, color=ORANGE_3B1B, weight=BOLD),
            Text("reward / success", font_size=19, color=GRAY_LIGHT),
        ).arrange(DOWN, buff=0.12).move_to(task_box)

        arrows = VGroup(
            Arrow(design_box.get_right(), controller_box.get_left(), color=GRAY_MID, buff=0.08, max_tip_length_to_length_ratio=0.09),
            Arrow(controller_box.get_right(), task_box.get_left(), color=GRAY_MID, buff=0.08, max_tip_length_to_length_ratio=0.09),
        )
        top_group = VGroup(design_box, design_text, controller_box, controller_text, task_box, task_text)
        self.play(FadeIn(top_group, shift=UP * 0.12), run_time=1.1)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25), run_time=0.9)
        self.wait(3.8)

        samples_title = Text("During training, the controller sees many layouts:", font_size=25, color=GRAY_LIGHT, weight=BOLD)
        samples_title.move_to(DOWN * 0.55)
        self.play(FadeIn(samples_title, shift=UP * 0.15), run_time=0.8)

        layouts = VGroup()
        for i, x in enumerate([-3.3, -1.1, 1.1, 3.3]):
            body = RoundedRectangle(width=0.72, height=0.95, corner_radius=0.10, color=GRAY_LIGHT, stroke_width=1.6)
            body.move_to(RIGHT * x + DOWN * 1.45)
            dots = VGroup()
            offsets = [
                [0.0, 0.42, 0],
                [0.32, 0.10, 0],
                [-0.25, -0.25, 0],
                [0.08, -0.38, 0],
            ]
            for j in range(3):
                dots.add(Dot(body.get_center() + np.array(offsets[(i + j) % 4]), radius=0.055, color=YELLOW_3B1B))
            label = Text(f"layout {i + 1}", font_size=17, color=GRAY_MID)
            label.next_to(body, DOWN, buff=0.18)
            layouts.add(VGroup(body, dots, label))
        self.play(LaggedStart(*[FadeIn(l, scale=0.9) for l in layouts], lag_ratio=0.18), run_time=1.7)
        self.wait(5.0)
        self.play(FadeOut(VGroup(samples_title, layouts), run_time=0.7))

        update_arrow = CurvedArrow(
            task_box.get_bottom() + DOWN * 0.32,
            design_box.get_bottom() + DOWN * 0.32,
            angle=-TAU / 8.5,
            color=PURPLE_3B1B,
            stroke_width=2.6,
            tip_length=0.16,
        )
        update_label = Text("same rollout teaches both policies", font_size=22, color=PURPLE_3B1B, weight=BOLD)
        update_label.scale_to_fit_width(6.8)
        update_label.move_to(DOWN * 0.92)
        self.play(Create(update_arrow), FadeIn(update_label, shift=UP * 0.1), run_time=1.2)
        self.wait(4.8)

        takeaway = Text("This avoids training a brand-new controller from scratch for every sensor design.", font_size=23, color=YELLOW_3B1B, weight=BOLD)
        takeaway.scale_to_fit_width(11.3)
        takeaway.to_edge(DOWN, buff=0.30)
        self.play(FadeIn(takeaway, shift=UP * 0.08), run_time=0.8)
        self.wait(4.0)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
