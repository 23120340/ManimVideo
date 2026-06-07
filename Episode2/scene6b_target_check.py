"""
Episode 2, Scene 6B: Transparent Target Check
=============================================

Explains why the transparent-sphere experiment matters: it tests whether the
agent is relying on the visible target cue rather than some accidental shortcut.

Run:
    manim -pql scene6b_target_check.py Scene6BTargetCheck
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def make_target_panel(title, sphere_color, success, center, transparent=False):
    panel = RoundedRectangle(
        width=4.5,
        height=3.65,
        corner_radius=0.20,
        color=sphere_color,
        stroke_width=2.0,
        fill_color=GRAY_DARKER,
        fill_opacity=0.16,
    )
    panel.move_to(center)

    title_text = Text(title, font_size=24, color=sphere_color, weight=BOLD)
    title_text.move_to(panel.get_top() + DOWN * 0.42)

    room = Rectangle(width=2.25, height=1.25, color=GRAY_MID, stroke_width=1.3)
    room.move_to(panel.get_center() + UP * 0.30)
    robot = Dot(room.get_left() + RIGHT * 0.35, radius=0.075, color=BLUE_3B1B)

    if transparent:
        target = Circle(radius=0.16, color=sphere_color, stroke_width=2.2, fill_opacity=0)
        cue = Text("weak visual cue", font_size=15, color=sphere_color)
        path = DashedLine(robot.get_center(), room.get_right() + LEFT * 0.35, color=sphere_color, stroke_width=2.0)
    else:
        target = Circle(radius=0.16, color=sphere_color, stroke_width=2.0, fill_color=sphere_color, fill_opacity=0.80)
        cue = Text("visible green cue", font_size=15, color=sphere_color)
        path = VMobject(color=sphere_color, stroke_width=2.2)
        path.set_points_smoothly([
            robot.get_center(),
            room.get_center() + UP * 0.25,
            room.get_right() + LEFT * 0.35,
        ])
    target.move_to(room.get_right() + LEFT * 0.35)
    cue.next_to(room, DOWN, buff=0.10)

    bar_bg = Rectangle(width=2.30, height=0.28, color=GRAY_DIM, stroke_width=1.1, fill_color=GRAY_DARKER, fill_opacity=0.65)
    bar_bg.move_to(panel.get_bottom() + UP * 0.78)
    bar = Rectangle(width=2.30 * (success / 0.35), height=0.28, color=sphere_color, stroke_width=0, fill_color=sphere_color, fill_opacity=0.80)
    bar.align_to(bar_bg, LEFT)
    bar.move_to([bar_bg.get_left()[0] + bar.get_width() / 2, bar_bg.get_center()[1], 0])
    value = Text(f"success {success:.3f}", font_size=20, color=GRAY_LIGHT, weight=BOLD)
    value.next_to(bar_bg, DOWN, buff=0.15)

    return VGroup(panel, title_text, room, robot, target, path, cue, bar_bg, bar, value)


class Scene6BTargetCheck(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Does the Agent Really Use the Target Cue?", font_size=38, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.0))
        self.wait(0.35)

        green_panel = make_target_panel(
            "Green Target",
            GREEN_3B1B,
            0.314,
            LEFT * 2.75 + DOWN * 0.15,
            transparent=False,
        )
        clear_panel = make_target_panel(
            "Transparent Target",
            GRAY_MID,
            0.132,
            RIGHT * 2.75 + DOWN * 0.15,
            transparent=True,
        )

        self.play(FadeIn(green_panel[0:2], shift=UP * 0.12), run_time=0.65)
        self.play(Create(green_panel[2]), FadeIn(green_panel[3:5]), Create(green_panel[5]), FadeIn(green_panel[6]), run_time=1.0)
        self.play(FadeIn(green_panel[7]), GrowFromEdge(green_panel[8], LEFT), FadeIn(green_panel[9]), run_time=0.75)
        self.wait(0.45)

        self.play(FadeIn(clear_panel[0:2], shift=UP * 0.12), run_time=0.65)
        self.play(Create(clear_panel[2]), FadeIn(clear_panel[3:5]), Create(clear_panel[5]), FadeIn(clear_panel[6]), run_time=1.0)
        self.play(FadeIn(clear_panel[7]), GrowFromEdge(clear_panel[8], LEFT), FadeIn(clear_panel[9]), run_time=0.75)
        self.wait(0.55)

        drop_arrow = Arrow(
            green_panel[9].get_right() + RIGHT * 0.15,
            clear_panel[9].get_left() + LEFT * 0.15,
            color=RED_BRAIN,
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.18,
        )
        drop_text = Text("visual cue removed -> performance drops", font_size=23, color=RED_BRAIN, weight=BOLD)
        drop_text.to_edge(DOWN, buff=0.48)
        self.play(GrowArrow(drop_arrow), Write(drop_text, run_time=1.0))
        self.wait(2.0)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
