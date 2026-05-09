"""
scene7.py — Episode 2, Scene 7: Cliffhanger to Episode 3
=========================================================
Returns to the θ_brain | θ_body split, expands θ_body sub-parameters,
teases the morphable soft-robot idea, and sets up Episode 3.

Run: manim -pql scene7.py Scene2Cliffhanger
"""

# VO: Ta vừa thấy rằng thiết kế cảm biến có thể được tối ưu hoá bằng gradient.
# VO: Nhưng cảm biến chỉ là một phần nhỏ của cơ thể.
# VO: Điều gì xảy ra nếu ta áp dụng ý tưởng tương tự cho toàn bộ —
# VO: hình dạng tay chân, độ cứng vật liệu, số lượng khớp?
# VO: Đó là chủ đề của tập tiếp theo.

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


class Scene2Cliffhanger(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Recreate θ_brain | θ_body split from Ep1 Scene 1 ─────
        theta_full = MarkupText(
            "θ<sub>robot</sub>", font_size=52, color=YELLOW_3B1B,
        )
        theta_full.to_edge(UP, buff=0.55)
        self.play(Write(theta_full, run_time=1.0, rate_func=smooth))
        self.wait(0.3)

        # Split arrow
        split_arrow_l = Arrow(
            theta_full.get_bottom(),
            theta_full.get_bottom() + DOWN * 0.8 + LEFT * 2.2,
            color=GRAY_MID, buff=0, stroke_width=2.2,
            max_tip_length_to_length_ratio=0.25,
        )
        split_arrow_r = Arrow(
            theta_full.get_bottom(),
            theta_full.get_bottom() + DOWN * 0.8 + RIGHT * 2.2,
            color=GRAY_MID, buff=0, stroke_width=2.2,
            max_tip_length_to_length_ratio=0.25,
        )

        theta_brain = MarkupText(
            "θ<sub>brain</sub>", font_size=38, color=PURPLE_3B1B,
        )
        theta_brain.move_to(theta_full.get_bottom() + DOWN * 1.1 + LEFT * 2.2)

        theta_body = MarkupText(
            "θ<sub>body</sub>", font_size=38, color=TEAL_EP2,
        )
        theta_body.move_to(theta_full.get_bottom() + DOWN * 1.1 + RIGHT * 2.2)

        brain_box = SurroundingRectangle(
            theta_brain, color=PURPLE_3B1B, buff=0.22,
            stroke_width=2.0, corner_radius=0.1,
        )
        body_box = SurroundingRectangle(
            theta_body, color=TEAL_EP2, buff=0.22,
            stroke_width=2.0, corner_radius=0.1,
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

        # ── Highlight θ_body and expand sub-parameters ────────────
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

        # Sub-parameters expand below θ_body
        sub_params = [
            ("shape",          TEAL_EP2),
            ("joint stiffness", ORANGE_3B1B),
            ("material",       GREEN_3B1B),
            ("limb length",    BLUE_3B1B),
        ]

        sub_arrows  = VGroup()
        sub_labels  = VGroup()
        base_pt = theta_body.get_bottom() + DOWN * 0.2

        for i, (name, col) in enumerate(sub_params):
            angle_offset = (i - 1.5) * 0.7
            tip_pt = base_pt + DOWN * 1.1 + RIGHT * angle_offset
            arr = Arrow(
                base_pt, tip_pt,
                color=col, buff=0, stroke_width=2.0,
                max_tip_length_to_length_ratio=0.3,
            )
            lbl = Text(name, font_size=19, color=col)
            lbl.next_to(tip_pt, DOWN, buff=0.1)
            sub_arrows.add(arr)
            sub_labels.add(lbl)

        self.play(
            LaggedStart(
                *[GrowArrow(a, run_time=0.5) for a in sub_arrows],
                lag_ratio=0.18, run_time=1.2,
            ),
            LaggedStart(
                *[FadeIn(l, run_time=0.4) for l in sub_labels],
                lag_ratio=0.18, run_time=1.2,
            ),
        )
        self.wait(0.5)

        # ── Question text ─────────────────────────────────────────
        question_txt = Text(
            "If we can optimize sensors...\ncan we optimize the WHOLE BODY?",
            font_size=30, color=GRAY_LIGHT,
            line_spacing=1.35,
        )
        question_txt.to_edge(DOWN, buff=1.8)
        self.play(Write(question_txt, run_time=1.4, rate_func=smooth))
        self.play(
            question_txt.animate.set_color(YELLOW_3B1B),
            run_time=0.6, rate_func=smooth,
        )
        self.wait(0.8)

        # ── Soft robot blob morphing ───────────────────────────────
        self.play(
            FadeOut(VGroup(
                theta_full, split_arrow_l, split_arrow_r,
                theta_brain, brain_box,
                theta_body, body_box_new,
                sub_arrows, sub_labels, question_txt,
            ), run_time=0.8),
        )

        # "Soft robot" as a parametric blob that morphs between shapes
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

        blob0 = make_blob(rx=0.9, ry=0.7, seed=1)
        blob0.move_to(ORIGIN + DOWN * 0.2)

        blob_label = Text("Soft Robot", font_size=26, color=TEAL_EP2)
        blob_label.next_to(blob0, DOWN, buff=0.35)

        self.play(
            DrawBorderThenFill(blob0, run_time=1.0, rate_func=smooth),
            FadeIn(blob_label, run_time=0.7),
        )
        self.wait(0.3)

        # Morph through different shapes
        for seed in [7, 13, 21, 3]:
            blob_new = make_blob(
                rx=0.7 + (seed % 4) * 0.12,
                ry=0.6 + (seed % 3) * 0.15,
                seed=seed,
            )
            blob_new.move_to(ORIGIN + DOWN * 0.2)
            self.play(
                Transform(blob0, blob_new, run_time=0.9, rate_func=smooth),
            )
            self.wait(0.2)

        # ── Limb-like appendages morphing out ─────────────────────
        limb_group = VGroup()
        n_limbs = 4
        base_angles = np.linspace(PI / 6, PI * 5 / 4, n_limbs)
        for ang in base_angles:
            limb_start = blob0.get_center() + np.array([np.cos(ang) * 0.5, np.sin(ang) * 0.55, 0])
            limb_end   = blob0.get_center() + np.array([np.cos(ang) * 1.1, np.sin(ang) * 1.15, 0])
            limb = Line(
                limb_start, limb_end,
                color=GREEN_3B1B, stroke_width=5,
            )
            limb_tip = Circle(radius=0.1, color=GREEN_3B1B, fill_opacity=0.8, stroke_width=0)
            limb_tip.move_to(limb_end)
            limb_group.add(VGroup(limb, limb_tip))

        self.play(
            LaggedStart(
                *[GrowFromEdge(lg, LEFT, run_time=0.5) for lg in limb_group],
                lag_ratio=0.2, run_time=1.2,
            )
        )
        self.wait(0.4)

        # ── Episode 3 teaser ──────────────────────────────────────
        ep3_text = Text(
            "Episode 3: Designing bodies\nwith gradient descent",
            font_size=34, color=YELLOW_3B1B, weight=BOLD,
            line_spacing=1.35,
        )
        ep3_text.to_edge(UP, buff=0.5)
        self.play(Write(ep3_text, run_time=1.4, rate_func=smooth))
        self.wait(0.8)

        # ── Fade to black ─────────────────────────────────────────
        self.play(
            FadeOut(VGroup(blob0, blob_label, limb_group, ep3_text),
                    run_time=1.2, rate_func=smooth),
        )

        # "See you next time." fades in on black
        see_you = Text("See you next time.", font_size=36, color=GRAY_MID)
        see_you.move_to(ORIGIN)
        self.play(FadeIn(see_you, run_time=1.0, rate_func=smooth))
        self.wait(2.0)
        self.play(FadeOut(see_you, run_time=1.5, rate_func=smooth))
        self.wait(0.3)
