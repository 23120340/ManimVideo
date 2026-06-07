"""
Episode 3, Scene 5B: Limitations Checklist
=========================================

Adds a sober ending before the final synthesis.

Run:
    manim -pql scene5b_limitations.py Scene5BLimitations
"""

import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def risk_badge(label, color, kind):
    ring = Circle(radius=0.48, color=color, stroke_width=2.0, fill_color=color, fill_opacity=0.10)
    icon = VGroup()
    if kind == "model":
        icon.add(Rectangle(width=0.42, height=0.28, color=BLUE_3B1B, stroke_width=1.5).shift(LEFT * 0.16))
        icon.add(Circle(radius=0.17, color=ORANGE_3B1B, stroke_width=1.5).shift(RIGHT * 0.20))
        icon.add(Line(LEFT * 0.02, RIGHT * 0.04, color=RED_BRAIN, stroke_width=2.0))
    elif kind == "basin":
        curve = VMobject(color=color, stroke_width=2.0)
        curve.set_points_smoothly([LEFT * 0.34 + UP * 0.18, LEFT * 0.12 + DOWN * 0.24, RIGHT * 0.12 + DOWN * 0.05, RIGHT * 0.34 + UP * 0.12])
        icon.add(curve, Dot(LEFT * 0.12 + DOWN * 0.24, radius=0.04, color=YELLOW_3B1B))
    elif kind == "memory":
        icon.add(*[
            Rectangle(width=0.18, height=0.34, color=color, fill_color=color, fill_opacity=0.18, stroke_width=1.1).shift(LEFT * 0.24 + RIGHT * i * 0.16)
            for i in range(4)
        ])
    elif kind == "build":
        icon.add(Rectangle(width=0.50, height=0.32, color=color, stroke_width=1.5))
        icon.add(Polygon(UP * 0.30, LEFT * 0.16 + UP * 0.03, RIGHT * 0.16 + UP * 0.03, color=color, fill_color=color, fill_opacity=0.25))
    else:
        icon.add(Arc(radius=0.28, start_angle=PI * 0.15, angle=PI * 0.70, color=color, stroke_width=2.0))
        icon.add(Line(DOWN * 0.04, RIGHT * 0.24 + UP * 0.12, color=color, stroke_width=2.0))
    icon.move_to(ring)
    text = Text(label, font_size=16, color=color, weight=BOLD)
    text.next_to(ring, DOWN, buff=0.14)
    return VGroup(ring, icon, text)


class Scene5BLimitations(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("What Still Makes This Hard?", font_size=40, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(FadeIn(title, shift=DOWN * 0.10), run_time=0.75)
        self.wait(0.15)

        robot = VGroup(
            Ellipse(width=1.05, height=0.62, color=TEAL_EP2, stroke_width=2.4, fill_color=TEAL_EP2, fill_opacity=0.12),
            Dot(LEFT * 0.25 + UP * 0.02, radius=0.055, color=YELLOW_3B1B),
            Dot(RIGHT * 0.25 + UP * 0.02, radius=0.055, color=YELLOW_3B1B),
            Line(LEFT * 0.30 + DOWN * 0.28, LEFT * 0.55 + DOWN * 0.62, color=TEAL_EP2, stroke_width=2.0),
            Line(RIGHT * 0.30 + DOWN * 0.28, RIGHT * 0.55 + DOWN * 0.62, color=TEAL_EP2, stroke_width=2.0),
        ).move_to(UP * 0.10)

        items = [
            ("model", RED_BRAIN, "model", 100),
            ("optima", ORANGE_3B1B, "basin", 28),
            ("memory", BLUE_3B1B, "memory", -42),
            ("build", GREEN_3B1B, "build", -140),
            ("safety", PURPLE_3B1B, "safety", 178),
        ]
        badges = VGroup()
        spokes = VGroup()
        for label, color, kind, deg in items:
            angle = math.radians(deg)
            target = robot.get_center() + RIGHT * (3.25 * math.cos(angle)) + UP * (2.00 * math.sin(angle))
            badge = risk_badge(label, color, kind).move_to(target)
            badges.add(badge)
            spokes.add(Line(robot.get_center(), badge[0].get_center(), color=color, stroke_width=1.7, stroke_opacity=0.65))

        rings = VGroup(
            Ellipse(width=5.8, height=3.4, color=GRAY_DIM, stroke_width=1.1, stroke_opacity=0.35).move_to(robot),
            Ellipse(width=3.6, height=2.1, color=GRAY_DIM, stroke_width=1.0, stroke_opacity=0.25).move_to(robot),
        )
        self.play(Create(rings), FadeIn(robot, scale=0.9), run_time=0.85)
        self.play(LaggedStart(*[Create(s) for s in spokes], lag_ratio=0.08), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(b, scale=0.92) for b in badges], lag_ratio=0.10), run_time=1.15)
        scan_pts = [
            robot.get_center() + RIGHT * (2.90 * math.cos(math.radians(a))) + UP * (1.70 * math.sin(math.radians(a)))
            for a in range(0, 361, 36)
        ]
        scan_path = VMobject(color=YELLOW_3B1B, stroke_width=1.2)
        scan_path.set_points_smoothly(scan_pts)
        scan = Dot(scan_pts[0], radius=0.055, color=YELLOW_3B1B)
        self.play(FadeIn(scan, scale=0.8), run_time=0.20)
        self.play(MoveAlongPath(scan, scan_path), run_time=1.6, rate_func=smooth)
        self.play(
            LaggedStart(*[Indicate(badge[0], color=emphasis_color_of(badge[0]), scale_factor=1.13) for badge in badges], lag_ratio=0.10),
            run_time=1.2,
        )
        self.remove(scan)
        self.wait(0.4)

        takeaway = Text(
            "Powerful because it exposes constraints, not because it removes them.",
            font_size=24,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        takeaway.scale_to_fit_width(11.2)
        takeaway.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(takeaway, shift=UP * 0.08), run_time=0.8)
        self.wait(2.5)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
