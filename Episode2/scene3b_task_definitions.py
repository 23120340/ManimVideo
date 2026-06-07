"""
Episode 2, Scene 3B: PointGoalNav vs TargetNav
==============================================

Defines the two navigation tasks before showing results. This prevents the
photoreceptor claim from sounding broader than the experiments support.

Run:
    manim -pql scene3b_task_definitions.py Scene3BTaskDefinitions
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def make_task_card(title, subtitle, bullets, color):
    frame = RoundedRectangle(
        width=5.55,
        height=4.15,
        corner_radius=0.20,
        color=color,
        stroke_width=2.1,
        fill_color=GRAY_DARKER,
        fill_opacity=0.15,
    )
    title_text = Text(title, font_size=28, color=color, weight=BOLD)
    if title_text.width > 4.8:
        title_text.scale_to_fit_width(4.8)
    subtitle_text = Text(subtitle, font_size=18, color=GRAY_MID, slant=ITALIC)
    if subtitle_text.width > 4.6:
        subtitle_text.scale_to_fit_width(4.6)
    header = VGroup(title_text, subtitle_text).arrange(DOWN, buff=0.12)
    header.move_to(frame.get_top() + DOWN * 0.55)

    bullet_group = VGroup()
    for item in bullets:
        dot = Dot(radius=0.045, color=color)
        line = Text(item, font_size=20, color=GRAY_LIGHT)
        if line.width > 4.65:
            line.scale_to_fit_width(4.65)
        row = VGroup(dot, line).arrange(RIGHT, buff=0.15)
        bullet_group.add(row)
    bullet_group.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    if bullet_group.height > 1.18:
        bullet_group.scale_to_fit_height(1.18)
    bullet_group.move_to(frame.get_center() + DOWN * 0.92)
    bullet_group.align_to(frame.get_left() + RIGHT * 0.45, LEFT)

    return VGroup(frame, header, bullet_group)


def mini_map(color, target_known=True):
    room = Rectangle(width=2.0, height=1.35, color=GRAY_MID, stroke_width=1.4)
    obs1 = Rectangle(width=0.70, height=0.16, color=GRAY_DIM, fill_color=GRAY_DIM, fill_opacity=0.6, stroke_width=0)
    obs2 = Rectangle(width=0.60, height=0.16, color=GRAY_DIM, fill_color=GRAY_DIM, fill_opacity=0.6, stroke_width=0)
    obs1.move_to(room.get_center() + UP * 0.26 + LEFT * 0.35)
    obs2.move_to(room.get_center() + DOWN * 0.25 + RIGHT * 0.38)

    robot = Dot(room.get_corner(UL) + RIGHT * 0.25 + DOWN * 0.23, radius=0.08, color=GREEN_3B1B)
    goal = Circle(radius=0.12, color=color, fill_color=color, fill_opacity=0.25, stroke_width=1.8)
    goal.move_to(room.get_corner(DR) + LEFT * 0.25 + UP * 0.23)

    if target_known:
        path = VMobject(color=color, stroke_width=2.2)
        p0 = robot.get_center()
        p1 = room.get_center() + RIGHT * 0.55 + UP * 0.35
        p2 = room.get_center() + LEFT * 0.55 + DOWN * 0.28
        p3 = goal.get_center()
        path.set_points_smoothly([p0, p1, p2, p3])
        extra = Text("x,y goal given", font_size=13, color=color)
    else:
        path = DashedLine(robot.get_center(), goal.get_center(), color=color, stroke_width=2.0, dash_length=0.10)
        extra = Text("find the sphere", font_size=13, color=color)

    extra.next_to(room, DOWN, buff=0.10)
    return VGroup(room, obs1, obs2, robot, goal, path, extra)


class Scene3BTaskDefinitions(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text(
            "Two Navigation Tasks, Two Kinds of Information",
            font_size=36,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.34)
        self.play(Write(title, run_time=1.0))
        self.wait(0.35)

        point_card = make_task_card(
            "PointGoalNav",
            "the coordinate is given",
            [
                "goal: coordinate given",
                "GPS + Compass: yes",
                "vision: obstacle cues",
            ],
            BLUE_3B1B,
        )
        target_card = make_task_card(
            "TargetNav",
            "the object must be discovered",
            [
                "goal: coordinate unknown",
                "must see target",
                "vision: search cues",
            ],
            ORANGE_3B1B,
        )
        cards = VGroup(point_card, target_card).arrange(RIGHT, buff=0.52)
        cards.move_to(DOWN * 0.10)

        point_map = mini_map(BLUE_3B1B, target_known=True)
        point_map.scale(0.74)
        point_map.move_to(point_card.get_center() + UP * 0.55)

        target_map = mini_map(ORANGE_3B1B, target_known=False)
        target_map.scale(0.74)
        target_map.move_to(target_card.get_center() + UP * 0.55)

        self.play(FadeIn(point_card[0], shift=UP * 0.15), FadeIn(point_card[1]), run_time=0.65)
        self.play(Create(point_map[0]), FadeIn(point_map[1:5]), Create(point_map[5]), FadeIn(point_map[6]), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.1) for row in point_card[2]], lag_ratio=0.12), run_time=1.0)
        self.wait(0.55)

        self.play(FadeIn(target_card[0], shift=UP * 0.15), FadeIn(target_card[1]), run_time=0.65)
        self.play(Create(target_map[0]), FadeIn(target_map[1:5]), Create(target_map[5]), FadeIn(target_map[6]), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.1) for row in target_card[2]], lag_ratio=0.12), run_time=1.0)
        self.wait(0.75)

        comparison = VGroup(
            Text("Same robot.", font_size=24, color=GRAY_LIGHT),
            Text("Different information.", font_size=24, color=YELLOW_3B1B, weight=BOLD),
            Text("Different reason vision matters.", font_size=24, color=GRAY_LIGHT),
        ).arrange(RIGHT, buff=0.22)
        comparison.scale_to_fit_width(11.1)
        comparison.to_edge(DOWN, buff=0.55)
        self.play(Write(comparison, run_time=1.25))
        self.wait(2.3)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
