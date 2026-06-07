"""
Episode 2, Scene 5C: Human Intuition vs Search
==============================================

Explains why a human survey is meaningful: it compares intuitive placement
against computational search in a high-dimensional design space.

Run:
    manim -pql scene5c_human_survey.py Scene5CHumanSurvey
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


class Scene5CHumanSurvey(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Why Compare Against Human Intuition?", font_size=38, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(FadeIn(title, shift=DOWN * 0.10), run_time=0.75)
        self.wait(0.15)

        left = RoundedRectangle(width=5.0, height=3.65, corner_radius=0.22, color=BLUE_3B1B, stroke_width=2.2, fill_color=GRAY_DARKER, fill_opacity=0.15)
        right = RoundedRectangle(width=5.0, height=3.65, corner_radius=0.22, color=GREEN_3B1B, stroke_width=2.2, fill_color=GRAY_DARKER, fill_opacity=0.15)
        left.move_to(LEFT * 2.9 + DOWN * 0.1)
        right.move_to(RIGHT * 2.9 + DOWN * 0.1)

        left_title = Text("Human guess", font_size=27, color=BLUE_3B1B, weight=BOLD).move_to(left.get_top() + DOWN * 0.42)
        right_title = Text("Computational search", font_size=27, color=GREEN_3B1B, weight=BOLD).move_to(right.get_top() + DOWN * 0.42)

        body_l = RoundedRectangle(width=1.0, height=1.35, corner_radius=0.18, color=GRAY_LIGHT, stroke_width=1.8)
        body_l.move_to(left.get_center() + UP * 0.25)
        sensors_l = VGroup(
            Dot(body_l.get_top() + DOWN * 0.18, radius=0.07, color=YELLOW_3B1B),
            Dot(body_l.get_left() + RIGHT * 0.12, radius=0.07, color=YELLOW_3B1B),
            Dot(body_l.get_right() + LEFT * 0.12, radius=0.07, color=YELLOW_3B1B),
        )
        guess_note = Text("symmetry feels natural", font_size=18, color=GRAY_MID, slant=ITALIC)
        guess_note.next_to(body_l, DOWN, buff=0.28)

        body_r = RoundedRectangle(width=1.0, height=1.35, corner_radius=0.18, color=GRAY_LIGHT, stroke_width=1.8)
        body_r.move_to(right.get_center() + UP * 0.25)
        sensors_r = VGroup(
            Dot(body_r.get_bottom() + UP * 0.16 + LEFT * 0.10, radius=0.07, color=YELLOW_3B1B),
            Dot(body_r.get_right() + LEFT * 0.12 + UP * 0.25, radius=0.07, color=YELLOW_3B1B),
            Dot(body_r.get_center() + LEFT * 0.20 + DOWN * 0.15, radius=0.07, color=YELLOW_3B1B),
        )
        search_note = Text("weird can be useful", font_size=18, color=GRAY_MID, slant=ITALIC)
        search_note.next_to(body_r, DOWN, buff=0.28)

        self.play(
            FadeIn(left),
            FadeIn(right),
            FadeIn(left_title, shift=DOWN * 0.08),
            FadeIn(right_title, shift=DOWN * 0.08),
            Create(body_l),
            Create(body_r),
            LaggedStart(*[FadeIn(d, scale=1.3) for d in sensors_l], lag_ratio=0.12),
            LaggedStart(*[FadeIn(d, scale=1.3) for d in sensors_r], lag_ratio=0.12),
            FadeIn(guess_note),
            FadeIn(search_note),
            run_time=1.25,
        )
        self.wait(0.75)

        bridge = Text(
            "The survey tests whether optimization finds layouts people would not naturally choose.",
            font_size=23,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        bridge.scale_to_fit_width(11.2)
        bridge.to_edge(DOWN, buff=0.50)
        self.play(FadeIn(bridge, shift=UP * 0.08), run_time=0.8)
        self.wait(2.4)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
