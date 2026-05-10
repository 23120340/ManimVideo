"""
scene7.py — Episode 2, Scene 7: Cliffhanger to Episode 3
=========================================================
Returns to the θ_brain | θ_body split, expands θ_body sub-parameters,
teases the morphable soft-robot idea, and sets up Episode 3.

Run: manim -pql scene7.py Scene2Cliffhanger
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


class Scene2Cliffhanger(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── θ_robot title ─────────────────────────────────────────
        theta_full = MarkupText(
            "θ<sub>robot</sub>", font_size=52, color=YELLOW_3B1B,
        )
        theta_full.to_edge(UP, buff=0.45)
        self.play(Write(theta_full, run_time=1.0, rate_func=smooth))
        self.wait(0.3)

        # ── Split: create boxes FIRST so arrows can point to their tops ─
        split_origin = theta_full.get_bottom() + DOWN * 0.1

        theta_brain = MarkupText(
            "θ<sub>brain</sub>", font_size=38, color=PURPLE_3B1B,
        )
        theta_brain.move_to(split_origin + DOWN * 1.35 + LEFT * 2.4)

        theta_body = MarkupText(
            "θ<sub>body</sub>", font_size=38, color=TEAL_EP2,
        )
        theta_body.move_to(split_origin + DOWN * 1.35 + RIGHT * 2.4)

        brain_box = SurroundingRectangle(
            theta_brain, color=PURPLE_3B1B, buff=0.22,
            stroke_width=2.0, corner_radius=0.1,
        )
        body_box = SurroundingRectangle(
            theta_body, color=TEAL_EP2, buff=0.22,
            stroke_width=2.0, corner_radius=0.1,
        )

        # Arrows computed AFTER boxes so tips land on box tops exactly
        split_arrow_l = Arrow(
            split_origin, brain_box.get_top(),
            color=GRAY_MID, buff=0.05, stroke_width=2.2,
            max_tip_length_to_length_ratio=0.25,
        )
        split_arrow_r = Arrow(
            split_origin, body_box.get_top(),
            color=GRAY_MID, buff=0.05, stroke_width=2.2,
            max_tip_length_to_length_ratio=0.25,
        )

        self.play(
            GrowArrow(split_arrow_l, run_time=0.7),
            GrowArrow(split_arrow_r, run_time=0.7),
        )
        self.play(
            FadeIn(theta_brain, scale=0.9, run_time=0.7),
            FadeIn(theta_body, scale=0.9, run_time=0.7),
            Create(brain_box, run_time=0.7),
            Create(body_box, run_time=0.7),
        )
        self.wait(0.5)

        # ── Highlight θ_body ──────────────────────────────────────
        self.play(
            Indicate(body_box, color=YELLOW_3B1B, scale_factor=1.12, run_time=1.0),
            theta_body.animate.set_color(YELLOW_3B1B),
        )
        body_box_new = SurroundingRectangle(
            theta_body, color=YELLOW_3B1B, buff=0.22,
            stroke_width=2.5, corner_radius=0.1,
        )
        self.play(ReplacementTransform(body_box, body_box_new, run_time=0.5))
        self.wait(0.3)

        # ── Sub-parameters: vertical list below θ_body (no overlap) ──
        sub_params = [
            ("shape",           TEAL_EP2),
            ("joint stiffness", ORANGE_3B1B),
            ("material",        GREEN_3B1B),
            ("limb length",     BLUE_3B1B),
        ]

        sub_items = VGroup()
        for name, col in sub_params:
            item = Text(f"• {name}", font_size=18, color=col)
            sub_items.add(item)
        sub_items.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        sub_items.next_to(body_box, DOWN, buff=0.38)
        sub_items.align_to(body_box, LEFT)

        expand_arrow = Arrow(
            body_box.get_bottom(),
            sub_items.get_top() + UP * 0.06,
            buff=0, color=TEAL_EP2, stroke_width=2.0,
            max_tip_length_to_length_ratio=0.28,
        )

        self.play(GrowArrow(expand_arrow, run_time=0.5))
        self.play(
            LaggedStart(
                *[FadeIn(item, shift=RIGHT * 0.2, run_time=0.35)
                  for item in sub_items],
                lag_ratio=0.2, run_time=1.0,
            ),
        )
        self.wait(0.5)

        # ── Question text — bên trái, không đè sub_labels ────────
        question_txt = Text(
            "If we can optimize sensors...\ncan we optimize the WHOLE BODY?",
            font_size=26, color=GRAY_LIGHT,
            line_spacing=1.35,
        )
        # Đặt bên trái màn hình, căn giữa dọc với sub_labels
        question_txt.move_to(LEFT * 3.2 + DOWN * 1.6)
        self.play(Write(question_txt, run_time=1.4, rate_func=smooth))
        self.play(
            question_txt.animate.set_color(YELLOW_3B1B),
            run_time=0.6, rate_func=smooth,
        )
        self.wait(0.8)

        # ── Fade out split diagram ────────────────────────────────
        self.play(
            FadeOut(VGroup(
                theta_full, split_arrow_l, split_arrow_r,
                theta_brain, brain_box,
                theta_body, body_box_new,
                expand_arrow, sub_items, question_txt,
            ), run_time=0.8),
        )

        # ── Soft robot blob morphing ───────────────────────────────
        def make_blob(n_pts=60, rx=0.9, ry=0.7, seed=0):
            rng = np.random.default_rng(seed)
            noise_amp = 0.18
            angles = np.linspace(0, 2 * PI, n_pts, endpoint=False)
            noise = noise_amp * np.sin(3 * angles + rng.uniform(0, 2 * PI))
            noise += noise_amp * 0.5 * np.sin(5 * angles + rng.uniform(0, 2 * PI))
            xs = (rx + noise) * np.cos(angles)
            ys = (ry + noise) * np.sin(angles)
            pts = np.column_stack([xs, ys, np.zeros(n_pts)])
            mob = VMobject(
                color=TEAL_EP2, stroke_width=2.8,
                fill_color=TEAL_EP2, fill_opacity=0.22,
            )
            mob.set_points_smoothly(pts)
            mob.close_path()
            return mob

        # Blob ở giữa, dịch lên một chút để ep3_text có chỗ phía dưới
        blob_center = UP * 0.3
        blob0 = make_blob(rx=0.9, ry=0.7, seed=1)
        blob0.move_to(blob_center)

        blob_label = Text("Soft Robot", font_size=24, color=TEAL_EP2)
        blob_label.next_to(blob0, DOWN, buff=0.28)

        self.play(
            DrawBorderThenFill(blob0, run_time=1.0, rate_func=smooth),
            FadeIn(blob_label, run_time=0.7),
        )
        self.wait(0.3)

        # Morph through shapes
        for seed in [7, 13, 21, 3]:
            blob_new = make_blob(
                rx=0.7 + (seed % 4) * 0.12,
                ry=0.6 + (seed % 3) * 0.15,
                seed=seed,
            )
            blob_new.move_to(blob_center)
            self.play(Transform(blob0, blob_new, run_time=0.9, rate_func=smooth))
            self.wait(0.2)

        # ── Limb appendages ───────────────────────────────────────
        limb_group = VGroup()
        n_limbs = 4
        base_angles = np.linspace(PI / 6, PI * 5 / 4, n_limbs)
        for ang in base_angles:
            limb_start = blob0.get_center() + np.array([np.cos(ang) * 0.5, np.sin(ang) * 0.55, 0])
            limb_end   = blob0.get_center() + np.array([np.cos(ang) * 1.0, np.sin(ang) * 1.05, 0])
            limb = Line(limb_start, limb_end, color=GREEN_3B1B, stroke_width=5)
            limb_tip = Circle(radius=0.09, color=GREEN_3B1B, fill_opacity=0.8, stroke_width=0)
            limb_tip.move_to(limb_end)
            limb_group.add(VGroup(limb, limb_tip))

        self.play(
            LaggedStart(
                *[GrowFromEdge(lg, LEFT, run_time=0.5) for lg in limb_group],
                lag_ratio=0.2, run_time=1.2,
            )
        )
        self.wait(0.4)

        # ── Episode 3 teaser — phía dưới blob, không đè ──────────
        ep3_text = Text(
            "Episode 3: Designing bodies\nwith gradient descent",
            font_size=30, color=YELLOW_3B1B, weight=BOLD,
            line_spacing=1.35,
        )
        # Đặt dưới blob_label, đủ khoảng cách
        ep3_text.next_to(blob_label, DOWN, buff=0.45)

        self.play(Write(ep3_text, run_time=1.4, rate_func=smooth))
        self.wait(0.8)

        # ── Fade to black ─────────────────────────────────────────
        self.play(
            FadeOut(
                Group(blob0, blob_label, limb_group, ep3_text),
                run_time=1.2, rate_func=smooth,
            ),
        )

        # "See you next time."
        see_you = Text("See you next time.", font_size=36, color=GRAY_MID)
        see_you.move_to(ORIGIN)
        self.play(FadeIn(see_you, run_time=1.0, rate_func=smooth))
        self.wait(2.0)
        self.play(FadeOut(see_you, run_time=1.5, rate_func=smooth))
        self.wait(0.3)