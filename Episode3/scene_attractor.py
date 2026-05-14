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
            "Design space is chaotic — yet it has STRUCTURE",
            font_size=28, color=YELLOW_3B1B, weight=BOLD,
        )
        title.to_edge(UP, buff=0.45)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1.5)

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
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES)
        self.play(Create(axes), run_time=1.4)

        # ── Lorenz system parameters ────────────────────────────────────
        sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
        dt = 0.008
        n_steps = 2400
        n_trajs = 10

        def lorenz_step(state):
            x, y, z = state
            return np.array([
                x + sigma * (y - x) * dt,
                y + (x * (rho - z) - y) * dt,
                z + (x * y - beta * z) * dt,
            ])

        # 10 starts at distance ε = 1e-3 apart along x
        epsilon = 1e-3
        starts = [np.array([1.0 + i * epsilon, 1.0, 1.0]) for i in range(n_trajs)]

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

            pts = [axes.c2p(*p) for p in traj[::3]]   # ~800 pts per curve
            curve = VMobject(stroke_width=1.6)
            curve.set_points_smoothly(pts)
            curve.set_color(traj_colors[i])
            curve.set_stroke(opacity=0.75)
            curves.add(curve)

            dot = Dot3D(point=axes.c2p(*s), radius=0.06, color=traj_colors[i])
            start_dots.add(dot)

        # ── Show clustered starting points ──────────────────────────────
        self.play(
            LaggedStart(*[FadeIn(d, scale=1.4) for d in start_dots],
                        lag_ratio=0.08),
            run_time=1.4,
        )

        epsilon_label = Text(
            "10 designs, ε = 0.001 apart",
            font_size=22, color=GRAY_LIGHT,
        )
        epsilon_label.to_edge(DOWN, buff=0.7)
        self.add_fixed_in_frame_mobjects(epsilon_label)
        self.play(FadeIn(epsilon_label), run_time=0.7)
        self.wait(0.6)

        # ── Reveal trajectories with slow camera rotation ───────────────
        self.begin_ambient_camera_rotation(rate=0.12)
        self.play(
            LaggedStart(*[Create(c) for c in curves], lag_ratio=0.03),
            run_time=9.0,
        )
        self.wait(2.5)

        # ── Punchline ───────────────────────────────────────────────────
        punch = Text(
            "Chaos — but every trajectory pulled to the same attractor",
            font_size=22, color=YELLOW_3B1B, weight=BOLD,
        )
        punch.to_edge(DOWN, buff=0.7)
        self.add_fixed_in_frame_mobjects(punch)
        self.play(
            FadeOut(epsilon_label),
            Write(punch),
            run_time=1.6,
        )
        self.wait(3.0)

        self.stop_ambient_camera_rotation()

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
