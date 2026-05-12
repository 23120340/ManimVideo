"""
scene3.py — Episode 3, Scene 3: Co-Design (Brain + Body)
Section A: single backward pass updates both θ and φ.
Section B: stiffness map on a soft-body robot.
Section C: scaling line chart — naive vs co-design.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


def make_box(label, w, h, color, fs=22):
    r = RoundedRectangle(
        width=w,
        height=h,
        corner_radius=0.12,
        color=color,
        stroke_width=2.5,
        fill_color=BG_COLOR,
        fill_opacity=1,
    )
    t = Text(label, font_size=fs, color=color, weight=BOLD)
    t.move_to(r.get_center())
    return VGroup(r, t)


class Scene3CoDesign(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title ──────────────────────────────────────────────────────
        title = Text(
            "Co-Design: Brain + Body Together",
            font_size=34,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.5)

        # ── SECTION A ──────────────────────────────────────────────────
        left_box = make_box("θ — body design", 2.8, 0.9, BLUE_3B1B, fs=22)
        left_box.move_to(LEFT * 2.4 + UP * 1.5)

        right_box = make_box("φ — controller", 2.8, 0.9, GREEN_3B1B, fs=22)
        right_box.move_to(RIGHT * 2.4 + UP * 1.5)

        self.play(
            LaggedStart(
                GrowFromCenter(left_box),
                GrowFromCenter(right_box),
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )

        merge_dot = Dot(point=ORIGIN, radius=0.09, color=GRAY_LIGHT)
        merge_label = Text(
            "Same backward pass",
            font_size=18,
            color=GRAY_LIGHT,
            slant=ITALIC,
        )
        merge_label.next_to(merge_dot, DOWN, buff=0.18)

        loss_box = make_box("Loss  L", 1.9, 0.75, YELLOW_3B1B, fs=22)
        loss_box.move_to(DOWN * 1.7)

        self.play(
            GrowFromCenter(loss_box),
            FadeIn(merge_dot, scale=0.6),
            FadeIn(merge_label, shift=DOWN * 0.1),
            run_time=1.0,
        )

        arr_up = Arrow(
            loss_box[0].get_top(),
            merge_dot.get_bottom(),
            color=YELLOW_3B1B,
            buff=0.08,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.18,
        )
        self.play(GrowArrow(arr_up), run_time=0.6)

        arr_to_theta = Arrow(
            merge_dot.get_top(),
            left_box[0].get_bottom(),
            color=BLUE_3B1B,
            buff=0.08,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.18,
        )
        arr_to_phi = Arrow(
            merge_dot.get_top(),
            right_box[0].get_bottom(),
            color=GREEN_3B1B,
            buff=0.08,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.18,
        )

        self.play(
            LaggedStart(
                GrowArrow(arr_to_theta),
                GrowArrow(arr_to_phi),
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )

        lbl_grad_theta = MathTex(
            r"\nabla_\theta", font_size=32, color=BLUE_3B1B
        )
        lbl_grad_theta.next_to(arr_to_theta.get_center(), LEFT, buff=0.18)

        lbl_grad_phi = MathTex(
            r"\nabla_\phi", font_size=32, color=GREEN_3B1B
        )
        lbl_grad_phi.next_to(arr_to_phi.get_center(), RIGHT, buff=0.18)

        self.play(
            FadeIn(lbl_grad_theta),
            FadeIn(lbl_grad_phi),
            run_time=0.6,
        )
        self.wait(1.5)

        # FadeOut Section A
        section_a = VGroup(
            left_box, right_box, merge_dot, merge_label,
            loss_box, arr_up, arr_to_theta, arr_to_phi,
            lbl_grad_theta, lbl_grad_phi,
        )
        self.play(FadeOut(section_a), run_time=1.0)
        self.wait(0.3)

        # ── SECTION B: Robot stiffness map ─────────────────────────────
        robot_center = LEFT * 1.0
        body_rect = Rectangle(
            width=1.5,
            height=1.0,
            color=GRAY_MID,
            fill_color=GRAY_DARKER,
            fill_opacity=1,
            stroke_width=2.5,
        ).move_to(robot_center)

        # 4 legs from corners
        corners = [
            body_rect.get_corner(UL),
            body_rect.get_corner(UR),
            body_rect.get_corner(DL),
            body_rect.get_corner(DR),
        ]
        leg_tips = [
            corners[0] + UP * 0.35 + LEFT * 0.3,
            corners[1] + UP * 0.35 + RIGHT * 0.3,
            corners[2] + DOWN * 0.35 + LEFT * 0.3,
            corners[3] + DOWN * 0.35 + RIGHT * 0.3,
        ]
        legs = VGroup(*[
            Line(c, t, color=GRAY_MID, stroke_width=2.5)
            for c, t in zip(corners, leg_tips)
        ])
        tips = VGroup(*[
            Circle(radius=0.14, color=RED_BRAIN, fill_opacity=0.9, stroke_width=0).move_to(t)
            for t in leg_tips
        ])
        soft_center = Circle(
            radius=0.38,
            color=BLUE_3B1B,
            fill_opacity=0.45,
            stroke_width=0,
        ).move_to(body_rect.get_center())

        robot_group = VGroup(body_rect, legs, soft_center, tips)

        # Legend
        legend_row1 = VGroup(
            Circle(radius=0.12, color=RED_BRAIN, fill_opacity=0.9, stroke_width=0),
            Text("stiff — leg tips push", font_size=17, color=RED_BRAIN),
        ).arrange(RIGHT, buff=0.2)

        legend_row2 = VGroup(
            Circle(radius=0.12, color=BLUE_3B1B, fill_opacity=0.55, stroke_width=0),
            Text("soft — body center flexes", font_size=17, color=BLUE_3B1B),
        ).arrange(RIGHT, buff=0.2)

        legend = VGroup(legend_row1, legend_row2).arrange(
            DOWN, buff=0.4, aligned_edge=LEFT
        )
        legend.move_to(RIGHT * 3.0)
        legend.set_y(robot_center[1])

        self.play(
            FadeIn(body_rect),
            Create(legs),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[GrowFromCenter(t) for t in tips], lag_ratio=0.15),
            run_time=1.0,
        )
        self.play(FadeIn(soft_center), run_time=0.7)
        self.play(FadeIn(legend, shift=LEFT * 0.2), run_time=0.9)
        self.wait(1.5)

        # FadeOut Section B
        section_b = VGroup(robot_group, legend)
        self.play(FadeOut(section_b), run_time=1.0)
        self.wait(0.3)

        # ── SECTION C: line chart ──────────────────────────────────────
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1, 0.5],
            x_length=6,
            y_length=2.8,
            axis_config={"color": GRAY_MID, "stroke_width": 2, "include_ticks": True},
            tips=False,
        )
        axes.move_to(DOWN * 0.3)

        x_axis_label = Text(
            "Model size / parameters",
            font_size=18,
            color=GRAY_LIGHT,
        )
        x_axis_label.next_to(axes, DOWN, buff=0.35)

        y_axis_label = Text(
            "Loss",
            font_size=18,
            color=GRAY_LIGHT,
        )
        y_axis_label.next_to(axes, LEFT, buff=0.2)
        y_axis_label.rotate(PI / 2)

        # naive curve: dashed, RED_BRAIN, slight upward (worse)
        naive_curve_solid = axes.plot(
            lambda x: 0.78 - 0.10 * x + 0.04 * x ** 1.2,
            x_range=[0.1, 4.9],
            color=RED_BRAIN,
            stroke_width=3,
        )
        naive_curve = DashedVMobject(naive_curve_solid, num_dashes=22)

        codesign_curve = axes.plot(
            lambda x: 0.35 - 0.045 * (x - 0.3) if x < 0.3 else 0.35 - 0.045 * (x - 0.3),
            x_range=[0.1, 4.9],
            color=GREEN_3B1B,
            stroke_width=3,
        )
        # Better: monotonic improvement with model size
        codesign_curve = axes.plot(
            lambda x: max(0.07, 0.50 - 0.085 * x),
            x_range=[0.1, 4.9],
            color=GREEN_3B1B,
            stroke_width=3.5,
        )

        naive_label = Text(
            "naive scaling",
            font_size=17,
            color=RED_BRAIN,
        )
        naive_y_end = 0.78 - 0.10 * 4.7 + 0.04 * 4.7 ** 1.2
        naive_label.next_to(axes.c2p(4.7, naive_y_end), RIGHT, buff=0.15)

        codesign_label = Text(
            "co-design",
            font_size=17,
            color=GREEN_3B1B,
            weight=BOLD,
        )
        codesign_y_end = max(0.07, 0.50 - 0.085 * 4.7)
        codesign_label.next_to(axes.c2p(4.7, codesign_y_end), RIGHT, buff=0.15)

        # Bottom callout
        callout_text = Text(
            "More parameters → BETTER, not worse",
            font_size=22,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        callout_text.to_edge(DOWN, buff=0.5)
        callout_rect = SurroundingRectangle(
            callout_text,
            color=YELLOW_3B1B,
            buff=0.18,
            corner_radius=0.1,
            stroke_width=2,
        )

        self.play(
            Create(axes),
            FadeIn(x_axis_label),
            FadeIn(y_axis_label),
            run_time=1.2,
        )
        self.play(Create(naive_curve), run_time=1.2)
        self.play(Write(naive_label), run_time=0.6)
        self.play(Create(codesign_curve), run_time=1.2)
        self.play(Write(codesign_label), run_time=0.6)
        self.play(
            Write(callout_text),
            Create(callout_rect),
            run_time=1.5,
        )
        self.wait(2.0)

        # ── FadeOut all ────────────────────────────────────────────────
        everything = VGroup(
            title,
            axes, x_axis_label, y_axis_label,
            naive_curve, naive_label,
            codesign_curve, codesign_label,
            callout_text, callout_rect,
        )
        self.play(FadeOut(everything), run_time=1.2)
        self.wait(0.4)
