"""
common.py — Shared assets cho series "Trí tuệ nằm trong cơ thể"
================================================================

Chứa:
  • Bảng màu 3Blue1Brown style
  • Font Montserrat (set default cho cả Text và MarkupText)
  • Helpers: create_fish(), create_neural_net()

Mọi file scene trong series import từ đây.
"""

from manim import *
import numpy as np


# ────────────────────────────────────────────────────────────────
# Bảng màu (theo kịch bản 0.3)
# ────────────────────────────────────────────────────────────────
BG_COLOR    = "#1C1C1C"
BLUE_3B1B   = "#3B82F6"
YELLOW_3B1B = "#FBBF24"
RED_BRAIN   = "#EF4444"
GREEN_3B1B  = "#10B981"
PURPLE_3B1B = "#A78BFA"
ORANGE_3B1B = "#F97316"
PINK_3B1B   = "#EC4899"
GRAY_LIGHT  = "#E5E7EB"
GRAY_MID    = "#9CA3AF"
GRAY_DIM    = "#6B7280"
GRAY_DARKER = "#374151"


# ────────────────────────────────────────────────────────────────
# Font Việt — Montserrat (CHỈ áp dụng cho text tiếng Việt)
# ────────────────────────────────────────────────────────────────
# Montserrat có Vietnamese subset đầy đủ: ă/â/ê/ô/ơ/ư + dấu thanh + đ.
# Text tiếng Anh giữ font mặc định của Manim (Sans) cho đồng nhất với
# style toán học của 3Blue1Brown.
#
# Dùng:  vn("Trí tuệ nằm trong cơ thể", font_size=44, ...)
# Thay vì:  Text("Trí tuệ nằm trong cơ thể", font="Montserrat", ...)
VN_FONT = "Montserrat"


def vn(text, **kwargs):
    """Tạo Text tiếng Việt với font Montserrat.

    Tự gán font="Montserrat" nếu caller chưa truyền.
    Mọi tham số khác giống Text() của Manim.
    """
    kwargs.setdefault("font", VN_FONT)
    return Text(text, **kwargs)


def vn_markup(text, **kwargs):
    """MarkupText tiếng Việt với font Montserrat.

    Dùng khi cần inline markup (subscript, color span) trong text VN.
    """
    kwargs.setdefault("font", VN_FONT)
    return MarkupText(text, **kwargs)


# ────────────────────────────────────────────────────────────────
# Helper: cá schematic
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
        [0.2, 0.5, 0], [-0.7, 0.5, 0],
        angle=-PI / 2,
        color=color, stroke_width=stroke_width,
    )
    return VGroup(body, tail, eye, fin)


# ────────────────────────────────────────────────────────────────
# Helper: mạng nơ-ron schematic
# ────────────────────────────────────────────────────────────────
def create_neural_net(
    layer_sizes,
    radius=0.13, h_buff=0.55, v_buff=0.32,
    node_color=BLUE_3B1B, edge_color=GRAY_DIM,
):
    """Tiny MLP. Returns: (full_group, edges_VGroup, layers_list)"""
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
# Helper: title card chuẩn (dùng ở Scene 0, 5, 7)
# ────────────────────────────────────────────────────────────────
def make_title_card(title, subtitle=None, title_color=YELLOW_3B1B,
                    is_vietnamese=True):
    """Title card kiểu 3Blue1Brown — title to + subtitle italic.

    is_vietnamese=True (mặc định) sẽ dùng font Montserrat.
    """
    text_fn = vn if is_vietnamese else Text
    title_text = text_fn(title, font_size=56, color=title_color, weight=BOLD)
    if subtitle:
        sub_text = text_fn(subtitle, font_size=28, color=GRAY_LIGHT, slant=ITALIC)
        return VGroup(title_text, sub_text).arrange(DOWN, buff=0.4)
    return title_text
