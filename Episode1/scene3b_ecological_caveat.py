"""
Episode 1, Scene 3B: Ecological Caveat
======================================

Adds the scientific caution missing from simple animal examples: a feature is
interpreted relative to a task, environment, evidence, and alternative hypotheses.

Run:
    manim -pql scene3b_ecological_caveat.py Scene3BEcologicalCaveat
"""

import os

from manim import *
from common import *


ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def caveat_node(label, color, radius=0.38):
    dot = Circle(radius=radius, color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.12)
    text = Text(label, font_size=17, color=color, weight=BOLD)
    text.move_to(dot)
    return VGroup(dot, text)


def svg_asset(filename, color, max_width=1.35, max_height=0.92):
    icon = SVGMobject(os.path.join(ASSET_DIR, filename))
    icon.set_color(color)
    icon.set_fill(color, opacity=0.76)
    icon.set_stroke(color, width=0.55, opacity=0.92)
    icon.scale_to_fit_width(max_width)
    if icon.height > max_height:
        icon.scale_to_fit_height(max_height)
    return icon


def context_chip(label, color, width=1.36):
    box = RoundedRectangle(
        width=width,
        height=0.46,
        corner_radius=0.12,
        color=color,
        stroke_width=1.55,
        fill_color=color,
        fill_opacity=0.10,
    )
    text = Text(label, font_size=15, color=color, weight=BOLD)
    if text.width > width - 0.20:
        text.scale_to_fit_width(width - 0.20)
    text.move_to(box)
    return VGroup(box, text)


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
            width=5.05,
            height=3.05,
            corner_radius=0.20,
            color=RED_BRAIN,
            stroke_width=2.2,
            fill_color=RED_BRAIN,
            fill_opacity=0.08,
        )
        bad_box.move_to(LEFT * 2.88 + DOWN * 0.10)
        bad_title = Text("Too simple", font_size=25, color=RED_BRAIN, weight=BOLD)
        bad_title.move_to(bad_box.get_top() + DOWN * 0.42)
        bad_cow = svg_asset("cow.svg", RED_BRAIN, max_width=1.48, max_height=0.86)
        bad_cause = caveat_node("one\ncause", RED_BRAIN, radius=0.46)
        bad_chain = VGroup(
            bad_cow,
            Arrow(ORIGIN, RIGHT * 1.05, color=RED_BRAIN, buff=0.08, stroke_width=2.2, tip_length=0.14),
            bad_cause,
        ).arrange(RIGHT, buff=0.32)
        bad_chain.move_to(bad_box.get_center() + DOWN * 0.02)
        bad_cross = VGroup(
            Line(bad_cause.get_center() + LEFT * 0.34 + UP * 0.34, bad_cause.get_center() + RIGHT * 0.34 + DOWN * 0.34, color=RED_BRAIN, stroke_width=3.0),
            Line(bad_cause.get_center() + LEFT * 0.34 + DOWN * 0.34, bad_cause.get_center() + RIGHT * 0.34 + UP * 0.34, color=RED_BRAIN, stroke_width=3.0),
        )
        bad_caption = Text("feature -> single story", font_size=16, color=GRAY_MID, slant=ITALIC)
        bad_caption.next_to(bad_chain, DOWN, buff=0.28)

        good_box = RoundedRectangle(
            width=5.05,
            height=3.05,
            corner_radius=0.20,
            color=GREEN_3B1B,
            stroke_width=2.2,
            fill_color=GREEN_3B1B,
            fill_opacity=0.08,
        )
        good_box.move_to(RIGHT * 2.88 + DOWN * 0.10)
        good_title = Text("Better frame", font_size=25, color=GREEN_3B1B, weight=BOLD)
        good_title.move_to(good_box.get_top() + DOWN * 0.42)
        good_cow = svg_asset("cow.svg", GRAY_LIGHT, max_width=1.26, max_height=0.78)
        claim_label = Text("feature\nclaim", font_size=17, color=GREEN_3B1B, weight=BOLD, line_spacing=1.05)
        claim = VGroup(good_cow, claim_label).arrange(DOWN, buff=0.12)
        claim.move_to(good_box.get_center() + LEFT * 1.35 + DOWN * 0.03)
        chips = VGroup(
            context_chip("task", BLUE_3B1B, width=1.25),
            context_chip("environment", ORANGE_3B1B, width=1.58),
            context_chip("cost", PURPLE_3B1B, width=1.25),
            context_chip("evidence", GREEN_3B1B, width=1.38),
        )
        chip_grid = VGroup(
            VGroup(chips[0], chips[1]).arrange(RIGHT, buff=0.16),
            VGroup(chips[2], chips[3]).arrange(RIGHT, buff=0.16),
        ).arrange(DOWN, buff=0.22)
        chip_grid.move_to(good_box.get_center() + RIGHT * 0.95 + DOWN * 0.04)
        good_arrow = Arrow(
            claim.get_right() + RIGHT * 0.12,
            chip_grid.get_left() + LEFT * 0.12,
            color=GREEN_3B1B,
            stroke_width=2.0,
            tip_length=0.13,
            buff=0.04,
        )
        good_caption = Text("read the claim inside context", font_size=16, color=GRAY_MID, slant=ITALIC)
        good_caption.move_to(good_box.get_bottom() + UP * 0.28)

        self.play(FadeIn(bad_box), FadeIn(good_box), run_time=0.7)
        self.play(FadeIn(bad_title, shift=DOWN * 0.08), FadeIn(good_title, shift=DOWN * 0.08), run_time=0.75)
        self.play(FadeIn(bad_chain, shift=UP * 0.1), run_time=0.65)
        self.play(Create(bad_cross), FadeIn(bad_caption, shift=UP * 0.06), run_time=0.55)
        self.play(FadeIn(claim, shift=RIGHT * 0.08), GrowArrow(good_arrow), run_time=0.65)
        self.play(LaggedStart(*[FadeIn(chip, scale=0.94) for chip in chips], lag_ratio=0.10), FadeIn(good_caption, shift=UP * 0.06), run_time=0.9)
        self.wait(0.75)

        note_lines = VGroup(
            Text("Stripes support a hypothesis.", font_size=23, color=YELLOW_3B1B, weight=BOLD),
            Text("Context decides how broad the claim is.", font_size=23, color=YELLOW_3B1B, weight=BOLD),
        ).arrange(DOWN, buff=0.08)
        note_box = RoundedRectangle(
            width=10.8,
            height=0.92,
            corner_radius=0.16,
            color=YELLOW_3B1B,
            stroke_width=1.45,
            fill_color=YELLOW_3B1B,
            fill_opacity=0.06,
        )
        if note_lines.width > note_box.width - 0.45:
            note_lines.scale_to_fit_width(note_box.width - 0.45)
        note_lines.move_to(note_box)
        zebra_note = VGroup(note_box, note_lines).move_to(DOWN * 2.55)
        self.play(FadeIn(zebra_note, shift=UP * 0.08), run_time=0.8)
        self.wait(2.6)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
