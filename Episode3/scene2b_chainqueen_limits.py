"""
Episode 3, Scene 2B: Why ChainQueen-Style Differentiable Physics Matters
========================================================================

Run:
    manim -pql scene2b_chainqueen_limits.py Scene2BChainQueenLimits
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def info_card(title, lines, color, width=3.55):
    frame = RoundedRectangle(
        width=width,
        height=2.28,
        corner_radius=0.18,
        color=color,
        stroke_width=2,
        fill_color=GRAY_DARKER,
        fill_opacity=0.16,
    )
    head = Text(title, font_size=22, color=color, weight=BOLD)
    head.move_to(frame.get_top() + DOWN * 0.35)
    body = VGroup(*[Text(line, font_size=20, color=GRAY_LIGHT) for line in lines])
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    body.move_to(frame.get_center() + DOWN * 0.22)
    return VGroup(frame, head, body)


def gradient_arc(start, end, drop=0.90, color=RED, stroke_width=2.4):
    """
    Draw a Bezier arc bowing DOWNWARD from `start` to `end`,
    then attach a proper arrowhead at `end`.

    `start` and `end` should be the BOTTOM centres of the boxes.
    `drop`  controls how deep the arc bows (Manim units).
    """
    # Control points pulled DOWN below start/end
    bot_y = min(start[1], end[1]) - drop
    p1 = np.array([start[0], bot_y, 0])
    p2 = np.array([end[0],   bot_y, 0])

    arc = CubicBezier(start, p1, p2, end, color=color, stroke_width=stroke_width)

    # Tangent at end = direction from p2 → end (last Bezier handle)
    tangent = normalize(end - p2)
    angle   = angle_of_vector(tangent)

    tip = Triangle(color=color, fill_color=color, fill_opacity=1.0)
    tip.scale(0.10)
    # Triangle default: pointy side UP (90°). Rotate so it points along tangent.
    tip.rotate(angle - PI / 2)
    tip.move_to(end)

    mid_x = (start[0] + end[0]) / 2
    label = Text("gradient", font_size=18, color=color, weight=BOLD)
    label.move_to(np.array([mid_x, bot_y - 0.30, 0]))

    return VGroup(arc, tip), label


class Scene2BChainQueenLimits(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title ──────────────────────────────────────────────────────────
        title = Text(
            "Why Soft-Robot Physics Is Hard",
            font_size=40,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.36)
        self.play(Write(title, run_time=1.0))
        self.wait(0.35)

        # ── Cards (upper band) ─────────────────────────────────────────────
        cards = VGroup(
            info_card("Deformation", ["flex", "many states"],                  BLUE_3B1B),
            info_card("Contact",     ["ground force", "friction"],             ORANGE_3B1B),
            info_card("Materials",   ["stiffness", "elasticity", "actuators"], GREEN_3B1B),
        ).arrange(RIGHT, buff=0.32)
        cards.scale_to_fit_width(11.2)
        cards.next_to(title, DOWN, buff=0.38)

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.14),
            run_time=1.3,
        )
        self.wait(0.8)

        self.play(cards.animate.scale(0.78).next_to(title, DOWN, buff=0.30), run_time=0.8)

        # ── Lower section ──────────────────────────────────────────────────
        lower_y = -1.20

        # --- Particle grid (left) ---
        grid = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5.2,
            y_length=2.5,
            background_line_style={
                "stroke_color": GRAY_DIM,
                "stroke_width": 1,
                "stroke_opacity": 0.35,
            },
            axis_config={"stroke_opacity": 0},
        )
        grid.move_to(LEFT * 3.1 + UP * lower_y)

        particles = VGroup()
        for i in range(7):
            for j in range(4):
                particles.add(
                    Dot(
                        grid.c2p(-2.0 + i * 0.34, -0.48 + j * 0.28),
                        radius=0.038,
                        color=TEAL_EP2,
                    )
                )
        soft_label = Text("soft body as particles", font_size=18, color=TEAL_EP2)
        soft_label.next_to(grid, DOWN, buff=0.18)

        # --- Flow graph (right) ---
        steps  = ["state",   "physics",   "reward"]
        colors = [BLUE_3B1B, ORANGE_3B1B, GREEN_3B1B]

        graph = VGroup()
        for step, color in zip(steps, colors):
            box  = RoundedRectangle(
                width=1.42, height=0.72,
                corner_radius=0.14,
                color=color,
                stroke_width=2,
            )
            text = Text(step, font_size=18, color=color, weight=BOLD).move_to(box)
            graph.add(VGroup(box, text))

        graph.arrange(RIGHT, buff=0.52)
        graph.move_to(RIGHT * 2.85 + UP * lower_y)

        # Forward arrows (state→physics, physics→reward)
        graph_arrows = VGroup(
            Arrow(
                graph[0][0].get_right(), graph[1][0].get_left(),
                color=GRAY_MID, buff=0.08,
                stroke_width=2.0, max_tip_length_to_length_ratio=0.09,
            ),
            Arrow(
                graph[1][0].get_right(), graph[2][0].get_left(),
                color=GRAY_MID, buff=0.08,
                stroke_width=2.0, max_tip_length_to_length_ratio=0.09,
            ),
        )

        # Gradient arc: reward → state, bowing BELOW the boxes
        arc_start = graph[2][0].get_bottom() + LEFT  * 0.08
        arc_end   = graph[0][0].get_bottom() + RIGHT * 0.08
        back_arrow, back_label = gradient_arc(
            arc_start, arc_end,
            drop=0.78,
            color=RED_BRAIN,
            stroke_width=2.4,
        )

        # ── Animate lower section ──────────────────────────────────────────
        self.play(Create(grid), FadeIn(soft_label), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(p, scale=0.6) for p in particles], lag_ratio=0.01),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[FadeIn(g, scale=0.9) for g in graph], lag_ratio=0.13),
            run_time=0.85,
        )
        self.play(
            GrowArrow(graph_arrows[0]),
            GrowArrow(graph_arrows[1]),
            run_time=0.55,
        )
        # Animate arc separately so tip appears cleanly after arc is drawn
        arc_mob, tip_mob = back_arrow[0], back_arrow[1]
        self.play(Create(arc_mob), run_time=0.7)
        self.play(FadeIn(tip_mob), FadeIn(back_label), run_time=0.4)
        self.wait(0.8)

        # ── Takeaway ───────────────────────────────────────────────────────
        caveat = Text(
            "A gradient is a direction under a model, not a guarantee of global truth.",
            font_size=23,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        caveat.scale_to_fit_width(11.5)
        caveat.to_edge(DOWN, buff=0.42)
        self.play(Write(caveat, run_time=1.2))
        self.wait(2.2)

        self.play(FadeOut(Group(*self.mobjects), run_time=1.1))
        self.wait(0.2)