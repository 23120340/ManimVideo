"""
SCENE 4 — Định nghĩa toán học của bài toán (7:30 – 11:00)
=========================================================

Tập 1 — "Cá chết vẫn biết bơi"

Phần "math heart" của tập này. Chuyển từ wonder sang math.

A. Side-by-side: Design space θ | Performance space U(θ)
B. Đường cong U(θ) 1D — con trỏ trượt, đỉnh = thiết kế tối ưu
C. Phương trình θ* = arg max U(θ)
D. Pipeline: θ → simulator → controller → reward → U(θ)
E. Phân nhánh: Physics-based (Newton) vs Learning-based (NN)

Run:
    manim -pql scene4.py Scene4MathFormulation
"""

from manim import *
import numpy as np
from common import *


class Scene4MathFormulation(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # Intro
        intro = Text(
            "Formalizing the problem in math",
            font_size=40, color=GRAY_LIGHT, weight=BOLD,
        )
        self.play(Write(intro), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(intro), run_time=0.8)

        # ============================================================
        # PART A — Hai không gian song song
        # ============================================================
        # Pane TRÁI: Design space θ — vẽ một grid 2D với vài chấm đại diện thiết kế
        ds_axes = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1],
            x_length=4.5, y_length=3.0,
            background_line_style={
                "stroke_color": GRAY_DARKER, "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            axis_config={"stroke_color": GRAY_DIM, "stroke_width": 1.5},
        ).move_to(LEFT * 3.5 + DOWN * 0.3)

        ds_label = MarkupText(
            'Design Space  θ',
            font_size=26, color=BLUE_3B1B, weight=BOLD,
        ).next_to(ds_axes, UP, buff=0.4)

        # Vài chấm = thiết kế cụ thể
        rng = np.random.default_rng(3)
        ds_dots = VGroup(*[
            Dot(ds_axes.coords_to_point(*p), radius=0.07, color=BLUE_3B1B)
            for p in rng.uniform([-2.5, -1.7], [2.5, 1.7], size=(8, 2))
        ])

        ds_caption = Text(
            "each point = one body design",
            font_size=18, color=GRAY_LIGHT, slant=ITALIC,
        ).next_to(ds_axes, DOWN, buff=0.3)

        # Pane PHẢI: Performance space U
        ps_axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 1, 0.25],
            x_length=4.5, y_length=3.0,
            axis_config={"stroke_color": GRAY_DIM, "stroke_width": 1.5},
        ).move_to(RIGHT * 3.5 + DOWN * 0.3)

        ps_label = MarkupText(
            'Utility Function  U(θ)',
            font_size=26, color=YELLOW_3B1B, weight=BOLD,
        ).next_to(ps_axes, UP, buff=0.4)

        # U(θ) — đường cong có 1 đỉnh (Gaussian-like)
        u_curve = ps_axes.plot(
            lambda x: 0.85 * np.exp(-((x - 3.0) ** 2) / 1.2) + 0.05,
            x_range=[0, 5],
            color=YELLOW_3B1B, stroke_width=3,
        )

        ps_caption = Text(
            'each point = a score  ("survival rate")',
            font_size=18, color=GRAY_LIGHT, slant=ITALIC,
        ).next_to(ps_axes, DOWN, buff=0.3)

        divider = DashedLine(UP * 3, DOWN * 3,
                             color=GRAY_DIM, stroke_opacity=0.4,
                             dash_length=0.18)

        self.play(Create(divider), run_time=0.6)
        self.play(
            Create(ds_axes), Write(ds_label),
            run_time=1.2,
        )
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in ds_dots], lag_ratio=0.1),
            FadeIn(ds_caption),
            run_time=1.3,
        )
        self.wait(0.5)
        self.play(
            Create(ps_axes), Write(ps_label),
            run_time=1.2,
        )
        self.play(Create(u_curve), FadeIn(ps_caption), run_time=1.5)
        self.wait(2.5)

        # ============================================================
        # PART B — Con trỏ trượt trên ds, U sáng theo
        # ============================================================
        # Tracker để map từ x_design → x_axes
        x_tracker = ValueTracker(0.5)

        # Marker trên design space (chạy ngang ở y=0)
        ds_marker = always_redraw(lambda: Dot(
            ds_axes.coords_to_point(x_tracker.get_value() * 1.0 - 2.5, 0),
            radius=0.12, color=ORANGE_3B1B,
        ))

        # Marker trên performance space (chạy theo curve)
        ps_marker = always_redraw(lambda: Dot(
            ps_axes.coords_to_point(
                x_tracker.get_value(),
                0.85 * np.exp(-((x_tracker.get_value() - 3.0) ** 2) / 1.2) + 0.05,
            ),
            radius=0.12, color=ORANGE_3B1B,
        ))

        # Đường nét đứt nối 2 marker — biểu diễn ánh xạ θ → U(θ)
        connector = always_redraw(lambda: DashedLine(
            ds_marker.get_center(), ps_marker.get_center(),
            color=ORANGE_3B1B, stroke_opacity=0.5,
            dash_length=0.12, stroke_width=1.5,
        ))

        self.add(ds_marker, ps_marker, connector)

        # Trượt từ 0.5 → 5
        self.play(x_tracker.animate.set_value(5.0),
                  run_time=2.5, rate_func=linear)
        self.play(x_tracker.animate.set_value(0.3),
                  run_time=2.0, rate_func=linear)
        # Dừng ở đỉnh
        self.play(x_tracker.animate.set_value(3.0),
                  run_time=1.5, rate_func=smooth)
        self.wait(0.8)

        # Highlight đỉnh = thiết kế tối ưu
        peak_circle = Circle(
            radius=0.25, color=GREEN_3B1B, stroke_width=2.5,
        ).move_to(ps_marker.get_center())
        peak_label = MarkupText(
            'θ*  =  optimal design',
            font_size=22, color=GREEN_3B1B, weight=BOLD,
        ).next_to(peak_circle, UP, buff=0.2)

        self.play(Create(peak_circle), Write(peak_label), run_time=1.2)
        self.wait(2.0)

        # ============================================================
        # PART C — Phương trình tối ưu
        # ============================================================
        # Clear marker dynamic
        self.remove(ds_marker, ps_marker, connector)
        # Để giữ vị trí ds/ps marker hiện tại như "snapshot"
        snap_ds = Dot(ds_axes.coords_to_point(0.5, 0),
                      radius=0.12, color=ORANGE_3B1B)
        snap_ps = Dot(ps_marker.get_center(), radius=0.12, color=ORANGE_3B1B)

        # Phương trình to ở giữa
        eq = MarkupText(
            'θ*  =  arg max  U(θ)',
            font_size=44, color=GRAY_LIGHT,
        )
        eq.move_to(UP * 2.7)
        sub_theta = MarkupText('θ', font_size=22, color=GRAY_LIGHT)
        sub_theta.next_to(eq, DOWN, buff=0).shift(LEFT * 1.05 + UP * 0.55)

        eq_box = SurroundingRectangle(
            VGroup(eq, sub_theta), color=YELLOW_3B1B,
            buff=0.25, stroke_width=2, stroke_opacity=0.85,
        )

        self.play(
            FadeOut(VGroup(ds_dots, ds_caption, ps_caption,
                           peak_circle, peak_label)),
            FadeIn(snap_ds), FadeIn(snap_ps),
            run_time=0.6,
        )
        self.play(Write(eq), FadeIn(sub_theta), run_time=1.5)
        self.play(Create(eq_box), run_time=0.7)
        self.wait(1.5)

        # Vấn đề: U không có công thức đóng
        catch = Text(
            "Problem: U(θ) has no closed-form expression.",
            font_size=24, color=RED_BRAIN, weight=BOLD,
        ).to_edge(DOWN, buff=0.4)
        catch_2 = Text(
            "We must simulate the body in an environment to evaluate U.",
            font_size=20, color=GRAY_LIGHT, slant=ITALIC,
        ).next_to(catch, UP, buff=0.2)

        self.play(Write(catch), run_time=1.2)
        self.play(FadeIn(catch_2, shift=UP * 0.15), run_time=0.8)
        self.wait(2.5)

        # Clear toàn bộ part A-C
        all_abc = VGroup(
            ds_axes, ds_label, ps_axes, ps_label, u_curve, divider,
            snap_ds, snap_ps, eq, sub_theta, eq_box, catch, catch_2,
        )
        self.play(FadeOut(all_abc), run_time=1.0)

        # ============================================================
        # PART D — Pipeline: θ → simulator → controller → reward → U
        # ============================================================
        nodes_label = ["θ", "Simulator", "Controller", "Reward", "U(θ)"]
        nodes_color = [BLUE_3B1B, GRAY_LIGHT, RED_BRAIN, GREEN_3B1B, YELLOW_3B1B]
        node_group = VGroup()
        positions = []
        for i, (lbl, col) in enumerate(zip(nodes_label, nodes_color)):
            x = -5.5 + i * 2.75
            box = RoundedRectangle(
                width=2.0, height=1.0, corner_radius=0.15,
                color=col, stroke_width=2.5, fill_opacity=0.15,
            ).move_to([x, 0, 0])
            text = MarkupText(lbl, font_size=22, color=col)
            text.move_to(box.get_center())
            node_group.add(VGroup(box, text))
            positions.append([x, 0, 0])

        # Mũi tên giữa các node
        arrows = VGroup()
        for i in range(len(nodes_label) - 1):
            a = Arrow(
                np.array(positions[i]) + RIGHT * 1.05,
                np.array(positions[i + 1]) + LEFT * 1.05,
                color=GRAY_LIGHT, stroke_width=2.5, buff=0,
                max_tip_length_to_length_ratio=0.15,
            )
            arrows.add(a)

        pipeline_title = Text(
            "Pipeline for evaluating U(θ)",
            font_size=28, color=GRAY_LIGHT, weight=BOLD,
        ).to_edge(UP, buff=0.6)

        self.play(Write(pipeline_title), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in node_group],
                        lag_ratio=0.2),
            run_time=2.0,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15),
            run_time=1.2,
        )

        # Pulse "data flow" qua từng node
        for _ in range(2):
            for node in node_group:
                self.play(
                    node[0].animate.set_stroke(width=4.5).set_fill(opacity=0.4),
                    run_time=0.18,
                )
                self.play(
                    node[0].animate.set_stroke(width=2.5).set_fill(opacity=0.15),
                    run_time=0.18,
                )

        self.wait(2.0)

        # Caption nhỏ ở dưới
        pipe_cap = Text(
            "Each new design θ = re-run the entire pipeline.",
            font_size=20, color=YELLOW_3B1B, slant=ITALIC,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(pipe_cap), run_time=1.2)
        self.wait(2.5)

        d_pack = VGroup(pipeline_title, node_group, arrows, pipe_cap)
        self.play(FadeOut(d_pack), run_time=1.0)

        # ============================================================
        # PART E — Phân nhánh 2 trường phái
        # ============================================================
        branch_title = Text(
            "Two approaches to this problem:",
            font_size=30, color=GRAY_LIGHT, weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Write(branch_title), run_time=1.0)

        # Trái: Physics-based
        phys_box = RoundedRectangle(
            width=5.5, height=4.5, corner_radius=0.2,
            color=BLUE_3B1B, stroke_width=2,
        ).move_to(LEFT * 3.5 + DOWN * 0.3)

        phys_title = Text(
            "Physics-based", font_size=28, color=BLUE_3B1B, weight=BOLD,
        ).move_to(phys_box.get_top() + DOWN * 0.5)

        # Newton equation
        newton = MarkupText(
            'F  =  m · a',
            font_size=32, color=GRAY_LIGHT,
        ).move_to(phys_box.get_center() + UP * 0.6)

        # Sơ đồ lò xo + khối
        spring_y = phys_box.get_center()[1] - 0.4
        wall_x = phys_box.get_center()[0] - 2.2
        block_x = phys_box.get_center()[0] + 0.8

        wall = Line([wall_x, spring_y - 0.4, 0], [wall_x, spring_y + 0.4, 0],
                    color=GRAY_LIGHT, stroke_width=3)
        wall_hatch = VGroup(*[
            Line([wall_x - 0.15, spring_y + 0.4 - i * 0.2, 0],
                 [wall_x, spring_y + 0.3 - i * 0.2, 0],
                 color=GRAY_LIGHT, stroke_width=1)
            for i in range(5)
        ])

        n_zig = 8
        block_offset = ValueTracker(0)

        def make_spring():
            offset = block_offset.get_value()
            current_block_x = block_x + offset
            pts = [[wall_x, spring_y, 0]]
            for i in range(n_zig):
                x = wall_x + (current_block_x - wall_x) * (i + 1) / (n_zig + 1)
                y = spring_y + (0.18 if i % 2 == 0 else -0.18)
                pts.append([x, y, 0])
            pts.append([current_block_x, spring_y, 0])
            s = VMobject(color=GRAY_LIGHT, stroke_width=2)
            s.set_points_as_corners(pts)
            return s

        spring = always_redraw(make_spring)

        block = always_redraw(lambda: Square(
            side_length=0.6, color=BLUE_3B1B,
            fill_opacity=0.4, stroke_width=2,
        ).move_to([block_x + 0.3 + block_offset.get_value(), spring_y, 0]))

        phys_caption = Text(
            "know physics  →  write model  →  optimize",
            font_size=18, color=GRAY_LIGHT, slant=ITALIC,
        ).move_to(phys_box.get_bottom() + UP * 0.4)

        # Phải: Learning-based
        learn_box = RoundedRectangle(
            width=5.5, height=4.5, corner_radius=0.2,
            color=PURPLE_3B1B, stroke_width=2,
        ).move_to(RIGHT * 3.5 + DOWN * 0.3)

        learn_title = Text(
            "Learning-based", font_size=28, color=PURPLE_3B1B, weight=BOLD,
        ).move_to(learn_box.get_top() + DOWN * 0.5)

        # Mạng nơ-ron nhỏ: input (eye) → NN → output (action)
        nn_grp, _, _ = create_neural_net(
            layer_sizes=[3, 4, 4, 2],
            radius=0.10, h_buff=0.4, v_buff=0.27,
            node_color=PURPLE_3B1B,
        )
        nn_grp.scale(0.7).move_to(learn_box.get_center() + UP * 0.3)

        # Input/output icons
        input_icon = Text("eye", font_size=16, color=GRAY_LIGHT)
        input_icon.next_to(nn_grp, LEFT, buff=0.25)
        output_icon = Text("action", font_size=16, color=GRAY_LIGHT)
        output_icon.next_to(nn_grp, RIGHT, buff=0.25)

        learn_caption = Text(
            "no formula  →  learn from data",
            font_size=18, color=GRAY_LIGHT, slant=ITALIC,
        ).move_to(learn_box.get_bottom() + UP * 0.4)

        # Build cả hai bên
        self.play(
            Create(phys_box), Create(learn_box),
            run_time=1.0,
        )
        self.play(
            Write(phys_title), Write(learn_title),
            run_time=0.8,
        )
        self.play(
            Write(newton),
            Create(nn_grp),
            run_time=1.5,
        )
        self.play(
            Create(wall), Create(wall_hatch), Create(spring), FadeIn(block),
            FadeIn(input_icon), FadeIn(output_icon),
            run_time=1.5,
        )
        self.play(
            FadeIn(phys_caption, shift=UP * 0.1),
            FadeIn(learn_caption, shift=UP * 0.1),
            run_time=0.8,
        )

        # Block dao động trong physics pane (gợi simulation đang chạy)
        # Xóa vòng for cũ, thay bằng:
        for shift_amt in [0.2, -0.4, 0.4, -0.2]:
            self.play(
                block_offset.animate.increment_value(shift_amt),
                run_time=0.4, rate_func=smooth,
            )

        self.wait(2.0)

        # Kết: visual cơ thể đi nhánh trái, mắt → hành vi đi nhánh phải
        bridge = MarkupText(
            'Body (rigid)  →  <span foreground="' + BLUE_3B1B + '">left</span>  ·  '
            'Eye → behavior  →  <span foreground="' + PURPLE_3B1B + '">right</span>',
            font_size=22, color=GRAY_LIGHT,
        ).to_edge(DOWN, buff=0.3)

        self.play(Write(bridge), run_time=1.5)
        self.wait(3.0)

        # Detach always_redraw mobjects before FadeOut — otherwise they
        # keep getting redrawn at full opacity each frame and the fade flickers.
        self.remove(spring, block)

        all_e = VGroup(
            branch_title, phys_box, learn_box,
            phys_title, learn_title, newton,
            wall, wall_hatch,
            nn_grp, input_icon, output_icon,
            phys_caption, learn_caption, bridge,
        )
        self.play(FadeOut(all_e), run_time=1.5)
        self.wait(0.4)
