"""
Episode 1, Scene 2B: Vision Trade-Offs
======================================

Turns the biological eye montage into a design-space argument.

Run:
    manim -pql scene2b_vision_tradeoffs.py Scene2BVisionTradeoffs
"""

from manim import *
from common import *


def chip(label, color, width=1.65):
    box = RoundedRectangle(
        width=width,
        height=0.52,
        corner_radius=0.15,
        color=color,
        stroke_width=1.7,
        fill_color=color,
        fill_opacity=0.13,
    )
    text = Text(label, font_size=16, color=GRAY_LIGHT, weight=BOLD)
    if text.width > width - 0.22:
        text.scale_to_fit_width(width - 0.22)
    text.move_to(box)
    return VGroup(box, text)


def goat_icon(color=BLUE_3B1B):
    fov = Arc(radius=0.67, start_angle=132 * DEGREES, angle=126 * DEGREES, color=color, stroke_width=1.2)
    fov.shift(RIGHT * 0.02 + DOWN * 0.02)
    body = Ellipse(width=0.72, height=0.38, color=color, stroke_width=1.6, fill_color=color, fill_opacity=0.11)
    body.shift(LEFT * 0.08 + DOWN * 0.08)
    neck = Line(RIGHT * 0.20 + UP * 0.04, RIGHT * 0.38 + UP * 0.15, color=color, stroke_width=1.5)
    head = Ellipse(width=0.34, height=0.24, color=color, stroke_width=1.6, fill_color=color, fill_opacity=0.12)
    head.rotate(-12 * DEGREES)
    head.move_to(RIGHT * 0.48 + UP * 0.15)
    snout = Polygon(
        RIGHT * 0.60 + UP * 0.21,
        RIGHT * 0.82 + UP * 0.14,
        RIGHT * 0.61 + UP * 0.06,
        color=color,
        fill_color=BG_COLOR,
        fill_opacity=0.45,
        stroke_width=1.2,
    )
    ear = Polygon(
        RIGHT * 0.36 + UP * 0.26,
        RIGHT * 0.26 + UP * 0.43,
        RIGHT * 0.50 + UP * 0.31,
        color=color,
        fill_color=color,
        fill_opacity=0.14,
        stroke_width=1.2,
    )
    horn_front = Arc(radius=0.16, start_angle=60 * DEGREES, angle=118 * DEGREES, color=GRAY_LIGHT, stroke_width=1.15)
    horn_back = Arc(radius=0.14, start_angle=82 * DEGREES, angle=106 * DEGREES, color=GRAY_LIGHT, stroke_width=1.05)
    horn_front.shift(RIGHT * 0.45 + UP * 0.30)
    horn_back.shift(RIGHT * 0.32 + UP * 0.29)
    beard = Line(RIGHT * 0.55 + UP * 0.02, RIGHT * 0.48 + DOWN * 0.20, color=color, stroke_width=1.1)
    legs = VGroup(*[
        Line(LEFT * 0.34 + RIGHT * i * 0.18 + DOWN * 0.23, LEFT * 0.38 + RIGHT * i * 0.18 + DOWN * 0.52, color=color, stroke_width=1.25)
        for i in range(4)
    ])
    tail = Line(LEFT * 0.48 + UP * 0.02, LEFT * 0.65 + UP * 0.18, color=color, stroke_width=1.25)
    eye = Dot(RIGHT * 0.55 + UP * 0.17, radius=0.022, color=YELLOW_3B1B)
    return VGroup(fov, body, neck, head, snout, ear, horn_back, horn_front, beard, legs, tail, eye)


def scallop_icon(color=PURPLE_3B1B):
    center = DOWN * 0.12
    radius = 0.46
    arc = Arc(radius=radius, start_angle=18 * DEGREES, angle=144 * DEGREES, color=color, stroke_width=1.7)
    arc.shift(center)
    base = Dot(DOWN * 0.36, radius=0.025, color=color)
    ribs = VGroup()
    eyes = VGroup()
    for angle in np.linspace(26, 154, 9):
        point = center + np.array([radius * np.cos(angle * DEGREES), radius * np.sin(angle * DEGREES), 0])
        ribs.add(Line(base.get_center(), point, color=color, stroke_width=0.85, stroke_opacity=0.78))
        eyes.add(Dot(point, radius=0.016, color=YELLOW_3B1B))
    ears = VGroup(
        Polygon(LEFT * 0.18 + DOWN * 0.35, LEFT * 0.42 + DOWN * 0.22, LEFT * 0.30 + DOWN * 0.42, color=color, fill_color=color, fill_opacity=0.10, stroke_width=1.0),
        Polygon(RIGHT * 0.18 + DOWN * 0.35, RIGHT * 0.42 + DOWN * 0.22, RIGHT * 0.30 + DOWN * 0.42, color=color, fill_color=color, fill_opacity=0.10, stroke_width=1.0),
    )
    hinge = Arc(radius=0.16, start_angle=20 * DEGREES, angle=140 * DEGREES, color=color, stroke_width=1.15)
    hinge.move_to(DOWN * 0.29)
    return VGroup(arc, ribs, ears, hinge, eyes, base)


def eagle_icon(color=ORANGE_3B1B):
    acuity = VGroup(
        Line(LEFT * 0.02, RIGHT * 0.72 + UP * 0.09, color=color, stroke_width=1.15, stroke_opacity=0.78),
        Line(LEFT * 0.02, RIGHT * 0.72 + DOWN * 0.09, color=color, stroke_width=1.15, stroke_opacity=0.78),
    )
    head = VMobject(color=color, stroke_width=1.6, fill_opacity=0)
    head.set_points_smoothly([
        LEFT * 0.34 + DOWN * 0.12,
        LEFT * 0.18 + UP * 0.24,
        RIGHT * 0.16 + UP * 0.25,
        RIGHT * 0.34 + UP * 0.10,
        RIGHT * 0.18 + DOWN * 0.22,
        LEFT * 0.10 + DOWN * 0.26,
        LEFT * 0.34 + DOWN * 0.12,
    ])
    beak = Polygon(
        RIGHT * 0.25 + UP * 0.08,
        RIGHT * 0.67 + UP * 0.01,
        RIGHT * 0.28 + DOWN * 0.13,
        color=color,
        fill_color=color,
        fill_opacity=0.18,
        stroke_width=1.2,
    )
    hook = Arc(radius=0.10, start_angle=-28 * DEGREES, angle=-105 * DEGREES, color=color, stroke_width=1.15)
    hook.shift(RIGHT * 0.56 + DOWN * 0.06)
    brow = Line(LEFT * 0.03 + UP * 0.10, RIGHT * 0.11 + UP * 0.05, color=GRAY_LIGHT, stroke_width=1.05)
    eye = Dot(RIGHT * 0.06 + UP * 0.04, radius=0.022, color=YELLOW_3B1B)
    neck = Line(LEFT * 0.22 + DOWN * 0.17, LEFT * 0.38 + DOWN * 0.42, color=color, stroke_width=1.4)
    return VGroup(acuity, head, beak, hook, brow, eye, neck)


def variable_pair(header, labels, color):
    header_text = Text(header, font_size=12, color=color, weight=BOLD)
    items = VGroup(*[
        chip(label, color, width=max(1.34, 0.15 * len(label) + 0.78)).scale(0.82)
        for label in labels
    ]).arrange(DOWN, buff=0.18)
    return VGroup(header_text, items).arrange(DOWN, buff=0.10)


class Scene2BVisionTradeoffs(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("There Is No Universal Eye", font_size=38, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.30)
        self.play(Write(title, run_time=1.0))
        self.wait(0.35)

        axis = DoubleArrow(
            LEFT * 4.35,
            RIGHT * 4.35,
            color=GRAY_MID,
            stroke_width=2.4,
            max_tip_length_to_length_ratio=0.035,
        )
        axis.move_to(UP * 1.04)
        left_label = Text("wide field of view", font_size=20, color=BLUE_3B1B, weight=BOLD)
        right_label = Text("high acuity", font_size=20, color=ORANGE_3B1B, weight=BOLD)
        left_label.next_to(axis.get_left(), DOWN, buff=0.22)
        right_label.next_to(axis.get_right(), DOWN, buff=0.22)

        goat_dot = Dot(axis.point_from_proportion(0.17), radius=0.075, color=BLUE_3B1B)
        eagle_dot = Dot(axis.point_from_proportion(0.84), radius=0.075, color=ORANGE_3B1B)
        scallop_dot = Dot(axis.point_from_proportion(0.42), radius=0.075, color=PURPLE_3B1B)
        goat_label = Text("goat", font_size=15, color=BLUE_3B1B).next_to(goat_dot, UP, buff=0.10)
        eagle_label = Text("eagle", font_size=15, color=ORANGE_3B1B).next_to(eagle_dot, UP, buff=0.10)
        scallop_label = Text("scallop", font_size=15, color=PURPLE_3B1B).next_to(scallop_dot, UP, buff=0.10)

        goat_marker = goat_icon(BLUE_3B1B).scale(0.70).next_to(goat_label, UP, buff=0.08)
        scallop_marker = scallop_icon(PURPLE_3B1B).scale(0.68).next_to(scallop_label, UP, buff=0.08)
        eagle_marker = eagle_icon(ORANGE_3B1B).scale(0.72).next_to(eagle_label, UP, buff=0.08)

        self.play(GrowArrow(axis), FadeIn(left_label), FadeIn(right_label), run_time=0.9)
        self.play(
            LaggedStart(
                FadeIn(goat_dot, scale=1.4), FadeIn(goat_label), FadeIn(goat_marker, shift=DOWN * 0.08),
                FadeIn(scallop_dot, scale=1.4), FadeIn(scallop_label), FadeIn(scallop_marker, shift=DOWN * 0.08),
                FadeIn(eagle_dot, scale=1.4), FadeIn(eagle_label), FadeIn(eagle_marker, shift=DOWN * 0.08),
                lag_ratio=0.16,
            ),
            run_time=1.2,
        )
        self.wait(0.55)

        design_title = Text("design variables", font_size=25, color=GRAY_LIGHT, weight=BOLD)
        design_title.move_to(DOWN * 0.48)
        link_arrow = Arrow(
            axis.get_center() + DOWN * 0.34,
            design_title.get_top() + UP * 0.10,
            color=GRAY_DIM,
            stroke_width=1.5,
            tip_length=0.12,
            buff=0.02,
        )
        link_label = Text("trade-offs depend on variables", font_size=13, color=GRAY_MID)
        link_label.next_to(link_arrow, RIGHT, buff=0.12)
        self.play(GrowArrow(link_arrow), FadeIn(link_label, shift=LEFT * 0.05), run_time=0.6)
        self.play(FadeIn(design_title, shift=UP * 0.12), run_time=0.5)

        variable_groups = VGroup(
            variable_pair("coverage", ["FOV", "placement"], BLUE_3B1B),
            variable_pair("detail", ["resolution", "optics"], ORANGE_3B1B),
            variable_pair("constraints", ["sensitivity", "energy cost"], PURPLE_3B1B),
        ).arrange(RIGHT, buff=0.56)
        variable_groups.move_to(DOWN * 1.42)
        self.play(
            LaggedStart(*[FadeIn(group, scale=0.94) for group in variable_groups], lag_ratio=0.10),
            run_time=1.1,
        )
        self.wait(0.7)

        bottom_text = Text(
            "Biology optimizes for a niche, not for a pretty eye diagram.",
            font_size=20,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        bottom_box = RoundedRectangle(
            width=11.3,
            height=0.58,
            corner_radius=0.14,
            color=YELLOW_3B1B,
            stroke_width=1.5,
            fill_color=YELLOW_3B1B,
            fill_opacity=0.07,
        )
        bottom_text.scale_to_fit_width(bottom_box.width - 0.45)
        bottom = VGroup(bottom_box, bottom_text)
        bottom.move_to(DOWN * 2.94)
        self.play(Write(bottom, run_time=1.2))
        self.wait(2.2)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
