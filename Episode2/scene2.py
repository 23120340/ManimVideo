"""
scene2.py — Episode 2, Scene 2: What is a photoreceptor?
=========================================================
Explains the three design parameters of a photoreceptor (position, direction,
field of view) and shows how the optimizer — not the engineer — chooses them.

Run: manim -pql scene2.py Scene2Photoreceptor
"""

# VO: Photoreceptor là một bộ cảm biến đơn giản: nó lấy trung bình ánh sáng
# VO: trong một vùng nhỏ của không gian. Ba tham số xác định nó: vị trí đặt
# VO: trên cơ thể robot, hướng nhìn, và góc trường nhìn. Trong bài toán này,
# VO: cả ba đều là biến số — không phải do kỹ sư quyết định.

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


class Scene2Photoreceptor(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title ─────────────────────────────────────────────────
        title = Text("What is a Photoreceptor?", font_size=42, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title, run_time=1.2, rate_func=smooth))
        self.wait(0.4)

        # ── 10×10 pixel grid (camera frame simulation) ────────────
        rng = np.random.default_rng(31)
        palette = [BLUE_3B1B, GREEN_3B1B, TEAL_EP2, PURPLE_3B1B, ORANGE_3B1B]

        cell = 0.155
        grid_group = VGroup()
        for r in range(10):
            for c in range(10):
                col = palette[rng.integers(len(palette))]
                sq = Square(
                    side_length=cell,
                    fill_color=col, fill_opacity=0.80,
                    stroke_color=BG_COLOR, stroke_width=0.4,
                )
                sq.move_to(RIGHT * c * cell + DOWN * r * cell)
                grid_group.add(sq)
        grid_group.move_to(LEFT * 3.5 + DOWN * 0.1)

        self.play(
            LaggedStart(
                *[FadeIn(sq, scale=0.75) for sq in grid_group],
                lag_ratio=0.012, run_time=1.6,
            )
        )
        self.wait(0.3)

        # ── Highlight 3×3 patch ───────────────────────────────────
        # Find the center of cells (4,4) to (6,6) relative to grid origin
        patch_cells = VGroup(*[
            grid_group[r * 10 + c]
            for r in range(3, 6)
            for c in range(3, 6)
        ])
        surround_rect = SurroundingRectangle(
            patch_cells, color=YELLOW_3B1B, stroke_width=2.8, buff=0.03,
        )
        self.play(
            Create(surround_rect, run_time=0.9, rate_func=smooth),
        )
        self.wait(0.3)

        # ── Arrow + single large square ───────────────────────────
        receptor_sq = Square(
            side_length=0.65,
            fill_color=TEAL_EP2, fill_opacity=0.75,
            stroke_color=TEAL_EP2, stroke_width=2.5,
        )
        receptor_sq.move_to(RIGHT * 0.5 + DOWN * 0.1)
        
        arrow_cam = Arrow(
            surround_rect.get_right() + RIGHT * 0.1,
            receptor_sq.get_left(),                   # ← thay đổi ở đây
            color=GRAY_LIGHT, buff=0.1, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.3,
        )

        receptor_label = Text(
            "1 photoreceptor\n= spatial average",
            font_size=20, color=GRAY_LIGHT, line_spacing=1.3,
        )
        receptor_label.next_to(receptor_sq, RIGHT, buff=0.25)

        self.play(
            Create(arrow_cam, run_time=0.7, rate_func=smooth),
            FadeIn(receptor_sq, scale=0.8, run_time=0.7),
        )
        self.play(Write(receptor_label, run_time=0.8))
        self.wait(0.5)

        # ── Fade grid / receptor to upper area, make room ─────────
        grid_label_group = VGroup(grid_group, surround_rect, arrow_cam, receptor_sq, receptor_label)
        self.play(
            grid_label_group.animate.scale(0.72).to_corner(UL, buff=0.9).shift(DOWN * 0.4),
            run_time=0.9, rate_func=smooth,
        )
        self.wait(0.2)

        # ── 3 design parameters ───────────────────────────────────
        params_title = Text("3 Design Parameters:", font_size=28, color=GRAY_LIGHT, weight=BOLD)
        params_title.move_to(LEFT * 1.0 + UP * 1.1)
        self.play(FadeIn(params_title, shift=UP * 0.2), run_time=0.7)

        # ① Position
        param1_num = Text("①", font_size=28, color=YELLOW_3B1B)
        param1_txt = Text("Position  (x, y, z)", font_size=24, color=GRAY_LIGHT)
        param1 = VGroup(param1_num, param1_txt).arrange(RIGHT, buff=0.15)
        param1.next_to(params_title, DOWN, buff=0.35, aligned_edge=LEFT)

        # Body schematic dot
        body_outline = RoundedRectangle(
            width=0.8, height=1.1, corner_radius=0.12,
            color=GRAY_DIM, stroke_width=1.8, fill_opacity=0,
        )
        body_outline.move_to(RIGHT * 5.5 + ORIGIN)
        pos_dot = Dot(body_outline.get_top() + DOWN * 0.15, radius=0.08, color=YELLOW_3B1B)

        self.play(
            FadeIn(param1, shift=LEFT * 0.2, run_time=0.7),
            Create(body_outline, run_time=0.8),
            FadeIn(pos_dot, run_time=0.5),
        )

        # Animate dot moving to different positions
        for pt in [body_outline.get_left() + RIGHT * 0.05,
                   body_outline.get_bottom() + UP * 0.15,
                   body_outline.get_right() + LEFT * 0.05,
                   body_outline.get_top() + DOWN * 0.15]:
            self.play(pos_dot.animate.move_to(pt), run_time=0.4, rate_func=smooth)
        self.wait(0.2)

        # ② Direction
        param2_num = Text("②", font_size=28, color=ORANGE_3B1B)
        param2_txt = Text("Direction  (azimuth, elevation)", font_size=24, color=GRAY_LIGHT)
        param2 = VGroup(param2_num, param2_txt).arrange(RIGHT, buff=0.15)
        param2.next_to(param1, DOWN, buff=0.28, aligned_edge=LEFT)

        dir_arrow = Arrow(
            body_outline.get_center(),
            body_outline.get_center() + UP * 0.5,
            color=ORANGE_3B1B, buff=0, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.35,
        )
        self.play(
            FadeIn(param2, shift=LEFT * 0.2, run_time=0.7),
            Create(dir_arrow, run_time=0.8),
        )
        # Rotate the arrow through angles
        for angle in [45 * DEGREES, 90 * DEGREES, 135 * DEGREES, 0 * DEGREES]:
            self.play(
                Rotate(dir_arrow, angle=angle - dir_arrow.get_angle(), about_point=body_outline.get_center()),
                run_time=0.45, rate_func=smooth,
            )
        self.wait(0.2)

        # ③ Field of View
        param3_num = Text("③", font_size=28, color=GREEN_3B1B)
        param3_txt = Text("Field of View (cone angle)", font_size=24, color=GRAY_LIGHT)
        param3 = VGroup(param3_num, param3_txt).arrange(RIGHT, buff=0.15)
        param3.next_to(param2, DOWN, buff=0.28, aligned_edge=LEFT)

        fov_sector = Sector(
            radius=0.55, angle=PI / 5,
            start_angle=PI / 2 - PI / 10,
            color=GREEN_3B1B, fill_opacity=0.28, stroke_width=1.5,
        )
        fov_sector.move_to(body_outline.get_center() + UP * 0.1)

        self.play(
            FadeIn(param3, shift=LEFT * 0.2, run_time=0.7),
            FadeIn(fov_sector, scale=0.4, run_time=0.7),
        )
        # Expand and contract
        self.play(
            fov_sector.animate.become(
                Sector(radius=0.7, angle=PI / 2.2,
                       start_angle=PI / 2 - PI / 4.4,
                       color=GREEN_3B1B, fill_opacity=0.22, stroke_width=1.5,
                       ).move_to(body_outline.get_center() + UP * 0.1)
            ),
            run_time=0.7, rate_func=smooth,
        )
        self.play(
            fov_sector.animate.become(
                Sector(radius=0.35, angle=PI / 8,
                       start_angle=PI / 2 - PI / 16,
                       color=GREEN_3B1B, fill_opacity=0.35, stroke_width=1.5,
                       ).move_to(body_outline.get_center() + UP * 0.1)
            ),
            run_time=0.7, rate_func=smooth,
        )
        self.wait(0.3)

        # ── Key insight box ───────────────────────────────────────
        insight_text = Text(
            "The optimizer picks ALL three.\nNot the engineer.",
            font_size=26, color=YELLOW_3B1B, line_spacing=1.35, weight=BOLD,
        )
        insight_box = SurroundingRectangle(
            insight_text, color=YELLOW_3B1B, buff=0.28, stroke_width=2.0,
            corner_radius=0.12,
        )
        insight_group = VGroup(insight_box, insight_text)
        insight_group.to_edge(DOWN, buff=0.45)

        self.play(
            Create(insight_box, run_time=0.9, rate_func=smooth),
            Write(insight_text, run_time=1.1, rate_func=smooth),
        )
        self.wait(0.8)

        # ── Progression: 1 → 4 → 16 photoreceptors ───────────────
        self.play(
            FadeOut(VGroup(
                grid_label_group, params_title, param1, param2, param3,
                body_outline, pos_dot, dir_arrow, fov_sector, insight_group,
            ), run_time=0.8),
        )

        prog_title = Text("Scaling up photoreceptors:", font_size=30, color=GRAY_LIGHT)
        prog_title.to_edge(UP, buff=1.0)
        self.play(FadeIn(prog_title, shift=DOWN * 0.2), run_time=0.7)

        def make_receptor_layout(n_sensors, center, color=TEAL_EP2):
            """Draw n_sensors dots arranged around a robot outline."""
            robot_r = RoundedRectangle(
                width=0.7, height=0.9, corner_radius=0.1,
                color=GRAY_DIM, stroke_width=1.5, fill_opacity=0.1,
            )
            robot_r.move_to(center)
            sensors = VGroup()
            angles = np.linspace(0, 2 * PI, n_sensors, endpoint=False)
            for a in angles:
                d = Dot(
                    center + np.array([np.cos(a) * 0.55, np.sin(a) * 0.65, 0]),
                    radius=0.09, color=color,
                )
                sensors.add(d)
            return VGroup(robot_r, sensors)

        centers = [LEFT * 3.5, ORIGIN, RIGHT * 3.5]
        sensor_counts = [1, 4, 16]
        sensor_labels = ["1 sensor", "4 sensors", "16 sensors"]

        robot_groups = VGroup()
        robot_labels_g = VGroup()

        for i, (ctr, n, lbl) in enumerate(zip(centers, sensor_counts, sensor_labels)):
            rg = make_receptor_layout(n, ctr)
            robot_groups.add(rg)
            rl = Text(lbl, font_size=22, color=GRAY_LIGHT)
            rl.next_to(rg, DOWN, buff=0.25)
            robot_labels_g.add(rl)
            self.play(
                FadeIn(rg, scale=0.85, run_time=0.7, rate_func=smooth),
                FadeIn(rl, run_time=0.5),
            )
            self.wait(0.3)

        # Arrows showing progression
        arr1 = Arrow(robot_groups[0].get_right(), robot_groups[1].get_left(),
                     color=GRAY_MID, buff=0.1, stroke_width=2)
        arr2 = Arrow(robot_groups[1].get_right(), robot_groups[2].get_left(),
                     color=GRAY_MID, buff=0.1, stroke_width=2)
        self.play(
            Create(arr1, run_time=0.5),
            Create(arr2, run_time=0.5),
        )
        self.wait(1.5)

        # ── FadeOut everything ────────────────────────────────────
        all_objects = VGroup(
            title, prog_title, robot_groups, robot_labels_g, arr1, arr2,
        )
        self.play(FadeOut(all_objects, run_time=1.2, rate_func=smooth))
        self.wait(0.2)
