"""
Episode 1, Scene 2C: Visual Acuity
==================================

Adds the missing "vision is not just eye shape" layer: acuity and resolution
allocation are design variables tied to task and environment.

Run:
    manim -pql scene2c_visual_acuity.py Scene2CVisualAcuity
"""

from manim import *
from common import *


class Scene2CVisualAcuity(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Visual Acuity Is a Design Variable", font_size=39, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(FadeIn(title, shift=DOWN * 0.10), run_time=0.8)
        self.wait(1.0)

        axis = Line(LEFT * 4.9, RIGHT * 4.9, color=GRAY_MID, stroke_width=3)
        axis.shift(DOWN * 0.95)
        axis.add_tip(tip_length=0.13)
        left_label = Text("wide / cheap sensing", font_size=22, color=BLUE_3B1B, weight=BOLD)
        right_label = Text("fine detail / high cost", font_size=22, color=ORANGE_3B1B, weight=BOLD)
        left_label.next_to(axis.get_start(), DOWN, buff=0.28)
        right_label.next_to(axis.get_end(), DOWN, buff=0.28)

        self.play(Create(axis), FadeIn(left_label), FadeIn(right_label), run_time=1.2)
        self.wait(3.0)

        animals = [
            ("scallop", -3.55, "many eyes\ncoarse alarm"),
            ("butterfly", -1.40, "signal receiver\nmatters"),
            ("human", 1.30, "central fovea\nfor detail"),
            ("falcon", 3.55, "long-range\nprey detection"),
        ]

        cards = VGroup()
        for name, x, note in animals:
            dot = Dot(axis.get_center() + RIGHT * x, radius=0.095, color=YELLOW_3B1B)
            stem = Line(dot.get_center(), dot.get_center() + UP * 0.34, color=GRAY_DIM, stroke_width=1.5)
            label = Text(name, font_size=22, color=GRAY_LIGHT, weight=BOLD)
            label.next_to(stem, UP, buff=0.12)
            detail = Text(note, font_size=18, color=GRAY_MID, line_spacing=1.15)
            detail.next_to(label, UP, buff=0.14)
            cards.add(VGroup(dot, stem, label, detail))

        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.18), run_time=2.4)
        self.wait(4.5)
        self.play(FadeOut(VGroup(axis, left_label, right_label, cards), run_time=0.25))

        camera = RoundedRectangle(width=3.6, height=2.0, corner_radius=0.20, color=BLUE_3B1B, stroke_width=2.2)
        camera.move_to(LEFT * 2.85 + UP * 0.55)
        cam_title = Text("camera thinking", font_size=24, color=BLUE_3B1B, weight=BOLD).move_to(camera.get_top() + DOWN * 0.35)
        cam_body = VGroup(
            Text("more pixels", font_size=19, color=GRAY_LIGHT, font="Consolas"),
            Text("more bandwidth", font_size=19, color=GRAY_LIGHT, font="Consolas"),
            Text("more compute", font_size=19, color=GRAY_LIGHT, font="Consolas"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        cam_body.move_to(camera.get_center() + DOWN * 0.18)

        design = RoundedRectangle(width=3.8, height=2.0, corner_radius=0.20, color=GREEN_3B1B, stroke_width=2.2)
        design.move_to(RIGHT * 2.85 + UP * 0.55)
        des_title = Text("design thinking", font_size=24, color=GREEN_3B1B, weight=BOLD).move_to(design.get_top() + DOWN * 0.35)
        des_body = VGroup(
            Text("needed detail", font_size=19, color=GRAY_LIGHT, font="Consolas"),
            Text("sensor placement", font_size=19, color=GRAY_LIGHT, font="Consolas"),
            Text("ignored noise", font_size=19, color=GRAY_LIGHT, font="Consolas"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        des_body.move_to(design.get_center() + DOWN * 0.18)

        self.play(
            FadeIn(camera),
            FadeIn(design),
            FadeIn(cam_title, shift=DOWN * 0.08),
            FadeIn(des_title, shift=DOWN * 0.08),
            FadeIn(cam_body, shift=RIGHT * 0.1),
            FadeIn(des_body, shift=LEFT * 0.1),
            run_time=1.15,
        )
        self.wait(5.0)

        caveat = Text(
            "High acuity helps only when\n"
            "the task pays for that information.",
            font_size=20,
            color=YELLOW_3B1B,
            weight=BOLD,
            line_spacing=1.05,
        )
        caveat_box = RoundedRectangle(
            width=8.65,
            height=0.82,
            corner_radius=0.16,
            color=YELLOW_3B1B,
            stroke_width=1.5,
            fill_color=YELLOW_3B1B,
            fill_opacity=0.07,
        )
        if caveat.width > caveat_box.width - 0.45:
            caveat.scale_to_fit_width(caveat_box.width - 0.45)
        caveat.move_to(caveat_box)
        caveat_group = VGroup(caveat_box, caveat).move_to(DOWN * 1.82)
        self.play(FadeIn(caveat_group, shift=UP * 0.08), run_time=0.8)
        self.wait(4.0)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
