"""
Episode 1, Scene 1B: Body-Eye-Brain Design Loop
===============================================

Introduces the recurring longform frame:
environment -> eye -> brain -> body -> environment.

Run:
    manim -pql scene1b_design_loop.py Scene1BDesignLoop
"""

from manim import *
from common import *


def make_loop_node(label, color, width=2.1):
    box = RoundedRectangle(
        width=width,
        height=0.78,
        corner_radius=0.18,
        color=color,
        stroke_width=2.2,
        fill_color=color,
        fill_opacity=0.12,
    )
    text = Text(label, font_size=22, color=color, weight=BOLD)
    text.move_to(box)
    return VGroup(box, text)


def make_param_card(title, lines, color, width=2.65, height=1.55):
    frame = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        color=color,
        stroke_width=2,
        fill_color=GRAY_DARKER,
        fill_opacity=0.16,
    )
    if title.startswith("theta_"):
        title_text = MathTex(
            rf"\theta_{{\mathrm{{{title.split('_', 1)[1]}}}}}",
            font_size=24,
            color=color,
        )
    else:
        title_text = Text(title, font_size=20, color=color, weight=BOLD)
    title_text.move_to(frame.get_top() + DOWN * 0.28)
    body = VGroup(*[Text(line, font_size=16, color=GRAY_LIGHT) for line in lines])
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
    body.move_to(frame.get_center() + DOWN * 0.14)
    return VGroup(frame, title_text, body)


class Scene1BDesignLoop(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = VGroup(
            Text("Design Only Makes Sense", font_size=30, color=YELLOW_3B1B, weight=BOLD),
            Text("in a Loop", font_size=27, color=YELLOW_3B1B, weight=BOLD),
        ).arrange(DOWN, buff=0.04)
        title.scale_to_fit_width(7.8)
        title.to_edge(UP, buff=0.20)
        self.play(Write(title, run_time=1.0))
        self.wait(0.35)

        loop_center = UP * 0.66
        world = make_loop_node("world", GRAY_LIGHT, width=1.85).move_to(loop_center + UP * 1.02)
        eye = make_loop_node("eye", BLUE_3B1B, width=1.65).move_to(loop_center + LEFT * 2.55)
        brain = make_loop_node("brain", RED_BRAIN, width=1.85).move_to(loop_center + DOWN * 1.02)
        body = make_loop_node("body", GREEN_3B1B, width=1.75).move_to(loop_center + RIGHT * 2.55)

        arrows = VGroup(
            Arrow(world[0].get_left(), eye[0].get_top(), color=GRAY_MID, buff=0.12, stroke_width=2.2, max_tip_length_to_length_ratio=0.08),
            Arrow(eye[0].get_bottom(), brain[0].get_left(), color=GRAY_MID, buff=0.12, stroke_width=2.2, max_tip_length_to_length_ratio=0.08),
            Arrow(brain[0].get_right(), body[0].get_bottom(), color=GRAY_MID, buff=0.12, stroke_width=2.2, max_tip_length_to_length_ratio=0.08),
            Arrow(body[0].get_top(), world[0].get_right(), color=GRAY_MID, buff=0.12, stroke_width=2.2, max_tip_length_to_length_ratio=0.08),
        )

        self.play(LaggedStart(*[FadeIn(n, scale=0.92) for n in [world, eye, brain, body]], lag_ratio=0.18), run_time=1.1)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.16), run_time=1.2)
        self.wait(0.5)

        task_box = RoundedRectangle(
            width=5.7,
            height=0.72,
            corner_radius=0.16,
            color=YELLOW_3B1B,
            stroke_width=2,
            fill_color=YELLOW_3B1B,
            fill_opacity=0.10,
        )
        task_text = Text("task + environment define what 'good' means", font_size=22, color=YELLOW_3B1B, weight=BOLD)
        task_text.scale_to_fit_width(task_box.width - 0.35)
        task_group = VGroup(task_box, task_text)
        task_group.move_to(DOWN * 2.28)
        self.play(Create(task_box), Write(task_text, run_time=1.0))
        self.wait(1.0)

        self.play(FadeOut(task_group, run_time=0.4))
        loop_group = VGroup(world, eye, brain, body, arrows)
        self.play(loop_group.animate.scale(1.12, about_point=loop_center).move_to(UP * 0.70), run_time=0.9)

        eye_card = make_param_card("theta_eye", ["position", "direction", "field of view"], BLUE_3B1B)
        brain_card = make_param_card("theta_brain", ["policy", "memory", "control gains"], RED_BRAIN)
        body_card = make_param_card("theta_body", ["shape", "stiffness", "material"], GREEN_3B1B)
        eye_card.move_to(eye.get_center() + DOWN * 2.42)
        brain_card.move_to(brain.get_center() + DOWN * 1.56)
        body_card.move_to(body.get_center() + DOWN * 2.42)
        cards = VGroup(eye_card, brain_card, body_card)

        self.play(FadeIn(eye_card, shift=UP * 0.12), run_time=0.65)
        self.play(FadeIn(brain_card, shift=UP * 0.12), run_time=0.65)
        self.play(FadeIn(body_card, shift=UP * 0.12), run_time=0.65)

        takeaway_box = RoundedRectangle(
            width=5.05,
            height=0.42,
            corner_radius=0.16,
            color=YELLOW_3B1B,
            stroke_width=1.35,
            fill_color=YELLOW_3B1B,
            fill_opacity=0.08,
        )
        takeaway_text = Text(
            "optimize the whole loop, not one part in isolation",
            font_size=13,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        takeaway_text.scale_to_fit_width(takeaway_box.width - 0.48)
        equation = VGroup(takeaway_box, takeaway_text)
        equation.move_to(DOWN * 3.38)
        self.play(Create(takeaway_box), Write(takeaway_text, run_time=1.1))
        self.wait(2.3)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
