"""
Episode 2, Scene 6D: Photoreceptor Limitations
==============================================

Keeps the photoreceptor result from sounding too broad.

Run:
    manim -pql scene6d_pr_limitations.py Scene6DPRLimitations
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def verdict_item(label, color, kind, positive=True):
    frame = RoundedRectangle(
        width=1.26,
        height=1.12,
        corner_radius=0.16,
        color=color,
        stroke_width=1.65,
        fill_color=color,
        fill_opacity=0.08,
    )
    icon = VGroup()
    if kind == "sensor":
        icon.add(*[
            Dot(LEFT * 0.23 + RIGHT * c * 0.23 + UP * 0.16 + DOWN * r * 0.16, radius=0.028, color=color)
            for r in range(3) for c in range(3)
        ])
    elif kind == "design":
        for x, y in [(-0.35, 0.18), (0, -0.10), (0.35, 0.22)]:
            icon.add(Line(LEFT * 0.37 + RIGHT * (x + 0.37) + UP * y, RIGHT * 0.37 + UP * y, color=color, stroke_width=1.25))
            icon.add(Dot(RIGHT * x + UP * y, radius=0.035, color=YELLOW_3B1B))
    elif kind == "task":
        icon.add(Rectangle(width=0.72, height=0.50, color=color, stroke_width=1.35))
        icon.add(Dot(RIGHT * 0.19 + UP * 0.14, radius=0.045, color=GREEN_3B1B))
        icon.add(VMobject(color=color, stroke_width=2.0).set_points_smoothly([LEFT * 0.28 + DOWN * 0.18, ORIGIN, RIGHT * 0.22 + UP * 0.16]))
    elif kind == "camera":
        icon.add(Rectangle(width=0.68, height=0.48, color=color, stroke_width=1.35))
        icon.add(Circle(radius=0.12, color=color, stroke_width=1.35))
    elif kind == "four":
        icon.add(*[
            Square(side_length=0.19, color=color, fill_color=color, fill_opacity=0.18, stroke_width=1.1).shift(LEFT * 0.12 + RIGHT * c * 0.24 + UP * 0.12 + DOWN * r * 0.24)
            for r in range(2) for c in range(2)
        ])
    else:
        sim = Rectangle(width=0.42, height=0.30, color=BLUE_3B1B, stroke_width=1.25).shift(LEFT * 0.20)
        real = Circle(radius=0.16, color=ORANGE_3B1B, stroke_width=1.25).shift(RIGHT * 0.24)
        icon.add(sim, real, Line(sim.get_right(), real.get_left(), color=GRAY_MID, stroke_width=1.2))
    icon.move_to(frame.get_center() + UP * 0.15)
    mark_color = GREEN_3B1B if positive else RED_BRAIN
    mark = Text("+" if positive else "x", font_size=15, color=mark_color, weight=BOLD)
    mark.move_to(frame.get_top() + DOWN * 0.15)
    text = Text(label, font_size=12, color=GRAY_LIGHT, weight=BOLD, line_spacing=0.9)
    if text.width > frame.width - 0.20:
        text.scale_to_fit_width(frame.width - 0.20)
    text.move_to(frame.get_bottom() + UP * 0.20)
    return VGroup(frame, icon, mark, text)


def constraint_icon(label, color, kind):
    ring = Circle(radius=0.34, color=color, stroke_width=2.0, fill_color=color, fill_opacity=0.10)
    if kind == "calibrate":
        icon = VGroup(ring, Line(ring.get_center(), ring.get_center() + UP * 0.25 + RIGHT * 0.13, color=color, stroke_width=2.0))
    elif kind == "noise":
        wave = VMobject(color=color, stroke_width=2.0)
        wave.set_points_smoothly([LEFT * 0.34, LEFT * 0.16 + UP * 0.16, ORIGIN + DOWN * 0.12, RIGHT * 0.18 + UP * 0.14, RIGHT * 0.34])
        icon = VGroup(ring, wave)
    else:
        bolt = Polygon(UP * 0.30, LEFT * 0.02, RIGHT * 0.11, DOWN * 0.30, LEFT * 0.17 + DOWN * 0.04, color=color, fill_color=color, fill_opacity=0.35)
        icon = VGroup(ring, bolt)
    text = Text(label, font_size=17, color=color, weight=BOLD)
    text.next_to(icon, DOWN, buff=0.16)
    return VGroup(icon, text)


class Scene6DPRLimitations(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("What the PR Result Does Not Prove", font_size=39, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.1))
        self.wait(1.2)

        left = RoundedRectangle(width=4.9, height=3.45, corner_radius=0.22, color=GREEN_3B1B, stroke_width=2.2, fill_color=GRAY_DARKER, fill_opacity=0.12)
        right = RoundedRectangle(width=4.9, height=3.45, corner_radius=0.22, color=RED_BRAIN, stroke_width=2.2, fill_color=GRAY_DARKER, fill_opacity=0.12)
        left.move_to(LEFT * 2.85 + DOWN * 0.15)
        right.move_to(RIGHT * 2.85 + DOWN * 0.15)
        self.play(FadeIn(left), FadeIn(right), run_time=0.8)

        yes_title = Text("Supported", font_size=27, color=GREEN_3B1B, weight=BOLD).move_to(left.get_top() + DOWN * 0.42)
        no_title = Text("Not implied", font_size=27, color=RED_BRAIN, weight=BOLD).move_to(right.get_top() + DOWN * 0.42)
        yes = VGroup(
            verdict_item("small", GREEN_3B1B, "sensor", True),
            verdict_item("design", GREEN_3B1B, "design", True),
            verdict_item("task", GREEN_3B1B, "task", True),
        ).arrange(RIGHT, buff=0.22)
        no = VGroup(
            verdict_item("camera", RED_BRAIN, "camera", False),
            verdict_item("4 px", RED_BRAIN, "four", False),
            verdict_item("sim=real", RED_BRAIN, "sim", False),
        ).arrange(RIGHT, buff=0.22)
        yes.move_to(left.get_center() + DOWN * 0.18)
        no.move_to(right.get_center() + DOWN * 0.18)
        self.play(Write(yes_title), Write(no_title), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.10) for t in yes], lag_ratio=0.15), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.10) for t in no], lag_ratio=0.15), run_time=1.1)
        self.play(
            LaggedStart(*[Indicate(item[2], color=emphasis_color_of(item[2]), scale_factor=1.25) for item in yes], lag_ratio=0.12),
            LaggedStart(*[Indicate(item[2], color=emphasis_color_of(item[2]), scale_factor=1.25) for item in no], lag_ratio=0.12),
            run_time=1.1,
        )
        self.wait(2.2)

        checks = VGroup(
            constraint_icon("calibration", BLUE_3B1B, "calibrate"),
            constraint_icon("noise", ORANGE_3B1B, "noise"),
            constraint_icon("power/size", PURPLE_3B1B, "power"),
        ).arrange(RIGHT, buff=1.2)
        checks.to_edge(DOWN, buff=0.52)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in checks], lag_ratio=0.18), run_time=1.2)
        self.play(
            Rotate(checks[0][0][1], angle=-PI / 5, about_point=checks[0][0][0].get_center()),
            ApplyWave(checks[1][0][1], amplitude=0.08),
            Flash(checks[2][0][1], color=emphasis_color_of(checks[2][0][1]), flash_radius=0.42),
            run_time=1.0,
        )
        self.wait(3.0)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
