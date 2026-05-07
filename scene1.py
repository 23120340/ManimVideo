"""
SCENE 1 — Câu hỏi chính (0:35 – 2:00)
=====================================

Tập 1 — "Cá chết vẫn biết bơi"
Series: "Trí tuệ nằm trong cơ thể" (3Blue1Brown style)

Hiện thực hoá Scene 1 trong kịch bản:
  A. Cá schematic + highlight BRAIN (đỏ) / BODY (xanh)
  B. Não fade out (cá chết) — thân vẫn quẫy
  C. Sweep aside — chuyển cảnh
  D. Split 2 pane: θ_brain (NN, "fast, flexible") | θ_body (cá + params, "slow, rigid")
  E. NN flicker (não thay đổi nhanh); body params chỉ pulse nhẹ (cứng)
  F. Đóng: θ = (θ_brain, θ_body) — cả hai đều là tham số

Lệnh chạy (xem README ở cuối):
    manim -pql scene1.py Scene1MainQuestion        # preview 480p, nhanh
    manim -pqh scene1.py Scene1MainQuestion        # 1080p, chất lượng cao

File này không phụ thuộc LaTeX (dùng MarkupText cho subscript)
và không cần file SVG ngoài (cá vẽ bằng primitives).
"""

from manim import *
import numpy as np


# ────────────────────────────────────────────────────────────────
# Bảng màu 3Blue1Brown (theo kịch bản 0.3)
# ────────────────────────────────────────────────────────────────
BG_COLOR    = "#1C1C1C"
BLUE_3B1B   = "#3B82F6"
YELLOW_3B1B = "#FBBF24"
RED_BRAIN   = "#EF4444"
GRAY_LIGHT  = "#E5E7EB"
GRAY_DIM    = "#6B7280"


# ────────────────────────────────────────────────────────────────
# Helpers — vẽ cá và mạng nơ-ron bằng primitives (không cần SVG)
# ────────────────────────────────────────────────────────────────
def create_fish(color=BLUE_3B1B, stroke_width=3):
    """
    Cá schematic, đầu hướng phải, đuôi hướng trái.
    Trả về VGroup theo thứ tự: [0] thân, [1] đuôi, [2] mắt, [3] vây lưng.
    """
    body = Ellipse(
        width=3.0, height=1.1,
        color=color, stroke_width=stroke_width,
    )
    tail = Polygon(
        [-1.45, 0, 0],
        [-2.30, 0.7, 0],
        [-2.00, 0, 0],
        [-2.30, -0.7, 0],
        color=color, stroke_width=stroke_width,
    )
    eye = Dot([1.0, 0.18, 0], radius=0.07, color=color)
    fin = ArcBetweenPoints(
        [0.2, 0.5, 0],
        [-0.7, 0.5, 0],
        angle=-PI / 2,
        color=color, stroke_width=stroke_width,
    )
    return VGroup(body, tail, eye, fin)


def create_neural_net(
    layer_sizes,
    radius=0.13, h_buff=0.55, v_buff=0.32,
    node_color=BLUE_3B1B, edge_color=GRAY_DIM,
):
    """Mạng MLP đơn giản; trả về (group_đầy_đủ, edges_VGroup, list_các_layer)."""
    layers = []
    for n in layer_sizes:
        layer = VGroup(*[
            Circle(radius=radius, color=node_color,
                   stroke_width=2, fill_opacity=0.25)
            for _ in range(n)
        ])
        layer.arrange(DOWN, buff=v_buff)
        layers.append(layer)

    nodes = VGroup(*layers).arrange(RIGHT, buff=h_buff)

    edges = VGroup()
    for i in range(len(layers) - 1):
        for n1 in layers[i]:
            for n2 in layers[i + 1]:
                edges.add(Line(
                    n1.get_right(), n2.get_left(),
                    stroke_width=1, color=edge_color, stroke_opacity=0.55,
                ))

    return VGroup(edges, nodes), edges, layers


# ────────────────────────────────────────────────────────────────
# Scene chính
# ────────────────────────────────────────────────────────────────
class Scene1MainQuestion(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ============================================================
        # PART A — Cá + nhãn BRAIN/BODY
        # VO: "Khi nói về trí tuệ nhân tạo, ta thường mặc định:
        #      trí tuệ nằm trong 'não' — trong mạng nơ-ron, trong các
        #      tham số được học. Cơ thể chỉ là phần cứng để chạy nó."
        # ============================================================
        fish = create_fish(color=GRAY_LIGHT).scale(1.4).move_to(ORIGIN)
        self.play(Create(fish), run_time=1.8)
        self.wait(0.5)

        # Highlight BRAIN (đầu — bên phải con cá)
        brain_glow = Circle(
            radius=0.55, color=RED_BRAIN,
            fill_opacity=0.45, stroke_width=2,
        ).move_to(fish[2].get_center())  # ngay tại con mắt

        brain_label = Text(
            "BRAIN", font_size=28, color=RED_BRAIN, weight=BOLD,
        ).next_to(brain_glow, UR, buff=0.45)
        brain_arrow = Line(
            brain_label.get_corner(DL) + DL * 0.05,
            brain_glow.get_top() + UR * 0.05,
            color=RED_BRAIN, stroke_width=2,
        )

        # Highlight BODY (thân — bên trái và giữa con cá)
        body_glow = Ellipse(
            width=2.4, height=1.0,
            color=BLUE_3B1B, fill_opacity=0.35, stroke_width=2,
        ).move_to(fish[0].get_center() + LEFT * 0.3)

        body_label = Text(
            "BODY", font_size=28, color=BLUE_3B1B, weight=BOLD,
        ).next_to(body_glow, DOWN, buff=0.6)
        body_arrow = Line(
            body_label.get_top() + UP * 0.05,
            body_glow.get_bottom() + DOWN * 0.05,
            color=BLUE_3B1B, stroke_width=2,
        )

        self.play(
            FadeIn(brain_glow),
            Create(brain_arrow),
            Write(brain_label),
            run_time=1.4,
        )
        self.wait(0.7)
        self.play(
            FadeIn(body_glow),
            Create(body_arrow),
            Write(body_label),
            run_time=1.4,
        )
        self.wait(3.0)

        # ============================================================
        # PART B — Não tắt (FadeOut). Thân vẫn quẫy theo dòng.
        # VO: "Nhưng con cá này không có não nữa.
        #      Nếu nó vẫn 'biết' bơi, thì kiến thức đó đang nằm ở đâu?"
        # ============================================================
        self.play(
            FadeOut(brain_glow),
            FadeOut(brain_arrow),
            brain_label.animate.set_color(GRAY_DIM).set_opacity(0.35),
            run_time=2.0,
        )

        # Body wiggle: dao động ngang nhẹ — gợi cảm giác bị dòng nước cuốn
        body_pack = VGroup(body_glow, body_arrow, body_label)
        for shift_dir in [RIGHT * 0.22, LEFT * 0.44, RIGHT * 0.44, LEFT * 0.22]:
            self.play(
                body_pack.animate.shift(shift_dir),
                run_time=0.7, rate_func=smooth,
            )
        self.wait(1.2)

        # ============================================================
        # PART C — Sweep aside, chuẩn bị split 2 pane
        # ============================================================
        old_stuff = VGroup(fish, brain_label, body_pack)
        self.play(FadeOut(old_stuff), run_time=1.2)
        self.wait(0.3)

        # ============================================================
        # PART D — Hai pane song song
        # Trái: θ_brain (mạng nơ-ron), nhãn "fast, flexible"
        # Phải: θ_body (đường viền cá + điểm vật lý), nhãn "slow, rigid"
        # ============================================================
        # ── Pane TRÁI ──
        nn_group, nn_edges, _ = create_neural_net(
            layer_sizes=[3, 5, 5, 2],
            radius=0.13, h_buff=0.55, v_buff=0.32,
            node_color=BLUE_3B1B,
        )
        nn_group.scale(0.85).move_to(LEFT * 3.6 + DOWN * 0.4)

        theta_brain = MarkupText(
            'θ<sub>brain</sub>', font_size=44, color=YELLOW_3B1B,
        ).next_to(nn_group, UP, buff=0.5)

        fast_label = Text(
            "fast, flexible",
            font_size=24, color=GRAY_LIGHT, slant=ITALIC,
        ).next_to(nn_group, DOWN, buff=0.5)

        # ── Pane PHẢI ──
        body_outline = create_fish(color=BLUE_3B1B)
        body_outline.scale(0.85).move_to(RIGHT * 3.6 + DOWN * 0.4)

        # Các điểm tham số vật lý (độ cứng, đàn hồi…) rải trên thân cá
        body_center = body_outline[0].get_center()
        param_offsets = [
            LEFT * 0.6 + UP * 0.18,
            LEFT * 0.15 + DOWN * 0.05,
            RIGHT * 0.45 + DOWN * 0.18,
            RIGHT * 0.85 + UP * 0.10,
            LEFT * 1.0 + DOWN * 0.12,
        ]
        param_dots = VGroup(*[
            Dot(body_center + off, radius=0.08, color=YELLOW_3B1B)
            for off in param_offsets
        ])

        theta_body = MarkupText(
            'θ<sub>body</sub>', font_size=44, color=YELLOW_3B1B,
        ).next_to(body_outline, UP, buff=0.5)
        theta_body.align_to(theta_brain, UP)

        slow_label = Text(
            "slow, rigid",
            font_size=24, color=GRAY_LIGHT, slant=ITALIC,
        ).next_to(body_outline, DOWN, buff=0.5)
        slow_label.align_to(fast_label, UP)

        # Vạch chia giữa 2 pane
        divider = DashedLine(
            UP * 3.0, DOWN * 3.0,
            color=GRAY_DIM, stroke_opacity=0.45, dash_length=0.18,
        )

        # Build pane trái
        self.play(Create(divider), run_time=0.8)
        self.play(
            Create(nn_group),
            Write(theta_brain),
            run_time=2.0,
        )
        self.play(FadeIn(fast_label, shift=UP * 0.15), run_time=0.7)
        self.wait(0.5)

        # Build pane phải
        self.play(
            Create(body_outline),
            Write(theta_body),
            run_time=2.0,
        )
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in param_dots],
                        lag_ratio=0.18),
            run_time=1.4,
        )
        self.play(FadeIn(slow_label, shift=UP * 0.15), run_time=0.7)
        self.wait(2.0)

        # ============================================================
        # PART E — Tốc độ thay đổi khác nhau
        # Trái: trọng số NN nhấp nháy liên tục (não học)
        # Phải: gần như đứng yên — chỉ pulse rất nhẹ (thân cứng)
        # VO: "Não thay đổi mỗi giây — học từ phản hồi của môi trường.
        #      Cơ thể thay đổi qua hàng triệu năm tiến hoá."
        # ============================================================
        rng = np.random.default_rng(42)
        for _ in range(8):
            idxs = rng.choice(len(nn_edges), size=8, replace=False)
            flashing = [nn_edges[i] for i in idxs]
            self.play(
                *[e.animate.set_stroke(YELLOW_3B1B, width=2.6, opacity=1.0)
                  for e in flashing],
                run_time=0.16, rate_func=rush_into,
            )
            self.play(
                *[e.animate.set_stroke(GRAY_DIM, width=1, opacity=0.55)
                  for e in flashing],
                run_time=0.16, rate_func=rush_from,
            )

        # Bên phải chỉ pulse một nhịp rất nhẹ — gợi "rigid"
        self.play(
            *[d.animate.scale(1.25) for d in param_dots],
            run_time=0.5,
        )
        self.play(
            *[d.animate.scale(1 / 1.25) for d in param_dots],
            run_time=0.5,
        )
        self.wait(2.0)

        # ============================================================
        # PART F — Đóng: cả hai đều là tham số
        # VO: "Cả hai bên đều là tham số.
        #      Và lâu nay, hầu hết công sức nghiên cứu AI dồn vào bên trái."
        # ============================================================
        unifying = MarkupText(
            'θ = (θ<sub>brain</sub>, θ<sub>body</sub>)',
            font_size=46, color=GRAY_LIGHT,
        ).to_edge(UP, buff=0.5)

        box = SurroundingRectangle(
            unifying, color=YELLOW_3B1B,
            buff=0.25, stroke_width=2, stroke_opacity=0.85,
        )

        self.play(Write(unifying), run_time=1.8)
        self.play(Create(box), run_time=1.0)

        caption = Text(
            "tham số  —  cả hai đều có thể tối ưu",
            font_size=22, color=YELLOW_3B1B, slant=ITALIC,
        ).next_to(box, DOWN, buff=0.3)
        self.play(FadeIn(caption, shift=UP * 0.15), run_time=0.8)
        self.wait(3.0)

        # Cliffhanger fade — kết thúc Scene 1
        everything = VGroup(
            divider, nn_group, theta_brain, fast_label,
            body_outline, theta_body, slow_label, param_dots,
            unifying, box, caption,
        )
        self.play(FadeOut(everything), run_time=1.5)
        self.wait(0.5)
