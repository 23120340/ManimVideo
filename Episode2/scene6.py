"""
scene6.py — Episode 2, Scene 6: Sim-to-Real Transfer
======================================================
Demonstrates that the 4-photoreceptor design trained entirely in simulation
transfers to a real robot with zero fine-tuning. Shows training curves,
sim-vs-real performance stats, and the successful real-world navigation.

Run: manim -pql scene6.py Scene2SimToReal
"""

# VO: Toàn bộ quá trình huấn luyện diễn ra trong simulator. Không có một bước
# VO: fine-tuning nào trong thế giới thực. Khi đặt robot TurtleBot thật vào
# VO: phòng thật với bóng hồng thật, nó vẫn tìm được. Đây là bằng chứng rằng
# VO: 4 số đủ — khi thiết kế được tối ưu đúng cách.

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


class Scene6SimToReal(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title ─────────────────────────────────────────────────
        title = Text("From Simulation to Reality", font_size=40, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.42)
        self.play(Write(title, run_time=1.1, rate_func=smooth))
        self.wait(0.4)

        # ── Two-panel split ───────────────────────────────────────
        divider = Line(UP * 2.8, DOWN * 2.8, color=GRAY_DIM, stroke_width=1.5)
        divider.move_to(ORIGIN)

        sim_label  = Text("Simulator", font_size=26, color=BLUE_3B1B, weight=BOLD)
        real_label = Text("Real World", font_size=26, color=ORANGE_3B1B, weight=BOLD)
        sim_label.move_to(LEFT * 3.2 + UP * 2.3)
        real_label.move_to(RIGHT * 3.2 + UP * 2.3)

        self.play(
            Create(divider, run_time=0.6),
            FadeIn(sim_label, run_time=0.6),
            FadeIn(real_label, run_time=0.6),
        )

        # ── Simulator panel (left) ────────────────────────────────
        sim_room = Rectangle(
            width=2.8, height=2.2,
            color=GRAY_DIM, stroke_width=2.0, fill_opacity=0,
        )
        sim_room.move_to(LEFT * 3.2 + DOWN * 0.2)

        # Grid floor (gray)
        sim_floor = VGroup()
        n_grid = 5
        cell_sz = sim_room.width / n_grid
        for r in range(n_grid):
            for c in range(n_grid):
                sq = Square(
                    side_length=cell_sz * 0.96,
                    fill_color=GRAY_DARKER,
                    fill_opacity=0.55,
                    stroke_color=GRAY_DIM, stroke_width=0.4,
                )
                sq.move_to(
                    sim_room.get_corner(UL)
                    + RIGHT * (c + 0.5) * cell_sz
                    + DOWN * (r + 0.5) * cell_sz
                )
                sim_floor.add(sq)

        # Sim robot
        sim_robot = RoundedRectangle(
            width=0.28, height=0.38, corner_radius=0.06,
            color=BLUE_3B1B, stroke_width=2, fill_opacity=0.35,
        )
        sim_robot.move_to(sim_room.get_corner(UL) + RIGHT * 0.3 + DOWN * 0.3)

        # Sensor pixels display
        sensor_colors = [BLUE_3B1B, GREEN_3B1B, YELLOW_3B1B, RED_BRAIN]
        sensor_pixels = VGroup()
        for idx, col in enumerate(sensor_colors):
            r, c = divmod(idx, 2)
            px = Square(
                side_length=0.14,
                fill_color=col, fill_opacity=0.85, stroke_width=0,
            )
            px.move_to(sim_robot.get_right() + RIGHT * 0.1 + UP * (0.07 - r * 0.14) + RIGHT * c * 0.14)
            sensor_pixels.add(px)

        self.play(
            Create(sim_room, run_time=0.7),
            FadeIn(sim_floor, run_time=0.6),
            FadeIn(sim_robot, run_time=0.5),
            FadeIn(sensor_pixels, run_time=0.5),
        )

        # Animate sim robot moving along a path
        sim_path_pts = [
            sim_room.get_corner(UL) + RIGHT * 0.3 + DOWN * 0.3,
            sim_room.get_corner(UL) + RIGHT * 0.9 + DOWN * 0.8,
            sim_room.get_corner(UL) + RIGHT * 1.8 + DOWN * 1.2,
            sim_room.get_corner(DL) + RIGHT * 2.2 + UP * 0.4,
            sim_room.get_corner(DR) + LEFT * 0.3 + UP * 0.3,
        ]

        sim_trail = VGroup()
        current_pt = sim_path_pts[0]
        for pt in sim_path_pts[1:]:
            segment = Line(current_pt, pt, color=BLUE_3B1B, stroke_width=2.2, stroke_opacity=0.75)
            sim_trail.add(segment)
            self.play(
                Create(segment),
                sim_robot.animate.move_to(pt),
                sensor_pixels.animate.shift(pt - current_pt),
                run_time=0.45,
                rate_func=smooth,
            )
            new_colors = np.random.default_rng(hash(tuple(pt)) % (2**31)).choice(sensor_colors, 4, replace=True)
            self.play(*[px.animate.set_fill(color=nc) for px, nc in zip(sensor_pixels, new_colors)], run_time=0.16)
            current_pt = pt
        self.wait(0.3)

        # ── Real world panel (right) ──────────────────────────────
        real_room = Rectangle(
            width=2.8, height=2.2,
            color=ORANGE_3B1B, stroke_width=2.0, fill_opacity=0,
        )
        real_room.move_to(RIGHT * 3.2 + DOWN * 0.2)

        real_floor = VGroup()
        warm_palette = ["#4A3728", "#3D2E1E", "#5C4533", "#4A3728", "#3D2E1E"]
        for r in range(n_grid):
            for c in range(n_grid):
                col = warm_palette[(r + c) % len(warm_palette)]
                sq = Square(
                    side_length=cell_sz * 0.96,
                    fill_color=col, fill_opacity=0.65,
                    stroke_color=GRAY_DARKER, stroke_width=0.4,
                )
                sq.move_to(
                    real_room.get_corner(UL)
                    + RIGHT * (c + 0.5) * cell_sz
                    + DOWN * (r + 0.5) * cell_sz
                )
                real_floor.add(sq)

        real_robot = RoundedRectangle(
            width=0.28, height=0.38, corner_radius=0.06,
            color=ORANGE_3B1B, stroke_width=2, fill_opacity=0.35,
        )
        real_robot.move_to(real_room.get_corner(UL) + RIGHT * 0.3 + DOWN * 0.3)

        goal_ball = Circle(
            radius=0.14, color=PINK_3B1B,
            stroke_width=2.0, fill_opacity=0.85,
        )
        goal_ball.move_to(real_room.get_corner(DR) + LEFT * 0.3 + UP * 0.3)

        goal_ball_lbl = Text("goal", font_size=13, color=PINK_3B1B)
        goal_ball_lbl.next_to(goal_ball, DOWN, buff=0.06)

        self.play(
            Create(real_room, run_time=0.7),
            FadeIn(real_floor, run_time=0.6),
            FadeIn(real_robot, run_time=0.5),
            FadeIn(goal_ball, run_time=0.5),
            FadeIn(goal_ball_lbl, run_time=0.4),
        )

        real_path_pts = [
            real_room.get_corner(UL) + RIGHT * 0.3 + DOWN * 0.3,
            real_room.get_corner(UL) + RIGHT * 0.9 + DOWN * 0.75,
            real_room.get_center() + RIGHT * 0.5 + DOWN * 0.15,
            real_room.get_corner(DR) + LEFT * 0.3 + UP * 0.3,
        ]
        real_trail = VGroup()
        current_pt = real_path_pts[0]
        for pt in real_path_pts[1:]:
            segment = Line(current_pt, pt, color=ORANGE_3B1B, stroke_width=2.2, stroke_opacity=0.78)
            real_trail.add(segment)
            self.play(
                Create(segment),
                real_robot.animate.move_to(pt),
                run_time=0.55,
                rate_func=smooth,
            )
            current_pt = pt
        self.play(Flash(goal_ball, color=emphasis_color_of(goal_ball), flash_radius=0.35), run_time=0.45)
        self.wait(0.3)

        # ── "Zero real-world fine-tuning" text ───────────────────
        zero_ft = Text("Zero real-world fine-tuning", font_size=26, color=GREEN_3B1B, weight=BOLD)
        zero_ft.to_edge(DOWN, buff=0.5)
        self.play(Write(zero_ft, run_time=1.0, rate_func=smooth))
        self.wait(0.5)

        # ── Fade panels, show training curve ─────────────────────
        self.play(
            FadeOut(VGroup(
                sim_room, sim_floor, sim_robot, sensor_pixels, sim_trail,
                real_room, real_floor, real_robot, real_trail, goal_ball, goal_ball_lbl,
                divider, sim_label, real_label, zero_ft,
            ), run_time=0.8),
        )

        # ── Training curve ────────────────────────────────────────
        # Title riêng cho curve — dùng subtitle nhỏ hơn, không đè lên title chính
        curve_title = Text("Training Curve (Simulator)", font_size=26, color=GRAY_LIGHT)
        curve_title.next_to(title, DOWN, buff=0.18)
        self.play(FadeIn(curve_title, run_time=0.7))

        # Axes — dịch trái và xuống vừa đủ để stats card có chỗ bên phải
        ax_origin = LEFT * 5 + DOWN * 1.8
        ax_w, ax_h = 5.5, 3.2

        x_axis = Arrow(ax_origin, ax_origin + RIGHT * ax_w, buff=0, color=GRAY_MID, stroke_width=2)
        y_axis = Arrow(ax_origin, ax_origin + UP * ax_h, buff=0, color=GRAY_MID, stroke_width=2)

        x_lbl = Text("Episodes (x1000)", font_size=17, color=GRAY_MID)
        x_lbl.next_to(x_axis, DOWN, buff=0.15).shift(RIGHT * 0.5)

        y_lbl = Text("Loss", font_size=17, color=GRAY_MID)
        y_lbl.next_to(y_axis, LEFT, buff=0.12).shift(UP * 0.3)

        tick_group = VGroup()
        for i, ep in enumerate([0, 2, 4, 6, 8, 10]):
            x_pos = ax_origin + RIGHT * (i / 5) * ax_w
            tick = Line(x_pos + DOWN * 0.06, x_pos + UP * 0.06, color=GRAY_MID, stroke_width=1.2)
            lbl = Text(str(ep), font_size=14, color=GRAY_MID)
            lbl.next_to(tick, DOWN, buff=0.08)
            tick_group.add(tick, lbl)

        self.play(
            Create(x_axis, run_time=0.6),
            Create(y_axis, run_time=0.6),
            FadeIn(x_lbl, run_time=0.5),
            FadeIn(y_lbl, run_time=0.5),
            FadeIn(tick_group, run_time=0.5),
        )

        # Loss curve
        n_pts = 30
        t = np.linspace(0, 1, n_pts)
        loss = 0.9 * np.exp(-3.5 * t) + 0.08 + 0.025 * np.sin(t * 20)
        loss = np.clip(loss, 0.05, 1.0)

        curve_pts = [
            ax_origin + RIGHT * (ti * ax_w) + UP * (li * ax_h)
            for ti, li in zip(t, loss)
        ]
        curve_vmob = VMobject(color=GREEN_3B1B, stroke_width=2.8)
        curve_vmob.set_points_smoothly([np.array([*p, 0]) if len(p) == 2 else p for p in curve_pts])

        self.play(Create(curve_vmob, run_time=2.5, rate_func=smooth))
        train_marker = Dot(curve_pts[0], radius=0.07, color=YELLOW_3B1B)
        self.play(FadeIn(train_marker, scale=0.8), run_time=0.20)
        self.play(MoveAlongPath(train_marker, curve_vmob), run_time=1.4, rate_func=smooth)
        self.play(Flash(train_marker, color=emphasis_color_of(train_marker), flash_radius=0.30), run_time=0.45)
        self.remove(train_marker)
        self.wait(0.3)

        self.wait(0.4)

        # ── Stats card — bên phải, giữa màn hình theo chiều dọc ──
        stats_lines = [
            "Point-goal:  91% (sim)  vs  87% (real)",
            "Target-find: 84% (sim)  vs  79% (real)",
        ]
        stats_group = VGroup()
        for line in stats_lines:
            t_obj = Text(line, font_size=19, color=GRAY_LIGHT)
            stats_group.add(t_obj)
        stats_group.arrange(DOWN, buff=0.28, aligned_edge=LEFT)

        stats_box = SurroundingRectangle(
            stats_group, color=TEAL_EP2, buff=0.25,
            stroke_width=2.0, corner_radius=0.12,
        )
        stats_all = VGroup(stats_box, stats_group)
        stats_all.move_to(RIGHT * 3.8 + UP * 0.3)

        self.play(
            Create(stats_box, run_time=0.8),
            LaggedStart(
                *[Write(t, run_time=0.8) for t in stats_group],
                lag_ratio=0.5, run_time=1.4,
            ),
        )
        self.wait(0.6)

        # ── Conclusion text — dưới stats card, không đè graph ────
        conclude_txt = Text(
            "The 4-pixel design transfers.\nNo retraining needed.",
            font_size=26, color=YELLOW_3B1B, weight=BOLD, line_spacing=1.35,
        )
        conclude_txt.next_to(stats_all, DOWN, buff=0.45)

        self.play(Write(conclude_txt, run_time=1.2, rate_func=smooth))
        self.wait(2.0)

        # ── FadeOut everything ────────────────────────────────────
        self.play(FadeOut(Group(*self.mobjects), run_time=1.2, rate_func=smooth))
        self.wait(0.2)
