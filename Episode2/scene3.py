"""
scene3.py — Episode 2, Scene 3: The Navigation Problem
========================================================
Demonstrates two navigation tasks (point-goal and target-finding) by drawing
a top-down floor plan with obstacles, three agent paths, and a performance
bar chart comparing blind / camera / 4-photoreceptor agents.

Run: manim -pql scene3.py Scene2Navigation
"""

# VO: Ta thử hai bài toán: point-goal navigation — biết toạ độ đích, di chuyển
# VO: tới đó không va vật cản. Và target navigation — tìm một vật thể cụ thể.
# VO: Kết quả gây bất ngờ: agent với 4 photoreceptor thực hiện gần ngang agent
# VO: với camera 128×128.

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


class Scene2Navigation(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title ─────────────────────────────────────────────────
        title = Text("The Task: Navigate to a Goal", font_size=38, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.38)
        self.play(Write(title, run_time=1.1, rate_func=smooth))
        self.wait(0.4)

        # ── Floor plan ────────────────────────────────────────────
        room = Rectangle(
            width=5.6, height=4.0,
            color=GRAY_MID, stroke_width=2.5, fill_opacity=0,
        )
        room.move_to(LEFT * 0.5 + DOWN * 0.3)

        # Obstacles (walls / furniture)
        obs1 = Rectangle(
            width=0.3, height=1.5,
            color=GRAY_MID, stroke_width=1.8,
            fill_color=GRAY_DARKER, fill_opacity=0.6,
        )
        obs1.move_to(room.get_center() + LEFT * 0.9 + UP * 0.4)

        obs2 = Rectangle(
            width=1.6, height=0.28,
            color=GRAY_MID, stroke_width=1.8,
            fill_color=GRAY_DARKER, fill_opacity=0.6,
        )
        obs2.move_to(room.get_center() + RIGHT * 0.7 + DOWN * 0.55)

        obs3 = Rectangle(
            width=0.28, height=0.9,
            color=GRAY_MID, stroke_width=1.8,
            fill_color=GRAY_DARKER, fill_opacity=0.6,
        )
        obs3.move_to(room.get_center() + LEFT * 0.1 + DOWN * 1.1)

        floor_plan = VGroup(room, obs1, obs2, obs3)

        # Start dot
        start_pos = room.get_corner(UL) + RIGHT * 0.38 + DOWN * 0.35
        start_dot = Dot(start_pos, radius=0.12, color=GREEN_3B1B)
        start_label = Text("START", font_size=16, color=GREEN_3B1B)
        start_label.next_to(start_dot, UP, buff=0.08)

        # Goal dot (glowing star approximation using nested circles)
        goal_pos = room.get_corner(DR) + LEFT * 0.38 + UP * 0.35
        goal_outer = Circle(radius=0.20, color=YELLOW_3B1B, stroke_width=2.2, fill_opacity=0.2)
        goal_inner = Dot(goal_pos, radius=0.10, color=YELLOW_3B1B)
        goal_outer.move_to(goal_pos)
        goal_label = Text("GOAL", font_size=16, color=YELLOW_3B1B)
        goal_label.next_to(goal_outer, DOWN, buff=0.08)

        self.play(
            Create(room, run_time=1.0, rate_func=smooth),
            run_time=1.0,
        )
        self.play(
            FadeIn(obs1, run_time=0.5),
            FadeIn(obs2, run_time=0.5),
            FadeIn(obs3, run_time=0.5),
        )
        self.play(
            FadeIn(start_dot, scale=1.3, run_time=0.6),
            FadeIn(start_label, run_time=0.5),
            FadeIn(goal_outer, scale=0.8, run_time=0.6),
            FadeIn(goal_inner, run_time=0.5),
            FadeIn(goal_label, run_time=0.5),
        )
        self.wait(0.4)

        # ── Path helper ───────────────────────────────────────────
        def make_path(points, color, stroke_width=2.8, dash=False):
            segs = VGroup()
            for i in range(len(points) - 1):
                p0 = np.array([*points[i], 0])
                p1 = np.array([*points[i + 1], 0])
                if dash:
                    n_dashes = max(3, int(np.linalg.norm(p1 - p0) / 0.12))
                    for j in range(n_dashes):
                        if j % 2 == 0:
                            t0 = j / n_dashes
                            t1 = min((j + 1) / n_dashes, 1.0)
                            segs.add(Line(
                                p0 + t0 * (p1 - p0), p0 + t1 * (p1 - p0),
                                color=color, stroke_width=stroke_width,
                            ))
                else:
                    segs.add(Line(p0, p1, color=color, stroke_width=stroke_width))
            return segs

        # RED: Blind agent — random zigzag
        sx, sy = start_pos[0], start_pos[1]
        gx, gy = goal_pos[0], goal_pos[1]
        red_pts = [
            (sx, sy), (sx + 0.3, sy - 0.6), (sx - 0.1, sy - 1.2),
            (sx + 0.7, sy - 1.5), (sx + 0.4, sy - 0.8), (sx + 1.1, sy - 1.1),
            (sx + 1.5, sy - 1.8), (sx + 0.9, sy - 2.3), (sx + 1.8, sy - 2.6),
            (gx, gy),
        ]
        red_path = make_path(red_pts, RED_BRAIN, stroke_width=2.2, dash=True)

        # BLUE: 128×128 camera — near straight line
        blue_pts = [
            (sx, sy), (sx + 0.2, sy - 0.5), (sx + 0.6, sy - 1.1),
            (sx + 1.2, sy - 1.8), (sx + 1.8, sy - 2.4), (gx, gy),
        ]
        blue_path = make_path(blue_pts, BLUE_3B1B, stroke_width=2.5)

        # GREEN: 4 photoreceptors — similar with minor detour
        green_pts = [
            (sx, sy), (sx + 0.15, sy - 0.55), (sx + 0.55, sy - 1.05),
            (sx + 0.95, sy - 1.35), (sx + 1.35, sy - 1.85),
            (sx + 1.75, sy - 2.35), (gx, gy),
        ]
        green_path = make_path(green_pts, GREEN_3B1B, stroke_width=2.5)

        # Path labels (positioned at mid-path)
        lbl_red  = Text("Blind agent",      font_size=18, color=RED_BRAIN)
        lbl_blue = Text("128×128 camera",   font_size=18, color=BLUE_3B1B)
        lbl_grn  = Text("4 photoreceptors", font_size=18, color=GREEN_3B1B)

        red_mid  = np.array([sx + 0.7, sy - 1.0, 0])
        blue_mid = np.array([sx + 1.0, sy - 1.4, 0])
        grn_mid  = np.array([sx + 1.55, sy - 2.1, 0])

        lbl_red.move_to(red_mid + LEFT * 1.1 + UP * 0.2)
        lbl_blue.move_to(blue_mid + LEFT * 1.3)
        lbl_grn.move_to(grn_mid + RIGHT * 1.1)

        # Animate each path
        self.play(
            LaggedStart(*[Create(s, run_time=0.18) for s in red_path], lag_ratio=0.1, run_time=1.8),
        )
        self.play(FadeIn(lbl_red, run_time=0.5))
        self.wait(0.2)

        self.play(
            LaggedStart(*[Create(s, run_time=0.15) for s in blue_path], lag_ratio=0.1, run_time=1.2),
        )
        self.play(FadeIn(lbl_blue, run_time=0.5))
        self.wait(0.2)

        self.play(
            LaggedStart(*[Create(s, run_time=0.15) for s in green_path], lag_ratio=0.1, run_time=1.2),
        )
        self.play(FadeIn(lbl_grn, run_time=0.5))
        self.wait(0.6)

        # ── Shift floor plan left for bar chart ───────────────────
        floor_group = VGroup(
            floor_plan, start_dot, start_label,
            goal_outer, goal_inner, goal_label,
            red_path, blue_path, green_path,
            lbl_red, lbl_blue, lbl_grn,
        )
        self.play(
            floor_group.animate.scale(0.72).to_edge(LEFT, buff=0.3).shift(DOWN * 0.1),
            run_time=0.9, rate_func=smooth,
        )

        # ── Performance bar chart ─────────────────────────────────
        chart_origin = RIGHT * 1.5 + DOWN * 1.2

        bar_data = [
            ("Blind",     0.31, RED_BRAIN),
            ("128×128",   0.91, BLUE_3B1B),
            ("4 pixels",  0.87, GREEN_3B1B),
        ]
        max_h = 2.2
        bar_w = 0.6
        gap   = 0.35

        bars_group  = VGroup()
        bar_labels_g = VGroup()
        pct_labels  = VGroup()

        for i, (name, val, col) in enumerate(bar_data):
            h = val * max_h
            x = chart_origin[0] + i * (bar_w + gap) - (bar_w + gap)
            bar_rect = Rectangle(
                width=bar_w, height=h,
                fill_color=col, fill_opacity=0.80,
                stroke_color=col, stroke_width=1.5,
            )
            bar_rect.move_to([x, chart_origin[1] + h / 2, 0])
            bars_group.add(bar_rect)

            name_lbl = Text(name, font_size=17, color=col)
            name_lbl.move_to([x, chart_origin[1] - 0.25, 0])
            bar_labels_g.add(name_lbl)

            pct_lbl = Text(f"{int(val*100)}%", font_size=18, color=GRAY_LIGHT)
            pct_lbl.move_to([x, chart_origin[1] + h + 0.22, 0])
            pct_labels.add(pct_lbl)

        chart_title = Text("Success Rate", font_size=22, color=GRAY_LIGHT)
        chart_title.move_to(chart_origin + UP * (max_h + 0.55) + LEFT * 0.0)

        # Axis line
        axis_line = Line(
            chart_origin + LEFT * 1.1,
            chart_origin + RIGHT * 2.1,
            color=GRAY_DIM, stroke_width=1.5,
        )

        self.play(Create(axis_line, run_time=0.5))
        self.play(FadeIn(chart_title, run_time=0.5))

        for bar, name_l, pct_l in zip(bars_group, bar_labels_g, pct_labels):
            self.play(
                GrowFromEdge(bar, DOWN, run_time=0.7, rate_func=smooth),
                FadeIn(name_l, run_time=0.4),
            )
            self.play(FadeIn(pct_l, shift=UP * 0.15, run_time=0.35))
        self.wait(0.5)

        # ── Punchline ─────────────────────────────────────────────
        punch = Text(
            "4 numbers  ≈  128×128 pixels\nfor navigation",
            font_size=28, color=YELLOW_3B1B, weight=BOLD, line_spacing=1.3,
        )
        punch.to_edge(DOWN, buff=0.4)
        self.play(Write(punch, run_time=1.3, rate_func=smooth))
        self.wait(2.2)

        # ── FadeOut everything ────────────────────────────────────
        all_objects = VGroup(
            title, floor_group,
            bars_group, bar_labels_g, pct_labels,
            chart_title, axis_line, punch,
        )
        self.play(FadeOut(all_objects, run_time=1.1, rate_func=smooth))
        self.wait(0.2)
