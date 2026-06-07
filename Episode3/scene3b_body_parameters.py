"""
Episode 3, Scene 3B: What Body Parameters Are Optimized?
=======================================================

Makes the body side of co-design concrete.

Run:
    manim -pql scene3b_body_parameters.py Scene3BBodyParameters
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def param_panel(title, color, kind):
    frame = RoundedRectangle(width=3.45, height=2.5, corner_radius=0.20, color=color, stroke_width=2.0, fill_color=GRAY_DARKER, fill_opacity=0.15)
    head = Text(title, font_size=24, color=color, weight=BOLD).move_to(frame.get_top() + DOWN * 0.38)
    visual = VGroup()
    center = frame.get_center() + DOWN * 0.05
    if kind == "shape":
        outlines = VGroup()
        for i, scale in enumerate([0.70, 0.90, 1.10]):
            body = Ellipse(width=0.76 * scale, height=0.42, color=color, stroke_width=1.8)
            body.move_to(center + LEFT * 0.78 + RIGHT * i * 0.78)
            tail = Polygon(body.get_left(), body.get_left() + LEFT * 0.25 + UP * 0.16, body.get_left() + LEFT * 0.25 + DOWN * 0.16, color=color, fill_opacity=0.0, stroke_width=1.5)
            outlines.add(VGroup(body, tail))
        arrows = VGroup(*[Arrow(outlines[i].get_right(), outlines[i + 1].get_left(), color=GRAY_MID, buff=0.08, stroke_width=1.6, max_tip_length_to_length_ratio=0.09) for i in range(2)])
        visual.add(outlines, arrows)
    elif kind == "material":
        strip = VGroup()
        for i, col in enumerate([BLUE_3B1B, TEAL_EP2, GREEN_3B1B, ORANGE_3B1B]):
            block = Rectangle(width=0.48, height=0.72, color=col, fill_color=col, fill_opacity=0.34, stroke_width=1.2)
            block.move_to(center + LEFT * 0.75 + RIGHT * i * 0.50)
            strip.add(block)
        soft = Text("soft", font_size=15, color=BLUE_3B1B).next_to(strip, DOWN, buff=0.18).align_to(strip, LEFT)
        stiff = Text("stiff", font_size=15, color=ORANGE_3B1B).next_to(strip, DOWN, buff=0.18).align_to(strip, RIGHT)
        visual.add(strip, soft, stiff)
    else:
        body = RoundedRectangle(width=1.20, height=0.62, corner_radius=0.18, color=color, stroke_width=2.0)
        body.move_to(center)
        arrows = VGroup(
            Arrow(body.get_left() + LEFT * 0.55, body.get_left(), color=ORANGE_3B1B, buff=0.05, stroke_width=2.2, max_tip_length_to_length_ratio=0.08),
            Arrow(body.get_right() + RIGHT * 0.55, body.get_right(), color=ORANGE_3B1B, buff=0.05, stroke_width=2.2, max_tip_length_to_length_ratio=0.08),
            Arrow(body.get_top() + UP * 0.42, body.get_top(), color=ORANGE_3B1B, buff=0.05, stroke_width=2.2, max_tip_length_to_length_ratio=0.08),
        )
        pulses = VGroup(*[Dot(a.get_start(), radius=0.045, color=ORANGE_3B1B) for a in arrows])
        visual.add(body, arrows, pulses)
    visual.move_to(frame.get_center() + DOWN * 0.08)
    return VGroup(frame, head, visual)


class Scene3BBodyParameters(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Body Design Is Not One Number", font_size=40, color=YELLOW_3B1B, weight=BOLD)
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.0))
        self.wait(0.35)

        panels = VGroup(
            param_panel("Shape", BLUE_3B1B, "shape"),
            param_panel("Material", GREEN_3B1B, "material"),
            param_panel("Actuation", ORANGE_3B1B, "actuation"),
        ).arrange(RIGHT, buff=0.35)
        panels.scale_to_fit_width(11.3)
        panels.move_to(UP * 0.55)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.12) for p in panels], lag_ratio=0.14), run_time=1.25)
        self.play(
            LaggedStart(*[Indicate(shape, color=emphasis_color_of(shape), scale_factor=1.10) for shape in panels[0][2][0]], lag_ratio=0.12),
            ApplyWave(panels[1][2][0], amplitude=0.08),
            LaggedStart(*[Flash(dot, color=emphasis_color_of(dot), flash_radius=0.22) for dot in panels[2][2][2]], lag_ratio=0.12),
            run_time=1.25,
        )
        self.wait(0.35)

        formula = MathTex(
            r"\theta_{\mathrm{body}}=\{\mathrm{geometry},\mathrm{material},\mathrm{actuators}\}",
            font_size=30,
            color=YELLOW_3B1B,
        )
        formula.scale_to_fit_width(10.6)
        formula.move_to(DOWN * 2.05)
        self.play(Write(formula, run_time=1.2))

        grad = VGroup(*[
            Arrow(DOWN * 1.20, panel.get_bottom() + DOWN * 0.10, color=RED_BRAIN, buff=0.05, stroke_width=1.8, max_tip_length_to_length_ratio=0.045)
            for panel in panels
        ])
        grad_label = Text("one simulated behavior updates all three", font_size=20, color=RED_BRAIN, weight=BOLD)
        grad_label.move_to(DOWN * 1.43)
        self.play(FadeIn(grad_label, shift=UP * 0.08), LaggedStart(*[GrowArrow(a) for a in grad], lag_ratio=0.12), run_time=1.0)
        self.play(
            LaggedStart(*[
                Succession(
                    a.animate.set_color(emphasis_color_of(a)).set_stroke(width=3.8),
                    a.animate.set_color(RED_BRAIN).set_stroke(width=2.6),
                )
                for a in grad
            ], lag_ratio=0.10),
            run_time=1.1,
        )
        self.wait(1.4)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)
