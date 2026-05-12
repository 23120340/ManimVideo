"""
scene5.py — Episode 3, Scene 5: Outro
"The Remaining Challenge" — sim-to-real gap, dead fish callback, final quote.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class Scene3Outro(Scene):
    def construct(self):
        # ── Background ──────────────────────────────────────────────
        self.camera.background_color = BG_COLOR

        # VO: "Sim-to-real gap vẫn là thách thức lớn nhất. Nhưng ý tưởng cốt lõi
        #       đã được chứng minh: gradient có thể chảy qua vật lý, và khi nó làm
        #       vậy, nó có thể thiết kế ra những cơ thể mà con người không tưởng
        #       tượng được. Tự nhiên đã làm điều này 4 tỉ năm. Ta vừa mới bắt đầu."

        # ── Section A: Sim-to-real gap ───────────────────────────────
        title = Text(
            "The Remaining Challenge",
            font_size=36,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.5)

        # Vertical divider
        divider = DashedLine(
            UP * 3.5, DOWN * 3.5,
            color=GRAY_DIM,
            stroke_width=1.5,
            dash_length=0.14,
        )
        self.play(Create(divider), run_time=0.7)

        # Left panel — In Simulation
        left_header = Text(
            "In Simulation",
            font_size=22,
            color=GREEN_3B1B,
            weight=BOLD,
        )
        left_header.move_to(LEFT * 3.2 + UP * 1.8)

        left_bullets_texts = [
            "• Perfect physics model",
            "• Instant evaluation",
            "• Gradient available",
        ]
        left_bullets = VGroup(*[
            Text(t, font_size=17, color=GREEN_3B1B)
            for t in left_bullets_texts
        ])
        left_bullets.arrange(DOWN, buff=0.3)
        left_bullets.next_to(left_header, DOWN, buff=0.3)
        left_bullets.set_x(LEFT[0] * 3.2)

        # Right panel — In Reality
        right_header = Text(
            "In Reality",
            font_size=22,
            color=RED_BRAIN,
            weight=BOLD,
        )
        right_header.move_to(RIGHT * 3.2 + UP * 1.8)

        right_bullets_texts = [
            "• Unmodeled friction, flex",
            "• Expensive fabrication",
            "• No gradient",
        ]
        right_bullets = VGroup(*[
            Text(t, font_size=17, color=RED_BRAIN)
            for t in right_bullets_texts
        ])
        right_bullets.arrange(DOWN, buff=0.3)
        right_bullets.next_to(right_header, DOWN, buff=0.3)
        right_bullets.set_x(RIGHT[0] * 3.2)

        # Sim-to-real gap double arrow + label at bottom center
        gap_arrow = DoubleArrow(
            start=LEFT * 1.2 + DOWN * 1.5,
            end=RIGHT * 1.2 + DOWN * 1.5,
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
        gap_label.next_to(gap_arrow, DOWN, buff=0.22)

        # Animate: left panel, then right panel, then arrow+label
        self.play(
            FadeIn(left_header, shift=RIGHT * 0.2),
            run_time=0.8,
        )
        self.play(
            LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in left_bullets], lag_ratio=0.25),
            run_time=1.0,
        )
        self.play(
            FadeIn(right_header, shift=LEFT * 0.2),
            run_time=0.8,
        )
        self.play(
            LaggedStart(*[FadeIn(b, shift=LEFT * 0.15) for b in right_bullets], lag_ratio=0.25),
            run_time=1.0,
        )
        self.play(
            GrowArrow(gap_arrow),
            Write(gap_label),
            run_time=1.2,
        )
        self.wait(2.0)

        # FadeOut all Section A
        all_A = VGroup(
            title, divider,
            left_header, left_bullets,
            right_header, right_bullets,
            gap_arrow, gap_label,
        )
        self.play(FadeOut(all_A), run_time=1.2)
        self.wait(0.4)

        # ── Section B: Dead fish callback ────────────────────────────
        fish_pos = UP * 0.5

        # Fish body: VMobject with smoothed ellipse-like shape
        fish_body_raw = np.array([
            [ 1.0,  0.0],
            [ 0.85,  0.3],
            [ 0.5,  0.38],
            [ 0.0,  0.38],
            [-0.5,  0.30],
            [-0.85,  0.12],
            [-1.0,  0.0],
            [-0.85, -0.12],
            [-0.5,  -0.30],
            [ 0.0,  -0.38],
            [ 0.5,  -0.38],
            [ 0.85, -0.3],
            [ 1.0,  0.0],
        ])
        fish_body_3d = np.column_stack([fish_body_raw, np.zeros(len(fish_body_raw))])
        fish_body = VMobject(
            color=BLUE_3B1B,
            stroke_width=2.5,
            fill_opacity=0,
        )
        fish_body.set_points_smoothly(fish_body_3d)

        # Tail: Triangle scaled and rotated, attached at left of body
        fish_tail = Triangle(
            color=BLUE_3B1B,
            stroke_width=2.5,
            fill_opacity=0,
        )
        fish_tail.scale(0.35)
        fish_tail.rotate(-PI / 2)
        fish_tail.next_to(fish_body, LEFT, buff=0.0)

        # Eye: small circle at right side of body
        fish_eye = Circle(
            radius=0.09,
            color=BLUE_3B1B,
            stroke_width=2,
            fill_opacity=0,
        )
        fish_eye.move_to(np.array([0.72, 0.15, 0]))

        fish = VGroup(fish_body, fish_tail, fish_eye)
        fish.move_to(fish_pos)

        fish_subtitle = Text(
            "Dead fish. Still swimming.",
            font_size=22,
            color=GRAY_MID,
            slant=ITALIC,
        )
        fish_subtitle.next_to(fish, DOWN, buff=0.4)

        nature_text = Text(
            "Nature did this for 4 billion years.",
            font_size=20,
            color=GRAY_LIGHT,
        )
        nature_text.next_to(fish_subtitle, DOWN, buff=0.5)

        we_text = Text(
            "We just started.",
            font_size=28,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        we_text.next_to(nature_text, DOWN, buff=0.4)

        # Animate
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

        # ── Section C: Final quote ────────────────────────────────────
        all_B = VGroup(fish, fish_subtitle, nature_text, we_text)
        self.play(FadeOut(all_B), run_time=1.2)
        self.wait(0.4)

        quote_line1 = Text(
            '"Intelligence is not in the brain."',
            font_size=28,
            color=GRAY_LIGHT,
        )
        quote_line2 = Text(
            "It is in the WHOLE LOOP —",
            font_size=32,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        quote_line3 = Text(
            "brain, body, and environment interacting.",
            font_size=24,
            color=GRAY_LIGHT,
            slant=ITALIC,
        )

        quote = VGroup(quote_line1, quote_line2, quote_line3)
        quote.arrange(DOWN, buff=0.5)
        quote.move_to(ORIGIN)

        self.play(
            LaggedStart(
                Write(quote_line1),
                Write(quote_line2),
                Write(quote_line3),
                lag_ratio=0.6,
            ),
            run_time=4.0,
        )
        self.wait(3.0)

        # FadeOut quote
        self.play(FadeOut(quote), run_time=1.2)
        self.wait(0.5)

        # "Fin."
        fin_text = Text(
            "Fin.",
            font_size=48,
            color=GRAY_MID,
            slant=ITALIC,
        )
        fin_text.move_to(ORIGIN)
        self.play(FadeIn(fin_text, scale=0.85), run_time=1.2)
        self.wait(2.0)

        # Final FadeOut
        self.play(FadeOut(fin_text), run_time=1.0)
        self.wait(0.5)
