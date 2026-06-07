"""
Episode 1, Scene 4B: Utility Depends on Context
===============================================

Expands the math formulation: utility is defined by task, environment, and cost.

Run:
    manim -pql scene4b_utility_context.py Scene4BUtilityContext
"""

from manim import *
from common import *


def utility_icon(label, color, kind):
    tile = RoundedRectangle(
        width=2.20,
        height=1.16,
        corner_radius=0.16,
        color=color,
        stroke_width=2.0,
        fill_color=GRAY_DARKER,
        fill_opacity=0.14,
    )
    icon = VGroup()
    if kind == "theta":
        body = Ellipse(width=0.58, height=0.34, color=color, stroke_width=2.0)
        eye = Dot(body.get_right() + LEFT * 0.14 + UP * 0.02, radius=0.035, color=YELLOW_3B1B)
        icon.add(body, eye)
    elif kind == "task":
        pole = Line(UP * 0.22, DOWN * 0.28, color=color, stroke_width=2.0)
        flag = Polygon(pole.get_top(), pole.get_top() + RIGHT * 0.38 + DOWN * 0.12, pole.get_top() + DOWN * 0.24, color=color, fill_color=color, fill_opacity=0.35)
        icon.add(pole, flag)
    elif kind == "world":
        icon.add(
            Line(LEFT * 0.42 + DOWN * 0.26, LEFT * 0.42 + UP * 0.26, color=color, stroke_width=2),
            Line(LEFT * 0.42 + UP * 0.26, RIGHT * 0.42 + UP * 0.26, color=color, stroke_width=2),
            Line(RIGHT * 0.42 + UP * 0.26, RIGHT * 0.42 + DOWN * 0.26, color=color, stroke_width=2),
        )
    else:
        battery = RoundedRectangle(width=0.64, height=0.34, corner_radius=0.04, color=color, stroke_width=2)
        nub = Rectangle(width=0.08, height=0.16, color=color, fill_color=color, fill_opacity=0.5).next_to(battery, RIGHT, buff=0.02)
        fill = Rectangle(width=0.30, height=0.20, color=color, fill_color=color, fill_opacity=0.35).move_to(battery.get_left() + RIGHT * 0.20)
        icon.add(battery, nub, fill)
    icon.move_to(tile.get_center() + UP * 0.11)
    text = Text(label, font_size=17, color=color, weight=BOLD)
    text.move_to(tile.get_bottom() + UP * 0.22)
    return VGroup(tile, icon, text)


def eye_layout(color=BLUE_3B1B):
    base = Ellipse(width=0.85, height=0.50, color=color, stroke_width=1.8)
    dots = VGroup(*[
        Dot(base.get_center() + LEFT * 0.20 + RIGHT * i * 0.20, radius=0.035, color=YELLOW_3B1B)
        for i in range(3)
    ])
    return VGroup(base, dots)


def context_world(title, color, success=True):
    frame = RoundedRectangle(width=4.55, height=2.05, corner_radius=0.22, color=color, stroke_width=2.0, fill_color=GRAY_DARKER, fill_opacity=0.10)
    label = Text(title, font_size=21, color=color, weight=BOLD).move_to(frame.get_top() + DOWN * 0.35)
    eye = eye_layout(color).scale(0.85).move_to(frame.get_left() + RIGHT * 1.20 + DOWN * 0.05)
    arena = Rectangle(width=1.52, height=0.98, color=GRAY_DIM, stroke_width=1.5).move_to(frame.get_right() + LEFT * 1.15 + DOWN * 0.07)
    goal = Dot(arena.get_right() + LEFT * 0.35 + UP * 0.20, radius=0.07, color=GREEN_3B1B)
    path_color = GREEN_3B1B if success else RED_BRAIN
    path = VMobject(color=path_color, stroke_width=3.0)
    if success:
        path.set_points_smoothly([
            arena.get_left() + RIGHT * 0.20 + DOWN * 0.22,
            arena.get_center() + LEFT * 0.05,
            goal.get_center(),
        ])
        badge = Text("works", font_size=17, color=GREEN_3B1B, weight=BOLD)
    else:
        wall = Line(arena.get_center() + UP * 0.34, arena.get_center() + DOWN * 0.34, color=RED_BRAIN, stroke_width=3.0)
        path.set_points_smoothly([
            arena.get_left() + RIGHT * 0.20 + DOWN * 0.22,
            arena.get_center() + LEFT * 0.10,
            arena.get_center() + RIGHT * 0.12,
        ])
        badge = Text("fails", font_size=17, color=RED_BRAIN, weight=BOLD)
        arena = VGroup(arena, wall)
    badge.move_to(frame.get_bottom() + UP * 0.25)
    arrow = Arrow(eye.get_right(), arena.get_left(), color=GRAY_MID, buff=0.10, stroke_width=2.0)
    return VGroup(frame, label, eye, arrow, arena, goal, path, badge)


class Scene4BUtilityContext(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("A Design Is Only Good in Context", font_size=38, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(FadeIn(title, shift=DOWN * 0.10), run_time=0.8)
        self.wait(1.2)

        formula = MathTex(
            r"\max_{\theta}\; U(\theta;\mathrm{task},\mathrm{environment},\mathrm{cost})",
            font_size=36,
            color=GRAY_LIGHT,
        )
        formula.scale_to_fit_width(11.4)
        formula.move_to(UP * 1.75)
        self.play(FadeIn(formula, shift=UP * 0.08), run_time=0.9)
        self.wait(2.6)

        boxes = VGroup(
            utility_icon("design", BLUE_3B1B, "theta"),
            utility_icon("task", GREEN_3B1B, "task"),
            utility_icon("world", ORANGE_3B1B, "world"),
            utility_icon("cost", PURPLE_3B1B, "cost"),
        ).arrange(RIGHT, buff=0.28)
        boxes.move_to(UP * 0.18)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.12) for b in boxes], lag_ratio=0.12), run_time=1.8)
        self.play(
            LaggedStart(*[
                Succession(
                    b[1].animate.scale(1.12).set_stroke(width=2.8),
                    b[1].animate.scale(1 / 1.12).set_stroke(width=2.0),
                )
                for b in boxes
            ], lag_ratio=0.18),
            run_time=1.4,
        )
        self.wait(1.1)

        left = context_world("TargetNav", GREEN_3B1B, success=True).move_to(LEFT * 2.35 + DOWN * 1.62)
        right = context_world("WallFollow", RED_BRAIN, success=False).move_to(RIGHT * 2.35 + DOWN * 1.62)
        left_shell = VGroup(left[0], left[1], left[2], left[3], left[4], left[5])
        right_shell = VGroup(right[0], right[1], right[2], right[3], right[4], right[5])
        self.play(
            FadeIn(left_shell),
            FadeIn(right_shell),
            run_time=1.0,
        )
        self.play(Create(left[6]), Create(right[6]), run_time=1.15, rate_func=smooth)
        self.play(
            FadeIn(left[7], shift=UP * 0.06),
            FadeIn(right[7], shift=UP * 0.06),
            Flash(left[5], color=emphasis_color_of(left[5]), flash_radius=0.25),
            Flash(right[4][1].get_center(), color=emphasis_color_of(right[4][1]), flash_radius=0.35),
            run_time=0.9,
        )
        same = Text("same layout, different world", font_size=18, color=GRAY_MID, slant=ITALIC)
        same.move_to(DOWN * 2.80)
        self.play(FadeIn(same, shift=UP * 0.06), run_time=0.65)
        self.wait(4.0)

        takeaway = Text("Optimization makes assumptions visible.", font_size=27, color=YELLOW_3B1B, weight=BOLD)
        takeaway.scale_to_fit_width(11.3)
        takeaway.to_edge(DOWN, buff=0.32)
        self.play(FadeOut(same), run_time=0.35)
        self.play(FadeIn(takeaway, shift=UP * 0.08), run_time=0.8)
        self.wait(4.0)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
