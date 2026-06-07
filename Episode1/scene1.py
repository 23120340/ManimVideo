"""
SCENE 1 — Câu hỏi chính (0:35 – 2:00)
=====================================

Tập 1 — "Cá chết vẫn biết bơi"

A. Cá schematic + highlight BRAIN (đỏ) / BODY (xanh)
B. Não fade out — thân vẫn quẫy
C. Sweep aside
D. Split 2 pane: θ_brain (NN, "fast, flexible") | θ_body (cá + dots, "slow, rigid")
E. NN flicker (não thay đổi nhanh); body params chỉ pulse nhẹ
F. Đóng: θ = (θ_brain, θ_body)

Run:
    manim -pql scene1.py Scene1MainQuestion
"""

from manim import *
import numpy as np
from common import *


class Scene1MainQuestion(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ============================================================
        # PART A — Cá + nhãn BRAIN/BODY
        # ============================================================
        fish = create_fish(color=GRAY_LIGHT).scale(1.4).move_to(ORIGIN)
        self.play(Create(fish), run_time=1.8)
        self.wait(0.5)

        brain_glow = Circle(
            radius=0.55, color=RED_BRAIN,
            fill_opacity=0.45, stroke_width=2,
        ).move_to(fish[2].get_center())

        brain_label = Text(
            "BRAIN", font_size=28, color=RED_BRAIN, weight=BOLD,
        ).next_to(brain_glow, UR, buff=0.45)
        brain_arrow = Line(
            brain_label.get_corner(DL) + DL * 0.05,
            brain_glow.get_top() + UR * 0.05,
            color=RED_BRAIN, stroke_width=2,
        )

        body_glow = Ellipse(
            width=2.4, height=1.0,
            color=BLUE_3B1B, fill_opacity=0.35, stroke_width=2,
        ).move_to(fish[0].get_center() + LEFT * 0.3)

        body_label = Text(
            "BODY", font_size=28, color=BLUE_3B1B, weight=BOLD,
        ).next_to(body_glow, DOWN, buff=0.6)
        body_arrow = Line(
            body_label.get_top() + UP * 0.05,
            body_glow.get_bottom() + DOWN * 0.05,
            color=BLUE_3B1B, stroke_width=2,
        )

        self.play(
            FadeIn(brain_glow), Create(brain_arrow), Write(brain_label),
            run_time=1.4,
        )
        self.wait(0.7)
        self.play(
            FadeIn(body_glow), Create(body_arrow), Write(body_label),
            run_time=1.4,
        )
        self.wait(3.0)

        # ============================================================
        # PART B — Não tắt; thân vẫn quẫy
        # ============================================================
        self.play(
            FadeOut(brain_glow), FadeOut(brain_arrow),
            brain_label.animate.set_color(GRAY_DIM).set_opacity(0.35),
            run_time=2.0,
        )

        body_pack = VGroup(body_glow, body_arrow, body_label)
        for shift_dir in [RIGHT * 0.22, LEFT * 0.44, RIGHT * 0.44, LEFT * 0.22]:
            self.play(body_pack.animate.shift(shift_dir),
                      run_time=0.7, rate_func=smooth)
        self.wait(1.2)

        # ============================================================
        # PART C — Sweep aside
        # ============================================================
        old_stuff = VGroup(fish, brain_label, body_pack)
        self.play(FadeOut(old_stuff), run_time=1.2)
        self.wait(0.3)

        # ============================================================
        # PART D — Hai pane song song
        # ============================================================
        nn_group, nn_edges, _ = create_neural_net(
            layer_sizes=[3, 5, 5, 2],
            radius=0.13, h_buff=0.55, v_buff=0.32,
            node_color=BLUE_3B1B,
        )
        nn_group.scale(0.85).move_to(LEFT * 3.6 + DOWN * 0.4)

        theta_brain = MathTex(
            r"\theta_{\mathrm{brain}}", font_size=44, color=YELLOW_3B1B,
        ).next_to(nn_group, UP, buff=0.5)

        fast_label = Text(
            "fast, flexible",
            font_size=24, color=GRAY_LIGHT, slant=ITALIC,
        ).next_to(nn_group, DOWN, buff=0.5)

        body_outline = create_fish(color=BLUE_3B1B)
        body_outline.scale(0.85).move_to(RIGHT * 3.6 + DOWN * 0.4)

        body_center = body_outline[0].get_center()
        param_offsets = [
            LEFT * 0.6 + UP * 0.18,
            LEFT * 0.15 + DOWN * 0.05,
            RIGHT * 0.45 + DOWN * 0.18,
            RIGHT * 0.85 + UP * 0.10,
            LEFT * 1.0 + DOWN * 0.12,
        ]
        param_dots = VGroup(*[
            Dot(body_center + off, radius=0.08, color=YELLOW_3B1B)
            for off in param_offsets
        ])

        theta_body = MathTex(
            r"\theta_{\mathrm{body}}", font_size=44, color=YELLOW_3B1B,
        ).next_to(body_outline, UP, buff=0.5)
        theta_body.align_to(theta_brain, UP)

        slow_label = Text(
            "slow, rigid",
            font_size=24, color=GRAY_LIGHT, slant=ITALIC,
        ).next_to(body_outline, DOWN, buff=0.5)
        slow_label.align_to(fast_label, UP)

        divider = DashedLine(
            UP * 3.0, DOWN * 3.0,
            color=GRAY_DIM, stroke_opacity=0.45, dash_length=0.18,
        )

        self.play(Create(divider), run_time=0.8)
        self.play(Create(nn_group), Write(theta_brain), run_time=2.0)
        self.play(FadeIn(fast_label, shift=UP * 0.15), run_time=0.7)
        self.wait(0.5)
        self.play(Create(body_outline), Write(theta_body), run_time=2.0)
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in param_dots], lag_ratio=0.18),
            run_time=1.4,
        )
        self.play(FadeIn(slow_label, shift=UP * 0.15), run_time=0.7)
        self.wait(2.0)

        # ============================================================
        # PART E — Tốc độ thay đổi khác nhau
        # ============================================================
        rng = np.random.default_rng(42)
        for _ in range(8):
            idxs = rng.choice(len(nn_edges), size=8, replace=False)
            flashing = [nn_edges[i] for i in idxs]
            self.play(
                *[e.animate.set_stroke(emphasis_color_of(e), width=2.6, opacity=1.0)
                  for e in flashing],
                run_time=0.16, rate_func=rush_into,
            )
            self.play(
                *[e.animate.set_stroke(GRAY_DIM, width=1, opacity=0.55)
                  for e in flashing],
                run_time=0.16, rate_func=rush_from,
            )

        self.play(*[d.animate.scale(1.25) for d in param_dots], run_time=0.5)
        self.play(*[d.animate.scale(1 / 1.25) for d in param_dots], run_time=0.5)
        self.wait(2.0)

        # ============================================================
        # PART F — Đóng
        # ============================================================
        unifying = MathTex(
            r"\theta=(\theta_{\mathrm{brain}},\theta_{\mathrm{body}})",
            font_size=46,
            color=GRAY_LIGHT,
        ).to_edge(UP, buff=0.5)

        box = SurroundingRectangle(
            unifying, color=emphasis_color_of(unifying),
            buff=0.25, stroke_width=2, stroke_opacity=0.85,
        )

        self.play(Write(unifying), run_time=1.8)
        self.play(Create(box), run_time=1.0)

        caption = Text(
            "parameters  —  both can be optimized",
            font_size=22, color=YELLOW_3B1B, slant=ITALIC,
        ).next_to(box, DOWN, buff=0.3)
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self.wait(3.0)

        everything = VGroup(
            divider, nn_group, theta_brain, fast_label,
            body_outline, theta_body, slow_label, param_dots,
            unifying, box, caption,
        )
        self.play(FadeOut(everything), run_time=1.5)
        self.wait(0.5)
