"""
scene1.py — Episode 2, Scene 1: Recap the 4-pixel cliffhanger from Ep1
========================================================================
Shows the previously-on recap, stepping from high-resolution pixel grids
down to a 2×2 grid of 4 pixels, then poses the central question.

Run: manim -pql scene1.py Scene2Ep1Recap
"""

# VO: Tập trước ta đã đặt câu hỏi: với chỉ bốn con số cập nhật mỗi 1/30 giây,
# VO: một robot có thể điều hướng trong không gian thực không?
# VO: Hôm nay ta tìm câu trả lời.

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np

_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

def load_color_svg(filename, color=GRAY_LIGHT, stroke_width=1.5):
            mob = SVGMobject(os.path.join(_ASSETS, filename))
            mob.set_stroke(color, width=stroke_width)
            return mob

class Scene1Ep1Recap(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── "Previously..." label ─────────────────────────────────
        prev_label = Text("Previously...", font_size=32, color=GRAY_MID)
        prev_label.to_corner(UL, buff=0.45)
        self.play(FadeIn(prev_label, shift=RIGHT * 0.3), run_time=0.8)
        self.wait(0.4)

        robot = (load_color_svg("robot.svg", color=ORANGE_3B1B)
                     .scale_to_fit_height(3.5)
                     .set_stroke(width=0)
                     .move_to(LEFT * 3.5))

        self.play(
            FadeIn(robot, run_time=1.2),
        )
        self.wait(0.3)

        # ── Pixel grid helper (draws grid as VGroup of squares) ───
        def make_grid(n, cell_size, seed=42):
            rng = np.random.default_rng(seed)
            palette = [BLUE_3B1B, GREEN_3B1B, YELLOW_3B1B,
                       RED_BRAIN, PURPLE_3B1B, TEAL_EP2]
            grid = VGroup()
            for r in range(n):
                for c in range(n):
                    col = palette[rng.integers(len(palette))]
                    sq = Square(
                        side_length=cell_size,
                        fill_color=col, fill_opacity=0.82,
                        stroke_color=BG_COLOR, stroke_width=0.5,
                    )
                    sq.move_to(RIGHT * c * cell_size + DOWN * r * cell_size)
                    grid.add(sq)
            grid.move_to(ORIGIN)
            return grid

        # Start with 8×8 grid on the right
        n_start = 8
        cell0 = 0.22
        grid = make_grid(n_start, cell0, seed=7)
        grid.shift(RIGHT * 2.8)

        label_res = Text("128 × 128", font_size=26, color=GRAY_LIGHT)
        label_res.next_to(grid, DOWN, buff=0.22)

        self.play(
            LaggedStart(*[FadeIn(sq, scale=0.8) for sq in grid], lag_ratio=0.015, run_time=1.5),
            FadeIn(label_res, run_time=0.8),
        )
        self.wait(0.5)

        # ── Step down through resolutions ─────────────────────────
        steps = [
            (6,  "64 × 64",  0.28,  9),
            (4,  "32 × 32",  0.40,  13),
            (3,  "16 × 16",  0.52,  17),
            (2,  "8 × 8",   0.72,  21),
        ]
        for (n, res_label, cell_sz, seed) in steps:
            new_grid = make_grid(n, cell_sz, seed=seed)
            new_grid.move_to(grid.get_center())
            new_label = Text(res_label, font_size=26, color=GRAY_LIGHT)
            new_label.next_to(new_grid, DOWN, buff=0.22)
            self.play(
                ReplacementTransform(grid, new_grid, run_time=0.9, rate_func=smooth),
                ReplacementTransform(label_res, new_label, run_time=0.7),
            )
            self.wait(0.3)
            grid = new_grid
            label_res = new_label

        # ── Land on 4 pixels (2×2, big squares) ──────────────────
        four_px_colors = [BLUE_3B1B, YELLOW_3B1B, RED_BRAIN, GREEN_3B1B]
        final_grid = VGroup()
        for idx, col in enumerate(four_px_colors):
            r, c = divmod(idx, 2)
            sq = Square(
                side_length=0.95,
                fill_color=col, fill_opacity=0.88,
                stroke_color=BG_COLOR, stroke_width=1.2,
            )
            sq.move_to(RIGHT * c * 0.95 + DOWN * r * 0.95)
            final_grid.add(sq)
        final_grid.move_to(grid.get_center())

        four_label = Text("4 pixels", font_size=32, color=YELLOW_3B1B, weight=BOLD)
        four_label.next_to(final_grid, DOWN, buff=0.28)

        self.play(
            ReplacementTransform(grid, final_grid, run_time=1.1, rate_func=smooth),
            ReplacementTransform(label_res, four_label, run_time=0.9),
        )

        # Pulse the final grid to draw attention
        self.play(
            final_grid.animate.scale(1.08).set_stroke(width=2.5),
            run_time=0.45, rate_func=there_and_back,
        )
        self.wait(0.6)

        # ── Big question ─────────────────────────────────────────
        question = Text(
            "Can a robot navigate\nwith only 4 numbers?",
            font_size=36, color=GRAY_LIGHT,
            line_spacing=1.3,
        )
        question.to_edge(DOWN, buff=0.7)

        self.play(
            Write(question, run_time=1.6, rate_func=smooth),
        )
        self.play(
            question.animate.set_color(YELLOW_3B1B),
            run_time=0.7, rate_func=smooth,
        )
        self.wait(2.5)

        # ── FadeOut everything ────────────────────────────────────
        all_objects = VGroup(
            prev_label, robot, final_grid, four_label, question,
        )
        self.play(FadeOut(all_objects, run_time=1.2, rate_func=smooth))
        self.wait(0.3)
