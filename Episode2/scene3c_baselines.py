"""
Episode 2, Scene 3C: Baselines
==============================

Explains what the photoreceptor comparisons control for.

Run:
    manim -pql scene3c_baselines.py Scene3CBaselines
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def baseline_card(name, color, kind):
    frame = RoundedRectangle(
        width=2.12,
        height=1.66,
        corner_radius=0.18,
        color=color,
        stroke_width=2.0,
        fill_color=GRAY_DARKER,
        fill_opacity=0.12,
    )
    icon = VGroup()
    if kind == "blind":
        icon.add(
            Line(LEFT * 0.38, RIGHT * 0.38, color=color, stroke_width=2.4),
            Line(LEFT * 0.30 + UP * 0.22, RIGHT * 0.30 + DOWN * 0.22, color=RED_BRAIN, stroke_width=2.6),
        )
    elif kind == "camera":
        cells = VGroup(*[
            Square(side_length=0.16, color=color, fill_color=color, fill_opacity=0.18, stroke_width=1)
            for _ in range(16)
        ]).arrange_in_grid(rows=4, cols=4, buff=0.05)
        icon.add(cells)
    else:
        positions = [
            LEFT * 0.42 + UP * 0.18,
            LEFT * 0.12 + DOWN * 0.22,
            RIGHT * 0.28 + UP * 0.26,
            RIGHT * 0.44 + DOWN * 0.08,
            LEFT * 0.36 + DOWN * 0.04,
            RIGHT * 0.02 + UP * 0.05,
        ]
        if kind == "optimized":
            positions = [RIGHT * 0.05 + UP * 0.28, RIGHT * 0.30 + UP * 0.18, RIGHT * 0.42, RIGHT * 0.26 + DOWN * 0.18, RIGHT * 0.04 + DOWN * 0.28]
        body = Ellipse(width=0.95, height=0.55, color=color, stroke_width=1.6)
        dots = VGroup(*[Dot(p, radius=0.045, color=YELLOW_3B1B) for p in positions])
        icon.add(body, dots)
    icon.scale(0.88)
    icon.move_to(frame.get_center() + UP * 0.16)
    label = Text(name, font_size=22, color=color, weight=BOLD, line_spacing=0.95)
    if label.width > 1.72:
        label.scale_to_fit_width(1.72)
    label.move_to(frame.get_bottom() + UP * 0.28)
    return VGroup(frame, icon, label)


def bar_chart(names, values, colors):
    axis = Line(LEFT * 4.7, RIGHT * 4.7, color=GRAY_DIM, stroke_width=1.4)
    bars = VGroup()
    labels = VGroup()
    for i, (name, val, color) in enumerate(zip(names, values, colors)):
        height = 0.42 + val * 1.55
        bar = Rectangle(width=0.52, height=height, color=color, fill_color=color, fill_opacity=0.55, stroke_width=1.5)
        bar.move_to(axis.get_left() + RIGHT * (1.0 + i * 2.45) + UP * height / 2)
        labels.add(Text(name, font_size=15, color=color, weight=BOLD).next_to(bar, DOWN, buff=0.18))
        bars.add(bar)
    metric = Text("SPL = success x efficient path", font_size=17, color=YELLOW_3B1B, weight=BOLD)
    metric.next_to(axis, UP, buff=1.72)
    return VGroup(axis, bars, labels, metric)


class Scene3CBaselines(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Baselines Make the Claim Meaningful", font_size=39, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.1))
        self.wait(1.1)

        cards = VGroup(
            baseline_card("blind", RED_BRAIN, "blind"),
            baseline_card("camera", BLUE_3B1B, "camera"),
            baseline_card("random", ORANGE_3B1B, "random"),
            baseline_card("opt PR", GREEN_3B1B, "optimized"),
        ).arrange(RIGHT, buff=0.35)
        cards.move_to(UP * 1.10)

        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in cards], lag_ratio=0.15), run_time=1.8)
        self.wait(2.6)

        chart = bar_chart(
            ["blind", "camera", "random", "opt"],
            [0.18, 0.88, 0.44, 0.78],
            [RED_BRAIN, BLUE_3B1B, ORANGE_3B1B, GREEN_3B1B],
        )
        chart.move_to(DOWN * 1.82)
        chart[3].move_to(UP * 0.02)
        self.play(FadeIn(chart[0]), FadeIn(chart[3], shift=UP * 0.08), run_time=0.7)
        self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in chart[1]], lag_ratio=0.12), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(label, shift=UP * 0.06) for label in chart[2]], lag_ratio=0.10), run_time=0.6)
        score_sweep = Line(
            chart[1][0].get_top() + LEFT * 0.28 + UP * 0.12,
            chart[1][-1].get_top() + RIGHT * 0.28 + UP * 0.12,
            color=YELLOW_3B1B,
            stroke_width=2.2,
        )
        score_sweep.set_opacity(0.0)
        self.add(score_sweep)
        self.play(
            score_sweep.animate.set_opacity(0.75).shift(UP * 0.18),
            run_time=0.55,
            rate_func=there_and_back,
        )
        self.play(
            Circumscribe(cards[3], color=emphasis_color_of(cards[3]), time_width=0.55),
            Circumscribe(chart[1][3], color=emphasis_color_of(chart[1][3]), time_width=0.55),
            Flash(chart[1][3].get_top(), color=emphasis_color_of(chart[1][3]), flash_radius=0.32),
            run_time=1.0,
        )
        self.remove(score_sweep)
        self.wait(2.8)

        takeaway = Text("The claim must beat cheap controls, not just look surprising.", font_size=25, color=YELLOW_3B1B, weight=BOLD)
        takeaway.scale_to_fit_width(11.2)
        takeaway.to_edge(DOWN, buff=0.38)
        self.play(Write(takeaway, run_time=1.2))
        self.wait(4.4)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
