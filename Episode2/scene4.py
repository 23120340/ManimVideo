"""
scene4.py — Episode 2, Scene 4: Bi-Level Optimization
=======================================================
The mathematical core of the paper. Shows the nested loop structure,
why naive Bayesian optimization is too slow, and how collapsing both
loops into a single rollout with joint gradient flow is the key trick.

Run: manim -pql scene4.py Scene2BiLevel
"""

# VO: Bài toán hai vòng: vòng ngoài tối ưu thiết kế cảm biến θ,
# VO: vòng trong tối ưu chính sách điều khiển φ.
# VO: Cách tiếp cận naive dùng Bayesian optimization cho vòng ngoài —
# VO: nhưng mỗi iteration mất nhiều ngày.
# VO: Trick của Andre: gộp cả hai thành một rollout duy nhất.
# VO: Gradient chảy ngược qua cả θ và φ cùng một lúc.

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


class Scene2BiLevel(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title ─────────────────────────────────────────────────
        title = Text("Bi-Level Optimization", font_size=42, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        self.play(Write(title, run_time=1.1, rate_func=smooth))
        self.wait(0.4)

        # ── Nested loops diagram ──────────────────────────────────
        outer_ellipse = Ellipse(
            width=6.2, height=3.2,
            color=BLUE_3B1B, stroke_width=2.8, fill_opacity=0.08,
        )
        outer_ellipse.move_to(DOWN * 0.5)

        inner_ellipse = Ellipse(
            width=3.2, height=1.6,
            color=GREEN_3B1B, stroke_width=2.5, fill_opacity=0.12,
        )
        inner_ellipse.move_to(DOWN * 0.5)

        outer_lbl = Text("θ  —  sensor design", font_size=24, color=BLUE_3B1B, weight=BOLD)
        outer_lbl.move_to(outer_ellipse.get_top() + DOWN * 0.28)

        inner_lbl = Text("φ  —  control policy", font_size=22, color=GREEN_3B1B, weight=BOLD)
        inner_lbl.move_to(inner_ellipse.get_center())

        outer_loop_label = Text("OUTER LOOP", font_size=16, color=BLUE_3B1B)
        outer_loop_label.next_to(outer_ellipse, LEFT, buff=0.12)

        inner_loop_label = Text("INNER LOOP", font_size=16, color=GREEN_3B1B)
        inner_loop_label.next_to(inner_ellipse, DOWN, buff=0.18)

        # Direction arrows on ellipses (clockwise for outer, counter for inner)
        outer_arc_arrow = CurvedArrow(
            outer_ellipse.get_right() + UP * 0.5,
            outer_ellipse.get_left() + UP * 0.5,
            angle=-PI / 1.6,
            color=BLUE_3B1B, stroke_width=2.2,
            tip_length=0.18,
        )
        inner_arc_arrow = CurvedArrow(
            inner_ellipse.get_left() + UP * 0.25,
            inner_ellipse.get_right() + UP * 0.25,
            angle=-PI / 2.0,
            color=GREEN_3B1B, stroke_width=2.2,
            tip_length=0.15,
        )

        self.play(
            Create(outer_ellipse, run_time=1.0, rate_func=smooth),
            run_time=1.0,
        )
        self.play(
            Create(inner_ellipse, run_time=0.8, rate_func=smooth),
            FadeIn(outer_lbl, run_time=0.6),
            FadeIn(inner_lbl, run_time=0.6),
        )
        self.play(
            Create(outer_arc_arrow, run_time=0.8),
            Create(inner_arc_arrow, run_time=0.8),
            FadeIn(outer_loop_label, run_time=0.5),
            FadeIn(inner_loop_label, run_time=0.5),
        )
        self.wait(0.8)

        # ── Naive approach: Bayesian outer loop ───────────────────
        naive_title = Text("Naive Approach: Bayesian Outer Loop", font_size=26, color=GRAY_LIGHT)
        naive_title.to_corner(DL, buff=0.6)

        cost_text = Text("Each outer iteration  →  1 000 rollouts", font_size=21, color=GRAY_MID)
        cost_text.next_to(naive_title, DOWN, buff=0.2, aligned_edge=LEFT)
        time_text = Text("≈  2 days per iteration", font_size=21, color=RED_BRAIN)
        time_text.next_to(cost_text, DOWN, buff=0.15, aligned_edge=LEFT)

        self.play(
            FadeIn(naive_title, run_time=0.7),
            FadeIn(cost_text, shift=RIGHT * 0.2, run_time=0.7),
        )
        self.play(FadeIn(time_text, shift=RIGHT * 0.2, run_time=0.7))

        red_x = Text("✗  Too slow.", font_size=26, color=RED_BRAIN, weight=BOLD)
        red_x.next_to(time_text, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(red_x, scale=1.2, run_time=0.6))
        self.wait(0.8)

        # ── Fade out naive section to make room ───────────────────
        self.play(
            FadeOut(VGroup(outer_ellipse, inner_ellipse, outer_lbl, inner_lbl,
                           outer_loop_label, inner_loop_label,
                           outer_arc_arrow, inner_arc_arrow,
                           naive_title, cost_text, time_text, red_x),
                    run_time=0.8),
        )

        # ── The trick: single rollout ─────────────────────────────
        trick_title = Text("The Trick: One Rollout, Two Gradients", font_size=30, color=GREEN_3B1B, weight=BOLD)
        trick_title.move_to(UP * 2.0)
        self.play(Write(trick_title, run_time=1.0, rate_func=smooth))
        self.wait(0.3)

        # Timeline bar
        timeline_bg = Rectangle(
            width=8.0, height=0.55,
            fill_color=GRAY_DARKER, fill_opacity=0.7,
            stroke_color=GRAY_DIM, stroke_width=1.5,
        )
        timeline_bg.move_to(UP * 0.6)

        timeline_label = Text("Single Rollout", font_size=20, color=GRAY_LIGHT)
        timeline_label.next_to(timeline_bg, UP, buff=0.15)

        self.play(
            FadeIn(timeline_bg, run_time=0.7),
            FadeIn(timeline_label, run_time=0.6),
        )

        # Interleaved design + control actions on timeline
        n_pairs = 6
        w_total = 7.6
        seg_w   = w_total / (n_pairs * 2)
        left_x  = timeline_bg.get_left()[0] + seg_w / 2 + 0.2

        design_segs  = VGroup()
        control_segs = VGroup()

        for i in range(n_pairs):
            x_d = left_x + i * 2 * seg_w
            x_c = x_d + seg_w

            d_rect = Rectangle(
                width=seg_w * 0.88, height=0.45,
                fill_color=BLUE_3B1B, fill_opacity=0.75,
                stroke_width=0,
            )
            d_rect.move_to([x_d, timeline_bg.get_center()[1], 0])
            design_segs.add(d_rect)

            c_rect = Rectangle(
                width=seg_w * 0.88, height=0.45,
                fill_color=GREEN_3B1B, fill_opacity=0.75,
                stroke_width=0,
            )
            c_rect.move_to([x_c, timeline_bg.get_center()[1], 0])
            control_segs.add(c_rect)

        self.play(
            LaggedStart(
                *[FadeIn(s, scale=0.9) for s in design_segs + control_segs],
                lag_ratio=0.08, run_time=1.4,
            )
        )

        # Legend
        leg_d = Square(side_length=0.18, fill_color=BLUE_3B1B, fill_opacity=1, stroke_width=0)
        leg_d_lbl = Text("design action (θ)", font_size=17, color=BLUE_3B1B)
        leg_d_grp = VGroup(leg_d, leg_d_lbl).arrange(RIGHT, buff=0.1)
        leg_d_grp.next_to(timeline_bg, DOWN, buff=0.18).shift(LEFT * 2.0)

        leg_c = Square(side_length=0.18, fill_color=GREEN_3B1B, fill_opacity=1, stroke_width=0)
        leg_c_lbl = Text("control action (φ)", font_size=17, color=GREEN_3B1B)
        leg_c_grp = VGroup(leg_c, leg_c_lbl).arrange(RIGHT, buff=0.1)
        leg_c_grp.next_to(timeline_bg, DOWN, buff=0.18).shift(RIGHT * 1.6)

        self.play(FadeIn(leg_d_grp, run_time=0.5), FadeIn(leg_c_grp, run_time=0.5))
        self.wait(0.3)

        # Backward gradient arrows
        grad_theta = Arrow(
            timeline_bg.get_left() + DOWN * 0.6,
            timeline_bg.get_left() + DOWN * 0.6 + RIGHT * 3.5,
            color=BLUE_3B1B, buff=0, stroke_width=2.8,
            max_tip_length_to_length_ratio=0.18,
        )
        grad_theta.flip()
        grad_theta.move_to(timeline_bg.get_left() + DOWN * 0.85 + RIGHT * 1.9)

        grad_phi = Arrow(
            timeline_bg.get_right() + DOWN * 0.6,
            timeline_bg.get_right() + DOWN * 0.6 + LEFT * 3.5,
            color=GREEN_3B1B, buff=0, stroke_width=2.8,
            max_tip_length_to_length_ratio=0.18,
        )
        grad_phi.move_to(timeline_bg.get_right() + DOWN * 1.2 + LEFT * 1.9)

        gt_lbl = Text("∇_θ", font_size=22, color=BLUE_3B1B)
        gt_lbl.next_to(grad_theta, UP, buff=0.08)
        gp_lbl = Text("∇_φ", font_size=22, color=GREEN_3B1B)
        gp_lbl.next_to(grad_phi, DOWN, buff=0.08)

        self.play(
            GrowArrow(grad_theta, run_time=0.9, rate_func=smooth),
            FadeIn(gt_lbl, run_time=0.6),
        )
        self.play(
            GrowArrow(grad_phi, run_time=0.9, rate_func=smooth),
            FadeIn(gp_lbl, run_time=0.6),
        )

        same_pass_lbl = Text("← same backward pass →", font_size=19, color=YELLOW_3B1B)
        same_pass_lbl.next_to(grad_phi, DOWN, buff=0.15)
        self.play(FadeIn(same_pass_lbl, run_time=0.6))
        self.wait(0.5)

        # ── Equations ─────────────────────────────────────────────
        eq1 = MathTex(
            r"\theta^* = \arg\max_\theta \, \mathbb{E}_\tau "
            r"\left[ R(\tau;\, \theta,\, \varphi^*(\theta)) \right]",
            font_size=32, color=GRAY_LIGHT,
        )
        eq1.to_edge(DOWN, buff=1.1)

        eq2 = MathTex(
            r"\nabla_\theta \mathcal{L}, \quad \nabla_\varphi \mathcal{L} \quad"
            r"\longleftarrow \text{same backward pass}",
            font_size=28, color=GRAY_LIGHT,
        )
        eq2.next_to(eq1, DOWN, buff=0.32)

        self.play(Write(eq1, run_time=1.6, rate_func=smooth))
        self.wait(0.4)
        self.play(Write(eq2, run_time=1.4, rate_func=smooth))
        self.wait(0.5)

        # ── Speedup callout ───────────────────────────────────────
        speedup_txt = Text(
            "10× faster convergence\nthan Bayesian outer loop",
            font_size=24, color=GREEN_3B1B, weight=BOLD, line_spacing=1.3,
        )
        speedup_box = SurroundingRectangle(
            speedup_txt, color=GREEN_3B1B, buff=0.22, stroke_width=2.0, corner_radius=0.1,
        )
        speedup_group = VGroup(speedup_box, speedup_txt)
        speedup_group.to_corner(DR, buff=0.5)

        self.play(
            Create(speedup_box, run_time=0.8),
            Write(speedup_txt, run_time=0.9),
        )
        self.wait(2.0)

        # ── FadeOut everything ────────────────────────────────────
        all_objects = VGroup(
            title, trick_title,
            timeline_bg, timeline_label, design_segs, control_segs,
            leg_d_grp, leg_c_grp,
            grad_theta, grad_phi, gt_lbl, gp_lbl, same_pass_lbl,
            eq1, eq2, speedup_group,
        )
        self.play(FadeOut(all_objects, run_time=1.2, rate_func=smooth))
        self.wait(0.2)
