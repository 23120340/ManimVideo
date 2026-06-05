"""
common.py — Shared assets for "Intelligence in the Body" series
===============================================================

Contains:
  • 3Blue1Brown-style color palette
  • create_fish()         — Fourier-smoothed fish silhouette
  • create_neural_net()  — MLP schematic
  • make_title_card()    — standard title card

Text convention (all scenes follow this):
  • Text(...)       for plain English text
  • MarkupText(...) for subscript / superscript  (e.g. θ<sub>brain</sub>)
  • Never set font= in Text or MarkupText — use the Pango system default.

Import in every scene:
    from common import *
"""

from manim import *
import numpy as np


# ────────────────────────────────────────────────────────────────
# Color palette (3Blue1Brown style)
# ────────────────────────────────────────────────────────────────
BG_COLOR    = "#1C1C1C"
BLUE_3B1B   = "#3B82F6"
YELLOW_3B1B = "#FBBF24"
RED_BRAIN   = "#EF4444"
GREEN_3B1B  = "#10B981"
PURPLE_3B1B = "#A78BFA"
ORANGE_3B1B = "#F97316"
PINK_3B1B   = "#EC4899"
GRAY_LIGHT  = "#E5E7EB"
GRAY_MID    = "#9CA3AF"
GRAY_DIM    = "#6B7280"
GRAY_DARKER = "#374151"


# ────────────────────────────────────────────────────────────────
# Fourier curve smoother
# ────────────────────────────────────────────────────────────────
def fourier_smooth(pts_2d, n_harmonics=8, n_out=150):
    """
    Spectral interpolation of a closed 2-D curve via DFT low-pass filter.

    pts_2d   : (N, 2) ndarray of control points tracing the outline
    n_harmonics : number of Fourier harmonics to keep (higher = more detail)
    n_out    : number of output sample points along the smoothed curve

    Returns (n_out, 3) ndarray of [x, y, 0] ready for VMobject.
    """
    z = pts_2d[:, 0] + 1j * pts_2d[:, 1]
    N = len(z)
    Z = np.fft.fft(z)

    # Zero-pad spectrum to n_out length — this IS spectral interpolation
    Z_pad = np.zeros(n_out, dtype=complex)
    half = min(n_harmonics + 1, (N + 1) // 2)
    Z_pad[:half] = Z[:half]               # DC + positive harmonics
    if half > 1:
        Z_pad[n_out - half + 1:] = Z[N - half + 1:]   # negative harmonics

    z_out = np.fft.ifft(Z_pad) * (n_out / N)
    return np.column_stack([z_out.real, z_out.imag, np.zeros(n_out)])


# ────────────────────────────────────────────────────────────────
# Helper: fish schematic
# ────────────────────────────────────────────────────────────────
def create_fish(color=BLUE_3B1B, stroke_width=2.5):
    """
    Detailed fish silhouette — head right, tail left.

    VGroup layout (backward-compatible):
      [0] body         — closed body outline (Fourier-smoothed)
      [1] tail         — caudal fin;  get_right() ≈ body-tail junction
      [2] eye          — VGroup(ring, dot);  get_center() used for anchors
      [3] spiny_dorsal — large spiny dorsal fin with individual spine lines
      [4] soft_dorsal  — small rounded soft dorsal fin
      [5] pectoral_fin — large fan-shaped side fin with ray lines
    """
    sw = stroke_width

    # ── Body ──────────────────────────────────────────────────────
    # Outline traced clockwise from mouth tip; Fourier-smoothed to 180 pts.
    raw_body = np.array([
        [ 1.55,  0.02],   # mouth tip
        [ 1.48,  0.22],   # upper lip
        [ 1.35,  0.42],   # lower forehead
        [ 1.12,  0.58],   # upper head
        [ 0.88,  0.70],   # nape / pre-dorsal
        [ 0.55,  0.76],   # dorsal front base
        [ 0.20,  0.76],   # mid-back
        [-0.18,  0.72],   # back center
        [-0.52,  0.64],   # back rear
        [-0.88,  0.48],   # caudal peduncle upper
        [-1.18,  0.25],   # caudal peduncle top
        [-1.38,  0.08],   # tail base top
        [-1.42,  0.00],   # tail centre
        [-1.38, -0.08],   # tail base bottom
        [-1.18, -0.25],   # caudal peduncle bottom
        [-0.88, -0.48],   # belly rear
        [-0.52, -0.62],   # belly centre
        [-0.18, -0.68],   # belly mid
        [ 0.20, -0.68],   # belly front-centre
        [ 0.55, -0.62],   # belly front (pectoral area)
        [ 0.90, -0.48],   # lower chest
        [ 1.22, -0.28],   # chest
        [ 1.48, -0.08],   # chin / lower jaw
    ])
    body_pts = fourier_smooth(raw_body, n_harmonics=8, n_out=180)
    body = VMobject(color=color, stroke_width=sw, fill_opacity=0)
    body.set_points_as_corners(body_pts)
    body.close_path()

    mouth = Arc(
        radius=0.10,
        angle=-65 * DEGREES,
        start_angle=200 * DEGREES,
        color=color,
        stroke_width=sw * 0.75,
    )
    mouth.move_to(np.array([1.49, -0.03, 0]))

    # ── Tail (caudal fin) ─────────────────────────────────────────
    tail_root = np.array([-1.40, 0.0])
    top_raw = np.array([
        [tail_root[0], tail_root[1]], [-1.52,  0.12], [-1.65,  0.26],
        [-1.85,  0.44], [-2.08,  0.60], [-2.28,  0.70],
        [-2.18,  0.52], [-2.00,  0.34], [-1.82,  0.18],
        [-1.62,  0.05], [tail_root[0], tail_root[1]],
    ])
    top_lobe = VMobject(color=color, stroke_width=sw, fill_opacity=0)
    top_lobe.set_points_smoothly(
        np.column_stack([top_raw, np.zeros(len(top_raw))]))

    bot_raw = top_raw.copy()
    bot_raw[:, 1] *= -1                    # mirror vertically
    bot_lobe = VMobject(color=color, stroke_width=sw, fill_opacity=0)
    bot_lobe.set_points_smoothly(
        np.column_stack([bot_raw, np.zeros(len(bot_raw))]))

    ray_lines = VGroup()
    for t in np.linspace(0.18, 0.82, 5):
        y = t * 0.70
        x_base = tail_root[0] - 0.06 - t * 0.04
        x_tip  = -1.55 - t * 0.64
        ray_lines.add(
            Line([x_base,  y * 0.18, 0], [x_tip,  y * 0.88, 0],
                 color=color, stroke_width=sw * 0.45),
            Line([x_base, -y * 0.18, 0], [x_tip, -y * 0.88, 0],
                 color=color, stroke_width=sw * 0.45),
        )
    tail = VGroup(top_lobe, bot_lobe, ray_lines)

    # ── Eye ───────────────────────────────────────────────────────
    eye_pos = np.array([1.10, 0.22, 0])
    eye_ring = Circle(radius=0.12, color=color,
                      stroke_width=sw * 0.85, fill_opacity=0)
    eye_ring.move_to(eye_pos)
    eye_dot  = Dot(eye_pos, radius=0.05, color=color)
    eye = VGroup(eye_ring, eye_dot)

    # ── Spiny dorsal fin ──────────────────────────────────────────
    n_sp = 9
    sp_x = np.linspace(0.50, -0.48, n_sp)
    sp_base_y = np.interp(sp_x, [-0.48, 0.50], [0.61, 0.71])
    sp_h = np.array([0.26, 0.36, 0.43, 0.46, 0.44, 0.38, 0.30, 0.21, 0.12])
    sp_tip_y = sp_base_y + sp_h

    membrane_pts = (
        [[sp_x[0], sp_base_y[0], 0]] +
        [[x, y, 0] for x, y in zip(sp_x, sp_tip_y)] +
        [[sp_x[-1], sp_base_y[-1], 0]]
    )
    membrane = VMobject(color=color, stroke_width=sw * 0.9, fill_opacity=0)
    membrane.set_points_smoothly(np.array(membrane_pts))

    spiny_dorsal = VGroup(membrane)
    for x, ty, by in zip(sp_x, sp_tip_y, sp_base_y):
        spiny_dorsal.add(
            Line([x, by, 0], [x, ty, 0],
                 color=color, stroke_width=sw * 0.55))

    # ── Soft dorsal fin ───────────────────────────────────────────
    s_x = np.linspace(-0.50, -0.90, 5)
    s_base_y = np.interp(s_x, [-0.90, -0.50], [0.45, 0.61])
    s_h = np.array([0.22, 0.20, 0.16, 0.11, 0.06])
    s_tip_y = s_base_y + s_h

    sd_pts = (
        [[s_x[0], s_base_y[0], 0]] +
        [[x, y, 0] for x, y in zip(s_x, s_tip_y)] +
        [[s_x[-1], s_base_y[-1], 0]]
    )
    soft_fin_outline = VMobject(color=color, stroke_width=sw * 0.9,
                                fill_opacity=0)
    soft_fin_outline.set_points_smoothly(np.array(sd_pts))

    soft_dorsal = VGroup(soft_fin_outline)
    for x, ty, by in zip(s_x, s_tip_y, s_base_y):
        soft_dorsal.add(
            Line([x, by, 0], [x, ty, 0],
                 color=color, stroke_width=sw * 0.50))

    # ── Pectoral fin ──────────────────────────────────────────────
    pec_raw = np.array([
        [ 0.82, -0.08], [ 0.72,  0.06], [ 0.58,  0.14],
        [ 0.46,  0.06], [ 0.44, -0.12], [ 0.52, -0.32],
        [ 0.66, -0.40], [ 0.80, -0.28], [ 0.82, -0.08],
    ])
    pec_outline = VMobject(color=color, stroke_width=sw * 0.85,
                           fill_opacity=0)
    pec_outline.set_points_smoothly(
        np.column_stack([pec_raw, np.zeros(len(pec_raw))]))

    pec_fin = VGroup(pec_outline)
    ray_base = np.array([0.78, -0.08, 0])
    ray_targets = [
        [0.66,  0.02, 0],
        [0.56, -0.03, 0],
        [0.52, -0.13, 0],
        [0.56, -0.24, 0],
        [0.66, -0.31, 0],
    ]
    for target in ray_targets:
        pec_fin.add(
            Line(ray_base, target,
                 color=color, stroke_width=sw * 0.40))

    return VGroup(VGroup(body, mouth), tail, eye, spiny_dorsal, soft_dorsal, pec_fin)


# ────────────────────────────────────────────────────────────────
# Helper: neural-net schematic
# ────────────────────────────────────────────────────────────────
def create_neural_net(
    layer_sizes,
    radius=0.13, h_buff=0.55, v_buff=0.32,
    node_color=BLUE_3B1B, edge_color=GRAY_DIM,
):
    """Tiny MLP schematic. Returns (full_group, edges_VGroup, layers_list)."""
    layers = []
    for n in layer_sizes:
        layer = VGroup(*[
            Circle(radius=radius, color=node_color,
                   stroke_width=2, fill_opacity=0.25)
            for _ in range(n)
        ])
        layer.arrange(DOWN, buff=v_buff)
        layers.append(layer)

    nodes = VGroup(*layers).arrange(RIGHT, buff=h_buff)
    edges = VGroup()
    for i in range(len(layers) - 1):
        for n1 in layers[i]:
            for n2 in layers[i + 1]:
                edges.add(Line(
                    n1.get_right(), n2.get_left(),
                    stroke_width=1, color=edge_color, stroke_opacity=0.55,
                ))

    return VGroup(edges, nodes), edges, layers


# ────────────────────────────────────────────────────────────────
# Helper: title card
# ────────────────────────────────────────────────────────────────
def make_title_card(title, subtitle=None, title_color=YELLOW_3B1B):
    """Standard 3B1B-style title card — large bold title + optional italic subtitle."""
    title_text = Text(title, font_size=56, color=title_color, weight=BOLD)
    if subtitle:
        sub_text = Text(subtitle, font_size=28, color=GRAY_LIGHT, slant=ITALIC)
        return VGroup(title_text, sub_text).arrange(DOWN, buff=0.4)
    return title_text
