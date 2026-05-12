"""
scene3.py — Episode 3, Scene 3: Co-Design
"Co-Design: Brain + Body Together"

Shows how gradient updates both controller and body parameters simultaneously,
then visualizes stiffness distribution on a 4-legged robot,
and demonstrates why more parameters → better performance (no curse of dimensionality).
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *


class Scene3CoDesign(Scene):
    def construct(self):
        # ── Background ──────────────────────────────────────────────
        self.camera.background_color = BG_COLOR

        # VO: "Điều thú vị là: khi ta tăng số lượng tham số thiết kế cơ thể,
        #       hiệu năng không giảm — nó tăng. Đây là khác biệt lớn so với
        #       học máy thông thường. Gradient descent đủ mạnh để tận dụng
        #       không gian thiết kế lớn hơn."

        # ── Section A: Title ─────────────────────────────────────────
        title = Text(
            "Co-Design: Brain + Body Together",
            font_size=36,
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.5)

        # ── Section A: Two-loop diagram (bi-level optimization) ──────
        center_pos = DOWN * 0.5

        outer_ellipse = Ellipse(
            width=5.0, height=2.8,
            color=BLUE_3B1B,
            stroke_width=2.5,
            fill_opacity=0,
        )
        outer_ellipse.move_to(center_pos)

        inner_ellipse = Ellipse(
            width=2.8, height=1.5,
            color=GREEN_3B1B,
            stroke_width=2.5,
            fill_opacity=0,
        )
        inner_ellipse.move_to(center_pos)

        outer_label = Text(
            "θ — body design",
            font_size=20,
            color=BLUE_3B1B,
        )
        outer_label.next_to(outer_ellipse, UP, buff=0.2)

        inner_label = Text(
            "φ — controller",
            font_size=20,
            color=GREEN_3B1B,
        )
        inner_label.move_to(center_pos)

        self.play(
            Create(outer_ellipse),
            run_time=1.2,
        )
        self.play(
            Write(outer_label),
            run_time=0.8,
        )
        self.play(
            Create(inner_ellipse),
            run_time=1.0,
        )
        self.play(
            Write(inner_label),
            run_time=0.8,
        )
        self.wait(0.8)

        # Gradient arrows pointing back into ellipses
        grad_theta = MathTex(r"\nabla_\theta \mathcal{L}", font_size=36, color=BLUE_3B1B)
        grad_phi   = MathTex(r"\nabla_\phi \mathcal{L}", font_size=36, color=GREEN_3B1B)

        grads = VGroup(grad_theta, grad_phi)
        grads.arrange(RIGHT, buff=1.0)
        grads.move_to(DOWN * 2.5)

        # Arrows from gradient labels pointing UP toward respective ellipses
        arr_theta = Arrow(
            start=grad_theta.get_top() + UP * 0.05,
            end=outer_ellipse.get_bottom() + DOWN * 0.05,
            color=BLUE_3B1B,
            buff=0.1,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.2,
        )
        arr_phi = Arrow(
            start=grad_phi.get_top() + UP * 0.05,
            end=inner_ellipse.get_bottom() + DOWN * 0.05,
            color=GREEN_3B1B,
            buff=0.1,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.2,
        )

        self.play(
            FadeIn(grad_theta, shift=UP * 0.3),
            FadeIn(grad_phi, shift=UP * 0.3),
            run_time=0.9,
        )
        self.play(
            GrowArrow(arr_theta),
            GrowArrow(arr_phi),
            run_time=1.0,
        )
        self.wait(1.0)

        # FadeOut loops, keep gradient equations
        self.play(
            FadeOut(VGroup(outer_ellipse, outer_label, inner_ellipse, inner_label,
                           arr_theta, arr_phi)),
            run_time=1.0,
        )
        self.wait(0.5)

        # ── Section B: 4-legged robot stiffness visualization ────────
        # Fade out gradient equations, show robot
        self.play(
            FadeOut(VGroup(grad_theta, grad_phi)),
            run_time=0.8,
        )

        # Robot body: top-down schematic
        robot_body = Rectangle(
            width=1.4, height=1.0,
            color=GRAY_MID,
            fill_color=GRAY_DARKER,
            fill_opacity=1.0,
            stroke_width=2.5,
        )
        robot_body.move_to(ORIGIN)

        # 4 legs from body corners to tips
        corners = [
            robot_body.get_corner(UL),
            robot_body.get_corner(UR),
            robot_body.get_corner(DL),
            robot_body.get_corner(DR),
        ]
        leg_offsets = [
            np.array([-0.7,  0.55, 0]),
            np.array([ 0.7,  0.55, 0]),
            np.array([-0.7, -0.55, 0]),
            np.array([ 0.7, -0.55, 0]),
        ]

        legs = VGroup()
        leg_tips = VGroup()
        for corner, offset in zip(corners, leg_offsets):
            tip_pos = corner + offset
            leg_line = Line(corner, tip_pos, color=GRAY_MID, stroke_width=2.5)
            tip_dot = Circle(
                radius=0.13,
                color=RED_BRAIN,
                fill_color=RED_BRAIN,
                fill_opacity=0.85,
                stroke_width=0,
            )
            tip_dot.move_to(tip_pos)
            legs.add(leg_line)
            leg_tips.add(tip_dot)

        # Soft center overlay
        body_center_soft = Circle(
            radius=0.35,
            color=BLUE_3B1B,
            fill_color=BLUE_3B1B,
            fill_opacity=0.4,
            stroke_width=0,
        )
        body_center_soft.move_to(ORIGIN)

        robot_group = VGroup(robot_body, legs)

        # Stiffness legend (right of robot)
        legend_dot_red = Circle(
            radius=0.1,
            color=RED_BRAIN,
            fill_color=RED_BRAIN,
            fill_opacity=0.85,
            stroke_width=0,
        )
        legend_label_red = Text(
            "stiff  (leg tips — push)",
            font_size=16,
            color=RED_BRAIN,
        )
        row1 = VGroup(legend_dot_red, legend_label_red)
        row1.arrange(RIGHT, buff=0.2)

        legend_dot_blue = Circle(
            radius=0.1,
            color=BLUE_3B1B,
            fill_color=BLUE_3B1B,
            fill_opacity=0.7,
            stroke_width=0,
        )
        legend_label_blue = Text(
            "soft   (body center — flex)",
            font_size=16,
            color=BLUE_3B1B,
        )
        row2 = VGroup(legend_dot_blue, legend_label_blue)
        row2.arrange(RIGHT, buff=0.2)

        legend = VGroup(row1, row2)
        legend.arrange(DOWN, buff=0.35)
        legend.move_to(RIGHT * 3.5)

        # Animate robot
        self.play(FadeIn(robot_group), run_time=0.9)
        self.play(
            LaggedStart(*[GrowFromCenter(t) for t in leg_tips], lag_ratio=0.2),
            run_time=1.0,
        )
        self.play(FadeIn(body_center_soft, scale=0.5), run_time=0.8)
        self.play(FadeIn(legend, shift=LEFT * 0.3), run_time=0.9)
        self.wait(1.5)

        # FadeOut robot section
        self.play(
            FadeOut(VGroup(robot_group, leg_tips, body_center_soft, legend)),
            run_time=1.0,
        )
        self.wait(0.3)

        # ── Section C: "No curse of dimensionality" line chart ───────
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1, 0.5],
            x_length=5,
            y_length=3,
            axis_config={
                "color": GRAY_MID,
                "stroke_width": 2,
                "include_tip": True,
            },
        )
        axes.move_to(DOWN * 0.5)

        x_axis_label = Text("# design parameters", font_size=18, color=GRAY_LIGHT)
        x_axis_label.next_to(axes, DOWN, buff=0.3)

        y_axis_label = Text("performance", font_size=18, color=GRAY_LIGHT)
        y_axis_label.next_to(axes, LEFT, buff=0.3)
        y_axis_label.rotate(PI / 2)

        self.play(
            Create(axes),
            FadeIn(x_axis_label),
            FadeIn(y_axis_label),
            run_time=1.2,
        )

        # Naive scaling curve (RED, DASHED) — decreasing
        naive_curve = axes.plot(
            lambda x: 0.85 - 0.12 * x,
            x_range=[0.2, 4.8],
            color=RED_BRAIN,
            stroke_width=2.5,
        )
        naive_curve_dashed = DashedVMobject(naive_curve, num_dashes=18)

        naive_label = Text("naive scaling", font_size=16, color=RED_BRAIN)
        naive_label.move_to(axes.c2p(4.0, 0.42) + RIGHT * 0.5)

        # Co-design curve (GREEN, SOLID) — stays flat then increases
        codesign_curve = axes.plot(
            lambda x: 0.4 + 0.11 * (x - 0.5) ** 1.3 if x >= 0.5 else 0.4,
            x_range=[0.2, 4.8],
            color=GREEN_3B1B,
            stroke_width=2.5,
        )

        codesign_label = Text("co-design", font_size=16, color=GREEN_3B1B)
        codesign_label.move_to(axes.c2p(4.0, 0.72) + RIGHT * 0.4)

        self.play(Create(naive_curve_dashed), run_time=1.2)
        self.play(Write(naive_label), run_time=0.7)
        self.play(Create(codesign_curve), run_time=1.2)
        self.play(Write(codesign_label), run_time=0.7)
        self.wait(0.8)

        # Callout at bottom
        callout_text = Text(
            "More parameters → better, not worse.\nThe curse of dimensionality doesn't apply here.",
            font_size=20,
            color=YELLOW_3B1B,
            weight=BOLD,
            line_spacing=1.35,
        )
        callout_text.to_edge(DOWN, buff=0.5)
        callout_rect = SurroundingRectangle(
            callout_text,
            color=YELLOW_3B1B,
            stroke_width=2,
            buff=0.18,
            corner_radius=0.1,
        )
        self.play(
            Write(callout_text),
            Create(callout_rect),
            run_time=1.8,
        )
        self.wait(2.0)

        # ── FadeOut all ──────────────────────────────────────────────
        all_objects = VGroup(
            title,
            axes, x_axis_label, y_axis_label,
            naive_curve_dashed, naive_label,
            codesign_curve, codesign_label,
            callout_text, callout_rect,
        )
        self.play(FadeOut(all_objects), run_time=1.5)
        self.wait(0.5)
