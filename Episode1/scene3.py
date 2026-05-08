"""
SCENE 3 — Cú twist: Sọc ngựa vằn (5:30 – 7:30)
==============================================

Tập 1 — "Cá chết vẫn biết bơi"

Khoảnh khắc "aha" của tập này: trực giác con người đoán SAI vì sao ngựa vằn
có sọc; câu trả lời thật là để đuổi muỗi.

A. Ngựa vằn + câu hỏi "Vì sao có sọc?"
B. Hai đáp án phổ biến: 🦁 camouflage / 🐎 đàn lớn
C. Góc nhìn sư tử: ngựa vằn từ xa = một khối xám mờ (sư tử thị lực ~1/4 người)
D. Zoom muỗi đậu trên sọc → trượt đi (disorientation)
E. Nông dân sơn sọc lên... bò
F. Title card: "ANSWER: MOSQUITOES"
G. VO chốt: trực giác sai vì cơ thể không tiến hoá để ta thấy đẹp

Run:
    manim -pql scene3.py Scene3ZebraTwist
"""

from manim import *
import numpy as np
from common import *


# ────────────────────────────────────────────────────────────────
# Helper: vẽ ngựa vằn schematic
# ────────────────────────────────────────────────────────────────
def create_zebra(stripe_color=GRAY_LIGHT, body_color="#000000",
                 with_stripes=True, scale=1.0):
    """
    Ngựa vằn schematic: thân ellipse + cổ + đầu + 4 chân + đuôi + sọc.
    Trả về VGroup để dễ animate.
    """
    body = Ellipse(width=2.6, height=1.1, color=stripe_color, stroke_width=2.5,
                   fill_color=body_color, fill_opacity=1)
    neck = Polygon(
        [0.9, 0.3, 0], [1.5, 1.0, 0],
        [1.7, 0.95, 0], [1.1, 0.15, 0],
        color=stripe_color, stroke_width=2.5,
        fill_color=body_color, fill_opacity=1,
    )
    head = Ellipse(width=0.9, height=0.55, color=stripe_color, stroke_width=2.5,
                   fill_color=body_color, fill_opacity=1)
    head.move_to([1.85, 1.05, 0]).rotate(-15 * DEGREES)
    eye = Dot([2.0, 1.18, 0], radius=0.05, color=stripe_color)

    leg_fl = Line([0.7, -0.5, 0], [0.7, -1.6, 0], color=stripe_color, stroke_width=4)
    leg_fr = Line([0.4, -0.5, 0], [0.4, -1.6, 0], color=stripe_color, stroke_width=4)
    leg_bl = Line([-0.7, -0.5, 0], [-0.7, -1.6, 0], color=stripe_color, stroke_width=4)
    leg_br = Line([-1.0, -0.5, 0], [-1.0, -1.6, 0], color=stripe_color, stroke_width=4)

    tail = Line([-1.3, 0.1, 0], [-1.7, -0.6, 0], color=stripe_color, stroke_width=2.5)

    parts = VGroup(body, neck, head, eye, leg_fl, leg_fr, leg_bl, leg_br, tail)

    # Sọc — line trắng xếp dọc thân
    stripes = VGroup()
    if with_stripes:
        for x in np.linspace(-1.1, 1.1, 9):
            stripe = Line(
                [x, -0.5, 0], [x, 0.5, 0],
                color=stripe_color, stroke_width=4.5,
            )
            stripes.add(stripe)
        # Sọc cổ
        for i in range(4):
            t = i / 3.0
            x = 1.0 + t * 0.5
            y = 0.3 + t * 0.6
            s = Line(
                [x - 0.05, y - 0.1, 0], [x + 0.1, y + 0.15, 0],
                color=stripe_color, stroke_width=3.5,
            )
            stripes.add(s)

    full = VGroup(parts, stripes)
    full.scale(scale)
    return full


def create_lion_silhouette(scale=1.0):
    """Sư tử minimal silhouette — thân + đầu + đuôi."""
    body = Ellipse(width=2.4, height=0.9, color=ORANGE_3B1B,
                   fill_opacity=0.85, stroke_width=2)
    head = Circle(radius=0.5, color=ORANGE_3B1B,
                  fill_opacity=0.85, stroke_width=2)
    head.move_to([1.5, 0.5, 0])
    # Bờm
    mane = Circle(radius=0.7, color="#B45309",
                  fill_opacity=0.6, stroke_width=0).move_to(head.get_center())
    tail = ArcBetweenPoints([-1.2, 0, 0], [-1.7, 0.7, 0], angle=-PI / 3,
                            color=ORANGE_3B1B, stroke_width=3)
    tail_tip = Dot([-1.7, 0.75, 0], radius=0.08, color="#B45309")
    legs = VGroup(*[
        Line([x, -0.4, 0], [x, -1.2, 0], color=ORANGE_3B1B, stroke_width=3.5)
        for x in [0.6, 0.3, -0.6, -0.9]
    ])
    return VGroup(mane, body, head, tail, tail_tip, legs).scale(scale)


# ────────────────────────────────────────────────────────────────
# Main scene
# ────────────────────────────────────────────────────────────────
class Scene3ZebraTwist(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ============================================================
        # PART A — Ngựa vằn xuất hiện + câu hỏi
        # ============================================================
        zebra = create_zebra(scale=1.4).move_to(DOWN * 0.5)
        ground = Line(LEFT * 7, RIGHT * 7, color=GRAY_DIM, stroke_width=1.5)
        ground.move_to(DOWN * 2.7)

        self.play(Create(ground), run_time=0.5)
        self.play(FadeIn(zebra, shift=UP * 0.3), run_time=1.5)
        self.wait(0.6)

        question = Text(
            "Why do zebras have stripes?",
            font_size=42, color=YELLOW_3B1B, weight=BOLD,
        ).to_edge(UP, buff=0.6)
        self.play(Write(question), run_time=1.2)
        self.wait(2.0)

        # ============================================================
        # PART B — Hai đáp án phổ biến
        # ============================================================
        # Mở khung trắc nghiệm
        guess_box_left = RoundedRectangle(
            width=5.5, height=1.7, corner_radius=0.2,
            color=GRAY_DIM, stroke_width=1.5,
        ).move_to(LEFT * 3.3 + DOWN * 0.5)
        guess_box_right = RoundedRectangle(
            width=5.5, height=1.7, corner_radius=0.2,
            color=GRAY_DIM, stroke_width=1.5,
        ).move_to(RIGHT * 3.3 + DOWN * 0.5)

        # Icon sư tử nhỏ
        lion_icon = create_lion_silhouette(scale=0.35)
        lion_icon.move_to(guess_box_left.get_left() + RIGHT * 0.9)

        zebra_icon = create_zebra(scale=0.35).move_to(
            guess_box_right.get_left() + RIGHT * 0.9 + DOWN * 0.1
        )

        guess_a = Text(
            "A. Camouflage from lions",
            font_size=22, color=GRAY_LIGHT,
        ).next_to(lion_icon, RIGHT, buff=0.4)
        guess_b = Text(
            "B. Appear as a larger herd",
            font_size=22, color=GRAY_LIGHT,
        ).next_to(zebra_icon, RIGHT, buff=0.4)

        # Thu nhỏ ngựa vằn và câu hỏi lên góc trên
        self.play(
            zebra.animate.scale(0.4).move_to(UP * 2.7 + LEFT * 5.5),
            question.animate.scale(0.4).move_to(UP * 2.7 + LEFT * 1.5).set_color(GRAY_LIGHT),
            run_time=1.2,
        )

        self.play(
            Create(guess_box_left), Create(guess_box_right),
            run_time=1.0,
        )
        self.play(
            FadeIn(lion_icon), Write(guess_a),
            FadeIn(zebra_icon), Write(guess_b),
            run_time=1.5,
        )
        self.wait(2.5)

        # ============================================================
        # PART C — Góc nhìn sư tử: ngựa vằn = khối xám mờ
        # ============================================================
        old_layout = VGroup(
            zebra, question, guess_box_left, guess_box_right,
            lion_icon, guess_a, zebra_icon, guess_b, ground,
        )
        self.play(FadeOut(old_layout), run_time=1.0)

        # 2 panel: trái = mắt người, phải = mắt sư tử
        panel_label_human = Text(
            "Human Vision",
            font_size=24, color=GRAY_LIGHT, weight=BOLD,
        ).move_to(LEFT * 3.5 + UP * 3)
        panel_label_lion = Text(
            "Lion Vision  (~1/4 resolution)",
            font_size=24, color=ORANGE_3B1B, weight=BOLD,
        ).move_to(RIGHT * 3.5 + UP * 3)

        # Ngựa vằn ở 2 panel — bản trái nét, bản phải mờ
        zebra_human = create_zebra(scale=0.55).move_to(LEFT * 3.5 + DOWN * 0.3)

        # "Mờ" mô phỏng = giảm số sọc + low-pass, ở đây hack bằng:
        # vẽ ngựa vằn nhưng KHÔNG có sọc (chỉ blob xám)
        zebra_lion_blur = VGroup(
            Ellipse(width=2.6 * 0.55, height=1.1 * 0.55,
                    color=GRAY_MID, fill_opacity=0.7, stroke_width=0),
            Ellipse(width=0.9 * 0.55, height=0.55 * 0.55,
                    color=GRAY_MID, fill_opacity=0.7, stroke_width=0,
                    ).move_to(np.array([1.85 * 0.55, 1.05 * 0.55, 0])).rotate(-15 * DEGREES),
            *[Line([x, -0.5 * 0.55, 0], [x, -1.6 * 0.55, 0],
                   color=GRAY_MID, stroke_width=2.5)
              for x in [0.7 * 0.55, 0.4 * 0.55, -0.7 * 0.55, -1.0 * 0.55]],
        ).move_to(RIGHT * 3.5 + DOWN * 0.3)

        # Halo blur quanh bản phải
        blur_halo = Circle(
            radius=1.6, color=GRAY_MID, fill_opacity=0.15, stroke_width=0,
        ).move_to(zebra_lion_blur.get_center())

        divider = DashedLine(UP * 3.5, DOWN * 3.0,
                             color=GRAY_DIM, stroke_opacity=0.4,
                             dash_length=0.18)

        self.play(Create(divider), run_time=0.5)
        self.play(
            Write(panel_label_human), Write(panel_label_lion),
            run_time=1.0,
        )
        self.play(FadeIn(zebra_human), run_time=1.0)
        self.play(FadeIn(blur_halo), FadeIn(zebra_lion_blur), run_time=1.2)

        # Caption
        cap_left = Text(
            "Stripes clearly visible",
            font_size=20, color=GRAY_LIGHT, slant=ITALIC,
        ).next_to(zebra_human, DOWN, buff=0.4)
        cap_right = Text(
            "A gray blur.\nNo stripes.",
            font_size=20, color=ORANGE_3B1B, slant=ITALIC,
            line_spacing=0.9,
        ).next_to(zebra_lion_blur, DOWN, buff=0.4)

        self.play(FadeIn(cap_left), FadeIn(cap_right), run_time=0.8)
        self.wait(3.0)

        # Punchline
        punch = Text(
            "Except: lions CANNOT see the stripes from hunting distance.",
            font_size=22, color=YELLOW_3B1B, weight=BOLD,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(punch), run_time=1.8)
        self.wait(2.5)

        # Clear
        c_panel = VGroup(
            panel_label_human, panel_label_lion,
            zebra_human, zebra_lion_blur, blur_halo,
            divider, cap_left, cap_right, punch,
        )
        self.play(FadeOut(c_panel), run_time=1.0)

        # ============================================================
        # PART D — Zoom muỗi đậu lên sọc, trượt đi
        # ============================================================
        # Vẽ một mảng sọc to chiếm giữa frame (zoom-in da ngựa)
        skin_stripes = VGroup()
        for x in np.linspace(-5, 5, 14):
            s = Rectangle(
                width=0.35, height=4.2,
                color=GRAY_LIGHT, fill_opacity=0.95, stroke_width=0,
            ).move_to([x, 0, 0])
            skin_stripes.add(s)

        # Khoảng đen giữa các sọc
        skin_bg = Rectangle(
            width=14, height=4.2, color="#000000",
            fill_opacity=1, stroke_width=0,
        ).set_z_index(-1)

        skin_label = Text(
            "Zoom: zebra skin",
            font_size=22, color=YELLOW_3B1B, slant=ITALIC,
        ).to_edge(UP, buff=0.4)

        self.play(FadeIn(skin_bg), run_time=0.5)
        self.play(
            LaggedStart(*[GrowFromCenter(s) for s in skin_stripes], lag_ratio=0.04),
            FadeIn(skin_label),
            run_time=1.5,
        )
        self.wait(0.5)

        # Muỗi: dot nhỏ + 2 cánh
        def make_mosquito(pos):
            body = Dot(pos, radius=0.08, color=RED_BRAIN)
            wing_l = Ellipse(width=0.25, height=0.12,
                             color=GRAY_LIGHT, stroke_width=1,
                             fill_opacity=0.4).next_to(body, UL, buff=0.02)
            wing_r = Ellipse(width=0.25, height=0.12,
                             color=GRAY_LIGHT, stroke_width=1,
                             fill_opacity=0.4).next_to(body, UR, buff=0.02)
            return VGroup(wing_l, wing_r, body)

        mosquito = make_mosquito(np.array([-4, 2.5, 0]))
        self.play(FadeIn(mosquito), run_time=0.5)

        # Bay zigzag + cố đậu xuống — disorientation
        rng = np.random.default_rng(99)
        target_path = [
            np.array([-3, 1.5, 0]),
            np.array([-1.5, 1.0, 0]),
            np.array([0, 0.5, 0]),     # lao xuống
            np.array([0.5, 0.6, 0]),   # bị "trượt" sang ngang
            np.array([1.5, 0.4, 0]),
            np.array([2.5, 1.0, 0]),   # bay lên lại
            np.array([4.0, 2.5, 0]),
        ]
        for pos in target_path:
            self.play(mosquito.animate.move_to(pos),
                      run_time=0.5 + rng.uniform(-0.1, 0.1),
                      rate_func=smooth)

        slip_label = Text(
            "Mosquitoes can't land — stripes confuse their compound eyes",
            font_size=22, color=YELLOW_3B1B, weight=BOLD,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(slip_label), run_time=1.5)
        self.wait(2.5)

        d_pack = VGroup(skin_bg, skin_stripes, skin_label, mosquito, slip_label)
        self.play(FadeOut(d_pack), run_time=1.0)

        # ============================================================
        # PART E — Cú lật bài: nông dân sơn sọc lên BÒ
        # ============================================================
        # Bò: thân, đầu, sừng, vú, 4 chân
        cow_body = Ellipse(width=3.0, height=1.3, color=GRAY_LIGHT,
                           stroke_width=2.5, fill_color="#000000",
                           fill_opacity=1)
        cow_head = Ellipse(width=1.2, height=0.85, color=GRAY_LIGHT,
                           stroke_width=2.5, fill_color="#000000",
                           fill_opacity=1).move_to([1.8, 0.4, 0])
        horn_l = Line([1.7, 0.85, 0], [1.5, 1.2, 0], color=GRAY_LIGHT,
                      stroke_width=3)
        horn_r = Line([2.0, 0.85, 0], [2.2, 1.2, 0], color=GRAY_LIGHT,
                      stroke_width=3)
        cow_legs = VGroup(*[
            Line([x, -0.6, 0], [x, -1.7, 0], color=GRAY_LIGHT, stroke_width=4)
            for x in [1.0, 0.5, -0.7, -1.2]
        ])
        cow_tail = Line([-1.5, 0.2, 0], [-2.0, -0.5, 0],
                        color=GRAY_LIGHT, stroke_width=2.5)
        cow = VGroup(cow_body, cow_head, horn_l, horn_r, cow_legs, cow_tail)
        cow.scale(1.0).move_to(DOWN * 0.4)

        cow_label = Text(
            "Cow.  Ordinary.",
            font_size=24, color=GRAY_LIGHT,
        ).to_edge(UP, buff=0.5)

        self.play(FadeIn(cow), Write(cow_label), run_time=1.5)
        self.wait(1.0)

        # Sơn sọc lên bò
        cow_stripes = VGroup()
        for x in np.linspace(-1.3, 1.3, 9):
            s = Line(
                [x, -0.6, 0], [x, 0.3, 0],
                color=GRAY_LIGHT, stroke_width=4.5,
            )
            cow_stripes.add(s)
        cow_stripes.move_to(cow_body.get_center() + DOWN * 0.0)

        cow_label_2 = Text(
            "Stripe-painted cow.  A real experiment.",
            font_size=24, color=YELLOW_3B1B, weight=BOLD,
        ).to_edge(UP, buff=0.5)

        self.play(Transform(cow_label, cow_label_2), run_time=0.8)
        self.play(
            LaggedStart(*[Create(s) for s in cow_stripes], lag_ratio=0.08),
            run_time=1.5,
        )
        self.wait(1.2)

        # Stat: giảm bệnh do muỗi truyền
        stat_box = RoundedRectangle(
            width=10.0, height=1.4, corner_radius=0.15,
            color=GREEN_3B1B, stroke_width=2,
        ).to_edge(DOWN, buff=0.5)
        stat_text = MarkupText(
            'Stripe-painted farms  →  '
            f'<span foreground="{GREEN_3B1B}"><b>fewer mosquito-borne diseases</b></span>',
            font_size=20, color=GRAY_LIGHT,
        ).move_to(stat_box.get_center())

        self.play(Create(stat_box), Write(stat_text), run_time=1.5)
        self.wait(2.5)

        e_pack = VGroup(cow, cow_stripes, cow_label, stat_box, stat_text)
        self.play(FadeOut(e_pack), run_time=1.0)

        # ============================================================
        # PART F — Title card: "ANSWER: MOSQUITOES"
        # ============================================================
        # Title card EN giữ font mặc định
        answer_title = Text(
            "ANSWER:  MOSQUITOES",
            font_size=56, color=YELLOW_3B1B, weight=BOLD,
        )
        underline = Line(
            answer_title.get_left() + DOWN * 0.5,
            answer_title.get_right() + DOWN * 0.5,
            color=YELLOW_3B1B, stroke_width=2,
        )
        answer_vn = Text(
            "The real answer: not lions, not herd size.",
            font_size=24, color=GRAY_LIGHT, slant=ITALIC,
        ).next_to(underline, DOWN, buff=0.3)

        self.play(Write(answer_title), run_time=1.5)
        self.play(Create(underline), run_time=0.5)
        self.play(FadeIn(answer_vn, shift=UP * 0.15), run_time=0.7)
        self.wait(2.5)

        # ============================================================
        # PART G — VO chốt: trực giác sai
        # ============================================================
        self.play(
            FadeOut(VGroup(answer_title, underline, answer_vn)),
            run_time=0.8,
        )

        moral_l1 = Text(
            "When guessing  «design intelligence»  by human intuition,",
            font_size=26, color=GRAY_LIGHT,
        )
        moral_l2 = Text(
            "we are wrong.",
            font_size=44, color=RED_BRAIN, weight=BOLD,
        )
        moral_l3 = Text(
            "Bodies didn't evolve for  US  to find beautiful.",
            font_size=24, color=GRAY_LIGHT, slant=ITALIC,
        )
        moral_l4 = Text(
            "They evolved to solve the problem they face.",
            font_size=24, color=YELLOW_3B1B, slant=ITALIC,
        )
        moral = VGroup(moral_l1, moral_l2, moral_l3, moral_l4).arrange(DOWN, buff=0.45)

        self.play(Write(moral_l1), run_time=1.5)
        self.play(Write(moral_l2), run_time=0.8)
        self.wait(0.6)
        self.play(Write(moral_l3), run_time=1.2)
        self.play(Write(moral_l4), run_time=1.2)
        self.wait(3.5)

        self.play(FadeOut(moral), run_time=1.5)
        self.wait(0.4)
