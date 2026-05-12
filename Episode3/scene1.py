"""
scene1.py — Episode 3, Scene 1: Hook
"RL learns in 10,000 rollouts. This: 12. Why?"

Demonstrates a soft robot learning to walk in 12 iterations,
showing how gradient flows through physics simulation.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class Scene3Hook(Scene):
    def construct(self):
        # ── Background ──────────────────────────────────────────────
        self.camera.background_color = BG_COLOR

        # VO: "RL thông thường cần hàng chục nghìn lần thử. Cái này chỉ cần 12.
        #       Lý do nằm ở một ý tưởng đơn giản: thay vì coi simulator là hộp đen,
        #       ta mở nó ra — và để gradient chảy qua chính các bước vật lý."

        # ── Step 1: Title ───────────────────────────────────────────
        title = Text(
            "RL learns in 10,000 rollouts.  This: 12.  Why?",
            font_size=32,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=2.0)
        self.wait(1.0)

        # ── Step 2: Soft robot body ─────────────────────────────────
        # Central ellipse body
        robot_center = UP * 0.2

        body_ellipse = Ellipse(
            width=1.2, height=0.8,
            color=TEAL_EP2,
            fill_color=TEAL_EP2,
            fill_opacity=0.3,
            stroke_width=2.5,
        )
        body_ellipse.move_to(robot_center)

        # 4 limbs at ±45° above and below horizontal
        limb_length = 0.65
        limb_angles = [
            PI / 4,       # upper-right
            -PI / 4,      # lower-right
            3 * PI / 4,   # upper-left
            -3 * PI / 4,  # lower-left
        ]

        limbs = VGroup()
        tips = VGroup()
        for angle in limb_angles:
            start = robot_center + np.array([
                np.cos(angle) * 0.5,
                np.sin(angle) * 0.35,
                0,
            ])
            end = robot_center + np.array([
                np.cos(angle) * (0.5 + limb_length),
                np.sin(angle) * (0.35 + limb_length * 0.6),
                0,
            ])
            limb = Line(start, end, color=TEAL_EP2, stroke_width=2.5)
            tip = Circle(radius=0.1, color=TEAL_EP2, fill_color=TEAL_EP2, fill_opacity=0.6, stroke_width=2)
            tip.move_to(end)
            limbs.add(limb)
            tips.add(tip)

        robot = VGroup(body_ellipse, limbs, tips)

        self.play(FadeIn(body_ellipse), run_time=0.8)
        self.play(
            LaggedStart(*[Create(l) for l in limbs], lag_ratio=0.15, run_time=1.2),
        )
        self.play(
            LaggedStart(*[GrowFromCenter(t) for t in tips], lag_ratio=0.15, run_time=0.8),
        )
        self.wait(0.5)

        # ── Step 3: Iteration label + progress bar ──────────────────
        iter_label_prefix = Text("Iteration: ", font_size=22, color=GRAY_MID)
        iter_label_prefix.move_to(LEFT * 4.5 + UP * 1.5)

        iter_num = Text("1", font_size=22, color=YELLOW_3B1B, weight=BOLD)
        iter_num.next_to(iter_label_prefix, RIGHT, buff=0.1)

        # Progress bar background
        bar_bg = Rectangle(
            width=2.8, height=0.18,
            color=GRAY_DARKER, fill_color=GRAY_DARKER, fill_opacity=1.0,
            stroke_width=1,
        )
        bar_bg.next_to(iter_label_prefix, DOWN, buff=0.28)

        # Progress bar fill (starts at 1/12 width)
        bar_fill = Rectangle(
            width=2.8 / 12, height=0.18,
            color=TEAL_EP2, fill_color=TEAL_EP2, fill_opacity=1.0,
            stroke_width=0,
        )
        bar_fill.move_to(bar_bg.get_left() + RIGHT * (2.8 / 12) / 2)

        bar_label_12 = Text("12", font_size=14, color=GRAY_DIM)
        bar_label_12.next_to(bar_bg, RIGHT, buff=0.12)

        self.play(
            FadeIn(iter_label_prefix, shift=RIGHT * 0.2),
            FadeIn(iter_num, shift=RIGHT * 0.2),
            run_time=0.8,
        )
        self.play(
            FadeIn(bar_bg),
            FadeIn(bar_fill),
            FadeIn(bar_label_12),
            run_time=0.6,
        )
        self.wait(0.5)

        # ── Step 4: Iterations 1→5: robot tilts ────────────────────
        # Simulate robot learning — it starts leaning, tilting
        for i in range(2, 7):
            new_num = Text(str(i), font_size=22, color=YELLOW_3B1B, weight=BOLD)
            new_num.next_to(iter_label_prefix, RIGHT, buff=0.1)

            new_bar_fill = Rectangle(
                width=2.8 * i / 12, height=0.18,
                color=TEAL_EP2, fill_color=TEAL_EP2, fill_opacity=1.0,
                stroke_width=0,
            )
            new_bar_fill.move_to(bar_bg.get_left() + RIGHT * (2.8 * i / 12) / 2)

            if i == 2:
                self.play(
                    robot.animate.rotate(PI / 8).shift(RIGHT * 0.3),
                    ReplacementTransform(iter_num, new_num),
                    ReplacementTransform(bar_fill, new_bar_fill),
                    run_time=0.7,
                )
            elif i == 3:
                self.play(
                    robot.animate.rotate(-PI / 12).shift(RIGHT * 0.1),
                    ReplacementTransform(iter_num, new_num),
                    ReplacementTransform(bar_fill, new_bar_fill),
                    run_time=0.7,
                )
            elif i == 4:
                self.play(
                    robot.animate.rotate(PI / 16),
                    ReplacementTransform(iter_num, new_num),
                    ReplacementTransform(bar_fill, new_bar_fill),
                    run_time=0.7,
                )
            else:
                self.play(
                    ReplacementTransform(iter_num, new_num),
                    ReplacementTransform(bar_fill, new_bar_fill),
                    run_time=0.6,
                )
            iter_num = new_num
            bar_fill = new_bar_fill

        self.wait(0.4)

        # ── Step 5: Iteration 6 — limbs extend, body stabilizes ─────
        new_num_6 = Text("6", font_size=22, color=YELLOW_3B1B, weight=BOLD)
        new_num_6.next_to(iter_label_prefix, RIGHT, buff=0.1)
        new_bar_6 = Rectangle(
            width=2.8 * 6 / 12, height=0.18,
            color=TEAL_EP2, fill_color=TEAL_EP2, fill_opacity=1.0,
            stroke_width=0,
        )
        new_bar_6.move_to(bar_bg.get_left() + RIGHT * (2.8 * 6 / 12) / 2)

        self.play(
            robot.animate.scale(1.15).rotate(-PI / 10),
            ReplacementTransform(iter_num, new_num_6),
            ReplacementTransform(bar_fill, new_bar_6),
            run_time=0.9,
        )
        iter_num = new_num_6
        bar_fill = new_bar_6
        self.wait(0.4)

        # Iterations 7–11
        for i in range(7, 12):
            new_num = Text(str(i), font_size=22, color=YELLOW_3B1B, weight=BOLD)
            new_num.next_to(iter_label_prefix, RIGHT, buff=0.1)

            new_bar = Rectangle(
                width=2.8 * i / 12, height=0.18,
                color=TEAL_EP2, fill_color=TEAL_EP2, fill_opacity=1.0,
                stroke_width=0,
            )
            new_bar.move_to(bar_bg.get_left() + RIGHT * (2.8 * i / 12) / 2)

            self.play(
                ReplacementTransform(iter_num, new_num),
                ReplacementTransform(bar_fill, new_bar),
                run_time=0.45,
            )
            iter_num = new_num
            bar_fill = new_bar

        # ── Step 6: Iteration 12 — upright, smooth movement ─────────
        new_num_12 = Text("12", font_size=22, color=GREEN_3B1B, weight=BOLD)
        new_num_12.next_to(iter_label_prefix, RIGHT, buff=0.1)
        new_bar_12 = Rectangle(
            width=2.8, height=0.18,
            color=GREEN_3B1B, fill_color=GREEN_3B1B, fill_opacity=1.0,
            stroke_width=0,
        )
        new_bar_12.move_to(bar_bg.get_left() + RIGHT * 2.8 / 2)

        # Robot straightens up
        self.play(
            robot.animate.rotate(-PI / 16).scale(1.0 / 1.15),
            ReplacementTransform(iter_num, new_num_12),
            ReplacementTransform(bar_fill, new_bar_12),
            run_time=0.9,
        )
        iter_num = new_num_12
        bar_fill = new_bar_12

        # Dotted path the robot traces
        path_line = DashedLine(
            LEFT * 2 + DOWN * 0.4,
            RIGHT * 2 + DOWN * 0.4,
            color=GREEN_3B1B,
            stroke_width=2,
            dash_length=0.12,
        )
        self.play(Create(path_line), run_time=1.0)

        # Robot glides along path
        self.play(
            robot.animate.shift(RIGHT * 1.2),
            run_time=1.2,
        )
        self.play(
            robot.animate.shift(LEFT * 1.2),
            run_time=1.0,
        )
        self.wait(0.5)

        # ── Step 7: Callout box at bottom ───────────────────────────
        callout_text = Text(
            "Gradient flows through the physics simulation itself",
            font_size=22,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        callout_text.to_edge(DOWN, buff=0.55)
        callout_rect = SurroundingRectangle(
            callout_text,
            color=YELLOW_3B1B,
            stroke_width=2,
            buff=0.18,
            corner_radius=0.1,
        )
        self.play(
            Write(callout_text),
            Create(callout_rect),
            run_time=1.5,
        )
        self.wait(2.0)

        # ── Step 8: FadeOut all ─────────────────────────────────────
        all_objects = VGroup(
            title,
            robot,
            iter_label_prefix, iter_num,
            bar_bg, bar_fill, bar_label_12,
            path_line,
            callout_text, callout_rect,
        )
        self.play(FadeOut(all_objects), run_time=1.5)
        self.wait(0.5)
