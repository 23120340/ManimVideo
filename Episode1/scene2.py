"""
SCENE 2 — Sự đa dạng kinh ngạc của mắt sinh học (2:00 – 5:30)
=============================================================

Tập 1 — "Cá chết vẫn biết bơi"

6 thẻ (cards) lần lượt trượt vào, mỗi thẻ ~25s,
kết thúc bằng grid 2×3 recap.

Card 1 — Mèo vs dê (đồng tử dọc vs ngang)
Card 2 — Đại bàng có 2 fovea
Card 3 — Sò điệp 200 con mắt (gương, không thấu kính)
Card 4 — Cá hang động: tiến hoá xoá mắt
Card 5 — Tarsier: mắt to bằng cả não
Card 6 — Bướm: nhìn nhau mờ, hoa văn dành cho chim

Run:
    manim -pql scene2.py Scene2EyeDiversity
    manim -pql scene2.py Scene2EyeDiversity -n 0,5    # chỉ Card 1
"""

from manim import *
import numpy as np
from common import *


# ────────────────────────────────────────────────────────────────
# Helpers nội bộ scene
# ────────────────────────────────────────────────────────────────
def make_card_header(card_num, total, title_vn):
    """Header cho card: '01 / 06' (số) trên + title VN to ở giữa."""
    counter = Text(
        f"{card_num:02d} / {total:02d}",
        font_size=18, color=GRAY_DIM,
    )
    title_text = Text(
        title_vn, font_size=38, color=YELLOW_3B1B, weight=BOLD,
    )
    header = VGroup(counter, title_text).arrange(DOWN, buff=0.2)
    header.to_edge(UP, buff=0.5)
    return header, counter, title_text


def make_eye(pupil_shape="round", iris_color=GRAY_LIGHT, scale=1.0):
    """Vẽ mắt với đồng tử khác hình. shape: round | vertical | horizontal."""
    sclera = Ellipse(
        width=2.4 * scale, height=1.4 * scale,
        color=GRAY_LIGHT, stroke_width=2, fill_opacity=0.05,
    )
    iris = Circle(
        radius=0.55 * scale, color=iris_color,
        stroke_width=2, fill_opacity=0.4,
    )
    if pupil_shape == "vertical":
        pupil = Ellipse(
            width=0.18 * scale, height=0.85 * scale,
            color=BLACK, fill_opacity=1, stroke_width=0,
        )
    elif pupil_shape == "horizontal":
        pupil = Ellipse(
            width=0.95 * scale, height=0.22 * scale,
            color=BLACK, fill_opacity=1, stroke_width=0,
        )
    else:
        pupil = Circle(
            radius=0.18 * scale, color=BLACK,
            fill_opacity=1, stroke_width=0,
        )
    return VGroup(sclera, iris, pupil)


# ────────────────────────────────────────────────────────────────
# Main scene
# ────────────────────────────────────────────────────────────────
class Scene2EyeDiversity(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        intro = Text(
            "The Astonishing Diversity of Biological Eyes",
            font_size=36, color=GRAY_LIGHT, weight=BOLD,
        )
        self.play(Write(intro), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(intro), run_time=0.8)

        thumbs = []
        thumbs.append(self.card_1_cat_vs_goat())
        thumbs.append(self.card_2_eagle_fovea())
        thumbs.append(self.card_3_scallop())
        thumbs.append(self.card_4_cave_fish())
        thumbs.append(self.card_5_tarsier())
        thumbs.append(self.card_6_butterfly())

        self.play_recap_grid(thumbs)

    # ------------------------------------------------------------
    # Card 1 — Mèo vs dê
    # ------------------------------------------------------------
    def card_1_cat_vs_goat(self):
        header, _, _ = make_card_header(1, 6, "Cat  vs  Goat")
        self.play(Write(header), run_time=0.8)

        cat_eye = make_eye("vertical", iris_color=ORANGE_3B1B, scale=1.2)
        cat_eye.move_to(LEFT * 3.5 + UP * 0.3)
        cat_label = Text("Cat", font_size=26, color=GRAY_LIGHT)
        cat_label.next_to(cat_eye, DOWN, buff=0.5)

        goat_eye = make_eye("horizontal", iris_color=YELLOW_3B1B, scale=1.2)
        goat_eye.move_to(RIGHT * 3.5 + UP * 0.3)
        goat_label = Text("Goat", font_size=26, color=GRAY_LIGHT)
        goat_label.next_to(goat_eye, DOWN, buff=0.5)

        self.play(FadeIn(cat_eye, shift=RIGHT * 0.3), Write(cat_label), run_time=1.0)
        self.play(FadeIn(goat_eye, shift=LEFT * 0.3), Write(goat_label), run_time=1.0)
        self.wait(0.8)

        # FOV cones
        cat_fov = Sector(
            radius=1.5, angle=50 * DEGREES,
            start_angle=-25 * DEGREES,
            color=ORANGE_3B1B, fill_opacity=0.2, stroke_width=1,
        ).move_arc_center_to(cat_eye.get_center())

        goat_fov = Sector(
            radius=1.5, angle=170 * DEGREES,
            start_angle=-85 * DEGREES,
            color=YELLOW_3B1B, fill_opacity=0.2, stroke_width=1,
        ).move_arc_center_to(goat_eye.get_center())

        self.play(FadeIn(cat_fov), FadeIn(goat_fov), run_time=1.2)

        cat_stat = Text(
            "predator · depth perception",
            font_size=20, color=ORANGE_3B1B, slant=ITALIC,
        ).next_to(cat_label, DOWN, buff=0.5)
        goat_stat = Text(
            "prey · ~330° field of view",
            font_size=20, color=YELLOW_3B1B, slant=ITALIC,
        ).next_to(goat_label, DOWN, buff=0.5)

        self.play(
            FadeIn(cat_stat, shift=UP * 0.15),
            FadeIn(goat_stat, shift=UP * 0.15),
            run_time=0.8,
        )
        self.wait(2.5)

        card_group = VGroup(
            header, cat_eye, cat_label, cat_fov, cat_stat,
            goat_eye, goat_label, goat_fov, goat_stat,
        )
        thumb = card_group.copy()
        self.play(FadeOut(card_group), run_time=0.8)
        return thumb

    # ------------------------------------------------------------
    # Card 2 — Đại bàng 2 fovea
    # ------------------------------------------------------------
    def card_2_eagle_fovea(self):
        header, _, _ = make_card_header(2, 6, "Eagle  ·  2 foveae")
        self.play(Write(header), run_time=0.8)

        # Người
        human_retina = Arc(
            radius=2.0, angle=PI, start_angle=0,
            color=GRAY_LIGHT, stroke_width=3,
        ).move_to(LEFT * 3.5 + DOWN * 0.4)
        human_fovea = Dot(
            human_retina.point_from_proportion(0.5),
            radius=0.12, color=YELLOW_3B1B,
        )
        human_label = Text("Human", font_size=24, color=GRAY_LIGHT)
        human_label.next_to(human_retina, DOWN, buff=0.5)
        # "1 fovea" - mix VN+EN, dùng Text() cho an toàn
        human_count = Text(
            "1 fovea", font_size=20, color=YELLOW_3B1B, slant=ITALIC,
        ).next_to(human_label, DOWN, buff=0.2)

        self.play(Create(human_retina), run_time=0.8)
        self.play(GrowFromCenter(human_fovea), Write(human_label), run_time=0.7)
        self.play(FadeIn(human_count), run_time=0.5)

        # Đại bàng
        eagle_retina = Arc(
            radius=2.0, angle=PI, start_angle=0,
            color=GRAY_LIGHT, stroke_width=3,
        ).move_to(RIGHT * 3.5 + DOWN * 0.4)
        eagle_fov_1 = Dot(
            eagle_retina.point_from_proportion(0.35),
            radius=0.12, color=YELLOW_3B1B,
        )
        eagle_fov_2 = Dot(
            eagle_retina.point_from_proportion(0.65),
            radius=0.12, color=YELLOW_3B1B,
        )
        eagle_label = Text("Eagle", font_size=24, color=GRAY_LIGHT)
        eagle_label.next_to(eagle_retina, DOWN, buff=0.5)
        eagle_count = Text(
            "2 fovea  →  spiral hunting",
            font_size=20, color=YELLOW_3B1B, slant=ITALIC,
        ).next_to(eagle_label, DOWN, buff=0.2)

        self.play(Create(eagle_retina), run_time=0.8)
        self.play(
            GrowFromCenter(eagle_fov_1), GrowFromCenter(eagle_fov_2),
            Write(eagle_label), run_time=0.8,
        )
        self.play(FadeIn(eagle_count), run_time=0.5)

        # Tia high-res
        center = eagle_retina.get_center()
        ray1 = DashedLine(
            eagle_fov_1.get_center(),
            center + UR * 2.5,
            color=YELLOW_3B1B, stroke_opacity=0.5,
            dash_length=0.1, stroke_width=1.5,
        )
        ray2 = DashedLine(
            eagle_fov_2.get_center(),
            center + UL * 2.5,
            color=YELLOW_3B1B, stroke_opacity=0.5,
            dash_length=0.1, stroke_width=1.5,
        )
        self.play(Create(ray1), Create(ray2), run_time=1.0)

        # Spiral
        spiral = ParametricFunction(
            lambda t: np.array([
                0.4 * np.exp(0.15 * t) * np.cos(t),
                0.4 * np.exp(0.15 * t) * np.sin(t),
                0,
            ]),
            t_range=[0, 4 * PI],
            color=ORANGE_3B1B, stroke_width=2,
        )
        spiral.scale(0.4).move_to(UP * 1.8)
        spiral_label = Text(
            "Hunting trajectory: logarithmic spiral",
            font_size=20, color=ORANGE_3B1B, slant=ITALIC,
        ).next_to(spiral, RIGHT, buff=0.4)

        self.play(Create(spiral), run_time=1.5)
        self.play(FadeIn(spiral_label, shift=LEFT * 0.2), run_time=0.6)
        self.wait(2.5)

        card_group = VGroup(
            header,
            human_retina, human_fovea, human_label, human_count,
            eagle_retina, eagle_fov_1, eagle_fov_2, eagle_label, eagle_count,
            ray1, ray2, spiral, spiral_label,
        )
        thumb = card_group.copy()
        self.play(FadeOut(card_group), run_time=0.8)
        return thumb

    # ------------------------------------------------------------
    # Card 3 — Sò điệp 200 mắt
    # ------------------------------------------------------------
    def card_3_scallop(self):
        header, _, _ = make_card_header(3, 6, "Scallop  ·  ~200 eyes")
        self.play(Write(header), run_time=0.8)

        # Vỏ sò
        shell = ArcBetweenPoints(
            LEFT * 2.5, RIGHT * 2.5, angle=-PI * 0.7,
            color=GRAY_LIGHT, stroke_width=3,
        )
        shell_top = Line(LEFT * 2.5, RIGHT * 2.5, color=GRAY_LIGHT, stroke_width=3)
        shell_group = VGroup(shell, shell_top).move_to(DOWN * 0.5)

        center = np.array([0, -0.5, 0])

        # Khía radial
        ridges = VGroup()
        for angle in np.linspace(-PI * 0.85, -PI * 0.15, 10):
            r1, r2 = 1.0, 2.4
            p1 = center + np.array([r1 * np.cos(angle), r1 * np.sin(angle), 0])
            p2 = center + np.array([r2 * np.cos(angle), r2 * np.sin(angle), 0])
            ridges.add(Line(p1, p2, color=GRAY_DIM, stroke_width=1))

        self.play(Create(shell_group), run_time=1.0)
        self.play(Create(ridges), run_time=0.8)

        # ~50 dots dọc viền (đại diện ~200)
        eye_dots = VGroup()
        rng = np.random.default_rng(11)
        for angle in np.linspace(-PI * 0.95, -PI * 0.05, 50):
            r = 2.4 + rng.uniform(-0.05, 0.05)
            pos = center + np.array([r * np.cos(angle), r * np.sin(angle), 0])
            eye_dots.add(Dot(pos, radius=0.05, color=BLUE_3B1B))

        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in eye_dots], lag_ratio=0.02),
            run_time=2.0,
        )
        self.wait(0.5)

        # Zoom-in callout: gương parabolic
        zoom_circle = Circle(
            radius=0.9, color=BLUE_3B1B, stroke_width=2,
        ).move_to(LEFT * 4.2 + UP * 1.5)
        mirror = Arc(
            radius=0.5, angle=PI, start_angle=-PI / 2,
            color=YELLOW_3B1B, stroke_width=2.5,
        ).move_to(zoom_circle.get_center() + DOWN * 0.15)
        reflect = Line(
            mirror.point_from_proportion(0.5),
            zoom_circle.get_center() + UP * 0.4,
            color=YELLOW_3B1B, stroke_width=1.5, stroke_opacity=0.7,
        )

        zoom_label = Text(
            "→ Each eye uses a mirror,\nnot a lens",
            font_size=18, color=YELLOW_3B1B, slant=ITALIC,
            line_spacing=0.8,
        ).next_to(zoom_circle, DOWN, buff=0.3)

        target_dot = eye_dots[10]
        zoom_line = DashedLine(
            target_dot.get_center(),
            zoom_circle.get_bottom() + RIGHT * 0.3,
            color=GRAY_DIM, stroke_opacity=0.5, dash_length=0.08,
        )

        self.play(Create(zoom_line), run_time=0.5)
        self.play(Create(zoom_circle), run_time=0.6)
        self.play(Create(mirror), Create(reflect), run_time=0.8)
        self.play(FadeIn(zoom_label), run_time=0.6)

        # Stat lớn — "200" số nên dùng Text bình thường
        stat = Text(
            "200", font_size=64, color=BLUE_3B1B, weight=BOLD,
        ).move_to(RIGHT * 4.5 + UP * 1.5)
        stat_caption = Text(
            "independent eyes",
            font_size=22, color=GRAY_LIGHT, slant=ITALIC,
        ).next_to(stat, DOWN, buff=0.15)

        self.play(Write(stat), run_time=1.0)
        self.play(FadeIn(stat_caption), run_time=0.4)
        self.wait(2.5)

        card_group = VGroup(
            header, shell_group, ridges, eye_dots,
            zoom_line, zoom_circle, mirror, reflect, zoom_label,
            stat, stat_caption,
        )
        thumb = card_group.copy()
        self.play(FadeOut(card_group), run_time=0.8)
        return thumb

    # ------------------------------------------------------------
    # Card 4 — Cá hang động (mất mắt qua tiến hoá)
    # ------------------------------------------------------------
    def card_4_cave_fish(self):
        header, _, _ = make_card_header(4, 6, "Cave Fish  ·  evolution erases eyes")
        self.play(Write(header), run_time=0.8)

        fish_stages = []
        x_positions = [-5, -1.7, 1.7, 5]
        eye_radii = [0.15, 0.10, 0.05, 0.0]
        gen_labels = ["Ancestor", "100 generations", "10,000 generations", "Today"]

        for x, eye_r, gen in zip(x_positions, eye_radii, gen_labels):
            f = create_fish(color=GRAY_LIGHT, stroke_width=2.5)
            f.scale(0.55).move_to(np.array([x, 0.5, 0]))
            # Bỏ mắt mặc định, vẽ mắt theo eye_r
            f[2].set_fill(opacity=0)
            f.remove(f[2])
            if eye_r > 0:
                eye = Dot(
                    f[0].get_center() + RIGHT * 0.55 + UP * 0.1,
                    radius=eye_r, color=GRAY_LIGHT,
                )
                f.add(eye)

            label = Text(gen, font_size=18, color=GRAY_DIM, slant=ITALIC)
            label.next_to(f, DOWN, buff=0.4)
            fish_stages.append(VGroup(f, label))

        for stage in fish_stages:
            self.play(FadeIn(stage, shift=UP * 0.1), run_time=0.6)
            self.wait(0.2)

        timeline = Arrow(
            LEFT * 6.2 + DOWN * 1.6,
            RIGHT * 6.2 + DOWN * 1.6,
            color=GRAY_DIM, stroke_width=2, buff=0,
        )
        timeline_label = Text(
            "evolutionary time  →",
            font_size=18, color=GRAY_DIM, slant=ITALIC,
        ).next_to(timeline, DOWN, buff=0.2)

        self.play(GrowArrow(timeline), FadeIn(timeline_label), run_time=0.8)

        why = Text(
            "Why?  →  Eyes are costly. In dark caves, useless.",
            font_size=22, color=YELLOW_3B1B, slant=ITALIC,
        ).to_edge(DOWN, buff=0.6)

        self.play(Write(why), run_time=1.5)
        self.wait(2.5)

        card_group = VGroup(*fish_stages, timeline, timeline_label, why, header)
        thumb = card_group.copy()
        self.play(FadeOut(card_group), run_time=0.8)
        return thumb

    # ------------------------------------------------------------
    # Card 5 — Tarsier
    # ------------------------------------------------------------
    def card_5_tarsier(self):
        header, _, _ = make_card_header(5, 6, "Tarsier  ·  eye = brain")
        self.play(Write(header), run_time=0.8)

        # Người
        human_brain = Circle(
            radius=1.0, color=PURPLE_3B1B,
            fill_opacity=0.3, stroke_width=2,
        ).move_to(LEFT * 3.5 + DOWN * 0.2)
        human_brain_label = Text(
            "brain", font_size=20, color=PURPLE_3B1B,
        ).move_to(human_brain.get_center())
        human_eye = Circle(
            radius=0.18, color=BLUE_3B1B,
            fill_opacity=0.5, stroke_width=2,
        ).next_to(human_brain, RIGHT, buff=0.2)
        human_label = Text(
            "Human", font_size=24, color=GRAY_LIGHT, weight=BOLD,
        ).next_to(human_brain, DOWN, buff=0.6)

        # Tarsier
        tarsier_brain = Circle(
            radius=0.45, color=PURPLE_3B1B,
            fill_opacity=0.3, stroke_width=2,
        ).move_to(RIGHT * 3.5 + DOWN * 0.2)
        tarsier_brain_label = Text(
            "brain", font_size=14, color=PURPLE_3B1B,
        ).move_to(tarsier_brain.get_center())
        tarsier_eye = Circle(
            radius=0.45, color=BLUE_3B1B,
            fill_opacity=0.5, stroke_width=2,
        ).next_to(tarsier_brain, RIGHT, buff=0.05)
        # "Tarsier" là tên loài, dùng Text bình thường
        tarsier_label = Text(
            "Tarsier", font_size=24, color=GRAY_LIGHT, weight=BOLD,
        ).next_to(tarsier_brain, DOWN, buff=0.6)

        self.play(
            FadeIn(human_brain), Write(human_brain_label), FadeIn(human_eye),
            run_time=1.0,
        )
        self.play(Write(human_label), run_time=0.6)
        self.wait(0.5)
        self.play(
            FadeIn(tarsier_brain), Write(tarsier_brain_label), FadeIn(tarsier_eye),
            run_time=1.0,
        )
        self.play(Write(tarsier_label), run_time=0.6)
        self.wait(0.8)

        eq = MarkupText(
            'eye  <span foreground="' + YELLOW_3B1B + '">≈</span>  brain',
            font_size=40, color=GRAY_LIGHT,
        ).to_edge(DOWN, buff=1.2)
        caption = Text(
            "the cost of hunting at night",
            font_size=20, color=YELLOW_3B1B, slant=ITALIC,
        ).next_to(eq, DOWN, buff=0.3)

        self.play(Write(eq), run_time=1.2)
        self.play(FadeIn(caption), run_time=0.6)
        self.wait(2.5)

        card_group = VGroup(
            header,
            human_brain, human_brain_label, human_eye, human_label,
            tarsier_brain, tarsier_brain_label, tarsier_eye, tarsier_label,
            eq, caption,
        )
        thumb = card_group.copy()
        self.play(FadeOut(card_group), run_time=0.8)
        return thumb

    # ------------------------------------------------------------
    # Card 6 — Bướm
    # ------------------------------------------------------------
    def card_6_butterfly(self):
        header, _, _ = make_card_header(6, 6, "Butterfly  ·  patterns not for each other")
        self.play(Write(header), run_time=0.8)

        b1 = self.draw_butterfly(scale=0.8).move_to(LEFT * 4 + DOWN * 0.3)
        b2 = self.draw_butterfly(scale=0.8).move_to(RIGHT * 4 + DOWN * 0.3)

        distance = DoubleArrow(
            b1.get_right() + RIGHT * 0.2,
            b2.get_left() + LEFT * 0.2,
            color=GRAY_DIM, stroke_width=1.5,
            buff=0, max_tip_length_to_length_ratio=0.04,
        )
        # "2 m" thuần số/đơn vị, Text() bình thường
        d_label = Text("2 m", font_size=18, color=GRAY_DIM).next_to(distance, UP, buff=0.15)

        self.play(FadeIn(b1), FadeIn(b2), run_time=1.0)
        self.play(Create(distance), Write(d_label), run_time=0.8)
        self.wait(0.5)

        eye_label = Text(
            'Left butterfly\'s view  →',
            font_size=20, color=YELLOW_3B1B, slant=ITALIC,
        ).next_to(b1, DOWN, buff=0.6)

        blur_view = Circle(
            radius=0.3, color=GRAY_LIGHT,
            fill_opacity=0.3, stroke_width=0,
        ).move_to(eye_label.get_center() + DOWN * 1.0 + RIGHT * 1.5)
        blur_outer = Circle(
            radius=0.5, color=GRAY_LIGHT,
            fill_opacity=0.15, stroke_width=0,
        ).move_to(blur_view.get_center())

        question = Text(
            "= just a blurry dot",
            font_size=22, color=GRAY_LIGHT, slant=ITALIC,
        ).next_to(blur_view, RIGHT, buff=0.5)

        self.play(FadeIn(eye_label), run_time=0.6)
        self.play(FadeIn(blur_outer), FadeIn(blur_view), run_time=1.0)
        self.play(Write(question), run_time=0.7)
        self.wait(1.5)

        punch = Text(
            "Vivid patterns → for BIRDS (predators with sharper vision)",
            font_size=22, color=YELLOW_3B1B, weight=BOLD,
        ).to_edge(DOWN, buff=0.6)

        self.play(Write(punch), run_time=1.5)
        self.wait(2.5)

        card_group = VGroup(
            header, b1, b2, distance, d_label,
            eye_label, blur_outer, blur_view, question, punch,
        )
        thumb = card_group.copy()
        self.play(FadeOut(card_group), run_time=0.8)
        return thumb

    def draw_butterfly(self, scale=1.0):
        """Bướm schematic 4 cánh."""
        body = Line(UP * 0.4, DOWN * 0.4, color=GRAY_LIGHT, stroke_width=3).scale(scale)
        wing_tl = Ellipse(
            width=1.0, height=0.7, color=PURPLE_3B1B,
            fill_opacity=0.5, stroke_width=2,
        ).move_to(np.array([-0.5, 0.2, 0])).scale(scale)
        wing_tr = Ellipse(
            width=1.0, height=0.7, color=PURPLE_3B1B,
            fill_opacity=0.5, stroke_width=2,
        ).move_to(np.array([0.5, 0.2, 0])).scale(scale)
        wing_bl = Ellipse(
            width=0.7, height=0.5, color=PINK_3B1B,
            fill_opacity=0.5, stroke_width=2,
        ).move_to(np.array([-0.4, -0.3, 0])).scale(scale)
        wing_br = Ellipse(
            width=0.7, height=0.5, color=PINK_3B1B,
            fill_opacity=0.5, stroke_width=2,
        ).move_to(np.array([0.4, -0.3, 0])).scale(scale)
        spot1 = Dot([-0.5, 0.2, 0], color=YELLOW_3B1B, radius=0.07).scale(scale)
        spot2 = Dot([0.5, 0.2, 0], color=YELLOW_3B1B, radius=0.07).scale(scale)
        return VGroup(wing_tl, wing_tr, wing_bl, wing_br, body, spot1, spot2)

    # ------------------------------------------------------------
    # Recap grid 2x3
    # ------------------------------------------------------------
    def play_recap_grid(self, thumbs):
        recap_title = Text(
            "Six species. Six visual strategies.",
            font_size=36, color=YELLOW_3B1B, weight=BOLD,
        ).to_edge(UP, buff=0.5)

        self.play(Write(recap_title), run_time=1.2)

        for thumb in thumbs:
            thumb.scale(0.22)

        grid_positions = [
            LEFT * 4.5 + UP * 0.8,
            ORIGIN + UP * 0.8,
            RIGHT * 4.5 + UP * 0.8,
            LEFT * 4.5 + DOWN * 1.8,
            ORIGIN + DOWN * 1.8,
            RIGHT * 4.5 + DOWN * 1.8,
        ]

        for thumb, pos in zip(thumbs, grid_positions):
            thumb.move_to(pos)

        frames = VGroup()
        for pos in grid_positions:
            frame = RoundedRectangle(
                width=4.0, height=2.4, corner_radius=0.15,
                color=GRAY_DIM, stroke_width=1.5,
            ).move_to(pos)
            frames.add(frame)

        self.play(
            LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.1),
            LaggedStart(*[FadeIn(t) for t in thumbs], lag_ratio=0.1),
            run_time=2.5,
        )
        self.wait(2.5)

        closing = Text(
            "And this is just the visible part — external structure.",
            font_size=22, color=GRAY_LIGHT, slant=ITALIC,
        ).to_edge(DOWN, buff=0.3)

        self.play(Write(closing), run_time=1.8)
        self.wait(3.0)

        all_recap = VGroup(recap_title, frames, *thumbs, closing)
        self.play(FadeOut(all_recap), run_time=1.5)
        self.wait(0.4)
