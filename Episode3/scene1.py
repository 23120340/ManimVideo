"""
scene1.py — Episode 3, Scene 1: Hook
"RL: 10,000 rollouts. This: 12." — animated iteration counter, progress bar,
soft robot that converges to walking, gradient-through-physics callout.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


class Scene1Hook(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title ──────────────────────────────────────────────────────
        title = Text(
            "RL: 10,000 rollouts.  This: 12.",
            font_size=30,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.8)
        self.wait(0.6)

        # ── Iteration counter row ──────────────────────────────────────
        iter_label = Text("Iteration", font_size=28, color=GRAY_MID)
        iter_num = Text("1", font_size=48, color=YELLOW_3B1B, weight=BOLD)
        iter_total = Text("/ 12", font_size=32, color=GRAY_MID)
        counter_row = VGroup(iter_label, iter_num, iter_total).arrange(
            RIGHT, buff=0.25, aligned_edge=DOWN
        )
        counter_row.move_to(UP * 2.4)

        self.play(FadeIn(counter_row, shift=UP * 0.1), run_time=0.8)

        # ── Progress bar ───────────────────────────────────────────────
        bar_bg = Rectangle(
            width=6.0,
            height=0.22,
            color=GRAY_DARKER,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(UP * 1.7)

        def make_bar_fill(value, color=TEAL_EP2):
            f = Rectangle(
                width=max(6.0 * value / 12, 0.001),
                height=0.22,
                color=color,
                fill_opacity=1,
                stroke_width=0,
            )
            f.move_to(bar_bg.get_left() + RIGHT * (6.0 * value / 12) / 2)
            return f

        bar_fill = make_bar_fill(1, TEAL_EP2)

        self.play(FadeIn(bar_bg), FadeIn(bar_fill), run_time=0.7)

        # ── Soft robot at DOWN*0.5 — limbs are individually addressable ─
        robot_pos = DOWN * 0.5
        body_ellipse = Ellipse(
            width=1.4, height=0.9,
            color=TEAL_EP2, fill_opacity=0.3, stroke_width=2.5,
        ).move_to(robot_pos)

        # Default limb anchor angles (where limb attaches to body)
        BASE_ANGLES = [PI / 4, 3 * PI / 4, -PI / 4, -3 * PI / 4]  # UR, UL, LR, LL
        LIMB_LEN = 0.65

        def build_limb(base_angle, pose_delta=0.0, x_shift=0.0):
            """A limb VGroup(line, tip) pivoted at its body-attachment point.
            pose_delta rotates the limb around the attachment point."""
            base_pt = robot_pos + np.array([
                np.cos(base_angle) * 0.55 + x_shift,
                np.sin(base_angle) * 0.4,
                0,
            ])
            actual_angle = base_angle + pose_delta
            tip_pt = base_pt + np.array([
                np.cos(actual_angle) * LIMB_LEN,
                np.sin(actual_angle) * LIMB_LEN,
                0,
            ])
            line = Line(base_pt, tip_pt, color=TEAL_EP2, stroke_width=3)
            tip = Circle(
                radius=0.1, color=TEAL_EP2,
                fill_opacity=0.6, stroke_width=0,
            ).move_to(tip_pt)
            return VGroup(line, tip)

        # Pre-compute per-iteration limb pose deltas:
        #   i=2-4: chaotic flailing (large random angles)
        #   i=5-7: damping (smaller random angles, transitioning)
        #   i=8-11: coordinated alternating gait (diagonal pairs in phase)
        #   i=12: neutral pose, ready to walk
        rng = np.random.default_rng(7)
        pose_deltas = {}
        for i in range(2, 13):
            for limb_idx in range(4):
                if i <= 4:
                    chaos = (5 - i) / 3.0           # 1.0, 0.67, 0.33
                    pose_deltas[(i, limb_idx)] = rng.uniform(-PI / 3, PI / 3) * chaos
                elif i <= 7:
                    damp = (8 - i) / 4.0            # 0.75, 0.5, 0.25
                    pose_deltas[(i, limb_idx)] = rng.uniform(-PI / 6, PI / 6) * damp
                elif i <= 11:
                    # Diagonal pairs (UR+LL) vs (UL+LR) alternate
                    pair = 0 if limb_idx in (0, 3) else 1
                    phase = (i - 8) * PI / 2 + pair * PI
                    pose_deltas[(i, limb_idx)] = np.sin(phase) * 0.22
                else:  # i == 12
                    pose_deltas[(i, limb_idx)] = 0.0

        # Initial limb set (iteration 1 — default neutral pose)
        limbs = VGroup(*[build_limb(a, 0.0) for a in BASE_ANGLES])

        robot = VGroup(body_ellipse, limbs)

        self.play(FadeIn(body_ellipse), run_time=0.6)
        self.play(
            LaggedStart(*[Create(l[0]) for l in limbs], lag_ratio=0.15),
            run_time=0.9,
        )
        self.play(
            LaggedStart(*[GrowFromCenter(l[1]) for l in limbs], lag_ratio=0.12),
            run_time=0.7,
        )
        self.wait(0.4)

        # ── Iteration loop 2 → 12 ──────────────────────────────────────
        for i in range(2, 13):
            num_color = GREEN_3B1B if i == 12 else YELLOW_3B1B
            new_num = Text(
                str(i), font_size=48, color=num_color, weight=BOLD,
            ).move_to(iter_num.get_center())

            fill_color = GREEN_3B1B if i == 12 else TEAL_EP2
            new_fill = make_bar_fill(i, fill_color)

            # Build new limbs at this iteration's pose
            new_limbs = VGroup(*[
                build_limb(BASE_ANGLES[k], pose_deltas[(i, k)])
                for k in range(4)
            ])

            self.play(
                ReplacementTransform(iter_num, new_num),
                ReplacementTransform(bar_fill, new_fill),
                ReplacementTransform(limbs, new_limbs),
                run_time=0.45,
            )
            iter_num = new_num
            bar_fill = new_fill
            limbs = new_limbs
            robot = VGroup(body_ellipse, limbs)

        self.wait(0.4)

        # ── Robot walks: body + limbs shift together, limbs cycle the gait ─
        # One full gait cycle = 2 phases (diagonal pair A lifts, then B lifts).
        for phase_idx, x_target in enumerate([0.75, 1.5]):
            # Alternate gait phase: pair 0 (UR+LL) lifts, then pair 1 (UL+LR)
            shifted_limbs = VGroup(*[
                build_limb(
                    BASE_ANGLES[k],
                    pose_delta=0.25 if (k in ((0, 3) if phase_idx == 0 else (1, 2))) else -0.08,
                    x_shift=x_target,
                )
                for k in range(4)
            ])
            self.play(
                body_ellipse.animate.shift(RIGHT * (x_target - (0 if phase_idx == 0 else 0.75))),
                ReplacementTransform(limbs, shifted_limbs),
                run_time=0.55,
            )
            limbs = shifted_limbs

        # Walk back to start
        for phase_idx, x_target in enumerate([0.75, 0.0]):
            shifted_limbs = VGroup(*[
                build_limb(
                    BASE_ANGLES[k],
                    pose_delta=0.25 if (k in ((1, 2) if phase_idx == 0 else (0, 3))) else -0.08,
                    x_shift=x_target,
                )
                for k in range(4)
            ])
            self.play(
                body_ellipse.animate.shift(LEFT * (1.5 - x_target if phase_idx == 0 else 0.75)),
                ReplacementTransform(limbs, shifted_limbs),
                run_time=0.55,
            )
            limbs = shifted_limbs

        robot = VGroup(body_ellipse, limbs)
        self.wait(0.3)

        # ── Bottom callout ─────────────────────────────────────────────
        callout_text = Text(
            "Gradient flows through the physics simulation",
            font_size=22,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        callout_text.to_edge(DOWN, buff=0.55)
        callout_rect = SurroundingRectangle(
            callout_text,
            color=YELLOW_3B1B,
            buff=0.18,
            corner_radius=0.1,
            stroke_width=2,
        )
        self.play(
            Write(callout_text),
            Create(callout_rect),
            run_time=1.5,
        )
        self.wait(2.0)

        # ── FadeOut all ────────────────────────────────────────────────
        everything = VGroup(
            title,
            counter_row,
            iter_num,
            bar_bg,
            bar_fill,
            robot,
            callout_text,
            callout_rect,
        )
        self.play(FadeOut(everything), run_time=1.2)
        self.wait(0.4)
