"""
scene2.py — Episode 3, Scene 2: Differentiable Simulation
Forward / backward pipelines (gradient through physics), then Explicit vs
Implicit integration trade-off.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


def make_box(label, w, h, color, fs=16):
    r = RoundedRectangle(
        width=w,
        height=h,
        corner_radius=0.1,
        color=color,
        stroke_width=2,
        fill_color=BG_COLOR,
        fill_opacity=1,
    )
    t = Text(label, font_size=fs, color=color, line_spacing=1.0)
    t.move_to(r.get_center())
    return VGroup(r, t)


def build_pipeline(y, arrow_color, arrow_dir=1):
    """Build a row of 5 boxes at given y. arrow_dir=+1 forward, -1 backward."""
    box_specs = [
        ("state₀", 0.95, BLUE_3B1B),
        ("physics\nstep", 1.15, ORANGE_3B1B),
        ("state₁", 0.95, BLUE_3B1B),
        ("...", 0.55, GRAY_MID),
        ("reward", 0.95, GREEN_3B1B),
    ]
    boxes = VGroup(*[make_box(lbl, w, 0.7, c, fs=15) for (lbl, w, c) in box_specs])
    boxes.arrange(RIGHT, buff=0.32).move_to(UP * y)

    arrows = VGroup()
    for i in range(len(boxes) - 1):
        a = boxes[i]
        b = boxes[i + 1]
        if arrow_dir == 1:
            arr = Arrow(
                a[0].get_right(),
                b[0].get_left(),
                buff=0.05,
                color=arrow_color,
                stroke_width=2.2,
                max_tip_length_to_length_ratio=0.3,
            )
        else:
            arr = Arrow(
                b[0].get_left(),
                a[0].get_right(),
                buff=0.05,
                color=arrow_color,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.3,
            )
        arrows.add(arr)
    return boxes, arrows


class Scene2DiffSim(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title ──────────────────────────────────────────────────────
        title = Text(
            "Differentiable Simulation",
            font_size=36,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.5)

        # ── SECTION A: Forward pipeline row ────────────────────────────
        fwd_boxes, fwd_arrows = build_pipeline(2.0, GRAY_MID, arrow_dir=1)
        fwd_label = Text(
            "FORWARD", font_size=18, color=GRAY_MID, weight=BOLD
        )
        fwd_label.next_to(fwd_boxes, LEFT, buff=0.35)

        self.play(
            LaggedStart(*[GrowFromCenter(b) for b in fwd_boxes], lag_ratio=0.18),
            run_time=1.4,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in fwd_arrows], lag_ratio=0.15),
            run_time=0.9,
        )
        self.play(FadeIn(fwd_label, shift=RIGHT * 0.15), run_time=0.6)
        self.wait(0.4)

        # ── SECTION A continued: Backward pipeline row ─────────────────
        bwd_boxes, bwd_arrows = build_pipeline(0.5, RED_BRAIN, arrow_dir=-1)
        bwd_label = Text(
            "BACKWARD", font_size=18, color=RED_BRAIN, weight=BOLD
        )
        bwd_label.next_to(bwd_boxes, LEFT, buff=0.35)

        self.play(
            LaggedStart(*[GrowFromCenter(b) for b in bwd_boxes], lag_ratio=0.18),
            run_time=1.4,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in bwd_arrows], lag_ratio=0.15),
            run_time=0.9,
        )
        self.play(FadeIn(bwd_label, shift=RIGHT * 0.15), run_time=0.6)

        # ── Explanation text ───────────────────────────────────────────
        bwd_explain = Text(
            "gradient flows through every physics step",
            font_size=20,
            color=RED_BRAIN,
            slant=ITALIC,
        )
        bwd_explain.move_to(DOWN * 0.5)
        self.play(Write(bwd_explain), run_time=1.2)
        self.wait(2.0)

        # ── FadeOut Section A ──────────────────────────────────────────
        section_a = VGroup(
            fwd_boxes, fwd_arrows, fwd_label,
            bwd_boxes, bwd_arrows, bwd_label,
            bwd_explain,
        )
        self.play(FadeOut(section_a), run_time=1.0)
        self.wait(0.3)

        # ── SECTION C: Explicit vs Implicit ────────────────────────────
        divider = DashedLine(
            UP * 2.5, DOWN * 2.5,
            color=GRAY_DIM,
            stroke_width=1.5,
            dash_length=0.14,
        )

        left_header = Text(
            "Explicit integration",
            font_size=24,
            color=GREEN_3B1B,
            weight=BOLD,
        )
        left_header.move_to(LEFT * 3.5 + UP * 1.8)

        left_bullets = VGroup(
            Text("• Store all intermediate states", font_size=18, color=GRAY_LIGHT),
            Text("• Memory grows with T steps", font_size=18, color=GRAY_LIGHT),
            Text("• T ≈ 1,000,000 steps/sec", font_size=18, color=GRAY_LIGHT),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        left_bullets.next_to(left_header, DOWN, buff=0.45)
        left_bullets.set_x(-3.5)

        right_header = Text(
            "Implicit integration",
            font_size=24,
            color=ORANGE_3B1B,
            weight=BOLD,
        )
        right_header.move_to(RIGHT * 3.5 + UP * 1.8)

        right_bullets = VGroup(
            Text("• Solve equation each step", font_size=18, color=GRAY_LIGHT),
            Text("• Less memory needed", font_size=18, color=GRAY_LIGHT),
            Text("• Slightly less accurate", font_size=18, color=GRAY_LIGHT),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        right_bullets.next_to(right_header, DOWN, buff=0.45)
        right_bullets.set_x(3.5)

        self.play(Create(divider), run_time=0.7)
        self.play(
            FadeIn(left_header, shift=RIGHT * 0.15),
            FadeIn(right_header, shift=LEFT * 0.15),
            run_time=0.9,
        )
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=UP * 0.1) for b in left_bullets],
                *[FadeIn(b, shift=UP * 0.1) for b in right_bullets],
                lag_ratio=0.18,
            ),
            run_time=1.6,
        )
        self.wait(2.0)

        # ── FadeOut everything ─────────────────────────────────────────
        everything = VGroup(
            title, divider,
            left_header, left_bullets,
            right_header, right_bullets,
        )
        self.play(FadeOut(everything), run_time=1.2)
        self.wait(0.4)
