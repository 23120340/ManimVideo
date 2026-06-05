"""
scene_attractor.py — Episode 3 supplemental: Design Space Attractor
====================================================================
The Lorenz attractor as a metaphor for co-design optimization landscape:
10 robot designs starting nearly identical diverge chaotically — yet all
get pulled toward the same strange attractor in design space.

Plays between scene3 (Co-Design) and scene4 (DiffuseBot).

Run: manim -pql scene_attractor.py SceneAttractor
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import numpy as np


class SceneAttractor(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title (fixed in frame, doesn't rotate with camera) ──────────
        title = Text(
            "Chaotic Design Space, Structured Attractor",
            font_size=28, color=YELLOW_3B1B, weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)
        title.set_opacity(0)
        self.add_fixed_in_frame_mobjects(title)
        self.play(title.animate.set_opacity(1), run_time=1.5)

        # ── 3D axes ─────────────────────────────────────────────────────
        axes = ThreeDAxes(
            x_range=[-30, 30, 10],
            y_range=[-30, 30, 10],
            z_range=[0, 55, 10],
            x_length=5.5,
            y_length=5.5,
            z_length=3.8,
            axis_config={"color": GRAY_DIM, "stroke_width": 1.2},
        )
        axes.scale(0.54)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES)

        # ── Lorenz system parameters ────────────────────────────────────
        sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
        dt = 0.008
        n_steps = 1800
        n_trajs = 10

        def lorenz_step(state):
            x, y, z = state
            return np.array([
                x + sigma * (y - x) * dt,
                y + (x * (rho - z) - y) * dt,
                z + (x * y - beta * z) * dt,
            ])

        # 10 starts at distance ε = 1e-3 apart, centered in the visible axes.
        epsilon = 1e-3
        start_center = np.array([0.0, 0.0, 27.5])
        starts = [
            start_center + np.array([(i - (n_trajs - 1) / 2) * epsilon, 0.0, 0.0])
            for i in range(n_trajs)
        ]

        traj_colors = [
            BLUE_3B1B, GREEN_3B1B, YELLOW_3B1B, RED_BRAIN, PURPLE_3B1B,
            ORANGE_3B1B, TEAL_EP2, PINK_3B1B, GRAY_LIGHT, "#60A5FA",
        ]

        # Pre-compute trajectories, subsample for performance.
        curves = VGroup()
        start_dots = VGroup()
        for i, s in enumerate(starts):
            traj = [s.copy()]
            state = s.copy()
            for _ in range(n_steps):
                state = lorenz_step(state)
                traj.append(state.copy())

            pts = [axes.c2p(*p) for p in traj[::7]]   # ~260 pts per curve
            curve = VMobject(stroke_width=1.6)
            curve.set_points_smoothly(pts)
            curve.set_color(traj_colors[i])
            curve.set_stroke(opacity=0.75)
            curves.add(curve)

            dot = Dot3D(point=axes.c2p(*s), radius=0.06, color=traj_colors[i])
            start_dots.add(dot)

        # The camera projection pulls tall 3D objects upward and left. Shift the
        # whole plot after creating every point so the visible attractor, not only
        # the mathematical origin, sits in the visual center of the frame.
        plot_group = VGroup(axes, curves, start_dots)
        plot_group.shift(RIGHT * 3.10 + DOWN * 3.55)

        self.play(Create(axes), run_time=1.4)

        def make_caption(text, color=GRAY_LIGHT, weight=NORMAL):
            caption_lines = []
            for line in text.split("\n"):
                words = VGroup(*[
                    Text(word, font_size=22, color=color, weight=weight)
                    for word in line.split()
                ])
                words.arrange(RIGHT, buff=0.12)
                caption_lines.append(words)

            caption = VGroup(*caption_lines)
            caption.arrange(DOWN, buff=0.08)
            caption.to_edge(DOWN, buff=0.55)
            caption.set_opacity(0)
            self.add_fixed_in_frame_mobjects(caption)
            return caption

        def replace_caption(old_caption, new_caption):
            self.play(
                old_caption.animate.set_opacity(0).shift(DOWN * 0.08),
                run_time=0.3,
            )
            new_caption.shift(DOWN * 0.08)
            self.play(
                new_caption.animate.set_opacity(1).shift(UP * 0.08),
                run_time=0.45,
            )
            self.remove(old_caption)
            return new_caption

        # ── Show clustered starting points ──────────────────────────────
        self.play(
            LaggedStart(*[FadeIn(d, scale=1.4) for d in start_dots],
                        lag_ratio=0.08),
            run_time=1.4,
        )

        caption = make_caption("10 starts\nnearly identical")
        caption.shift(DOWN * 0.08)
        self.play(caption.animate.set_opacity(1).shift(UP * 0.08), run_time=0.55)
        self.wait(1.7)

        # ── Reveal trajectories, then rotate the plot in place ──────────
        path_caption = make_caption("Tiny changes\ndifferent paths")
        caption = replace_caption(caption, path_caption)

        self.play(
            LaggedStart(*[Create(c) for c in curves], lag_ratio=0.03),
            run_time=6.4,
        )
        self.play(
            Rotate(
                plot_group,
                angle=-18 * DEGREES,
                axis=OUT,
                about_point=plot_group.get_center(),
            ),
            run_time=1.4,
            rate_func=smooth,
        )

        # ── Punchline ───────────────────────────────────────────────────
        punch = make_caption(
            "Different paths, same attractor basin",
            color=YELLOW_3B1B,
            weight=BOLD,
        )
        punch.to_edge(DOWN, buff=0.7)
        punch.set_opacity(0)
        self.play(caption.animate.set_opacity(0).shift(DOWN * 0.08), run_time=0.3)
        punch.shift(DOWN * 0.08)
        self.play(punch.animate.set_opacity(1).shift(UP * 0.08), run_time=0.5)
        self.wait(2.5)

        # ── FadeOut everything ──────────────────────────────────────────
        self.play(
            FadeOut(curves),
            FadeOut(start_dots),
            FadeOut(axes),
            FadeOut(title),
            FadeOut(punch),
            run_time=1.6,
        )
        self.wait(0.4)
