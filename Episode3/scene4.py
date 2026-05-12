"""
scene4.py — Episode 3, Scene 4: DiffuseBot (Generative Design)
Section A: LLM fails (split screen).
Section B: DiffuseBot horizontal pipeline — diffusion + physics gradient.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


class Scene3DiffuseBot(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title ──────────────────────────────────────────────────────
        title = Text(
            "Generative Design",
            font_size=38,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.5)

        # ── SECTION A: LLM fails (split screen) ─────────────────────────
        divider = DashedLine(
            UP * 2.5, DOWN * 1.8,
            color=GRAY_DIM,
            stroke_width=1.5,
            dash_length=0.15,
        )
        self.play(Create(divider), run_time=0.7)

        # Left side
        ask_label = Text(
            "Ask an LLM:",
            font_size=22,
            color=GRAY_MID,
        )
        ask_label.move_to(LEFT * 3.5 + UP * 2.0)

        ask_quote = Text(
            '"Design a robot to\npick strawberries"',
            font_size=20,
            color=GRAY_LIGHT,
            slant=ITALIC,
            line_spacing=1.35,
        )
        ask_quote.next_to(ask_label, DOWN, buff=0.45)
        ask_quote.set_x(-3.5)

        # Right side
        llm_label = Text(
            "LLM output:",
            font_size=22,
            color=RED_BRAIN,
            weight=BOLD,
        )
        llm_label.move_to(RIGHT * 3.5 + UP * 2.0)

        llm_bullets = VGroup(
            Text("• Arms locked at 90°", font_size=18, color=RED_BRAIN),
            Text("• Wheels face sideways", font_size=18, color=RED_BRAIN),
            Text("• No physics validation", font_size=18, color=RED_BRAIN),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        llm_bullets.next_to(llm_label, DOWN, buff=0.4)
        llm_bullets.set_x(3.5)

        # Bottom warning
        bottom_warning = Text(
            "LLMs have no simulator to check their designs.",
            font_size=22,
            color=ORANGE_3B1B,
            weight=BOLD,
        )
        bottom_warning.to_edge(DOWN, buff=0.55)

        self.play(FadeIn(ask_label, shift=RIGHT * 0.15), run_time=0.7)
        self.play(FadeIn(ask_quote, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(llm_label, shift=LEFT * 0.15), run_time=0.7)
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=LEFT * 0.15) for b in llm_bullets],
                lag_ratio=0.25,
            ),
            run_time=1.2,
        )
        self.play(Write(bottom_warning), run_time=1.2)
        self.wait(2.0)

        # FadeOut Section A (keep title)
        section_a = VGroup(
            divider, ask_label, ask_quote,
            llm_label, llm_bullets, bottom_warning,
        )
        self.play(FadeOut(section_a), run_time=1.0)
        self.wait(0.3)

        # ── SECTION B: DiffuseBot horizontal pipeline ──────────────────
        section_header = Text(
            "DiffuseBot: diffusion + physics gradient",
            font_size=22,
            color=TEAL_EP2,
            weight=BOLD,
        )
        section_header.move_to(UP * 2.0)
        self.play(FadeIn(section_header, shift=DOWN * 0.1), run_time=0.8)

        # Helper: a box with label centered
        def make_pipeline_box(text_str, color, w=2.4, h=1.1, fs=16):
            rect = RoundedRectangle(
                width=w,
                height=h,
                corner_radius=0.13,
                color=color,
                stroke_width=2.5,
                fill_color=BG_COLOR,
                fill_opacity=1,
            )
            t = Text(
                text_str,
                font_size=fs,
                color=color,
                line_spacing=1.2,
            )
            t.move_to(rect.get_center())
            return VGroup(rect, t)

        box1 = make_pipeline_box("Random\nnoise", GRAY_MID)
        box2 = make_pipeline_box("Diffusion\nmodel", PURPLE_3B1B)

        # Box 3 — has math symbol; build manually
        box3_rect = RoundedRectangle(
            width=2.4,
            height=1.1,
            corner_radius=0.13,
            color=ORANGE_3B1B,
            stroke_width=2.5,
            fill_color=BG_COLOR,
            fill_opacity=1,
        )
        box3_label = Text("+ physics", font_size=15, color=ORANGE_3B1B)
        box3_math = MathTex(
            r"\nabla_\theta\mathcal{L}",
            font_size=26,
            color=ORANGE_3B1B,
        )
        box3_inner = VGroup(box3_label, box3_math).arrange(DOWN, buff=0.10)
        box3_inner.move_to(box3_rect.get_center())
        box3 = VGroup(box3_rect, box3_inner)

        box4 = make_pipeline_box("Robot\ndesign θ", TEAL_EP2)

        pipeline = VGroup(box1, box2, box3, box4).arrange(RIGHT, buff=0.45)
        pipeline.move_to(UP * 0.5)

        # Arrows between consecutive boxes
        arrows = VGroup()
        boxes_list = [box1, box2, box3, box4]
        for i in range(3):
            a_rect = boxes_list[i][0]
            b_rect = boxes_list[i + 1][0]
            arr = Arrow(
                a_rect.get_right(),
                b_rect.get_left(),
                buff=0.05,
                color=GRAY_MID,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.3,
            )
            arrows.add(arr)

        # Descriptions below each box
        desc_strs = ["start", "denoise step", "guide signal", "valid output"]
        desc_colors = [GRAY_LIGHT, GRAY_LIGHT, ORANGE_3B1B, GRAY_LIGHT]
        descs = VGroup()
        for b, s, c in zip(boxes_list, desc_strs, desc_colors):
            d = Text(s, font_size=14, color=c, slant=ITALIC)
            d.next_to(b, DOWN, buff=0.35)
            descs.add(d)

        self.play(
            LaggedStart(
                *[GrowFromCenter(b) for b in boxes_list],
                lag_ratio=0.3,
            ),
            run_time=1.8,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[FadeIn(d, shift=UP * 0.1) for d in descs], lag_ratio=0.2),
            run_time=1.2,
        )
        self.wait(1.0)

        # Bottom insight callout
        insight = Text(
            "Conditioning signal is a PHYSICS GRADIENT — not text, not image",
            font_size=20,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        insight.to_edge(DOWN, buff=0.55)
        insight_rect = SurroundingRectangle(
            insight,
            color=YELLOW_3B1B,
            buff=0.18,
            corner_radius=0.1,
            stroke_width=2,
        )
        self.play(
            Write(insight),
            Create(insight_rect),
            run_time=1.8,
        )
        self.wait(2.5)

        # ── FadeOut all ────────────────────────────────────────────────
        everything = VGroup(
            title, section_header,
            pipeline, arrows, descs,
            insight, insight_rect,
        )
        self.play(FadeOut(everything), run_time=1.2)
        self.wait(0.4)
