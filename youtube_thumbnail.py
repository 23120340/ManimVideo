"""
YouTube thumbnail for the Computational Design video.

Render:
    manim -qh -s youtube_thumbnail.py YouTubeThumbnail
"""

from manim import *
import numpy as np


BG_COLOR = "#1C1C1C"
BLUE = "#3B82F6"
YELLOW = "#FBBF24"
GREEN = "#10B981"
PURPLE = "#A78BFA"
ORANGE = "#F97316"
PINK = "#EC4899"
GRAY_LIGHT = "#E5E7EB"
GRAY_MID = "#9CA3AF"
GRAY_DIM = "#6B7280"


def outlined_text(text, font_size, color, weight=BOLD):
    item = Text(text, font_size=font_size, color=color, weight=weight)
    item.set_stroke(BLACK, width=8, opacity=0.65, background=True)
    return item


class YouTubeThumbnail(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # Subtle radial accents behind the main graphic.
        glow = VGroup(
            Circle(radius=3.2, color=BLUE, fill_opacity=0.05, stroke_opacity=0)
            .move_to(RIGHT * 3.95 + UP * 0.1),
            Circle(radius=2.35, color=PURPLE, fill_opacity=0.07, stroke_opacity=0)
            .move_to(RIGHT * 4.2 + UP * 0.15),
            Circle(radius=1.45, color=YELLOW, fill_opacity=0.055, stroke_opacity=0)
            .move_to(RIGHT * 4.45 + DOWN * 0.05),
        )
        self.add(glow)

        # A quiet design-space panel. Keep it simple so the title dominates.
        panel = RoundedRectangle(
            width=5.2,
            height=4.6,
            corner_radius=0.28,
            color=BLUE,
            stroke_width=2,
            stroke_opacity=0.32,
        )
        panel.set_fill("#111827", opacity=0.23)
        panel.move_to(RIGHT * 4.15 + UP * 0.05)
        self.add(panel)

        grid = VGroup()
        for x in np.linspace(2.0, 6.25, 5):
            grid.add(Line([x, -2.25, 0], [x, 2.25, 0], color=GRAY_DIM,
                          stroke_width=0.7, stroke_opacity=0.13))
        for y in np.linspace(-2.0, 2.0, 5):
            grid.add(Line([1.65, y, 0], [6.55, y, 0], color=GRAY_DIM,
                          stroke_width=0.7, stroke_opacity=0.13))
        self.add(grid)

        # Minimal design-space landscape: score curve + optimization path.
        axes = VGroup(
            Arrow(
                RIGHT * 2.05 + DOWN * 1.55,
                RIGHT * 6.05 + DOWN * 1.55,
                buff=0,
                color=GRAY_MID,
                stroke_width=2.6,
                max_tip_length_to_length_ratio=0.045,
            ),
            Arrow(
                RIGHT * 2.25 + DOWN * 1.75,
                RIGHT * 2.25 + UP * 1.4,
                buff=0,
                color=GRAY_MID,
                stroke_width=2.6,
                max_tip_length_to_length_ratio=0.055,
            ),
        )
        self.add(axes)

        utility_curve = ParametricFunction(
            lambda t: np.array([
                4.05 + t,
                -0.42 * (t - 0.65) ** 2 + 0.42 * np.sin(1.65 * t) + 0.58,
                0,
            ]),
            t_range=[-1.65, 1.8],
            color=YELLOW,
            stroke_width=6,
        )
        utility_curve.set_stroke(opacity=0.9)
        self.add(utility_curve)

        path_points = [
            RIGHT * 2.62 + DOWN * 1.1,
            RIGHT * 3.18 + DOWN * 0.72,
            RIGHT * 3.82 + DOWN * 0.22,
            RIGHT * 4.58 + UP * 0.36,
            RIGHT * 5.05 + UP * 0.88,
        ]
        search_path = VGroup()
        for a, b in zip(path_points, path_points[1:]):
            search_path.add(Line(a, b, color=YELLOW, stroke_width=3.0,
                                 stroke_opacity=0.55))
        dots = VGroup(*[
            Dot(p, radius=0.075, color=BLUE if i < len(path_points) - 1 else YELLOW)
            for i, p in enumerate(path_points)
        ])
        best_ring = Circle(radius=0.22, color=YELLOW, stroke_width=3.0)
        best_ring.move_to(path_points[-1])
        self.add(search_path, dots, best_ring)

        panel_label = Text("DESIGN SPACE", font_size=22, color=GRAY_MID, weight=BOLD)
        panel_label.move_to(panel.get_top() + DOWN * 0.35)
        self.add(panel_label)

        # Left-side text block. Very few words, large enough for mobile.
        badge = RoundedRectangle(width=3.85, height=0.48, corner_radius=0.14,
                                 color=BLUE, stroke_width=2)
        badge.set_fill(BLUE, opacity=0.16)
        badge_text = Text("COMPUTATIONAL DESIGN", font_size=22,
                          color=BLUE, weight=BOLD)
        badge_text.scale_to_fit_width(3.45)
        badge_text.move_to(badge)
        badge_group = VGroup(badge, badge_text)
        badge_group.to_edge(LEFT, buff=0.55).to_edge(UP, buff=0.65)

        line_1 = VGroup(
            outlined_text("AI", 94, BLUE),
            outlined_text("LEARNS", 74, GRAY_LIGHT),
        ).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        line_2 = outlined_text("TO DESIGN", 92, YELLOW)
        main_title = VGroup(line_1, line_2).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        main_title.to_edge(LEFT, buff=0.48).shift(UP * 0.55)

        subtitle_bg = RoundedRectangle(width=5.15, height=0.58, corner_radius=0.16,
                                       color=YELLOW, stroke_width=0)
        subtitle_bg.set_fill(YELLOW, opacity=0.15)
        subtitle = Text("Nature  ->  Algorithms  ->  Designs",
                        font_size=25, color=GRAY_LIGHT, weight=BOLD)
        subtitle.scale_to_fit_width(4.85)
        subtitle_group = VGroup(subtitle_bg, subtitle)
        subtitle.move_to(subtitle_bg)
        subtitle_group.next_to(main_title, DOWN, buff=0.35, aligned_edge=LEFT)

        hook = Text("How machines learn to create", font_size=26,
                    color=GRAY_MID, slant=ITALIC)
        hook.next_to(subtitle_group, DOWN, buff=0.22, aligned_edge=LEFT)

        self.add(badge_group, main_title, subtitle_group, hook)

        # A little foreground depth.
        diagonal = Line(LEFT * 7 + DOWN * 3.25, RIGHT * 7 + DOWN * 2.25,
                        color=YELLOW, stroke_width=4, stroke_opacity=0.15)
        self.add(diagonal)
