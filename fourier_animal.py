"""
Fourier Epicycles tracing animal silhouettes.

Cách dùng:
    python -m manim -pql fourier_animal.py FourierFish
    python -m manim -pql fourier_animal.py FourierBird
    python -m manim -pql fourier_animal.py FourierCat
    python -m manim -pql fourier_animal.py FourierAll   # 3 con lần lượt

Nguyên lý:
    1. Lấy outline con thú (định nghĩa bằng điểm hoặc SVGMobject)
    2. Coi mỗi điểm (x, y) là số phức x + iy
    3. FFT để tách thành N sóng xoay (mỗi sóng = 1 vòng tròn)
    4. Animate các vòng tròn → đầu bút vẽ lại hình gốc
"""
from __future__ import annotations
import numpy as np
from manim import *

# ---------------------------------------------------------------------------
# Màu sắc 3b1b-style
# ---------------------------------------------------------------------------
BG        = "#1a1a2e"
BLUE_EP   = "#4fc3f7"   # epicycles
ORANGE_EP = "#ff9f43"   # pen tip circle
PATH_COL  = "#f9ca24"   # đường vẽ
GHOST_COL = "#ffffff22" # outline gốc mờ


# ---------------------------------------------------------------------------
# Định nghĩa animal paths (điểm (x, y) normalize về [-1, 1])
# Mỗi hàm trả về np.ndarray shape (N, 2), N ≈ 300-600 điểm, closed loop.
# ---------------------------------------------------------------------------

def _fish_points(n: int = 400) -> np.ndarray:
    """Cá — thân oval + đuôi tam giác."""
    t = np.linspace(0, TAU, n, endpoint=False)

    # Thân: oval nghiêng
    body_x = np.cos(t) * 1.2
    body_y = np.sin(t) * 0.55

    # Đuôi: thêm lõm ở t quanh PI (phần đuôi cá)
    tail_mod = 1 + 0.35 * np.exp(-((t - PI) ** 2) / 0.4) * np.cos(3 * (t - PI))
    x = body_x * tail_mod
    y = body_y

    # Vây lưng nhô lên ở t ≈ PI/2
    fin = 0.18 * np.exp(-((t - PI / 2) ** 2) / 0.08)
    y = y + fin

    pts = np.column_stack([x, y])
    return pts / np.max(np.abs(pts))  # normalize


def _bird_points(n: int = 500) -> np.ndarray:
    """Chim đang bay — hai cánh xoè."""
    t = np.linspace(0, TAU, n, endpoint=False)

    # Thân oval nhỏ
    bx = 0.25 * np.cos(t)
    by = 0.18 * np.sin(t)

    # Cánh trái và phải: dùng superposition sóng
    wing_l = 0.9 * np.exp(-((t - PI * 0.7) ** 2) / 0.25) * (
        np.cos(t - PI * 0.7) * 0.7 - np.sin(t - PI * 0.7) * 0.4
    )
    wing_r = 0.9 * np.exp(-((t - PI * 1.3) ** 2) / 0.25) * (
        -np.cos(t - PI * 1.3) * 0.7 - np.sin(t - PI * 1.3) * 0.4
    )

    x = bx + wing_l + wing_r
    y = by + 0.5 * (
        np.exp(-((t - PI * 0.7) ** 2) / 0.25) * np.sin(t - PI * 0.7) * 0.5
        + np.exp(-((t - PI * 1.3) ** 2) / 0.25) * np.sin(t - PI * 1.3) * 0.5
    )

    pts = np.column_stack([x, y])
    return pts / np.max(np.abs(pts))


def _cat_points(n: int = 500) -> np.ndarray:
    """Mặt mèo: tròn + 2 tai nhọn."""
    t = np.linspace(0, TAU, n, endpoint=False)

    # Đầu tròn
    r = np.ones_like(t)

    # Tai trái (t ≈ PI*0.55) và tai phải (t ≈ PI*0.45 theo chiều kia)
    ear_l = 0.45 * np.exp(-((t - PI * 0.45) ** 2) / 0.015)
    ear_r = 0.45 * np.exp(-((t - PI * 0.55) ** 2) / 0.015)
    r = r + ear_l + ear_r

    # Cằm hơi nhọn ở t=3PI/2
    chin = -0.08 * np.exp(-((t - 3 * PI / 2) ** 2) / 0.05)
    r = r + chin

    x = r * np.cos(t)
    y = r * np.sin(t)
    pts = np.column_stack([x, y])
    return pts / np.max(np.abs(pts))


# ---------------------------------------------------------------------------
# FFT helper
# ---------------------------------------------------------------------------

def fourier_coefficients(pts: np.ndarray, n_terms: int):
    """
    Trả về list (freq, coeff) sắp xếp theo |coeff| giảm dần.
    pts: (N, 2) float array.
    """
    z = pts[:, 0] + 1j * pts[:, 1]
    N = len(z)
    raw = np.fft.fft(z) / N
    freqs = np.fft.fftfreq(N, d=1.0 / N).astype(int)
    order = np.argsort(-np.abs(raw))
    return [(int(freqs[i]), raw[i]) for i in order[:n_terms]]


# ---------------------------------------------------------------------------
# Base Scene
# ---------------------------------------------------------------------------

class _FourierBase(Scene):
    ANIMAL_PTS: np.ndarray = None   # override in subclass
    ANIMAL_NAME: str       = ""
    N_TERMS: int           = 60
    DRAW_TIME: float       = 7.0
    SCALE: float           = 2.8    # scale vào màn hình
    SHOW_GHOST: bool       = True

    def construct(self):
        self.camera.background_color = BG

        pts = self.ANIMAL_PTS * self.SCALE
        coeffs = fourier_coefficients(pts, self.N_TERMS)

        # ── Ghost outline ────────────────────────────────────────────────
        if self.SHOW_GHOST:
            ghost = VMobject(color=GHOST_COL, stroke_width=1.5)
            ghost_pts = np.column_stack([pts, np.zeros(len(pts))])
            ghost.set_points_smoothly(ghost_pts)
            ghost.close_path()
            self.add(ghost)

        # ── Tiêu đề ──────────────────────────────────────────────────────
        title = Text(
            f"Fourier Series  ·  {self.ANIMAL_NAME}  ·  {self.N_TERMS} terms",
            font_size=22, color=WHITE,
        ).to_edge(UP, buff=0.3)
        self.add(title)

        # ── ValueTracker t ∈ [0, 1] ──────────────────────────────────────
        t_track = ValueTracker(0)

        # ── Drawn path ───────────────────────────────────────────────────
        drawn = VMobject(stroke_color=PATH_COL, stroke_width=2.5, fill_opacity=0)
        tip_history: list[np.ndarray] = []

        def _tip(t_val: float) -> np.ndarray:
            center = np.array([0.0, 0.0])
            for freq, coeff in coeffs:
                amp   = abs(coeff)
                phase = np.angle(coeff) + freq * t_val * TAU
                center = center + amp * np.array([np.cos(phase), np.sin(phase)])
            return center

        def update_drawn(mob: VMobject):
            tip = _tip(t_track.get_value())
            tip_history.append(tip)
            if len(tip_history) > 1:
                pts3d = np.column_stack([
                    np.array(tip_history),
                    np.zeros(len(tip_history)),
                ])
                mob.set_points_smoothly(pts3d)

        drawn.add_updater(update_drawn)

        # ── Epicycles (always_redraw) ────────────────────────────────────
        def build_epicycles() -> VGroup:
            grp = VGroup()
            center = np.array([0.0, 0.0])
            t_val  = t_track.get_value()

            for freq, coeff in coeffs:
                amp   = abs(coeff)
                if amp < 0.015:
                    continue
                phase     = np.angle(coeff) + freq * t_val * TAU
                new_center = center + amp * np.array([np.cos(phase), np.sin(phase)])

                opacity = max(0.08, min(0.55, amp / (coeffs[0][1].__abs__() + 1e-9)))

                circ = Circle(
                    radius=float(amp),
                    stroke_color=BLUE_EP,
                    stroke_width=0.8,
                    stroke_opacity=opacity,
                    fill_opacity=0,
                ).move_to([*center, 0])

                spoke = Line(
                    [*center, 0], [*new_center, 0],
                    stroke_color=BLUE_EP,
                    stroke_width=1.2,
                    stroke_opacity=min(0.9, opacity * 1.8),
                )
                grp.add(circ, spoke)
                center = new_center

            # Bút chì (dot ở đầu)
            dot = Dot([*center, 0], radius=0.06, color=ORANGE_EP)
            grp.add(dot)
            return grp

        epicycles = always_redraw(build_epicycles)

        # ── Thêm vào scene ───────────────────────────────────────────────
        self.add(drawn, epicycles)

        # ── Animate ──────────────────────────────────────────────────────
        self.play(
            t_track.animate.set_value(1),
            run_time=self.DRAW_TIME,
            rate_func=linear,
        )
        drawn.remove_updater(update_drawn)

        # Highlight path vừa vẽ
        self.play(
            drawn.animate.set_stroke(color=PATH_COL, width=3, opacity=1),
            FadeOut(epicycles),
            run_time=0.8,
        )
        self.wait(1.5)


# ---------------------------------------------------------------------------
# Concrete scenes
# ---------------------------------------------------------------------------

class FourierFish(_FourierBase):
    ANIMAL_PTS  = _fish_points()
    ANIMAL_NAME = "Cá"
    N_TERMS     = 60


class FourierBird(_FourierBase):
    ANIMAL_PTS  = _bird_points()
    ANIMAL_NAME = "Chim"
    N_TERMS     = 80


class FourierCat(_FourierBase):
    ANIMAL_PTS  = _cat_points()
    ANIMAL_NAME = "Mèo"
    N_TERMS     = 70


# ---------------------------------------------------------------------------
# FourierAll — 3 con lần lượt trên cùng 1 scene
# ---------------------------------------------------------------------------

class FourierAll(Scene):
    """Ba con thú lần lượt, mỗi con ~5s."""

    CONFIGS = [
        (_fish_points(), "Cá",  50, 2.5),
        (_bird_points(), "Chim", 70, 2.4),
        (_cat_points(),  "Mèo", 60, 2.4),
    ]

    def construct(self):
        self.camera.background_color = BG

        for pts_raw, name, n_terms, scale in self.CONFIGS:
            self._render_one(pts_raw * scale, name, n_terms)
            self.wait(0.4)
            self.clear()

    def _render_one(self, pts: np.ndarray, name: str, n_terms: int):
        coeffs = fourier_coefficients(pts, n_terms)

        title = Text(
            f"{name}  ·  {n_terms} vòng tròn Fourier",
            font_size=26, color=WHITE,
        ).to_edge(UP, buff=0.3)
        self.add(title)

        ghost = VMobject(color=GHOST_COL, stroke_width=1.2)
        g3 = np.column_stack([pts, np.zeros(len(pts))])
        ghost.set_points_smoothly(g3)
        ghost.close_path()
        self.add(ghost)

        t_track = ValueTracker(0)
        drawn    = VMobject(stroke_color=PATH_COL, stroke_width=2.5, fill_opacity=0)
        history: list[np.ndarray] = []

        def _tip(tv):
            c = np.array([0.0, 0.0])
            for freq, coeff in coeffs:
                amp   = abs(coeff)
                phase = np.angle(coeff) + freq * tv * TAU
                c += amp * np.array([np.cos(phase), np.sin(phase)])
            return c

        def upd(mob):
            history.append(_tip(t_track.get_value()))
            if len(history) > 1:
                mob.set_points_smoothly(
                    np.column_stack([np.array(history), np.zeros(len(history))])
                )

        drawn.add_updater(upd)

        def build():
            grp = VGroup()
            c = np.array([0.0, 0.0])
            tv = t_track.get_value()
            for freq, coeff in coeffs:
                amp   = abs(coeff)
                if amp < 0.015:
                    continue
                ph     = np.angle(coeff) + freq * tv * TAU
                nc     = c + amp * np.array([np.cos(ph), np.sin(ph)])
                opa    = max(0.08, min(0.5, amp / (abs(coeffs[0][1]) + 1e-9)))
                grp.add(
                    Circle(radius=float(amp), stroke_color=BLUE_EP,
                           stroke_width=0.7, stroke_opacity=opa,
                           fill_opacity=0).move_to([*c, 0]),
                    Line([*c, 0], [*nc, 0], stroke_color=BLUE_EP,
                         stroke_width=1, stroke_opacity=min(0.85, opa * 1.8)),
                )
                c = nc
            grp.add(Dot([*c, 0], radius=0.055, color=ORANGE_EP))
            return grp

        epis = always_redraw(build)
        self.add(drawn, epis)
        self.play(t_track.animate.set_value(1), run_time=5.0, rate_func=linear)
        drawn.remove_updater(upd)
        self.play(drawn.animate.set_stroke(width=3), FadeOut(epis), run_time=0.6)
        self.wait(0.8)
