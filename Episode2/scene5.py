"""
scene5.py — Episode 2, Scene 5: The Surprise — optimal sensor points DOWN
==========================================================================
The "aha moment" scene. Builds suspense by showing what humans would intuitively
place (all-forward sensors), then reveals the optimizer's answer: one sensor
faces straight down. Explains the wall-detection logic via floor contrast,
and shows the human survey result.

Run: manim -pql scene5.py Scene2Surprise
"""

# VO: Khi ta nhìn vào thiết kế tối ưu, có một chi tiết lạ: một trong bốn
# VO: photoreceptor nhìn xuống đất. Tại sao? Vì agent này đã biết toạ độ mục
# VO: tiêu — thứ duy nhất nó cần biết thêm là: có tường không? Và tường phản
# VO: ánh lên mặt sàn trước khi ta va vào nó.

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


class Scene2Surprise(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title ─────────────────────────────────────────────────
        title = Text("The Optimal Sensor Design", font_size=40, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        self.play(Write(title, run_time=1.1, rate_func=smooth))
        self.wait(0.4)

        # ── Robot body (top-down view) ────────────────────────────
        robot_body = RoundedRectangle(
            width=1.2, height=1.6,
            corner_radius=0.2,
            color=GRAY_MID, stroke_width=2.5,
            fill_color=GRAY_DARKER, fill_opacity=0.5,
        )
        robot_body.move_to(UP * 0.3)

        robot_lbl = Text("Robot (top-down)", font_size=18, color=GRAY_MID)
        robot_lbl.next_to(robot_body, DOWN, buff=0.2)

        self.play(
            Create(robot_body, run_time=0.9, rate_func=smooth),
            FadeIn(robot_lbl, run_time=0.6),
        )
        self.wait(0.3)

        # ── "What would YOU place?" — forward arrows ──────────────
        intuitive_q = Text("What would YOU place?", font_size=28, color=GRAY_LIGHT)
        intuitive_q.to_corner(UL, buff=0.8).shift(DOWN * 0.4)
        self.play(FadeIn(intuitive_q, run_time=0.7))

        forward_arrows = VGroup()
        arrow_directions = [
            (UP * 0.6, "forward"),
            (UP * 0.6 + RIGHT * 0.5, "fwd-right"),
            (UP * 0.6 + LEFT * 0.5, "fwd-left"),
            (RIGHT * 0.7, "right"),
        ]
        for direction, _ in arrow_directions:
            tip = robot_body.get_center() + direction * 1.05
            arr = Arrow(
                robot_body.get_center() + direction * 0.65,
                tip,
                color=GRAY_LIGHT, buff=0, stroke_width=2.5,
                max_tip_length_to_length_ratio=0.35,
            )
            forward_arrows.add(arr)

        self.play(
            LaggedStart(
                *[GrowArrow(a, run_time=0.5) for a in forward_arrows],
                lag_ratio=0.2, run_time=1.4,
            )
        )
        self.wait(1.0)

        # ── Pause then reveal optimizer's answer ─────────────────
        optimizer_q = Text("What the optimizer found:", font_size=28, color=YELLOW_3B1B, weight=BOLD)
        optimizer_q.to_corner(UR, buff=0.8).shift(DOWN * 0.4 + LEFT * 0.2)
        self.play(FadeIn(optimizer_q, run_time=0.8))
        self.wait(0.5)

        # Replace forward arrows with optimal design:
        # 3 forward/sideways + 1 pointing DOWN (highlighted)
        optimal_arrows = VGroup()
        optimal_configs = [
            (UP * 0.7,              GRAY_MID),   # forward
            (UP * 0.5 + LEFT * 0.55, GRAY_MID),  # fwd-left
            (RIGHT * 0.8,           GRAY_MID),   # side-right
            (DOWN * 0.85,           YELLOW_3B1B),# STRAIGHT DOWN — the surprise
        ]
        for direction, col in optimal_configs:
            tip = robot_body.get_center() + direction * 1.08
            arr = Arrow(
                robot_body.get_center() + direction * 0.65,
                tip,
                color=col, buff=0, stroke_width=2.8,
                max_tip_length_to_length_ratio=0.35,
            )
            optimal_arrows.add(arr)

        self.play(
            FadeOut(forward_arrows, run_time=0.5),
            run_time=0.5,
        )
        self.play(
            LaggedStart(
                *[GrowArrow(a, run_time=0.55) for a in optimal_arrows[:3]],
                lag_ratio=0.2, run_time=1.0,
            )
        )
        self.wait(0.3)
        # Dramatic reveal of downward sensor
        self.play(
            GrowArrow(optimal_arrows[3], run_time=0.9, rate_func=smooth),
        )
        self.play(
            Indicate(optimal_arrows[3], color=YELLOW_3B1B, scale_factor=1.4, run_time=1.0),
        )

        down_lbl = Text("Points DOWN?!", font_size=22, color=YELLOW_3B1B, weight=BOLD)
        down_lbl.next_to(robot_body, RIGHT, buff=0.3).shift(DOWN * 0.85)
        self.play(FadeIn(down_lbl, scale=1.2, run_time=0.7))
        self.wait(0.5)

        # ── Question float ────────────────────────────────────────
        why_q = Text("Why does a sensor point at the floor?", font_size=26, color=GRAY_LIGHT)
        why_q.to_edge(DOWN, buff=1.8)
        self.play(
            why_q.animate.shift(UP * 0.4),
            FadeIn(why_q, run_time=0.9),
        )
        self.wait(0.6)

        # ── Explanation unfolds ───────────────────────────────────
        self.play(
            FadeOut(VGroup(intuitive_q, optimizer_q, why_q, down_lbl), run_time=0.6),
            VGroup(robot_body, robot_lbl, optimal_arrows).animate.scale(0.7).to_corner(UR, buff=0.7),
            run_time=0.8,
        )

        # GPS-like knowledge
        exp1 = Text("① Robot already knows goal coords (GPS-like)", font_size=22, color=GRAY_LIGHT)
        exp1.move_to(LEFT * 1.0 + UP * 2.0)
        gps_icon = VGroup(
            Circle(radius=0.15, color=GREEN_3B1B, stroke_width=2, fill_opacity=0.3),
            Text("GPS", font_size=12, color=GREEN_3B1B),
        )
        gps_icon[1].move_to(gps_icon[0].get_center())
        gps_icon.next_to(exp1, LEFT, buff=0.2)

        self.play(FadeIn(exp1, shift=RIGHT * 0.3, run_time=0.7))
        self.play(FadeIn(gps_icon, run_time=0.5))
        self.wait(0.3)

        exp2 = Text("② What it needs: detect WALLS before collision", font_size=22, color=RED_BRAIN)
        exp2.next_to(exp1, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(FadeIn(exp2, shift=RIGHT * 0.3, run_time=0.7))
        self.wait(0.3)

        # Mini floor-sensor demo
        exp3 = Text("③ Floor texture changes near walls → early warning", font_size=22, color=YELLOW_3B1B)
        exp3.next_to(exp2, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(FadeIn(exp3, shift=RIGHT * 0.3, run_time=0.7))
        self.wait(0.3)

        # Animated mini demo: robot approaching wall, floor sensor contrast change
        mini_floor = Rectangle(
            width=3.2, height=0.4,
            fill_color=GRAY_DARKER, fill_opacity=0.8,
            stroke_color=GRAY_DIM, stroke_width=1.5,
        )
        mini_floor.move_to(DOWN * 1.6 + LEFT * 1.0)

        wall_rect = Rectangle(
            width=0.18, height=1.0,
            fill_color=GRAY_MID, fill_opacity=0.9,
            stroke_color=GRAY_MID, stroke_width=1.5,
        )
        wall_rect.move_to(mini_floor.get_right() + LEFT * 0.09)

        mini_robot_r = RoundedRectangle(
            width=0.3, height=0.4, corner_radius=0.06,
            color=BLUE_3B1B, stroke_width=2, fill_opacity=0.3,
        )
        mini_robot_r.move_to(mini_floor.get_left() + RIGHT * 0.3 + UP * 0.35)

        # Floor sensor beam (downward)
        sensor_beam = Line(
            mini_robot_r.get_bottom(),
            mini_robot_r.get_bottom() + DOWN * 0.35,
            color=YELLOW_3B1B, stroke_width=2.5,
        )

        # Contrast indicator dot on floor
        contrast_dot = Dot(
            sensor_beam.get_end(), radius=0.08, color=YELLOW_3B1B,
        )

        self.play(
            FadeIn(mini_floor, run_time=0.5),
            FadeIn(wall_rect, run_time=0.5),
            FadeIn(mini_robot_r, run_time=0.5),
            Create(sensor_beam, run_time=0.4),
            FadeIn(contrast_dot, run_time=0.4),
        )

        # Robot moves towards wall
        shift_vec = RIGHT * 1.3
        self.play(
            mini_robot_r.animate.shift(shift_vec),
            sensor_beam.animate.shift(shift_vec),
            contrast_dot.animate.shift(shift_vec).set_color(RED_BRAIN),
            run_time=1.2, rate_func=smooth,
        )
        detect_lbl = Text("Wall detected!", font_size=16, color=RED_BRAIN)
        detect_lbl.next_to(contrast_dot, DOWN, buff=0.12)
        self.play(FadeIn(detect_lbl, scale=1.2, run_time=0.5))
        self.wait(0.6)

        # ── Human survey bars ─────────────────────────────────────
        self.play(
            FadeOut(VGroup(
                mini_floor, wall_rect, mini_robot_r, sensor_beam,
                contrast_dot, detect_lbl,
                exp1, exp2, exp3, gps_icon,
            ), run_time=0.7),
        )

        survey_title = Text("Humans surveyed before seeing the result:", font_size=24, color=GRAY_LIGHT)
        survey_title.move_to(LEFT * 1.0 + UP * 2.0)
        self.play(FadeIn(survey_title, run_time=0.7))

        survey_data = [
            ("Forward-facing\n(wrong)", 0.82, RED_BRAIN),
            ("Downward/mixed\n(close)", 0.18, GREEN_3B1B),
        ]
        bar_origin = DOWN * 0.5 + LEFT * 1.5
        bar_max_h = 2.0
        bar_w = 0.9

        bars_s = VGroup()
        labs_s = VGroup()
        pcts_s = VGroup()

        for i, (name, val, col) in enumerate(survey_data):
            h = val * bar_max_h
            x = bar_origin[0] + i * 2.2
            b = Rectangle(
                width=bar_w, height=h,
                fill_color=col, fill_opacity=0.82,
                stroke_color=col, stroke_width=1.5,
            )
            b.move_to([x, bar_origin[1] + h / 2, 0])
            bars_s.add(b)

            lb = Text(name, font_size=17, color=col, line_spacing=1.2)
            lb.move_to([x, bar_origin[1] - 0.4, 0])
            labs_s.add(lb)

            pc = Text(f"{int(val*100)}%", font_size=20, color=GRAY_LIGHT, weight=BOLD)
            pc.move_to([x, bar_origin[1] + h + 0.28, 0])
            pcts_s.add(pc)

        axis_s = Line(
            [bar_origin[0] - 0.7, bar_origin[1], 0],
            [bar_origin[0] + 3.5, bar_origin[1], 0],
            color=GRAY_DIM, stroke_width=1.5,
        )
        self.play(Create(axis_s, run_time=0.4))
        for b, lb, pc in zip(bars_s, labs_s, pcts_s):
            self.play(
                GrowFromEdge(b, DOWN, run_time=0.7, rate_func=smooth),
                FadeIn(lb, run_time=0.5),
            )
            self.play(FadeIn(pc, shift=UP * 0.15, run_time=0.35))
        self.wait(0.5)

        # ── Lesson box ────────────────────────────────────────────
        lesson_txt = Text(
            "Intuition fails when\nthe constraints are non-obvious.",
            font_size=24, color=YELLOW_3B1B, weight=BOLD, line_spacing=1.35,
        )
        lesson_box = SurroundingRectangle(
            lesson_txt, color=YELLOW_3B1B, buff=0.28,
            stroke_width=2.0, corner_radius=0.12,
        )
        lesson_grp = VGroup(lesson_box, lesson_txt)
        lesson_grp.to_corner(DR, buff=0.5)

        self.play(
            Create(lesson_box, run_time=0.8),
            Write(lesson_txt, run_time=1.0),
        )
        self.wait(2.0)

        # ── FadeOut everything ────────────────────────────────────
        all_objects = VGroup(
            title, survey_title, bars_s, labs_s, pcts_s, axis_s, lesson_grp,
            robot_body, robot_lbl, optimal_arrows,
        )
        self.play(FadeOut(all_objects, run_time=1.2, rate_func=smooth))
        self.wait(0.2)
