"""
scene5.py — Episode 3, Scene 5: Outro
"The Remaining Challenge" — sim-to-real gap, dead fish callback, final quote.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


class Scene5Outro(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Section A: Sim-to-real gap ─────────────────────────────────
        title = Text(
            "The Remaining Challenge",
            font_size=36,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.5)

        divider = DashedLine(
            UP * 2.5, DOWN * 2.5,
            color=GRAY_DIM,
            stroke_width=1.5,
            dash_length=0.14,
        )
        self.play(Create(divider), run_time=0.7)

        # Left panel — In Simulation
        left_header = Text(
            "In Simulation",
            font_size=24,
            color=GREEN_3B1B,
            weight=BOLD,
        )
        left_header.move_to(LEFT * 3.5 + UP * 1.8)

        left_bullets = VGroup(
            Text("• Perfect physics model", font_size=18, color=GREEN_3B1B),
            Text("• Instant evaluation", font_size=18, color=GREEN_3B1B),
            Text("• Gradient available", font_size=18, color=GREEN_3B1B),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        left_bullets.next_to(left_header, DOWN, buff=0.4)
        left_bullets.set_x(-3.5)

        # Right panel — In Reality
        right_header = Text(
            "In Reality",
            font_size=24,
            color=RED_BRAIN,
            weight=BOLD,
        )
        right_header.move_to(RIGHT * 3.5 + UP * 1.8)

        right_bullets = VGroup(
            Text("• Unmodeled friction, flex", font_size=18, color=RED_BRAIN),
            Text("• Expensive fabrication", font_size=18, color=RED_BRAIN),
            Text("• No gradient", font_size=18, color=RED_BRAIN),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        right_bullets.next_to(right_header, DOWN, buff=0.4)
        right_bullets.set_x(3.5)

        # Gap arrow + label at bottom center
        gap_arrow = DoubleArrow(
            start=LEFT * 1.2 + DOWN * 1.7,
            end=RIGHT * 1.2 + DOWN * 1.7,
            color=ORANGE_3B1B,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
            buff=0,
        )
        gap_label = Text(
            "Sim-to-real gap",
            font_size=20,
            color=ORANGE_3B1B,
            weight=BOLD,
        )
        gap_label.next_to(gap_arrow, DOWN, buff=0.25)

        self.play(FadeIn(left_header, shift=RIGHT * 0.15), run_time=0.7)
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=RIGHT * 0.15) for b in left_bullets],
                lag_ratio=0.25,
            ),
            run_time=1.0,
        )
        self.play(FadeIn(right_header, shift=LEFT * 0.15), run_time=0.7)
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=LEFT * 0.15) for b in right_bullets],
                lag_ratio=0.25,
            ),
            run_time=1.0,
        )
        self.play(
            GrowArrow(gap_arrow),
            Write(gap_label),
            run_time=1.2,
        )
        self.wait(2.0)

        # FadeOut Section A
        all_A = VGroup(
            title, divider,
            left_header, left_bullets,
            right_header, right_bullets,
            gap_arrow, gap_label,
        )
        self.play(FadeOut(all_A), run_time=1.2)
        self.wait(0.4)

        # ── Section B: Dead fish callback ──────────────────────────────
        # Use the same create_fish() helper from Episode 1 for visual continuity
        fish = create_fish(color=GRAY_LIGHT, stroke_width=2.5)
        fish.scale(0.85).move_to(UP * 1.0)

        fish_subtitle = Text(
            "Dead fish. Still swimming.",
            font_size=24,
            color=GRAY_MID,
            slant=ITALIC,
        )
        fish_subtitle.next_to(fish, DOWN, buff=0.5)

        nature_text = Text(
            "Nature did this for 4 billion years.",
            font_size=22,
            color=GRAY_LIGHT,
        )
        nature_text.next_to(fish_subtitle, DOWN, buff=0.5)

        we_text = Text(
            "We just started.",
            font_size=32,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        we_text.next_to(nature_text, DOWN, buff=0.45)

        self.play(FadeIn(fish, scale=0.85), run_time=1.2)
        self.play(
            LaggedStart(
                Write(fish_subtitle),
                Write(nature_text),
                Write(we_text),
                lag_ratio=0.5,
            ),
            run_time=3.0,
        )
        self.wait(2.0)

        # FadeOut Section B
        all_B = VGroup(fish, fish_subtitle, nature_text, we_text)
        self.play(FadeOut(all_B), run_time=1.2)
        self.wait(0.4)

        # ── Section C: Final quote ─────────────────────────────────────
        quote_line1 = Text(
            '"Intelligence is not in the brain."',
            font_size=28,
            color=GRAY_LIGHT,
        )
        quote_line2 = Text(
            "It is in the WHOLE LOOP —",
            font_size=36,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        quote_line3 = Text(
            "brain, body, environment, interacting.",
            font_size=24,
            color=GRAY_LIGHT,
            slant=ITALIC,
        )

        quote = VGroup(quote_line1, quote_line2, quote_line3)
        quote.arrange(DOWN, buff=0.55)
        quote.move_to(ORIGIN)

        self.play(
            LaggedStart(
                Write(quote_line1),
                Write(quote_line2),
                Write(quote_line3),
                lag_ratio=0.6,
            ),
            run_time=4.5,
        )
        self.wait(3.0)
        self.play(FadeOut(quote), run_time=1.2)
        self.wait(0.5)

        # "Fin."
        fin_text = Text(
            "Fin.",
            font_size=52,
            color=GRAY_MID,
            slant=ITALIC,
        )
        fin_text.move_to(ORIGIN)
        self.play(FadeIn(fin_text, scale=0.85), run_time=1.2)
        self.wait(2.0)

        # Final FadeOut
        everything = VGroup(fin_text)
        self.play(FadeOut(everything), run_time=1.0)
        self.wait(0.4)
