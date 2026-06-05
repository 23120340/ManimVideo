"""
SCENE 0 — Cold open: Con cá chết (0:00 – 0:35)
==============================================

Tập 1 — "Cá chết vẫn biết bơi"

VO:
> Đây là một con cá đang bơi.
> [pause 2s]
> Nhưng có một chi tiết khiến đoạn video này trở nên kỳ lạ:
> [camera lùi]
> Con cá đã chết. Một sợi dây giữ đầu nó cố định, và dòng nước đang chảy.
> Tất cả những gì bạn thấy — cái đuôi quẫy, cơ thể uốn lượn — chỉ là tương
> tác giữa một xác cá và dòng nước. Vậy mà nó vẫn bơi.

Lưu ý production:
- Bản hoàn thiện nên dùng stock footage cá thật + Transform sang phiên bản
  schematic. File này dùng schematic stand-in từ đầu đến cuối.
- Camera pull-back dùng `MovingCameraScene` (CE) tương đương `self.frame` của Grant.

Run:
    manim -pql scene0.py Scene0ColdOpen
"""

from manim import *
import numpy as np
from common import *


class Scene0ColdOpen(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ============================================================
        # PART A — Cá đang "bơi" (5 giây đầu)
        # ============================================================
        fish = create_fish(color=GRAY_LIGHT, stroke_width=3)
        fish.scale(1.2).move_to(ORIGIN)

        self.play(FadeIn(fish), run_time=1.0)

        # Quẫy đuôi: rotate phần tail quanh điểm gắn vào thân
        # (tail.get_right() = điểm gần thân nhất của đuôi)
        tail_pivot = fish[1].get_right()
        for angle in [-15, 30, -30, 30, -30, 15]:
            self.play(
                fish[1].animate.rotate(angle * DEGREES, about_point=tail_pivot),
                run_time=0.32, rate_func=smooth,
            )
        self.wait(0.8)

        # ============================================================
        # PART B — Camera pull-back, lộ ra sợi dây + dòng nước
        # ============================================================
        # Pull camera back để rộng tầm nhìn
        self.play(
            self.camera.frame.animate.scale(2.3),
            run_time=2.5, rate_func=smooth,
        )

        # Sợi dây móc vào miệng cá, không trỏ vào mắt.
        rope_start = fish[0].get_right() + LEFT * 0.08 + DOWN * 0.04
        rope_end = RIGHT * 6 + UP * 4.5
        rope = Line(rope_start, rope_end, color=GRAY_LIGHT, stroke_width=2.5)
        anchor = Dot(rope_end, color=GRAY_LIGHT, radius=0.12)

        self.play(
            Create(rope, rate_func=rush_into),
            FadeIn(anchor),
            run_time=1.5,
        )
        self.wait(0.5)

        # Dòng nước chảy ngược (right → left), thể hiện bằng arrows
        flow_arrows = VGroup()
        rng = np.random.default_rng(7)
        for y in np.linspace(-5, 5, 10):
            for x_start in np.linspace(-7, 7, 7):
                # Bỏ qua arrow trùng vị trí cá
                if abs(y) < 1.2 and abs(x_start) < 2.5:
                    continue
                arrow = Arrow(
                    start=[x_start + 0.5, y + rng.uniform(-0.1, 0.1), 0],
                    end=[x_start - 0.5, y + rng.uniform(-0.1, 0.1), 0],
                    color=BLUE_3B1B, stroke_width=2,
                    max_tip_length_to_length_ratio=0.35,
                    buff=0,
                ).set_opacity(0.45)
                flow_arrows.add(arrow)

        self.play(
            LaggedStart(*[GrowArrow(a) for a in flow_arrows], lag_ratio=0.015),
            run_time=2.5,
        )
        self.wait(2.0)

        # ============================================================
        # PART C — Nhãn lộ sự thật: "Con cá đã chết."
        # ============================================================
        reveal = Text(
            "The fish is dead.",
            font_size=42, color=RED_BRAIN, weight=BOLD,
        )
        reveal.move_to(self.camera.frame.get_center() + DOWN * 5.0)

        self.play(Write(reveal), run_time=1.5)

        # X eye — dead fish indicator
        eye_c = fish[2].get_center()
        arm = 0.20
        dead_eye = VGroup(
            Line(eye_c + np.array([-arm,  arm, 0]), eye_c + np.array([ arm, -arm, 0]),
                 color=RED_BRAIN, stroke_width=3),
            Line(eye_c + np.array([ arm,  arm, 0]), eye_c + np.array([-arm, -arm, 0]),
                 color=RED_BRAIN, stroke_width=3),
        )
        self.play(Create(dead_eye), run_time=0.5)
        self.wait(2.0)

        # Highlight đuôi — vẫn đang quẫy mặc dù cá đã chết
        tail_circle = Circle(
            radius=0.7, color=YELLOW_3B1B,
            stroke_width=2.5, fill_opacity=0.15,
        ).move_to(fish[1].get_center())
        tail_label = Text(
            "still moving", font_size=24, color=YELLOW_3B1B, slant=ITALIC,
        ).next_to(tail_circle, DOWN, buff=0.4)

        self.play(
            Create(tail_circle),
            FadeIn(tail_label, shift=UP * 0.15),
            run_time=1.2,
        )
        # Quẫy thêm vài lần để emphasize
        for angle in [-25, 50, -50, 25]:
            self.play(
                fish[1].animate.rotate(angle * DEGREES, about_point=tail_pivot),
                run_time=0.3, rate_func=smooth,
            )
        self.wait(2.0)

        # ============================================================
        # PART D — Title card transition
        # ============================================================
        all_old = VGroup(
            fish, rope, anchor, flow_arrows,
            reveal, tail_circle, tail_label, dead_eye,
        )
        self.play(FadeOut(all_old), run_time=1.5)

        title = Text(
            "Intelligence in the Body",
            font_size=56, color=YELLOW_3B1B, weight=BOLD,
        )
        subtitle = Text(
            "Ep. 1  ·  The Dead Fish That Swims",
            font_size=28, color=GRAY_LIGHT, slant=ITALIC,
        )
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.4)
        title_group.move_to(self.camera.frame.get_center())

        self.play(Write(title), run_time=2.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)
        self.wait(2.5)

        self.play(FadeOut(title_group), run_time=1.5)
        self.wait(0.4)
