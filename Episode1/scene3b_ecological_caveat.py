"""
Episode 1, Scene 3B: Ecological Caveat
======================================

Adds the scientific caution missing from simple animal examples: a feature is
interpreted relative to a task, environment, evidence, and alternative hypotheses.

Run:
    manim -pql scene3b_ecological_caveat.py Scene3BEcologicalCaveat
"""

from manim import *
from common import *


def caveat_node(label, color, radius=0.38):
    dot = Circle(radius=radius, color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.12)
    text = Text(label, font_size=17, color=color, weight=BOLD)
    text.move_to(dot)
    return VGroup(dot, text)


def mini_zebra(color=GRAY_LIGHT):
    body = Ellipse(width=1.25, height=0.62, color=color, stroke_width=2.0)
    head = Ellipse(width=0.35, height=0.30, color=color, stroke_width=2.0)
    head.next_to(body, RIGHT, buff=-0.05)
    legs = VGroup(
        Line(body.get_bottom() + LEFT * 0.28, body.get_bottom() + LEFT * 0.42 + DOWN * 0.38, color=color, stroke_width=1.8),
        Line(body.get_bottom() + RIGHT * 0.18, body.get_bottom() + RIGHT * 0.28 + DOWN * 0.38, color=color, stroke_width=1.8),
    )
    stripes = VGroup(*[
        Line(body.get_center() + LEFT * 0.48 + RIGHT * i * 0.18 + UP * 0.26,
             body.get_center() + LEFT * 0.36 + RIGHT * i * 0.18 + DOWN * 0.26,
             color=color, stroke_width=1.3)
        for i in range(6)
    ])
    return VGroup(body, head, legs, stripes)


class Scene3BEcologicalCaveat(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Be Careful With Evolutionary Stories", font_size=38, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.0))
        self.wait(0.35)

        bad_box = RoundedRectangle(
            width=4.85,
            height=2.9,
            corner_radius=0.20,
            color=RED_BRAIN,
            stroke_width=2.2,
            fill_color=RED_BRAIN,
            fill_opacity=0.08,
        )
        bad_box.move_to(LEFT * 3.05 + DOWN * 0.15)
        bad_title = Text("Too simple", font_size=26, color=RED_BRAIN, weight=BOLD)
        bad_title.move_to(bad_box.get_top() + DOWN * 0.42)
        bad_zebra = mini_zebra(RED_BRAIN).scale(0.78)
        bad_cause = caveat_node("one\ncause", RED_BRAIN, radius=0.48)
        bad_chain = VGroup(
            bad_zebra,
            Arrow(ORIGIN, RIGHT * 1.15, color=RED_BRAIN, buff=0.08, stroke_width=2.4),
            bad_cause,
        ).arrange(RIGHT, buff=0.32)
        bad_chain.move_to(bad_box.get_center() + DOWN * 0.06)
        bad_cross = VGroup(
            Line(bad_cause.get_center() + LEFT * 0.34 + UP * 0.34, bad_cause.get_center() + RIGHT * 0.34 + DOWN * 0.34, color=RED_BRAIN, stroke_width=3.0),
            Line(bad_cause.get_center() + LEFT * 0.34 + DOWN * 0.34, bad_cause.get_center() + RIGHT * 0.34 + UP * 0.34, color=RED_BRAIN, stroke_width=3.0),
        )
        bad_caption = Text("story too narrow", font_size=17, color=GRAY_MID, slant=ITALIC)
        bad_caption.next_to(bad_chain, DOWN, buff=0.35)

        good_box = RoundedRectangle(
            width=4.85,
            height=2.9,
            corner_radius=0.20,
            color=GREEN_3B1B,
            stroke_width=2.2,
            fill_color=GREEN_3B1B,
            fill_opacity=0.08,
        )
        good_box.move_to(RIGHT * 3.05 + DOWN * 0.15)
        good_title = Text("Better frame", font_size=26, color=GREEN_3B1B, weight=BOLD)
        good_title.move_to(good_box.get_top() + DOWN * 0.42)
        center = caveat_node("feature", GREEN_3B1B, radius=0.50)
        task = caveat_node("task", BLUE_3B1B, radius=0.36)
        env = caveat_node("world", ORANGE_3B1B, radius=0.36)
        cost = caveat_node("cost", PURPLE_3B1B, radius=0.36)
        evidence = caveat_node("data", GREEN_3B1B, radius=0.36)
        context_nodes = VGroup(task, env, cost, evidence)
        context_nodes[0].move_to(center.get_center() + UP * 0.78)
        context_nodes[1].move_to(center.get_center() + RIGHT * 1.12)
        context_nodes[2].move_to(center.get_center() + DOWN * 0.78)
        context_nodes[3].move_to(center.get_center() + LEFT * 1.12)
        links = VGroup(*[
            Line(center.get_center(), node.get_center(), color=GRAY_DIM, stroke_width=1.6)
            for node in context_nodes
        ])
        good_map = VGroup(links, center, context_nodes)
        good_map.move_to(good_box.get_center() + DOWN * 0.18)

        self.play(FadeIn(bad_box), FadeIn(good_box), run_time=0.7)
        self.play(FadeIn(bad_title, shift=DOWN * 0.08), FadeIn(good_title, shift=DOWN * 0.08), run_time=0.75)
        self.play(FadeIn(bad_chain, shift=UP * 0.1), run_time=0.65)
        self.play(Create(bad_cross), FadeIn(bad_caption, shift=UP * 0.06), run_time=0.55)
        self.play(Create(links), FadeIn(center, scale=0.9), run_time=0.65)
        self.play(LaggedStart(*[FadeIn(n, scale=0.9) for n in context_nodes], lag_ratio=0.10), run_time=0.8)
        self.wait(0.75)

        zebra_note = Text(
            "Stripes support a hypothesis.\nContext decides how broad the claim is.",
            font_size=26,
            color=YELLOW_3B1B,
            weight=BOLD,
            line_spacing=1.05,
        )
        zebra_note.scale_to_fit_width(10.8)
        zebra_note.to_edge(DOWN, buff=0.78)
        self.play(FadeIn(zebra_note, shift=UP * 0.08), run_time=0.8)
        self.wait(2.6)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
