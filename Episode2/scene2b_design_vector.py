"""
Episode 2, Scene 2B: Photoreceptor Design Vector
================================================

Expands the photoreceptor definition from "three ideas" into the actual
parameterization used for design: position, orientation, and field of view.

Run:
    manim -pql scene2b_design_vector.py Scene2BDesignVector
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def labeled_chip(text, color, width=0.76, height=0.34, font_size=15):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.10,
        color=color,
        stroke_width=1.45,
        fill_color=color,
        fill_opacity=0.13,
    )
    label = Text(text, font_size=font_size, color=GRAY_LIGHT, weight=BOLD)
    if label.width > width - 0.18:
        label.scale_to_fit_width(width - 0.18)
    label.move_to(box)
    return VGroup(box, label)


def make_card(title, lines, color, width=2.85, height=2.02):
    frame = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        color=color,
        stroke_width=2.1,
        fill_color=GRAY_DARKER,
        fill_opacity=0.18,
    )
    title_text = Text(title, font_size=20, color=color, weight=BOLD)
    if title_text.width > width - 0.35:
        title_text.scale_to_fit_width(width - 0.35)
    title_text.move_to(frame.get_top() + DOWN * 0.36)

    body = VGroup()
    for line in lines:
        line_text = Text(line, font_size=17, color=GRAY_LIGHT)
        if line_text.width > width - 0.45:
            line_text.scale_to_fit_width(width - 0.45)
        body.add(line_text)
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    if body.height > height - 0.95:
        body.scale_to_fit_height(height - 0.95)
    body.move_to(frame.get_center() + DOWN * 0.18)

    return VGroup(frame, title_text, body)


def anchored_cone(origin, angle=55 * DEGREES, fov=50 * DEGREES, length=1.15, color=GREEN_3B1B):
    p0 = np.array(origin)
    p1 = p0 + length * np.array([np.cos(angle - fov / 2), np.sin(angle - fov / 2), 0])
    p2 = p0 + length * np.array([np.cos(angle + fov / 2), np.sin(angle + fov / 2), 0])
    return Polygon(p0, p1, p2, color=color, stroke_width=1.8, fill_color=color, fill_opacity=0.20)


class Scene2BDesignVector(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text(
            "A Photoreceptor Is a Design Vector",
            font_size=39,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.0))
        self.wait(0.35)

        robot = RoundedRectangle(
            width=1.15,
            height=1.62,
            corner_radius=0.20,
            color=GRAY_MID,
            stroke_width=2.3,
            fill_color=GRAY_DARKER,
            fill_opacity=0.35,
        )
        robot.move_to(LEFT * 4.45 + DOWN * 0.1)
        robot_label = Text("robot body", font_size=17, color=GRAY_MID)
        robot_label.next_to(robot, DOWN, buff=0.14)

        sensor = Dot(robot.get_top() + DOWN * 0.25 + RIGHT * 0.06, radius=0.075, color=YELLOW_3B1B)
        cone = anchored_cone(sensor.get_center(), angle=55 * DEGREES, fov=50 * DEGREES, length=1.10)
        sensor_label = Text("one PR sensor", font_size=18, color=YELLOW_3B1B, weight=BOLD)
        sensor_label.next_to(cone, UP, buff=0.12)

        self.play(Create(robot), FadeIn(robot_label), run_time=0.8)
        self.play(FadeIn(sensor, scale=1.4), FadeIn(cone, scale=0.55), run_time=0.8)
        self.play(FadeIn(sensor_label, shift=UP * 0.1), run_time=0.45)
        self.wait(0.45)
        self.play(FadeOut(sensor_label, run_time=0.35))

        vector = MathTex(
            r"\theta_i=\bigl(x_i,\ y_i,\ z_i,\ \operatorname{pitch}_i,\ \operatorname{yaw}_i,\ \operatorname{roll}_i,\ \operatorname{fov}_i\bigr)",
            font_size=34,
            color=GRAY_LIGHT,
        )
        if vector.width > 9.25:
            vector.scale_to_fit_width(9.25)
        vector.move_to(RIGHT * 1.25 + UP * 1.82)
        vector_box = SurroundingRectangle(vector, color=emphasis_color_of(vector), buff=0.22, stroke_width=1.7)
        self.play(Create(vector_box), Write(vector, run_time=1.25))
        self.wait(0.55)

        position_card = make_card(
            "Position",
            ["body anchor", "x / y / z"],
            BLUE_3B1B,
        )
        orientation_card = make_card(
            "Orientation",
            ["look direction", "pitch / yaw / roll"],
            ORANGE_3B1B,
        )
        fov_card = make_card(
            "Field of View",
            ["cone width", "fov"],
            GREEN_3B1B,
        )

        cards = VGroup(position_card, orientation_card, fov_card)
        cards.arrange(RIGHT, buff=0.54)
        cards.scale_to_fit_width(8.00)
        cards.move_to(RIGHT * 1.25 + DOWN * 0.35)

        pos_chips = VGroup(
            labeled_chip("x", BLUE_3B1B, width=0.70),
            labeled_chip("y", BLUE_3B1B, width=0.70),
            labeled_chip("z", BLUE_3B1B, width=0.70),
        )
        pos_chips.arrange(RIGHT, buff=0.07)
        pos_chips.next_to(position_card, DOWN, buff=0.16)

        ori_chips = VGroup(
            labeled_chip("pitch", ORANGE_3B1B, width=0.86, font_size=14),
            labeled_chip("yaw", ORANGE_3B1B, width=0.76, font_size=14),
            labeled_chip("roll", ORANGE_3B1B, width=0.76, font_size=14),
        )
        ori_chips.arrange(RIGHT, buff=0.07)
        ori_chips.next_to(orientation_card, DOWN, buff=0.16)

        fov_chips = VGroup(labeled_chip("fov", GREEN_3B1B, width=0.82))
        fov_chips.next_to(fov_card, DOWN, buff=0.16)

        self.play(FadeIn(position_card, shift=UP * 0.2), run_time=0.65)
        new_sensor_center = robot.get_left() + RIGHT * 0.16
        sensor_shift = new_sensor_center - sensor.get_center()
        self.play(
            LaggedStart(*[FadeIn(chip, scale=0.85) for chip in pos_chips], lag_ratio=0.12),
            sensor.animate.move_to(new_sensor_center),
            cone.animate.shift(sensor_shift),
            run_time=0.8,
        )
        self.wait(0.35)

        direction_arrow = Arrow(
            sensor.get_center(),
            sensor.get_center() + RIGHT * 0.62 + UP * 0.08,
            color=ORANGE_3B1B,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.10,
        )
        self.play(FadeIn(orientation_card, shift=UP * 0.2), Create(direction_arrow), run_time=0.75)
        self.play(
            LaggedStart(*[FadeIn(chip, scale=0.85) for chip in ori_chips], lag_ratio=0.12),
            Rotate(direction_arrow, angle=-45 * DEGREES, about_point=sensor.get_center()),
            run_time=0.85,
        )
        self.wait(0.35)

        self.play(FadeIn(fov_card, shift=UP * 0.2), FadeIn(fov_chips, scale=0.9), run_time=0.75)
        wide_cone = anchored_cone(sensor.get_center(), angle=30 * DEGREES, fov=82 * DEGREES, length=1.22)
        wide_cone.set_fill(opacity=0.16)
        self.play(Transform(cone, wide_cone), run_time=0.75)
        self.wait(0.45)

        insight = Text(
            "One sensor = 7 numbers.  N sensors = 7N variables.",
            font_size=24,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        insight.scale_to_fit_width(11.2)
        note = Text(
            "Task-optimized layout, not hand-picked.",
            font_size=22,
            color=GRAY_LIGHT,
        )
        bottom_text = VGroup(insight, note).arrange(DOWN, buff=0.16)
        bottom_text.to_edge(DOWN, buff=0.42)
        self.play(Write(insight, run_time=1.0))
        self.play(FadeIn(note, shift=UP * 0.12), run_time=0.7)
        self.wait(2.2)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
