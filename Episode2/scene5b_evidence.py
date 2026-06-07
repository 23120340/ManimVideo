"""
Episode 2, Scene 5B: Evidence for Computational Design
======================================================

Shows the viewer what kind of evidence supports the photoreceptor result:
optimization trajectories, task metrics, and bandwidth comparison.

Run:
    manim -pql scene5b_evidence.py Scene5BEvidence
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def metric_bars(title, before, after, metric_label, color, center):
    group = VGroup()
    title_text = Text(title, font_size=22, color=color, weight=BOLD)
    max_h = 1.65
    bar_w = 0.48
    base_y = center[1] - 0.65
    xs = [center[0] - 0.38, center[0] + 0.38]

    bars = VGroup()
    labels = VGroup()
    values = VGroup()
    for x, val, name, col in [
        (xs[0], before, "before", GRAY_MID),
        (xs[1], after, "after", color),
    ]:
        bar = Rectangle(
            width=bar_w,
            height=max_h * val,
            color=col,
            stroke_width=1.5,
            fill_color=col,
            fill_opacity=0.75,
        )
        bar.move_to([x, base_y + (max_h * val) / 2, 0])
        bars.add(bar)

        label = Text(name, font_size=15, color=col)
        label.next_to(bar, DOWN, buff=0.10)
        labels.add(label)

        value = Text(f"{val:.3f}", font_size=17, color=GRAY_LIGHT)
        value.next_to(bar, UP, buff=0.10)
        values.add(value)

    axis = Line([center[0] - 0.85, base_y, 0], [center[0] + 0.85, base_y, 0], color=GRAY_DIM, stroke_width=1.4)
    metric = Text(metric_label, font_size=16, color=GRAY_MID)
    metric.next_to(axis, DOWN, buff=0.35)
    title_text.next_to(values, UP, buff=0.26)

    group.add(title_text, axis, bars, labels, values, metric)
    return group


class Scene5BEvidence(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("What Counts as Evidence?", font_size=40, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.0))
        self.wait(0.35)

        trajectory = RoundedRectangle(
            width=3.25,
            height=3.15,
            corner_radius=0.20,
            color=GREEN_3B1B,
            stroke_width=2.0,
            fill_color=GRAY_DARKER,
            fill_opacity=0.15,
        )
        trajectory.move_to(LEFT * 4.05 + DOWN * 0.15)
        traj_title = Text("Optimization Trajectories", font_size=21, color=GREEN_3B1B, weight=BOLD)
        traj_title.scale_to_fit_width(trajectory.get_width() - 0.32)
        traj_title.move_to(trajectory.get_top() + DOWN * 0.35)

        dots = VGroup()
        for i, (x, y, col) in enumerate([
            (-4.95, -0.65, RED_BRAIN),
            (-4.62, -0.35, ORANGE_3B1B),
            (-4.27, -0.05, YELLOW_3B1B),
            (-3.90, 0.18, GREEN_3B1B),
            (-3.55, 0.32, GREEN_3B1B),
        ]):
            dots.add(Dot([x, y, 0], radius=0.065 + i * 0.004, color=col))
        path = VMobject(color=GREEN_3B1B, stroke_width=2.2)
        path.set_points_smoothly([d.get_center() for d in dots])

        improve = Text("82.5% improved", font_size=25, color=GREEN_3B1B, weight=BOLD)
        improve.move_to(trajectory.get_bottom() + UP * 0.55)
        self.play(FadeIn(trajectory), FadeIn(traj_title), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=0.8) for d in dots], lag_ratio=0.15), Create(path), run_time=1.3)
        runner = Dot(dots[0].get_center(), radius=0.075, color=YELLOW_3B1B)
        self.play(FadeIn(runner, scale=0.8), run_time=0.2)
        self.play(MoveAlongPath(runner, path), run_time=1.1, rate_func=smooth)
        self.play(Flash(runner, color=emphasis_color_of(runner), flash_radius=0.28), run_time=0.45)
        self.remove(runner)
        self.play(Write(improve, run_time=0.85))
        self.wait(0.5)

        point_chart = metric_bars(
            "PointGoalNav",
            0.447,
            0.518,
            "SPL: higher is better",
            BLUE_3B1B,
            RIGHT * 0.05 + DOWN * 0.08,
        )
        target_chart = metric_bars(
            "TargetNav",
            0.363,
            0.405,
            "success rate",
            ORANGE_3B1B,
            RIGHT * 3.80 + DOWN * 0.08,
        )
        self.play(FadeIn(point_chart[0], shift=UP * 0.1), Create(point_chart[1]), run_time=0.55)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in point_chart[2]], lag_ratio=0.15), FadeIn(point_chart[3:]), run_time=1.0)
        self.play(FadeIn(target_chart[0], shift=UP * 0.1), Create(target_chart[1]), run_time=0.55)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in target_chart[2]], lag_ratio=0.15), FadeIn(target_chart[3:]), run_time=1.0)
        self.play(
            Flash(point_chart[2][1].get_top(), color=emphasis_color_of(point_chart[2][1]), flash_radius=0.24),
            Flash(target_chart[2][1].get_top(), color=emphasis_color_of(target_chart[2][1]), flash_radius=0.24),
            run_time=0.55,
        )
        self.wait(0.55)

        bandwidth_box = RoundedRectangle(
            width=8.8,
            height=0.82,
            corner_radius=0.18,
            color=TEAL_EP2,
            stroke_width=1.9,
            fill_color=TEAL_EP2,
            fill_opacity=0.10,
        )
        bandwidth_box.to_edge(DOWN, buff=0.62)
        bandwidth = Text(
            "64 PRs are still under 1% of a 128x128 camera's pixel count.",
            font_size=22,
            color=TEAL_EP2,
            weight=BOLD,
        )
        bandwidth.scale_to_fit_width(8.25)
        bandwidth.move_to(bandwidth_box)
        self.play(Create(bandwidth_box), Write(bandwidth, run_time=1.0))
        self.wait(2.0)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
