"""
scene4.py — Episode 3, Scene 4: Generative Design — DiffuseBot
Shows how LLMs fail at physical design, then presents the DiffuseBot pipeline
that combines diffusion models with differentiable simulation.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


def make_diffuse_box(label_str, box_width, box_height, box_color, font_size=18):
    """Create a pipeline box: RoundedRectangle + centered Text label."""
    rect = RoundedRectangle(
        width=box_width, height=box_height,
        corner_radius=0.13,
        color=box_color,
        stroke_width=2.5,
        fill_color=BG_COLOR,
        fill_opacity=1.0,
    )
    label = Text(label_str, font_size=font_size, color=box_color, line_spacing=1.35)
    label.move_to(rect.get_center())
    return VGroup(rect, label)


class Scene3DiffuseBot(Scene):
    def construct(self):
        # ── Background ──────────────────────────────────────────────
        self.camera.background_color = BG_COLOR

        # VO: "DiffuseBot kết hợp diffusion model với differentiable simulation.
        #       Thay vì dùng text hoặc image để guide quá trình denoising, nó dùng
        #       gradient từ simulator. Mỗi bước denoising, thiết kế được điều chỉnh
        #       về hướng 'vật lý hoạt động được'."

        # ── Section A: Title ─────────────────────────────────────────
        title = Text(
            "Generative Design",
            font_size=40,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.5)

        # ── Section A: LLM fails at physical design ──────────────────
        # Vertical divider
        divider_A = DashedLine(
            UP * 2.0, DOWN * 2.0,
            color=GRAY_DIM,
            stroke_width=1.5,
            dash_length=0.14,
        )
        self.play(Create(divider_A), run_time=0.7)

        # Left side — question
        ask_label = Text("Ask an LLM:", font_size=22, color=GRAY_MID)
        ask_label.move_to(LEFT * 3.2 + UP * 1.4)

        ask_body = Text(
            '"Design a robot\nto pick strawberries"',
            font_size=18,
            color=GRAY_LIGHT,
            line_spacing=1.35,
        )
        ask_body.next_to(ask_label, DOWN, buff=0.3)
        ask_body.set_x(LEFT[0] * 3.2)

        # Right side — bad LLM output
        llm_label = Text("LLM output:", font_size=22, color=RED_BRAIN, weight=BOLD)
        llm_label.move_to(RIGHT * 3.2 + UP * 1.4)

        llm_bullets_texts = [
            "• Arms locked at 90°",
            "• Wheels face sideways",
            "• No physics validation",
        ]
        llm_bullets = VGroup(*[
            Text(t, font_size=17, color=RED_BRAIN)
            for t in llm_bullets_texts
        ])
        llm_bullets.arrange(DOWN, buff=0.28)
        llm_bullets.next_to(llm_label, DOWN, buff=0.3)
        llm_bullets.set_x(RIGHT[0] * 3.2)

        # Bottom warning
        bottom_warn = Text(
            "LLMs have no simulator to check their designs.",
            font_size=20,
            color=ORANGE_3B1B,
            weight=BOLD,
        )
        bottom_warn.to_edge(DOWN, buff=0.55)

        self.play(
            FadeIn(ask_label, shift=RIGHT * 0.2),
            FadeIn(ask_body, shift=RIGHT * 0.2),
            run_time=1.0,
        )
        self.play(
            FadeIn(llm_label, shift=LEFT * 0.2),
            run_time=0.7,
        )
        self.play(
            LaggedStart(*[FadeIn(b, shift=LEFT * 0.15) for b in llm_bullets], lag_ratio=0.25),
            run_time=1.2,
        )
        self.play(Write(bottom_warn), run_time=1.0)
        self.wait(2.0)

        # Fade out right side and bottom
        self.play(
            FadeOut(VGroup(llm_label, llm_bullets, bottom_warn)),
            run_time=0.9,
        )
        self.wait(0.3)
        # Also fade out left side and divider for Section B
        self.play(
            FadeOut(VGroup(divider_A, ask_label, ask_body)),
            run_time=0.8,
        )
        self.wait(0.3)

        # ── Section B: DiffuseBot pipeline ───────────────────────────
        # 4 boxes stacked vertically, centered at RIGHT*2.5 + DOWN*0.3
        box1 = make_diffuse_box("Random noise", 3.0, 0.6, GRAY_MID, font_size=18)
        box2 = make_diffuse_box("Diffusion model\n(denoising step)", 3.0, 0.75, PURPLE_3B1B, font_size=18)
        box4 = make_diffuse_box("Robot design θ", 3.0, 0.6, TEAL_EP2, font_size=18)

        # Box 3 combines a text label + MathTex gradient symbol
        box3_rect = RoundedRectangle(
            width=3.0, height=0.75,
            corner_radius=0.13,
            color=ORANGE_3B1B,
            stroke_width=2.5,
            fill_color=BG_COLOR,
            fill_opacity=1.0,
        )
        box3_label_text = Text(
            "Simulation gradient  ",
            font_size=18,
            color=ORANGE_3B1B,
        )
        box3_label_math = MathTex(r"\nabla_\theta L", font_size=28, color=ORANGE_3B1B)
        box3_label_group = VGroup(box3_label_text, box3_label_math)
        box3_label_group.arrange(RIGHT, buff=0.05)
        box3_label_group.move_to(box3_rect.get_center())
        box3 = VGroup(box3_rect, box3_label_group)

        pipeline_boxes = VGroup(box1, box2, box3, box4)
        pipeline_boxes.arrange(DOWN, buff=0.5)
        pipeline_boxes.move_to(RIGHT * 2.5 + DOWN * 0.3)

        # Arrows between consecutive pipeline boxes
        pipe_arrows = VGroup()
        boxes_list = [box1, box2, box3, box4]
        for i in range(len(boxes_list) - 1):
            arr = Arrow(
                start=boxes_list[i].get_bottom(),
                end=boxes_list[i + 1].get_top(),
                color=GRAY_MID,
                buff=0.05,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.25,
            )
            pipe_arrows.add(arr)

        # Left text explanation — 4 items, each aligned to corresponding box y
        left_explanations_texts = [
            "Start: pure noise",
            "Each step: denoise",
            "Guided by physics",
            "Result: valid robot",
        ]
        left_items = VGroup(*[
            Text(t, font_size=16, color=GRAY_LIGHT)
            for t in left_explanations_texts
        ])

        # Animate pipeline boxes and arrows with LaggedStart
        self.play(
            LaggedStart(
                GrowFromCenter(box1),
                GrowFromCenter(box2),
                GrowFromCenter(box3),
                GrowFromCenter(box4),
                lag_ratio=0.3,
            ),
            run_time=2.0,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in pipe_arrows], lag_ratio=0.35),
            run_time=1.2,
        )

        # Position left explanations aligned with boxes y-coordinates
        for i, (item, box) in enumerate(zip(left_items, boxes_list)):
            item.set_y(box.get_center()[1])
            item.set_x(LEFT[0] * 2.8)

        self.play(
            LaggedStart(*[FadeIn(item, shift=RIGHT * 0.2) for item in left_items], lag_ratio=0.3),
            run_time=1.5,
        )
        self.wait(1.0)

        # Key insight box at bottom
        insight_text = Text(
            "Unlike text/image diffusion — the conditioning signal is a PHYSICS GRADIENT",
            font_size=18,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        insight_text.to_edge(DOWN, buff=0.45)
        insight_rect = SurroundingRectangle(
            insight_text,
            color=YELLOW_3B1B,
            stroke_width=2,
            buff=0.18,
            corner_radius=0.1,
        )
        self.play(
            Write(insight_text),
            Create(insight_rect),
            run_time=1.8,
        )
        self.wait(2.5)

        # ── FadeOut all ──────────────────────────────────────────────
        all_objects = VGroup(
            title,
            pipeline_boxes,
            pipe_arrows,
            left_items,
            insight_text, insight_rect,
        )
        self.play(FadeOut(all_objects), run_time=1.5)
        self.wait(0.5)
