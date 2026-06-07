"""
Episode 3, Scene 4D: Robotization Pipeline
==========================================

Explains why a generated shape still needs to become a buildable robot.

Run:
    manim -pql scene4d_robotization_pipeline.py Scene4DRobotizationPipeline
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def stage_tile(label, color, kind):
    rect = RoundedRectangle(width=2.05, height=1.42, corner_radius=0.16, color=color, stroke_width=2.0, fill_color=GRAY_DARKER, fill_opacity=0.12)
    icon = VGroup()
    if kind == "geometry":
        icon.add(Polygon(LEFT * 0.38 + DOWN * 0.10, LEFT * 0.08 + UP * 0.30, RIGHT * 0.42 + UP * 0.10, RIGHT * 0.22 + DOWN * 0.34, color=color, stroke_width=2.0))
    elif kind == "material":
        icon.add(*[
            Rectangle(width=0.26, height=0.48, color=col, fill_color=col, fill_opacity=0.30, stroke_width=1.2).shift(LEFT * 0.39 + RIGHT * i * 0.26)
            for i, col in enumerate([BLUE_3B1B, TEAL_EP2, GREEN_3B1B, ORANGE_3B1B])
        ])
    elif kind == "actuators":
        body = RoundedRectangle(width=0.76, height=0.42, corner_radius=0.12, color=color, stroke_width=1.8)
        icon.add(
            body,
            Arrow(LEFT * 0.72, body.get_left(), color=color, buff=0.04, stroke_width=2.0, max_tip_length_to_length_ratio=0.08),
            Arrow(RIGHT * 0.72, body.get_right(), color=color, buff=0.04, stroke_width=2.0, max_tip_length_to_length_ratio=0.08),
        )
    elif kind == "controller":
        left = VGroup(*[Dot(LEFT * 0.35 + UP * y, radius=0.04, color=color) for y in [-0.22, 0, 0.22]])
        right = VGroup(*[Dot(RIGHT * 0.35 + UP * y, radius=0.04, color=color) for y in [-0.12, 0.12]])
        edges = VGroup(*[Line(a.get_center(), b.get_center(), color=color, stroke_width=0.9, stroke_opacity=0.55) for a in left for b in right])
        icon.add(edges, left, right)
    else:
        plate = Rectangle(width=0.78, height=0.38, color=color, stroke_width=1.8)
        nozzle = Polygon(UP * 0.28, LEFT * 0.16 + UP * 0.02, RIGHT * 0.16 + UP * 0.02, color=color, fill_color=color, fill_opacity=0.22)
        icon.add(plate, nozzle)
    icon.move_to(rect.get_center() + UP * 0.12)
    text = Text(label, font_size=18, color=color, weight=BOLD)
    text.move_to(rect.get_bottom() + UP * 0.23)
    return VGroup(rect, icon, text)


def constraint_chip(label, color, kind):
    base = RoundedRectangle(width=2.15, height=0.86, corner_radius=0.14, color=color, stroke_width=1.8, fill_color=color, fill_opacity=0.07)
    icon = VGroup()
    if kind == "wall":
        icon.add(Line(LEFT * 0.23, RIGHT * 0.23, color=color, stroke_width=3.2), Line(LEFT * 0.23 + DOWN * 0.16, RIGHT * 0.23 + DOWN * 0.16, color=color, stroke_width=1.2))
    elif kind == "support":
        icon.add(Polygon(LEFT * 0.28 + DOWN * 0.18, RIGHT * 0.28 + DOWN * 0.18, UP * 0.24, color=color, stroke_width=1.8))
    elif kind == "wiring":
        wire = VMobject(color=color, stroke_width=2.0)
        wire.set_points_smoothly([LEFT * 0.32, LEFT * 0.08 + UP * 0.15, RIGHT * 0.10 + DOWN * 0.14, RIGHT * 0.32])
        icon.add(wire, Dot(LEFT * 0.32, radius=0.035, color=color), Dot(RIGHT * 0.32, radius=0.035, color=color))
    else:
        ring = Arc(radius=0.30, start_angle=PI, angle=-PI, color=color, stroke_width=2.0)
        needle = Line(ORIGIN, RIGHT * 0.22 + UP * 0.08, color=color, stroke_width=2.0)
        icon.add(ring, needle)
    icon.move_to(base.get_left() + RIGHT * 0.48)
    text = Text(label, font_size=16, color=GRAY_LIGHT, weight=BOLD)
    text.move_to(base.get_left() + RIGHT * 1.35)
    return VGroup(base, icon, text)


class Scene4DRobotizationPipeline(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Robotization: From Shape to Machine", font_size=39, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.1))
        self.wait(1.2)

        boxes = VGroup(
            stage_tile("geometry", PURPLE_3B1B, "geometry"),
            stage_tile("material", GREEN_3B1B, "material"),
            stage_tile("actuators", ORANGE_3B1B, "actuators"),
            stage_tile("controller", BLUE_3B1B, "controller"),
            stage_tile("build", RED_BRAIN, "fabrication"),
        )
        boxes.arrange(RIGHT, buff=0.22)
        boxes.move_to(UP * 0.95)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), color=GRAY_MID, buff=0.05, stroke_width=2.0, max_tip_length_to_length_ratio=0.09) for i in range(len(boxes) - 1)])
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.12) for b in boxes], lag_ratio=0.12), run_time=1.8)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=1.0)
        packet = Dot(boxes[0].get_center() + DOWN * 0.48, radius=0.07, color=YELLOW_3B1B)
        self.play(FadeIn(packet, scale=0.8), run_time=0.25)
        for box in boxes[1:]:
            self.play(packet.animate.move_to(box.get_center() + DOWN * 0.48), run_time=0.28, rate_func=smooth)
        self.play(Flash(packet, color=RED_BRAIN, flash_radius=0.30), run_time=0.45)
        self.remove(packet)
        self.wait(2.6)

        loop = CurvedArrow(boxes[-1].get_bottom(), boxes[0].get_bottom(), angle=-TAU / 4, color=YELLOW_3B1B, stroke_width=2.4, tip_length=0.15)
        loop_label = Text("build fails -> revise", font_size=23, color=YELLOW_3B1B, weight=BOLD)
        loop_label.move_to(DOWN * 0.85)
        self.play(Create(loop), FadeIn(loop_label, shift=UP * 0.12), run_time=1.3)
        self.play(
            Flash(boxes[-1], color=emphasis_color_of(boxes[-1]), flash_radius=0.35),
            Circumscribe(boxes[0], color=emphasis_color_of(boxes[0]), time_width=0.55),
            run_time=0.9,
        )
        self.wait(2.8)

        constraints = VGroup(
            constraint_chip("wall", BLUE_3B1B, "wall"),
            constraint_chip("support", GREEN_3B1B, "support"),
            constraint_chip("wiring", PURPLE_3B1B, "wiring"),
            constraint_chip("limits", ORANGE_3B1B, "limits"),
        ).arrange(RIGHT, buff=0.55)
        constraints.scale_to_fit_width(10.8)
        constraints.to_edge(DOWN, buff=0.95)
        brace = Brace(constraints, UP, color=GRAY_DIM)
        brace_label = Text("engineering constraints", font_size=21, color=GRAY_MID, slant=ITALIC)
        brace_label.next_to(brace, UP, buff=0.12)
        self.play(GrowFromCenter(brace), FadeIn(brace_label), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in constraints], lag_ratio=0.12), run_time=1.2)
        self.play(
            LaggedStart(*[Indicate(c[1], color=emphasis_color_of(c[1]), scale_factor=1.12) for c in constraints], lag_ratio=0.12),
            run_time=1.25,
        )
        self.wait(3.6)

        takeaway = Text("A robot is generated, then negotiated with reality.", font_size=25, color=YELLOW_3B1B, weight=BOLD)
        takeaway.scale_to_fit_width(11.3)
        takeaway.to_edge(DOWN, buff=0.46)
        self.play(FadeOut(VGroup(brace, brace_label, constraints), shift=DOWN * 0.08), run_time=0.45)
        self.play(FadeIn(takeaway, shift=UP * 0.08), run_time=0.75)
        self.wait(4.2)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
