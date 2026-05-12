"""
scene1.py — Episode 3, Scene 1: Hook
"RL: 10,000 rollouts. This: 12." — animated iteration counter, progress bar,
soft robot that converges to walking, gradient-through-physics callout.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


class Scene3Hook(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title ──────────────────────────────────────────────────────
        title = Text(
            "RL: 10,000 rollouts.  This: 12.",
            font_size=30,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.8)
        self.wait(0.6)

        # ── Iteration counter row ──────────────────────────────────────
        iter_label = Text("Iteration", font_size=28, color=GRAY_MID)
        iter_num = Text("1", font_size=48, color=YELLOW_3B1B, weight=BOLD)
        iter_total = Text("/ 12", font_size=32, color=GRAY_MID)
        counter_row = VGroup(iter_label, iter_num, iter_total).arrange(
            RIGHT, buff=0.25, aligned_edge=DOWN
        )
        counter_row.move_to(UP * 2.4)

        self.play(FadeIn(counter_row, shift=UP * 0.1), run_time=0.8)

        # ── Progress bar ───────────────────────────────────────────────
        bar_bg = Rectangle(
            width=6.0,
            height=0.22,
            color=GRAY_DARKER,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(UP * 1.7)

        def make_bar_fill(value, color=TEAL_EP2):
            f = Rectangle(
                width=max(6.0 * value / 12, 0.001),
                height=0.22,
                color=color,
                fill_opacity=1,
                stroke_width=0,
            )
            f.move_to(bar_bg.get_left() + RIGHT * (6.0 * value / 12) / 2)
            return f

        bar_fill = make_bar_fill(1, TEAL_EP2)

        self.play(FadeIn(bar_bg), FadeIn(bar_fill), run_time=0.7)

        # ── Soft robot at DOWN*0.5 ─────────────────────────────────────
        robot_pos = DOWN * 0.5
        body_ellipse = Ellipse(
            width=1.4,
            height=0.9,
            color=TEAL_EP2,
            fill_opacity=0.3,
            stroke_width=2.5,
        ).move_to(robot_pos)

        angles = [PI / 4, 3 * PI / 4, -PI / 4, -3 * PI / 4]
        limbs = VGroup()
        tips = VGroup()
        for a in angles:
            base = body_ellipse.get_center() + np.array(
                [np.cos(a) * 0.55, np.sin(a) * 0.4, 0]
            )
            tip_pt = body_ellipse.get_center() + np.array(
                [np.cos(a) * 1.15, np.sin(a) * 0.9, 0]
            )
            limbs.add(Line(base, tip_pt, color=TEAL_EP2, stroke_width=3))
            tips.add(
                Circle(
                    radius=0.1,
                    color=TEAL_EP2,
                    fill_opacity=0.6,
                    stroke_width=0,
                ).move_to(tip_pt)
            )

        robot = VGroup(body_ellipse, limbs, tips)

        self.play(FadeIn(body_ellipse), run_time=0.6)
        self.play(
            LaggedStart(*[Create(l) for l in limbs], lag_ratio=0.15),
            run_time=0.9,
        )
        self.play(
            LaggedStart(*[GrowFromCenter(t) for t in tips], lag_ratio=0.12),
            run_time=0.7,
        )
        self.wait(0.4)

        # ── Iteration loop 2 → 12 ──────────────────────────────────────
        current_rotation = 0.0
        for i in range(2, 13):
            num_color = GREEN_3B1B if i == 12 else YELLOW_3B1B
            new_num = Text(
                str(i),
                font_size=48,
                color=num_color,
                weight=BOLD,
            )
            new_num.move_to(iter_num.get_center())

            fill_color = GREEN_3B1B if i == 12 else TEAL_EP2
            new_fill = make_bar_fill(i, fill_color)

            # Robot motion script
            if i == 2:
                robot_anim = robot.animate.rotate(PI / 12)
                current_rotation += PI / 12
            elif i == 3:
                robot_anim = robot.animate.rotate(-PI / 8)
                current_rotation -= PI / 8
            elif i == 4:
                robot_anim = robot.animate.rotate(PI / 16)
                current_rotation += PI / 16
            elif i == 5:
                robot_anim = robot.animate.rotate(-PI / 20)
                current_rotation -= PI / 20
            elif i == 6:
                robot_anim = robot.animate.rotate(-current_rotation).scale(1.05)
                current_rotation = 0.0
            elif i in (7, 9, 11):
                robot_anim = robot.animate.shift(UP * 0.05)
            elif i in (8, 10):
                robot_anim = robot.animate.shift(DOWN * 0.05)
            else:  # i == 12
                robot_anim = robot.animate.scale(1.0)

            self.play(
                ReplacementTransform(iter_num, new_num),
                ReplacementTransform(bar_fill, new_fill),
                robot_anim,
                run_time=0.5,
            )
            iter_num = new_num
            bar_fill = new_fill

        self.wait(0.4)

        # ── Robot walks (right, then back) ─────────────────────────────
        self.play(robot.animate.shift(RIGHT * 1.5), run_time=1.0)
        self.play(robot.animate.shift(LEFT * 1.5), run_time=0.8)
        self.wait(0.3)

        # ── Bottom callout ─────────────────────────────────────────────
        callout_text = Text(
            "Gradient flows through the physics simulation",
            font_size=22,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        callout_text.to_edge(DOWN, buff=0.55)
        callout_rect = SurroundingRectangle(
            callout_text,
            color=YELLOW_3B1B,
            buff=0.18,
            corner_radius=0.1,
            stroke_width=2,
        )
        self.play(
            Write(callout_text),
            Create(callout_rect),
            run_time=1.5,
        )
        self.wait(2.0)

        # ── FadeOut all ────────────────────────────────────────────────
        everything = VGroup(
            title,
            counter_row,
            iter_num,
            bar_bg,
            bar_fill,
            robot,
            callout_text,
            callout_rect,
        )
        self.play(FadeOut(everything), run_time=1.2)
        self.wait(0.4)
