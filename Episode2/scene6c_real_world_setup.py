"""
Episode 2, Scene 6C: Real-World Setup
=====================================

Adds the sim-to-real details for the photoreceptor demo.

Run:
    manim -pql scene6c_real_world_setup.py Scene6CRealWorldSetup
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


class Scene6CRealWorldSetup(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("From Simulation to a Real Robot", font_size=40, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(FadeIn(title, shift=DOWN * 0.10), run_time=0.75)
        self.wait(0.15)

        sim_box = RoundedRectangle(width=4.6, height=3.55, corner_radius=0.22, color=BLUE_3B1B, stroke_width=2.2, fill_color=GRAY_DARKER, fill_opacity=0.15)
        real_box = RoundedRectangle(width=4.6, height=3.55, corner_radius=0.22, color=GREEN_3B1B, stroke_width=2.2, fill_color=GRAY_DARKER, fill_opacity=0.15)
        sim_box.move_to(LEFT * 3.0 + DOWN * 0.10)
        real_box.move_to(RIGHT * 3.0 + DOWN * 0.10)

        sim_title = Text("Train in simulation", font_size=25, color=BLUE_3B1B, weight=BOLD).move_to(sim_box.get_top() + DOWN * 0.40)
        real_title = Text("Deploy on hardware", font_size=25, color=GREEN_3B1B, weight=BOLD).move_to(real_box.get_top() + DOWN * 0.40)

        sim_world = Rectangle(width=2.6, height=1.35, color=GRAY_MID, stroke_width=1.4)
        sim_world.move_to(sim_box.get_center() + UP * 0.30)
        sim_robot = Dot(sim_world.get_left() + RIGHT * 0.35, radius=0.08, color=BLUE_3B1B)
        sim_target = Circle(radius=0.14, color=GREEN_3B1B, fill_color=GREEN_3B1B, fill_opacity=0.75).move_to(sim_world.get_right() + LEFT * 0.35)
        sim_path = VMobject(color=BLUE_3B1B, stroke_width=2.2)
        sim_path.set_points_smoothly([sim_robot.get_center(), sim_world.get_center() + UP * 0.25, sim_target.get_center()])

        real_robot = RoundedRectangle(width=1.25, height=1.0, corner_radius=0.18, color=GRAY_LIGHT, stroke_width=2.0)
        real_robot.move_to(real_box.get_center() + UP * 0.28)
        pr_ring = VGroup()
        for x in [-0.44, -0.15, 0.15, 0.44]:
            pr_ring.add(Dot(real_robot.get_center() + np.array([x, 0.42, 0]), radius=0.035, color=YELLOW_3B1B))
            pr_ring.add(Dot(real_robot.get_center() + np.array([x, -0.42, 0]), radius=0.035, color=YELLOW_3B1B))
        for y in [-0.24, 0.0, 0.24]:
            pr_ring.add(Dot(real_robot.get_center() + np.array([-0.56, y, 0]), radius=0.035, color=YELLOW_3B1B))
            pr_ring.add(Dot(real_robot.get_center() + np.array([0.56, y, 0]), radius=0.035, color=YELLOW_3B1B))
        real_label = Text("64 PRs", font_size=24, color=YELLOW_3B1B, weight=BOLD).next_to(real_robot, DOWN, buff=0.28)

        arrow = Arrow(sim_box.get_right(), real_box.get_left(), color=YELLOW_3B1B, buff=0.18, stroke_width=2.4, max_tip_length_to_length_ratio=0.09)
        arrow_label = Text("transfer", font_size=18, color=YELLOW_3B1B, weight=BOLD).next_to(arrow, UP, buff=0.12)

        self.play(
            FadeIn(sim_box),
            FadeIn(real_box),
            FadeIn(sim_title, shift=DOWN * 0.08),
            FadeIn(real_title, shift=DOWN * 0.08),
            Create(sim_world),
            FadeIn(sim_robot),
            FadeIn(sim_target),
            Create(sim_path),
            Create(real_robot),
            LaggedStart(*[FadeIn(d, scale=1.2) for d in pr_ring], lag_ratio=0.04),
            FadeIn(real_label),
            run_time=1.35,
        )
        self.play(GrowArrow(arrow), FadeIn(arrow_label), run_time=0.75)
        self.wait(0.65)

        note = Text(
            "Key point: the real demo tests transfer, not massive real-world retraining.",
            font_size=23,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        note.scale_to_fit_width(11.1)
        note.to_edge(DOWN, buff=0.50)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.8)
        self.wait(2.4)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
