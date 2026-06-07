"""
SCENE 6 — Setup cho Tập 2 (13:00 – 17:00)
=========================================

Tập 1 — "Cá chết vẫn biết bơi"

A. Quay lại sơ đồ θ_brain | θ_body từ Scene 1
B. θ_body tách thành: shape, eye position, eye resolution, FOV, sensor count
C. Pixel reduction: 128 → 64 → 32 → 16 → 8 → 4 → 2 → 1
D. Câu hỏi cliffhanger: "Một robot 4 pixel có thể điều hướng trong nhà không?"
E. End card: "Ep. 2: Seeing the world with 4 pixels"

Run:
    manim -pql scene6.py Scene6Cliffhanger
"""

from manim import *
import numpy as np
from common import *


def make_pixelated_view(grid_size, target_pos, target_color=PINK_3B1B,
                       view_size=2.5):
    """
    Mô phỏng "robot nhìn thấy gì" ở độ phân giải grid_size x grid_size.
    target_pos: vị trí mục tiêu trong khung view (-1..1, -1..1).
    Trả về VGroup các Square biểu diễn pixel.
    """
    pixels = VGroup()
    cell = view_size / grid_size

    # Background pixel (nền sáng giả lập "phòng")
    rng = np.random.default_rng(7)

    for i in range(grid_size):
        for j in range(grid_size):
            # Toạ độ trong [-1, 1]
            nx = (j + 0.5) / grid_size * 2 - 1
            ny = 1 - (i + 0.5) / grid_size * 2

            # Khoảng cách đến target (hình tròn bán kính 0.4)
            dx, dy = nx - target_pos[0], ny - target_pos[1]
            dist = np.sqrt(dx * dx + dy * dy)

            if dist < 0.4:
                # Pixel có target
                t = max(0, 1 - dist / 0.4)
                color = target_color
                opacity = 0.4 + 0.5 * t
            else:
                # Nền — ngẫu nhiên xám nhạt
                color = GRAY_DARKER
                opacity = 0.15 + rng.uniform(0, 0.15)

            sq = Square(
                side_length=cell * 0.95,
                color=color, fill_color=color,
                fill_opacity=opacity, stroke_width=0.5,
                stroke_color=GRAY_DIM, stroke_opacity=0.3,
            )
            sq.move_to([
                -view_size / 2 + (j + 0.5) * cell,
                view_size / 2 - (i + 0.5) * cell,
                0,
            ])
            pixels.add(sq)

    # Khung viền
    border = Square(side_length=view_size, color=GRAY_LIGHT, stroke_width=2)
    return VGroup(pixels, border)


class Scene6Cliffhanger(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ============================================================
        # PART A — Recap split θ_brain | θ_body
        # ============================================================
        # Bên trái: NN
        nn_group, _, _ = create_neural_net(
            layer_sizes=[3, 5, 5, 2],
            radius=0.13, h_buff=0.55, v_buff=0.32,
            node_color=BLUE_3B1B,
        )
        nn_group.scale(0.75).move_to(LEFT * 4 + DOWN * 0.3)
        theta_brain = MathTex(
            r"\theta_{\mathrm{brain}}", font_size=36, color=YELLOW_3B1B,
        ).next_to(nn_group, UP, buff=0.4)

        # Bên phải: cá
        body_outline = create_fish(color=BLUE_3B1B).scale(0.75)
        body_outline.move_to(RIGHT * 4 + DOWN * 0.3)
        body_center = body_outline[0].get_center()
        body_dots = VGroup(*[
            Dot(body_center + off, radius=0.08, color=YELLOW_3B1B)
            for off in [
                LEFT * 0.5 + UP * 0.18,
                LEFT * 0.1 + DOWN * 0.05,
                RIGHT * 0.4 + DOWN * 0.18,
                RIGHT * 0.7 + UP * 0.10,
                LEFT * 0.85 + DOWN * 0.12,
            ]
        ])
        theta_body = MathTex(
            r"\theta_{\mathrm{body}}", font_size=36, color=YELLOW_3B1B,
        ).next_to(body_outline, UP, buff=0.4)
        theta_body.align_to(theta_brain, UP)

        divider = DashedLine(UP * 3, DOWN * 3,
                             color=GRAY_DIM, stroke_opacity=0.4,
                             dash_length=0.18)

        recap_title = Text(
            "Back to the start: two parameter sets",
            font_size=26, color=GRAY_LIGHT, weight=BOLD,
        ).to_edge(UP, buff=0.5)

        self.play(Write(recap_title), run_time=0.8)
        self.play(Create(divider), run_time=0.5)
        self.play(
            Create(nn_group), Write(theta_brain),
            run_time=1.2,
        )
        self.play(
            Create(body_outline), Write(theta_body),
            LaggedStart(*[GrowFromCenter(d) for d in body_dots], lag_ratio=0.1),
            run_time=1.5,
        )
        self.wait(2.0)

        # ============================================================
        # PART B — θ_body tách thành nhiều thành phần
        # ============================================================
        # Highlight bên phải, fade bên trái
        left_pack = VGroup(nn_group, theta_brain, divider)
        self.play(
            left_pack.animate.set_opacity(0.2),
            run_time=0.8,
        )

        # Move θ_body group ra giữa-trái, list components ở phải
        right_pack = VGroup(body_outline, theta_body, body_dots)
        self.play(
            right_pack.animate.scale(0.85).move_to(LEFT * 3 + DOWN * 0.5),
            run_time=1.0,
        )

        components = [
            "shape",
            "eye position",
            "eye resolution",
            "field of view",
            "sensor count",
        ]

        comp_group = VGroup()
        for i, label in enumerate(components):
            y = 2.2 - i * 0.95
            box = RoundedRectangle(
                width=4.8, height=0.7, corner_radius=0.1,
                color=BLUE_3B1B, stroke_width=1.5,
                fill_opacity=0.1,
            ).move_to([3, y, 0])
            en_text = Text(
                label, font_size=20, color=BLUE_3B1B, weight=BOLD,
            ).move_to(box.get_center())
            comp_group.add(VGroup(box, en_text))

        # Mũi tên từ θ_body → mỗi component
        arrows_to_comp = VGroup()
        for comp_box_group in comp_group:
            box = comp_box_group[0]
            a = Arrow(
                theta_body.get_right() + RIGHT * 0.1,
                box.get_left() + LEFT * 0.05,
                color=GRAY_DIM, stroke_width=1.5, buff=0,
                max_tip_length_to_length_ratio=0.06,
                stroke_opacity=0.6,
            )
            arrows_to_comp.add(a)

        self.play(
            LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in comp_group],
                        lag_ratio=0.18),
            run_time=2.5,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows_to_comp], lag_ratio=0.1),
            run_time=1.5,
        )
        self.wait(2.0)

        # Câu hỏi đầu tiên: tối ưu MẮT trước
        first_q = Text(
            "First question: optimize the  EYE.",
            font_size=26, color=YELLOW_3B1B, weight=BOLD,
        ).to_edge(DOWN, buff=0.4)

        # Highlight 3 thành phần liên quan đến mắt
        eye_highlights = VGroup()
        for i in [1, 2, 3, 4]:  # eye position, resolution, FOV, sensor count
            box = comp_group[i][0]
            h = SurroundingRectangle(
                box, color=emphasis_color_of(box), stroke_width=2.5,
                buff=0.05,
            )
            eye_highlights.add(h)

        self.play(
            Write(first_q),
            LaggedStart(*[Create(h) for h in eye_highlights], lag_ratio=0.15),
            run_time=2.0,
        )
        self.wait(2.5)

        # Clear A+B
        ab_pack = VGroup(
            recap_title, left_pack, right_pack,
            comp_group, arrows_to_comp, first_q, eye_highlights,
        )
        self.play(FadeOut(ab_pack), run_time=1.0)

        # ============================================================
        # PART C — Pixel reduction: 128 → 1
        # ============================================================
        section_title = Text(
            "Nature doesn't use high-resolution cameras.",
            font_size=28, color=GRAY_LIGHT, weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Write(section_title), run_time=1.0)

        # Mục tiêu: bóng hồng ở vị trí (0.3, 0.2)
        target_pos = np.array([0.3, 0.2])

        resolutions = [128, 64, 32, 16, 8, 4, 2, 1]
        # Để render nhanh, dùng max grid_size ảo hoá:
        # Manim render 128*128 = 16k squares sẽ rất chậm, nên cap ở 64
        # và dùng "visual approximation" cho 128.
        display_resolutions = [64, 32, 16, 8, 4, 2, 1]
        labels_text = ["~128 px", "64 px", "32 px", "16 px",
                       "8 px", "4 px", "2 px", "1 px"]

        # Hiển thị view 128 đầu tiên (giả với 64)
        view = make_pixelated_view(64, target_pos, view_size=4.0)
        view.move_to(ORIGIN)

        res_label = Text(
            labels_text[0], font_size=42, color=YELLOW_3B1B, weight=BOLD,
        ).next_to(view, RIGHT, buff=0.7)

        question_below = Text(
            "Can it still  see  the target?",
            font_size=22, color=GRAY_LIGHT, slant=ITALIC,
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(view), Write(res_label), run_time=1.2)
        self.play(FadeIn(question_below, shift=UP * 0.15), run_time=0.8)
        self.wait(1.5)

        # Lặp giảm độ phân giải
        for new_grid, lbl in zip(display_resolutions, labels_text[1:]):
            new_view = make_pixelated_view(new_grid, target_pos, view_size=4.0)
            new_view.move_to(ORIGIN)
            new_label = Text(
                lbl, font_size=42, color=YELLOW_3B1B, weight=BOLD,
            ).next_to(new_view, RIGHT, buff=0.7)

            self.play(
                Transform(view, new_view),
                Transform(res_label, new_label),
                run_time=0.8,
            )
            self.wait(0.6)

        # Dừng ở 1 pixel — dramatic pause
        self.wait(1.5)

        # Quay lại 4 pixel cho cliffhanger
        view_4 = make_pixelated_view(4, target_pos, view_size=4.0)
        view_4.move_to(ORIGIN)
        label_4 = Text(
            "4 px",
            font_size=64, color=YELLOW_3B1B, weight=BOLD,
        ).next_to(view_4, RIGHT, buff=0.7)

        self.play(
            Transform(view, view_4),
            Transform(res_label, label_4),
            run_time=1.2,
        )
        self.wait(1.5)

        # ============================================================
        # PART D — Câu hỏi cliffhanger
        # ============================================================
        self.play(
            FadeOut(VGroup(section_title, question_below, res_label)),
            view.animate.scale(0.7).shift(LEFT * 2.5),
            run_time=1.0,
        )

        cliff_l1 = Text(
            "Can a robot with",
            font_size=36, color=GRAY_LIGHT,
        )
        cliff_l2 = Text(
            "4 pixels",
            font_size=72, color=YELLOW_3B1B, weight=BOLD,
        )
        cliff_l3 = Text(
            "navigate indoors?",
            font_size=32, color=GRAY_LIGHT,
        )
        cliff_group = VGroup(cliff_l1, cliff_l2, cliff_l3).arrange(DOWN, buff=0.3)
        cliff_group.move_to(RIGHT * 2.5 + UP * 0.3)

        self.play(Write(cliff_l1), run_time=0.8)
        self.play(Write(cliff_l2), run_time=1.2)
        self.play(Write(cliff_l3), run_time=1.0)
        self.wait(3.0)

        # ============================================================
        # PART E — End card cho tập 2
        # ============================================================
        self.play(
            FadeOut(VGroup(view, cliff_group)),
            run_time=1.2,
        )

        ep2_title = Text(
            "Episode 2", font_size=32, color=GRAY_DIM, slant=ITALIC,
        )
        ep2_main = Text(
            "Seeing the world with 4 pixels",
            font_size=52, color=YELLOW_3B1B, weight=BOLD,
        )
        ep2_en = Text(
            "Coming soon.",
            font_size=22, color=GRAY_LIGHT, slant=ITALIC,
        )
        end_card = VGroup(ep2_title, ep2_main, ep2_en).arrange(DOWN, buff=0.4)
        end_card.move_to(ORIGIN)

        ec_box = SurroundingRectangle(
            end_card, color=YELLOW_3B1B, buff=0.6,
            stroke_width=2, stroke_opacity=0.8,
        )

        self.play(Write(ep2_title), run_time=0.6)
        self.play(Write(ep2_main), run_time=1.5)
        self.play(FadeIn(ep2_en, shift=UP * 0.15), run_time=0.6)
        self.play(Create(ec_box), run_time=0.7)
        self.wait(2.8)

        self.play(FadeOut(VGroup(end_card, ec_box)),
                  run_time=1.5)
        self.wait(0.4)
