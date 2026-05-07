"""
SCENE 7 — Outro & ghi chú nhân vật (17:00 – cuối)
==================================================

Tập 1 — "Cá chết vẫn biết bơi"

A. Title card "Thanks to" + danh sách nguồn gốc tutorial
B. Patreon shoutout / link tutorial gốc
C. Logo channel + outro nhỏ

Lưu ý:
- Tên các nhà nghiên cứu trong kịch bản gốc cần kiểm tra lại
  trước khi public (Andre Cazenave Souto, Andy Spielberg, Sönke Johnsen).
- Đây là placeholder — thay bằng credit thực khi đã xác nhận.

Run:
    manim -pql scene7.py Scene7Outro
"""

from manim import *
from common import *


class Scene7Outro(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ============================================================
        # PART A — "Thanks to" + danh sách
        # ============================================================
        thanks_header = vn(
            "Cảm ơn",
            font_size=48, color=YELLOW_3B1B, weight=BOLD,
        ).to_edge(UP, buff=0.8)
        thanks_sub = Text(
            "Thanks to",
            font_size=22, color=GRAY_DIM, slant=ITALIC,
        ).next_to(thanks_header, DOWN, buff=0.15)

        # Danh sách credit — placeholder
        credits = [
            ("Amir Zamir",      "Stanford / EPFL"),
            ("Andre Cazenave Souto", "Photoreceptor optimization"),
            ("Andy Spielberg",  "Differentiable simulation"),
            ("Sönke Johnsen",   "Visual ecology"),
        ]

        cred_group = VGroup()
        for name, role in credits:
            name_text = Text(
                name, font_size=24, color=GRAY_LIGHT, weight=BOLD,
            )
            role_text = Text(
                role, font_size=18, color=GRAY_DIM, slant=ITALIC,
            )
            row = VGroup(name_text, role_text).arrange(RIGHT, buff=0.5)
            cred_group.add(row)
        cred_group.arrange(DOWN, buff=0.35).move_to(ORIGIN)

        based_on = vn_markup(
            'Tập video dựa trên tutorial:  '
            f'<span foreground="{YELLOW_3B1B}"><i>'
            'Computational Design of Diverse Morphologies and Sensors '
            'for Vision and Robotics</i></span>',
            font_size=18, color=GRAY_LIGHT,
        ).to_edge(DOWN, buff=1.0)

        # Animate
        self.play(Write(thanks_header), run_time=1.2)
        self.play(FadeIn(thanks_sub), run_time=0.5)
        self.wait(0.5)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cred_group],
                        lag_ratio=0.25),
            run_time=2.5,
        )
        self.wait(2.0)
        self.play(Write(based_on), run_time=1.5)
        self.wait(3.0)

        all_a = VGroup(thanks_header, thanks_sub, cred_group, based_on)
        self.play(FadeOut(all_a), run_time=1.2)

        # ============================================================
        # PART B — Patreon shoutout
        # ============================================================
        patreon_title = vn(
            "Cảm ơn các Patreon đã ủng hộ",
            font_size=36, color=YELLOW_3B1B, weight=BOLD,
        ).to_edge(UP, buff=1.0)

        # 3 cột tên giả lập (placeholder)
        patreon_names_left = [
            "Nguyễn Anh", "Trần Bình", "Phạm Châu",
            "Đỗ Dương", "Lê Em", "Vũ Phúc",
        ]
        patreon_names_mid = [
            "Hoàng Giang", "Đinh Hà", "Bùi Khánh",
            "Phan Linh", "Trịnh Minh", "Đặng Nam",
        ]
        patreon_names_right = [
            "Lý Oanh", "Mai Phương", "Tạ Quang",
            "Ngô Sơn", "Hồ Thanh", "Cao Vy",
        ]

        def make_column(names):
            col = VGroup(*[
                vn(n, font_size=18, color=GRAY_LIGHT) for n in names
            ])
            return col.arrange(DOWN, buff=0.18, aligned_edge=LEFT)

        col_l = make_column(patreon_names_left).move_to(LEFT * 4 + DOWN * 0.3)
        col_m = make_column(patreon_names_mid).move_to(DOWN * 0.3)
        col_r = make_column(patreon_names_right).move_to(RIGHT * 4 + DOWN * 0.3)

        self.play(Write(patreon_title), run_time=1.0)
        self.play(
            LaggedStart(
                LaggedStart(*[FadeIn(n) for n in col_l], lag_ratio=0.05),
                LaggedStart(*[FadeIn(n) for n in col_m], lag_ratio=0.05),
                LaggedStart(*[FadeIn(n) for n in col_r], lag_ratio=0.05),
                lag_ratio=0.3,
            ),
            run_time=3.0,
        )
        self.wait(1.5)

        join = vn(
            "Tham gia tại:  patreon.com/trituetrongcothe",
            font_size=20, color=YELLOW_3B1B, slant=ITALIC,
        ).to_edge(DOWN, buff=0.8)
        self.play(Write(join), run_time=1.2)
        self.wait(2.5)

        all_b = VGroup(patreon_title, col_l, col_m, col_r, join)
        self.play(FadeOut(all_b), run_time=1.2)

        # ============================================================
        # PART C — Logo channel + outro
        # ============================================================
        # "Logo" tự vẽ: 3 vòng tròn lồng nhau (nhái style 3b1b pi creature
        # nhưng trừu tượng) + chữ kênh
        logo_outer = Circle(radius=1.0, color=YELLOW_3B1B, stroke_width=3)
        logo_mid = Circle(radius=0.65, color=BLUE_3B1B, stroke_width=2.5)
        logo_inner = Circle(radius=0.3, color=GRAY_LIGHT,
                           stroke_width=2, fill_opacity=0.3)
        logo = VGroup(logo_outer, logo_mid, logo_inner).move_to(UP * 0.8)

        channel_name = vn(
            "Trí tuệ nằm trong cơ thể",
            font_size=32, color=YELLOW_3B1B, weight=BOLD,
        ).next_to(logo, DOWN, buff=0.5)

        tagline = vn(
            "Khám phá toán học của thiết kế cơ thể.",
            font_size=20, color=GRAY_LIGHT, slant=ITALIC,
        ).next_to(channel_name, DOWN, buff=0.3)

        self.play(
            Create(logo_outer), Create(logo_mid), Create(logo_inner),
            run_time=1.5,
        )
        self.play(Write(channel_name), run_time=1.0)
        self.play(FadeIn(tagline, shift=UP * 0.15), run_time=0.7)
        self.wait(1.5)

        # Slow rotate logo
        self.play(
            Rotate(logo_mid, angle=PI, rate_func=linear),
            Rotate(logo_outer, angle=-PI / 2, rate_func=linear),
            run_time=3.0,
        )
        self.wait(1.0)

        end_text = vn(
            "Hẹn gặp lại ở tập sau.",
            font_size=24, color=GRAY_LIGHT,
        ).to_edge(DOWN, buff=0.8)
        self.play(Write(end_text), run_time=1.2)
        self.wait(2.5)

        # Fade tất cả
        self.play(
            FadeOut(VGroup(logo, channel_name, tagline, end_text)),
            run_time=2.0,
        )
        self.wait(0.4)
