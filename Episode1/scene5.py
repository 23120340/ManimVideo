"""
SCENE 5 — Carl Sims: 30 năm trước (11:00 – 13:00)
==================================================

Tập 1 — "Cá chết vẫn biết bơi"

A. Title card retro: "1994"
B. Quần thể 8 voxel-creature thử di chuyển — đa số ngã, vài con tiến lên
C. Một con biến hình mượt thành con cá schematic ban đầu
D. VO chốt: ý tưởng đó đang hồi sinh sau 30 năm

Run:
    manim -pql scene5.py Scene5CarlSims
"""

from manim import *
import numpy as np
from common import *


# ────────────────────────────────────────────────────────────────
# Helper: voxel creature ngẫu nhiên (2D silhouette)
# ────────────────────────────────────────────────────────────────
def make_voxel_creature(seed, color, scale=0.4):
    """
    Tạo một sinh vật voxel ngẫu nhiên: ô vuông xếp lại với nhau theo grid.
    Trả về VGroup của các Square.
    """
    rng = np.random.default_rng(seed)
    n_blocks = rng.integers(4, 9)
    cell = 0.4

    blocks = VGroup()
    used = set([(0, 0)])
    queue = [(0, 0)]

    # BFS thêm khối kề cạnh — cấu trúc liền mạch
    while len(used) < n_blocks and queue:
        cx, cy = queue.pop(0)
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if len(used) >= n_blocks:
                break
            if rng.random() < 0.6:
                nb = (cx + dx, cy + dy)
                if nb not in used:
                    used.add(nb)
                    queue.append(nb)

    for x, y in used:
        sq = Square(
            side_length=cell, color=color, stroke_width=1.5,
            fill_color=color, fill_opacity=0.6,
        )
        sq.move_to([x * cell, y * cell, 0])
        blocks.add(sq)

    blocks.scale(scale)
    return blocks


class Scene5CarlSims(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ============================================================
        # PART A — Title card retro "1994"
        # ============================================================
        # Hiệu ứng retro: chữ to + viền + 2 đường cắt ngang
        year = Text(
            "1994", font_size=140, color=YELLOW_3B1B, weight=BOLD,
        )
        line_top = Line(LEFT * 4, RIGHT * 4, color=YELLOW_3B1B,
                        stroke_width=2.5).next_to(year, UP, buff=0.5)
        line_bot = Line(LEFT * 4, RIGHT * 4, color=YELLOW_3B1B,
                        stroke_width=2.5).next_to(year, DOWN, buff=0.5)

        retro_caption = Text(
            "Karl Sims  ·  Evolved Virtual Creatures",
            font_size=24, color=GRAY_LIGHT, slant=ITALIC,
        ).next_to(line_bot, DOWN, buff=0.5)

        self.play(Create(line_top), Create(line_bot), run_time=1.0)
        self.play(Write(year), run_time=1.5)
        self.play(FadeIn(retro_caption, shift=UP * 0.2), run_time=0.8)
        self.wait(2.5)

        title_pack = VGroup(year, line_top, line_bot, retro_caption)
        self.play(FadeOut(title_pack), run_time=1.0)

        # ============================================================
        # PART B — Quần thể 8 voxel creatures cố di chuyển
        # ============================================================
        section_label = Text(
            "Evolving to  «go the farthest»",
            font_size=28, color=GRAY_LIGHT, weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(Write(section_label), run_time=0.8)

        # Mặt đất
        ground = Line(LEFT * 7, RIGHT * 7, color=GRAY_DIM, stroke_width=2)
        ground.move_to(DOWN * 2.5)
        self.play(Create(ground), run_time=0.5)

        # 8 sinh vật xếp ngang, bắt đầu cùng vạch xuất phát
        start_x = LEFT * 6.0
        start_line = DashedLine(
            start_x + UP * 2, start_x + DOWN * 2.5,
            color=YELLOW_3B1B, stroke_opacity=0.6, dash_length=0.15,
        )
        start_label = Text(
            "starting line",
            font_size=16, color=YELLOW_3B1B, slant=ITALIC,
        ).next_to(start_line, UP, buff=0.1)

        self.play(Create(start_line), FadeIn(start_label), run_time=0.6)

        # Tạo 8 con
        colors = [BLUE_3B1B, GREEN_3B1B, PURPLE_3B1B, ORANGE_3B1B,
                  PINK_3B1B, YELLOW_3B1B, RED_BRAIN, GRAY_LIGHT]
        creatures = []
        for i in range(8):
            c = make_voxel_creature(seed=i + 1, color=colors[i], scale=0.45)
            c.move_to(start_x + RIGHT * 0.05 + DOWN * 1.85)
            creatures.append(c)

        # Spawn lần lượt
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in creatures],
                        lag_ratio=0.1),
            run_time=1.5,
        )
        self.wait(0.5)

        # Mỗi con "cố đi" theo cách khác nhau:
        # 4 con tiến nhiều, 2 con tiến ít, 2 con ngã
        rng = np.random.default_rng(42)
        success_distances = [4.0, 3.5, 5.5, 0.8, 6.5, 1.2, 4.8, 0.3]

        # Animate parallel
        moves = []
        for c, d in zip(creatures, success_distances):
            # Random wiggle path
            path_anim = Succession(
                c.animate.shift(RIGHT * d * 0.3 + UP * 0.15).rotate(15 * DEGREES),
                c.animate.shift(RIGHT * d * 0.3 + DOWN * 0.15).rotate(-15 * DEGREES),
                c.animate.shift(RIGHT * d * 0.4 + UP * 0.05),
                run_time=1.0,
            )
            # Một số con ngã (rotate 90°)
            if d < 1.5:
                path_anim = c.animate.shift(RIGHT * 0.3 + DOWN * 0.2).rotate(80 * DEGREES)
            moves.append(path_anim)

        self.play(*moves, run_time=3.0)
        self.wait(1.0)

        # Highlight con thắng (di chuyển xa nhất)
        winner_idx = success_distances.index(max(success_distances))
        winner = creatures[winner_idx]
        winner_glow = Circle(
            radius=0.6, color=YELLOW_3B1B, stroke_width=3,
            fill_opacity=0.0,
        ).move_to(winner.get_center())
        winner_label = Text(
            "WINNER",
            font_size=18, color=YELLOW_3B1B, weight=BOLD,
        ).next_to(winner_glow, UP, buff=0.2)

        self.play(Create(winner_glow), Write(winner_label), run_time=1.0)
        self.wait(1.5)

        # Caption: không có thiết kế thủ công
        no_design = Text(
            "No manual design.  Only voxels and a utility function.",
            font_size=22, color=GRAY_LIGHT, slant=ITALIC,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(no_design), run_time=1.8)
        self.wait(2.5)

        # ============================================================
        # PART C — Con winner biến hình thành cá schematic
        # ============================================================
        # Fade các con khác để focus vào winner
        losers = VGroup(*[c for i, c in enumerate(creatures) if i != winner_idx])
        self.play(
            FadeOut(losers),
            FadeOut(VGroup(start_line, start_label, no_design,
                           winner_glow, winner_label, section_label, ground)),
            run_time=1.0,
        )

        # Di winner ra giữa và to lên — Transform sẽ override mọi rotation
        self.play(
            winner.animate.move_to(ORIGIN).scale(1.5),
            run_time=1.0,
        )

        # Transform thành cá (Transform tự lo việc khớp shape, kể cả rotation)
        target_fish = create_fish(color=BLUE_3B1B).scale(1.4).move_to(ORIGIN)
        self.play(Transform(winner, target_fish), run_time=2.5)
        self.wait(1.5)

        # ============================================================
        # PART D — VO chốt: ý tưởng đang hồi sinh
        # ============================================================
        revival_l1 = Text(
            "The same idea:",
            font_size=28, color=GRAY_LIGHT,
        )
        revival_l2 = Text(
            "let computers design bodies.",
            font_size=36, color=YELLOW_3B1B, weight=BOLD,
        )
        revival_group = VGroup(revival_l1, revival_l2).arrange(DOWN, buff=0.3)
        revival_group.to_edge(UP, buff=0.6)

        self.play(Write(revival_l1), run_time=1.0)
        self.play(Write(revival_l2), run_time=1.2)
        self.wait(1.0)

        why_now = Text(
            "30 years later: more compute, more data,\n"
            "new math tools  →  this idea is being revived.",
            font_size=22, color=GRAY_LIGHT, slant=ITALIC,
            line_spacing=0.9,
        ).to_edge(DOWN, buff=0.5)

        self.play(Write(why_now), run_time=2.0)
        self.wait(3.0)

        all_d = VGroup(winner, revival_group, why_now)
        self.play(FadeOut(all_d), run_time=1.5)
        self.wait(0.4)
