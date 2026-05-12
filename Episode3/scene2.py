"""
scene2.py — Episode 3, Scene 2: Differentiable Simulation
Shows forward pass pipeline, backward pass gradient flow,
and implicit vs explicit integration comparison.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


def make_pipeline_box(label_str, box_width, box_height, box_color, text_color=None, font_size=18):
    """Create a labeled RoundedRectangle box for the pipeline."""
    if text_color is None:
        text_color = box_color
    rect = RoundedRectangle(
        width=box_width, height=box_height,
        corner_radius=0.12,
        color=box_color,
        stroke_width=2.5,
        fill_color=BG_COLOR,
        fill_opacity=1.0,
    )
    label = Text(label_str, font_size=font_size, color=text_color, line_spacing=1.35)
    label.move_to(rect.get_center())
    return VGroup(rect, label)


class Scene3DiffSim(Scene):
    def construct(self):
        # ── Background ──────────────────────────────────────────────
        self.camera.background_color = BG_COLOR

        # VO: "Simulator là một chuỗi các bước vật lý. Khi ta đặt simulator
        #       vào trong vòng lặp tối ưu, gradient cần chảy ngược qua từng bước đó —
        #       giống như backpropagation trong mạng nơ-ron, nhưng thay vì ma trận
        #       trọng số, ta backprop qua các phương trình Newton."

        # ── Section A: Title ────────────────────────────────────────
        title = Text(
            "Differentiable Simulation",
            font_size=38,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.5)

        # ── Section A: Forward pipeline ──────────────────────────────
        fwd_label = Text("FORWARD PASS", font_size=20, color=GRAY_MID)

        # Build 5 pipeline boxes
        box_state0 = make_pipeline_box("state₀", 1.1, 0.7, BLUE_3B1B, BLUE_3B1B)
        box_phys   = make_pipeline_box("physics\nstep", 1.3, 0.7, ORANGE_3B1B, ORANGE_3B1B)
        box_state1 = make_pipeline_box("state₁", 1.1, 0.7, BLUE_3B1B, BLUE_3B1B)
        box_dots   = make_pipeline_box("...", 0.7, 0.7, GRAY_MID, GRAY_MID, font_size=22)
        box_reward = make_pipeline_box("reward", 1.1, 0.7, GREEN_3B1B, GREEN_3B1B)

        pipeline = VGroup(box_state0, box_phys, box_state1, box_dots, box_reward)
        pipeline.arrange(RIGHT, buff=0.6)
        pipeline.move_to(UP * 1.5)

        fwd_label.next_to(pipeline, UP, buff=0.3)

        # Animate boxes appearing
        self.play(FadeIn(fwd_label, shift=DOWN * 0.2), run_time=0.6)
        self.play(
            LaggedStart(
                GrowFromCenter(box_state0),
                GrowFromCenter(box_phys),
                GrowFromCenter(box_state1),
                GrowFromCenter(box_dots),
                GrowFromCenter(box_reward),
                lag_ratio=0.25,
            ),
            run_time=2.0,
        )

        # Forward arrows between boxes
        fwd_arrows = VGroup()
        box_list = [box_state0, box_phys, box_state1, box_dots, box_reward]
        for i in range(len(box_list) - 1):
            arr = Arrow(
                start=box_list[i].get_right(),
                end=box_list[i + 1].get_left(),
                color=GRAY_MID,
                buff=0.05,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.25,
            )
            fwd_arrows.add(arr)

        self.play(
            LaggedStart(*[GrowArrow(a) for a in fwd_arrows], lag_ratio=0.25),
            run_time=1.5,
        )
        self.wait(1.5)

        # ── Section B: Backward pass ─────────────────────────────────
        # 3 curved arrows going right-to-left under the pipeline
        bwd_arrows = VGroup()

        # reward -> state1
        bwd_arr1 = CurvedArrow(
            start_point=box_reward.get_bottom() + DOWN * 0.05,
            end_point=box_state1.get_bottom() + DOWN * 0.05,
            angle=-PI / 3,
            color=RED_BRAIN,
            stroke_width=2.5,
        )
        # state1 -> physics
        bwd_arr2 = CurvedArrow(
            start_point=box_state1.get_bottom() + DOWN * 0.05,
            end_point=box_phys.get_bottom() + DOWN * 0.05,
            angle=-PI / 3,
            color=RED_BRAIN,
            stroke_width=2.5,
        )
        # physics -> state0
        bwd_arr3 = CurvedArrow(
            start_point=box_phys.get_bottom() + DOWN * 0.05,
            end_point=box_state0.get_bottom() + DOWN * 0.05,
            angle=-PI / 3,
            color=RED_BRAIN,
            stroke_width=2.5,
        )
        bwd_arrows.add(bwd_arr1, bwd_arr2, bwd_arr3)

        bwd_label = Text(
            "BACKWARD PASS — gradient flows through physics",
            font_size=20,
            color=RED_BRAIN,
        )
        bwd_label.move_to(DOWN * 0.5)

        self.play(
            LaggedStart(
                Create(bwd_arr1),
                Create(bwd_arr2),
                Create(bwd_arr3),
                lag_ratio=0.35,
            ),
            run_time=2.0,
        )
        self.play(Write(bwd_label), run_time=1.0)
        self.wait(1.5)

        # ── Section C: Memory cost comparison ───────────────────────
        self.play(
            FadeOut(VGroup(bwd_arrows, bwd_label)),
            run_time=0.8,
        )

        # Move pipeline to top
        self.play(
            pipeline.animate.move_to(UP * 2.6).scale(0.78),
            fwd_label.animate.move_to(UP * 3.1).scale(0.78),
            FadeOut(fwd_arrows),
            run_time=1.0,
        )
        self.wait(0.4)

        # Vertical divider
        divider = DashedLine(
            UP * 3.5, DOWN * 3.5,
            color=GRAY_DIM,
            stroke_width=1.5,
            dash_length=0.15,
        )
        self.play(Create(divider), run_time=0.8)

        # Left column — Explicit integration
        left_header = Text(
            "Explicit integration",
            font_size=22,
            color=GREEN_3B1B,
            weight=BOLD,
        )
        left_header.move_to(LEFT * 2.8 + UP * 1.5)

        left_bullets_texts = [
            "• Store ALL intermediate states",
            "• Memory ∝ T steps",
            "• T ≈ 1,000,000 steps/sec",
        ]
        left_bullets = VGroup(*[
            Text(t, font_size=18, color=GRAY_LIGHT)
            for t in left_bullets_texts
        ])
        left_bullets.arrange(DOWN, buff=0.32)
        left_bullets.next_to(left_header, DOWN, buff=0.38)
        # Ensure x stays in left panel
        left_bullets.set_x(LEFT[0] * 2.8)

        # Right column — Implicit integration
        right_header = Text(
            "Implicit integration",
            font_size=22,
            color=ORANGE_3B1B,
            weight=BOLD,
        )
        right_header.move_to(RIGHT * 2.8 + UP * 1.5)

        right_bullets_texts = [
            "• Solve implicit equation each step",
            "• Lower memory usage",
            "• Slightly less accurate",
        ]
        right_bullets = VGroup(*[
            Text(t, font_size=18, color=GRAY_LIGHT)
            for t in right_bullets_texts
        ])
        right_bullets.arrange(DOWN, buff=0.32)
        right_bullets.next_to(right_header, DOWN, buff=0.38)
        right_bullets.set_x(RIGHT[0] * 2.8)

        # Animate headers
        self.play(
            FadeIn(left_header, shift=UP * 0.2),
            FadeIn(right_header, shift=UP * 0.2),
            run_time=0.9,
        )

        # Animate bullets with LaggedStart
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=RIGHT * 0.15) for b in left_bullets],
                *[FadeIn(b, shift=LEFT * 0.15) for b in right_bullets],
                lag_ratio=0.18,
            ),
            run_time=2.2,
        )
        self.wait(2.0)

        # ── FadeOut all ──────────────────────────────────────────────
        all_objects = VGroup(
            title,
            fwd_label,
            pipeline,
            divider,
            left_header, left_bullets,
            right_header, right_bullets,
        )
        self.play(FadeOut(all_objects), run_time=1.5)
        self.wait(0.5)
