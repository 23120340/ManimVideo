"""
Episode 2, Scene 5D: Bad Sensor Layouts
=======================================

Shows why sensor placement is not a decorative choice.

Run:
    manim -pql scene5d_bad_designs.py Scene5DBadDesigns
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def anchored_cone(origin, angle, fov, length, color, opacity=0.22):
    p0 = np.array(origin)
    p1 = p0 + length * np.array([np.cos(angle - fov / 2), np.sin(angle - fov / 2), 0])
    p2 = p0 + length * np.array([np.cos(angle + fov / 2), np.sin(angle + fov / 2), 0])
    return Polygon(p0, p1, p2, color=color, fill_color=color, fill_opacity=opacity, stroke_width=1.6)


class Scene5DBadDesigns(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("A Bad Sensor Layout Can Fail", font_size=41, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.1))
        self.wait(1.1)

        room = Rectangle(width=5.0, height=3.2, color=GRAY_MID, stroke_width=2)
        room.move_to(LEFT * 3.15 + DOWN * 0.25)
        wall = Rectangle(width=0.35, height=2.25, color=GRAY_DIM, fill_color=GRAY_DARKER, fill_opacity=0.65, stroke_width=1)
        wall.move_to(room.get_center() + RIGHT * 0.65)
        target = Circle(radius=0.18, color=GREEN_3B1B, stroke_width=2, fill_color=GREEN_3B1B, fill_opacity=0.25)
        target.move_to(room.get_right() + LEFT * 0.65 + UP * 0.85)
        target_label = Text("target", font_size=17, color=GREEN_3B1B).next_to(target, UP, buff=0.08)

        robot = RoundedRectangle(width=0.52, height=0.78, corner_radius=0.10, color=GRAY_LIGHT, stroke_width=2)
        robot.move_to(room.get_left() + RIGHT * 0.70 + DOWN * 0.80)
        self.play(Create(room), FadeIn(wall), FadeIn(target), FadeIn(target_label), FadeIn(robot), run_time=1.3)
        self.wait(2.0)

        bad_dot = Dot(robot.get_left() + RIGHT * 0.05, radius=0.06, color=RED_BRAIN)
        bad_cone = anchored_cone(bad_dot.get_center(), angle=PI, fov=PI / 5, length=1.25, color=RED_BRAIN, opacity=0.20)
        bad_label = Text("rear-facing PR", font_size=20, color=RED_BRAIN, weight=BOLD)
        bad_label.move_to(RIGHT * 2.8 + UP * 1.25)
        bad_notes = VGroup(
            Text("sees the past", font_size=19, color=GRAY_LIGHT, font="Consolas"),
            Text("misses target cue", font_size=19, color=GRAY_LIGHT, font="Consolas"),
            Text("controller guesses", font_size=19, color=GRAY_LIGHT, font="Consolas"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        bad_notes.next_to(bad_label, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(bad_cone), FadeIn(bad_dot), Write(bad_label), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.12) for n in bad_notes], lag_ratio=0.18), run_time=1.1)
        self.wait(4.8)

        good_dot = Dot(robot.get_right() + LEFT * 0.05, radius=0.06, color=GREEN_3B1B)
        good_cone = anchored_cone(good_dot.get_center(), angle=0, fov=PI / 3, length=1.65, color=GREEN_3B1B, opacity=0.20)
        good_label = Text("task-facing PR", font_size=20, color=GREEN_3B1B, weight=BOLD)
        good_label.move_to(RIGHT * 2.8 + DOWN * 0.85)
        good_notes = VGroup(
            Text("collects cue", font_size=19, color=GRAY_LIGHT, font="Consolas"),
            Text("reduces ambiguity", font_size=19, color=GRAY_LIGHT, font="Consolas"),
            Text("easier control", font_size=19, color=GRAY_LIGHT, font="Consolas"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        good_notes.next_to(good_label, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeOut(bad_cone), FadeOut(bad_dot), FadeIn(good_cone), FadeIn(good_dot), run_time=0.9)
        self.play(Write(good_label), LaggedStart(*[FadeIn(n, shift=RIGHT * 0.12) for n in good_notes], lag_ratio=0.18), run_time=1.4)
        self.wait(5.0)

        takeaway = Text("The body decides what information reaches the brain in the first place.", font_size=25, color=YELLOW_3B1B, weight=BOLD)
        takeaway.scale_to_fit_width(11.0)
        takeaway.to_edge(DOWN, buff=0.35)
        self.play(Write(takeaway, run_time=1.2))
        self.wait(4.0)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
