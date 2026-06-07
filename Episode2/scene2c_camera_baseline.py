"""
Episode 2, Scene 2C: Why Not Just Use a Camera?
===============================================

Explains bandwidth and why low-dimensional sensing can be meaningful.

Run:
    manim -pql scene2c_camera_baseline.py Scene2CCameraBaseline
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


class Scene2CCameraBaseline(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Why Not Just Use a Camera?", font_size=42, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(FadeIn(title, shift=DOWN * 0.10), run_time=0.75)
        self.wait(0.5)

        cam_box = RoundedRectangle(width=4.9, height=4.0, corner_radius=0.24, color=BLUE_3B1B, stroke_width=2.3, fill_color=GRAY_DARKER, fill_opacity=0.14)
        pr_box = RoundedRectangle(width=4.9, height=4.0, corner_radius=0.24, color=GREEN_3B1B, stroke_width=2.3, fill_color=GRAY_DARKER, fill_opacity=0.14)
        cam_box.move_to(LEFT * 2.85 + DOWN * 0.10)
        pr_box.move_to(RIGHT * 2.85 + DOWN * 0.10)

        cam_title = Text("128 x 128 camera", font_size=25, color=BLUE_3B1B, weight=BOLD).move_to(cam_box.get_top() + DOWN * 0.40)
        pr_title = Text("64 photoreceptors", font_size=25, color=GREEN_3B1B, weight=BOLD).move_to(pr_box.get_top() + DOWN * 0.40)

        grid = VGroup()
        cell = 0.078
        for r in range(16):
            for c in range(16):
                sq = Square(side_length=cell, color=BLUE_3B1B, stroke_width=0.25, fill_color=BLUE_3B1B, fill_opacity=0.35)
                sq.move_to(np.array([c * cell, -r * cell, 0]))
                grid.add(sq)
        grid.move_to(cam_box.get_center() + DOWN * 0.08)
        grid_label = Text("16,384 values\nper frame", font_size=16, color=GRAY_LIGHT, line_spacing=1.10, font="Consolas")
        grid_label.move_to(cam_box.get_bottom() + UP * 0.48)
        self.play(
            FadeIn(cam_box),
            FadeIn(pr_box),
            FadeIn(cam_title, shift=DOWN * 0.08),
            FadeIn(pr_title, shift=DOWN * 0.08),
            LaggedStart(*[FadeIn(s, scale=0.6) for s in grid], lag_ratio=0.002),
            FadeIn(grid_label),
            run_time=1.7,
        )
        self.wait(3.8)

        dots = VGroup()
        for r in range(8):
            for c in range(8):
                d = Dot(radius=0.047, color=GREEN_3B1B)
                d.move_to(np.array([c * 0.245, -r * 0.245, 0]))
                dots.add(d)
        dots.move_to(pr_box.get_center() + DOWN * 0.05)
        dot_label = Text("64 readings\n< 1% bandwidth", font_size=16, color=GRAY_LIGHT, line_spacing=1.10, font="Consolas")
        dot_label.move_to(pr_box.get_bottom() + UP * 0.48)
        self.play(
            LaggedStart(*[FadeIn(d, scale=1.4) for d in dots], lag_ratio=0.015),
            FadeIn(dot_label),
            run_time=1.5,
        )
        self.wait(4.8)

        warning = Text("The question is not 'camera bad'. It is 'how much sensing does this task need?'", font_size=23, color=YELLOW_3B1B, weight=BOLD)
        warning.scale_to_fit_width(11.5)
        warning.to_edge(DOWN, buff=0.42)
        self.play(FadeIn(warning, shift=UP * 0.08), run_time=0.8)
        self.wait(4.2)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
