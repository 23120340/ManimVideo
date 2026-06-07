"""
Episode 2 visual-first deep dives.

These classes keep the original render-list names, but replace the long
seminar-slide pages with visual explanations: cones, maps, charts, pipelines,
and short summary cards.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: F401,F403


def shrink_to_width(mobject, width):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def title_text(text, subtitle=None, font_size=39):
    title = Text(text, font_size=font_size, color=YELLOW_3B1B, weight=BOLD)
    shrink_to_width(title, 11.5)
    if subtitle:
        sub = Text(subtitle, font_size=18, color=GRAY_MID)
        shrink_to_width(sub, 10.8)
        group = VGroup(title, sub).arrange(DOWN, buff=0.12)
    else:
        group = title
    group.to_edge(UP, buff=0.34)
    return group


def caption(text, color=YELLOW_3B1B, width=11.2, buff=0.72, font_size=23):
    cap = Text(text, font_size=font_size, color=color, weight=BOLD)
    shrink_to_width(cap, width)
    cap.to_edge(DOWN, buff=buff)
    return cap


def chip(text, color, width=1.8, height=0.46, font_size=16):
    rect = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.12,
        color=color,
        stroke_width=1.6,
        fill_color=color,
        fill_opacity=0.10,
    )
    label = Text(text, font_size=font_size, color=color, weight=BOLD)
    shrink_to_width(label, width - 0.25)
    label.move_to(rect)
    return VGroup(rect, label)


def small_card(title, body, color, width=3.2, height=1.65):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        color=color,
        stroke_width=2.0,
        fill_color=GRAY_DARKER,
        fill_opacity=0.15,
    )
    head = Text(title, font_size=22, color=color, weight=BOLD)
    shrink_to_width(head, width - 0.35)
    body_text = Text(body, font_size=18, color=GRAY_LIGHT, line_spacing=1.05)
    shrink_to_width(body_text, width - 0.35)
    content = VGroup(head, body_text).arrange(DOWN, buff=0.16)
    if content.height > height - 0.28:
        content.scale_to_fit_height(height - 0.28)
    content.move_to(box)
    return VGroup(box, head, body_text)


def make_robot(center=ORIGIN, width=1.0, height=1.35, color=GRAY_LIGHT):
    body = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        color=color,
        stroke_width=2.0,
        fill_color=GRAY_DARKER,
        fill_opacity=0.28,
    )
    body.move_to(center)
    top = Line(body.get_top() + LEFT * 0.20, body.get_top() + RIGHT * 0.20, color=color, stroke_width=2.0)
    return VGroup(body, top)


def pr_cone(origin, angle=0, fov=45 * DEGREES, length=1.55, color=GREEN_3B1B, opacity=0.22):
    p0 = np.array(origin)
    p1 = p0 + length * np.array([np.cos(angle - fov / 2), np.sin(angle - fov / 2), 0])
    p2 = p0 + length * np.array([np.cos(angle + fov / 2), np.sin(angle + fov / 2), 0])
    cone = Polygon(p0, p1, p2, color=color, stroke_width=1.8, fill_color=color, fill_opacity=opacity)
    dot = Dot(p0, radius=0.065, color=YELLOW_3B1B)
    return VGroup(cone, dot)


def map_box(width=4.8, height=3.0, color=GRAY_MID):
    arena = Rectangle(width=width, height=height, color=color, stroke_width=1.6)
    grid = VGroup()
    for x in np.linspace(-width / 2 + 0.8, width / 2 - 0.8, 4):
        grid.add(Line([x, -height / 2, 0], [x, height / 2, 0], color=GRAY_DARKER, stroke_width=0.8))
    for y in np.linspace(-height / 2 + 0.65, height / 2 - 0.65, 3):
        grid.add(Line([-width / 2, y, 0], [width / 2, y, 0], color=GRAY_DARKER, stroke_width=0.8))
    return VGroup(arena, grid)


def metric_bars(title, before, after, label, color, scale=1.0):
    group = VGroup()
    title_mob = Text(title, font_size=22, color=color, weight=BOLD)
    max_h = 1.55 * scale
    bar_w = 0.45 * scale
    bars = VGroup()
    texts = VGroup()
    for x, val, name, col in [
        (-0.36 * scale, before, "before", GRAY_MID),
        (0.36 * scale, after, "after", color),
    ]:
        bar = Rectangle(
            width=bar_w,
            height=max_h * val,
            color=col,
            stroke_width=1.4,
            fill_color=col,
            fill_opacity=0.75,
        )
        bar.move_to([x, (max_h * val) / 2, 0])
        value = Text(f"{val:.3f}", font_size=15, color=GRAY_LIGHT).next_to(bar, UP, buff=0.08)
        name_text = Text(name, font_size=14, color=col).next_to(bar, DOWN, buff=0.08)
        bars.add(bar)
        texts.add(value, name_text)
    axis = Line(LEFT * 0.95 * scale, RIGHT * 0.95 * scale, color=GRAY_DIM, stroke_width=1.4)
    metric_label = Text(label, font_size=14, color=GRAY_MID)
    metric_label.next_to(axis, DOWN, buff=0.34)
    title_mob.next_to(bars, UP, buff=0.32)
    group.add(title_mob, axis, bars, texts, metric_label)
    return group


def clear_scene(scene):
    scene.play(FadeOut(Group(*scene.mobjects), run_time=0.9))
    scene.wait(0.15)


def _capture_style(target):
    snapshot = []
    for mob in target.family_members_with_points():
        data = {"mob": mob}
        try:
            data["color"] = mob.get_color()
        except Exception:
            pass
        try:
            data["opacity"] = mob.get_opacity()
        except Exception:
            pass
        if hasattr(mob, "get_stroke_width"):
            data["stroke_width"] = mob.get_stroke_width()
            data["stroke_color"] = mob.get_stroke_color()
            data["stroke_opacity"] = mob.get_stroke_opacity()
        if hasattr(mob, "get_fill_opacity"):
            data["fill_color"] = mob.get_fill_color()
            data["fill_opacity"] = mob.get_fill_opacity()
        snapshot.append(data)
    return snapshot


def _restore_style(snapshot):
    for data in snapshot:
        mob = data["mob"]
        if "color" in data and hasattr(mob, "set_color"):
            mob.set_color(data["color"])
        if "opacity" in data and hasattr(mob, "set_opacity"):
            mob.set_opacity(data["opacity"])
        if "stroke_width" in data and hasattr(mob, "set_stroke"):
            mob.set_stroke(
                color=data["stroke_color"],
                width=data["stroke_width"],
                opacity=data["stroke_opacity"],
            )
        if "fill_opacity" in data and hasattr(mob, "set_fill"):
            mob.set_fill(color=data["fill_color"], opacity=data["fill_opacity"])


def _stronger_same_hue(color):
    try:
        base = ManimColor(color)
    except Exception:
        base = WHITE
    return interpolate_color(base, WHITE, 0.24)


def _apply_emphasis(target):
    for mob in target.family_members_with_points():
        if hasattr(mob, "get_stroke_width"):
            sw = mob.get_stroke_width()
            if sw > 0.05:
                mob.set_stroke(
                    color=_stronger_same_hue(mob.get_stroke_color()),
                    width=sw + 0.80,
                    opacity=min(mob.get_stroke_opacity() + 0.25, 1.0),
                )
        if hasattr(mob, "get_fill_opacity"):
            fill_opacity = mob.get_fill_opacity()
            if fill_opacity > 0.04:
                mob.set_fill(
                    color=_stronger_same_hue(mob.get_fill_color()),
                    opacity=min(fill_opacity + 0.16, 0.95),
                )
        if hasattr(mob, "set_opacity"):
            try:
                mob.set_opacity(min(mob.get_opacity() + 0.10, 1.0))
            except Exception:
                pass


def _target_scale_factor(target):
    if target.width > 4.2 or target.height > 2.4:
        return 1.018
    return 1.032


def paced_voiceover(scene, targets, beat_time=12.0, color=None):
    """Emphasize one existing object at a time, then restore it cleanly."""
    active = None
    active_style = None
    active_scale = 1.0

    for target in targets:
        animations = []
        if active is not None:
            animations.append(active.animate.scale(1 / active_scale, about_point=active.get_center()))
            scene.play(*animations, run_time=0.42)
            _restore_style(active_style)

        target_style = _capture_style(target)
        _apply_emphasis(target)
        target_scale = _target_scale_factor(target)
        scene.play(target.animate.scale(target_scale, about_point=target.get_center()), run_time=0.48)
        scene.wait(beat_time)

        active = target
        active_style = target_style
        active_scale = target_scale

    if active is not None:
        scene.play(active.animate.scale(1 / active_scale, about_point=active.get_center()), run_time=0.42)
        _restore_style(active_style)


class Scene8PRSignalDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("What a Photoreceptor Sends", "A PR is a compressed task signal, not a tiny image.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        world = Rectangle(width=4.2, height=2.8, color=GRAY_MID, stroke_width=1.6)
        world.move_to(LEFT * 3.2 + UP * 0.25)

        patches = VGroup()
        patch_data = [
            (-4.40, 0.95, BLUE_3B1B), (-3.65, 0.80, GREEN_3B1B), (-2.95, 0.55, ORANGE_3B1B),
            (-4.20, -0.05, GREEN_3B1B), (-3.25, -0.15, RED_BRAIN), (-2.55, 0.05, YELLOW_3B1B),
            (-4.45, -0.80, GRAY_DIM), (-3.50, -0.78, BLUE_3B1B), (-2.65, -0.82, GREEN_3B1B),
        ]
        for x, y, color in patch_data:
            patches.add(
                Square(
                    side_length=0.42,
                    color=color,
                    fill_color=color,
                    fill_opacity=0.55,
                    stroke_width=1.0
                ).move_to([x, y, 0])
            )

        sensor_origin = world.get_left() + RIGHT * 0.42 + DOWN * 1.05
        cone = pr_cone(sensor_origin, angle=28 * DEGREES, fov=50 * DEGREES, length=1.95)

        # ===== Right panel layout constants =====
        chip_w = 1.35
        chip_gap = 0.22
        output_w = 3 * chip_w + 2 * chip_gap
        panel_x = 3.25

        # PR output card has the exact same width as 3 chips + 2 gaps
        mean_box = small_card(
            "PR output",
            "scalar\nreading",
            GREEN_3B1B,
            width=output_w,
            height=1.65
        )
        mean_box.move_to(RIGHT * panel_x + UP * 0.72)
        mean_box[2].shift(UP * 0.06)

        signal_dot = Dot(radius=0.065, color=GREEN_3B1B)
        signal_label = Text("value", font_size=13, color=GRAY_MID)
        signal_reading = VGroup(signal_dot, signal_label).arrange(RIGHT, buff=0.09)
        signal_reading.move_to(mean_box[0].get_bottom() + UP * 0.24)

        # Straight horizontal arrow
        arrow_y = mean_box[0].get_center()[1]
        arrow_start = np.array([world.get_right()[0] + 0.22, arrow_y, 0])
        arrow_end = np.array([mean_box[0].get_left()[0] - 0.22, arrow_y, 0])
        arrow = Arrow(
            arrow_start,
            arrow_end,
            color=YELLOW_3B1B,
            buff=0,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.08,
        )

        self.play(Create(world), FadeIn(patches, lag_ratio=0.05), run_time=1.1)
        self.play(FadeIn(cone, scale=0.9), run_time=0.7)
        self.play(
            GrowArrow(arrow),
            FadeIn(mean_box, shift=LEFT * 0.12),
            FadeIn(signal_reading, scale=1.2),
            run_time=1.0
        )
        self.wait(3.5)

        positions = [
            ("front", world.get_left() + RIGHT * 0.48 + UP * 0.05, 8 * DEGREES, GREEN_3B1B),
            ("down", world.get_center() + UP * 1.10 + RIGHT * 0.10, -95 * DEGREES, BLUE_3B1B),
            ("side", world.get_right() + LEFT * 0.55 + DOWN * 0.35, 175 * DEGREES, ORANGE_3B1B),
        ]

        # Chips are arranged once, with equal spacing and aligned to PR output
        chips = VGroup(
            chip("front", GREEN_3B1B, width=chip_w),
            chip("down", BLUE_3B1B, width=chip_w),
            chip("side", ORANGE_3B1B, width=chip_w),
        ).arrange(RIGHT, buff=chip_gap)

        chips.next_to(mean_box[0], DOWN, buff=chip_gap)

        for i, (name, origin, angle, color) in enumerate(positions):
            new_cone = pr_cone(
                origin,
                angle=angle,
                fov=42 * DEGREES,
                length=1.55,
                color=color,
                opacity=0.18
            )
            self.play(
                Transform(cone, new_cone),
                signal_dot.animate.set_color(color),
                run_time=0.75
            )
            self.play(FadeIn(chips[i], shift=UP * 0.08), run_time=0.35)
            self.wait(1.25)

        fov_line = VGroup(
            Text("narrow", font_size=18, color=ORANGE_3B1B, weight=BOLD),
            Line(LEFT * 1.15, RIGHT * 1.15, color=GRAY_MID, stroke_width=3).add_tip(tip_length=0.15),
            Text("wide", font_size=18, color=BLUE_3B1B, weight=BOLD),
        ).arrange(RIGHT, buff=0.18)

        fov_line.move_to(np.array([mean_box[0].get_center()[0], -1.28, 0]))

        wide_cone = pr_cone(
            world.get_center() + LEFT * 0.15 + DOWN * 0.05,
            angle=0,
            fov=88 * DEGREES,
            length=1.65,
            color=BLUE_3B1B,
            opacity=0.13
        )

        self.play(FadeIn(fov_line), Transform(cone, wide_cone), run_time=0.9)

        cap = caption("Placement and FOV decide which cue reaches the policy.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)

        paced_voiceover(
            self,
            [title, world, cone, mean_box, signal_reading, chips[0], chips[1], chips[2], fov_line, cap],
            beat_time=11.8
        )
        clear_scene(self)

class Scene9CameraBaselineDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Cameras, Bandwidth, and Baselines", "The fair question is useful information per cost.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        camera_box = RoundedRectangle(width=4.0, height=3.0, corner_radius=0.20, color=BLUE_3B1B, stroke_width=2.0)
        pr_box = RoundedRectangle(width=4.0, height=3.0, corner_radius=0.20, color=GREEN_3B1B, stroke_width=2.0)
        camera_box.move_to(LEFT * 2.9 + UP * 0.35)
        pr_box.move_to(RIGHT * 2.9 + UP * 0.35)
        cam_title = Text("128 x 128 camera", font_size=23, color=BLUE_3B1B, weight=BOLD).move_to(camera_box.get_top() + DOWN * 0.34)
        pr_title = Text("64 photoreceptors", font_size=23, color=GREEN_3B1B, weight=BOLD).move_to(pr_box.get_top() + DOWN * 0.34)
        grid = VGroup()
        for i in range(16):
            for j in range(16):
                grid.add(Square(side_length=0.049, color=BLUE_3B1B, fill_color=BLUE_3B1B, fill_opacity=0.40, stroke_width=0.22))
        grid.arrange_in_grid(rows=16, cols=16, buff=0.011)
        grid.move_to(camera_box.get_center() + DOWN * 0.08)
        dots = VGroup()
        for i in range(8):
            for j in range(8):
                dots.add(Dot(radius=0.031, color=GREEN_3B1B))
        dots.arrange_in_grid(rows=8, cols=8, buff=0.13)
        dots.move_to(pr_box.get_center() + DOWN * 0.08)
        cam_count = Text("16,384 values", font_size=17, color=GRAY_LIGHT).next_to(grid, DOWN, buff=0.22)
        pr_count = Text("64 readings", font_size=17, color=GRAY_LIGHT).next_to(dots, DOWN, buff=0.22)

        self.play(FadeIn(camera_box), FadeIn(pr_box), FadeIn(cam_title), FadeIn(pr_title), run_time=0.8)
        self.play(FadeIn(grid, lag_ratio=0.01), FadeIn(dots, lag_ratio=0.03), run_time=1.2)
        self.play(FadeIn(cam_count), FadeIn(pr_count), run_time=0.55)
        self.wait(3.5)

        baseline_title = Text("A result needs baselines", font_size=30, color=YELLOW_3B1B, weight=BOLD)
        baseline_title.move_to(UP * 1.70)
        baseline_cards = VGroup(
            small_card("blind", "GPS+Compass\nonly?", RED_BRAIN, width=2.25, height=1.28),
            small_card("camera", "rich visual\nreference", BLUE_3B1B, width=2.25, height=1.28),
            small_card("random PR", "low-res by\nchance?", ORANGE_3B1B, width=2.25, height=1.28),
            small_card("optimized PR", "value from\nsearch", GREEN_3B1B, width=2.25, height=1.28),
        ).arrange(RIGHT, buff=0.32)
        baseline_cards.move_to(DOWN * 0.05)
        self.play(FadeOut(VGroup(camera_box, pr_box, cam_title, pr_title, grid, dots, cam_count, pr_count), run_time=0.55))
        self.play(FadeIn(baseline_title, shift=DOWN * 0.08), LaggedStart(*[FadeIn(c, shift=UP * 0.10) for c in baseline_cards], lag_ratio=0.12), run_time=1.4)
        cap = caption("Definition before surprise: input, task, baseline, metric.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, baseline_title, baseline_cards[0], baseline_cards[1], baseline_cards[2], baseline_cards[3], cap], beat_time=12.4)
        clear_scene(self)



class Scene10PointGoalNavDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("PointGoalNav", "The coordinate is known; vision improves the route.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        # ===== Layout constants =====
        CARD_W = 2.65
        SMALL_CARD_H = 0.50
        METRIC_CARD_H = 1.22
        CARD_GAP = 0.28
        CARD_TITLE_FS = 15
        CARD_BODY_FS = 15

        def legend_card(text, color):
            box = RoundedRectangle(
                width=CARD_W,
                height=SMALL_CARD_H,
                corner_radius=0.10,
                color=color,
                stroke_width=1.5,
                fill_color=color,
                fill_opacity=0.08,
            )
            label = Text(text, font_size=CARD_TITLE_FS, color=color, weight=BOLD)
            shrink_to_width(label, CARD_W - 0.25)
            label.move_to(box)
            return VGroup(box, label)

        def metric_card():
            box = RoundedRectangle(
                width=CARD_W,
                height=METRIC_CARD_H,
                corner_radius=0.14,
                color=BLUE_3B1B,
                stroke_width=1.7,
                fill_color=GRAY_DARKER,
                fill_opacity=0.15,
            )
            head = Text("SPL", font_size=20, color=BLUE_3B1B, weight=BOLD)
            body = Text("success +\nshort path", font_size=CARD_BODY_FS, color=GRAY_LIGHT, line_spacing=1.05)

            content = VGroup(head, body).arrange(DOWN, buff=0.12)
            content.move_to(box)

            return VGroup(box, head, body)

        gps_label = legend_card("GPS goal arrow", YELLOW_3B1B)
        blind_tag = legend_card("blind route", RED_BRAIN)
        pr_tag = legend_card("PR helps avoid obstacle", GREEN_3B1B)
        metric = metric_card()

        side_panel = VGroup(gps_label, blind_tag, pr_tag, metric).arrange(
            DOWN,
            buff=CARD_GAP,
            aligned_edge=LEFT
        )
        side_panel.move_to(RIGHT * 4.45 + UP * 0.08)

        # Arena height equals total height of the 4-card side panel
        arena_h = side_panel.height
        arena = map_box(width=6.45, height=arena_h, color=GRAY_MID)
        arena.move_to(LEFT * 1.55 + side_panel.get_center()[1] * UP)

        start = Dot(
            arena[0].get_left() + RIGHT * 0.58 + DOWN * (arena_h * 0.32),
            radius=0.09,
            color=BLUE_3B1B
        )
        goal = Dot(
            arena[0].get_right() + LEFT * 0.58 + UP * (arena_h * 0.32),
            radius=0.13,
            color=GREEN_3B1B
        )

        obstacle = Rectangle(
            width=0.40,
            height=arena_h * 0.58,
            color=GRAY_DARKER,
            fill_color=GRAY_DARKER,
            fill_opacity=0.75
        )
        obstacle.move_to(arena[0].get_center() + RIGHT * 0.28)

        robot = make_robot(start.get_center(), width=0.45, height=0.58, color=BLUE_3B1B)
        cone = pr_cone(
            start.get_center() + RIGHT * 0.18,
            angle=25 * DEGREES,
            fov=48 * DEGREES,
            length=1.12,
            color=GREEN_3B1B,
            opacity=0.18
        )

        gps = Arrow(
            start.get_center(),
            goal.get_center(),
            color=YELLOW_3B1B,
            buff=0.13,
            stroke_width=2.55,
            max_tip_length_to_length_ratio=0.075
        )

        blind_path = VMobject(color=RED_BRAIN, stroke_width=2.7)
        blind_path.set_points_smoothly([
            start.get_center(),
            arena[0].get_center() + RIGHT * 0.23,
            goal.get_center()
        ])

        pr_path = VMobject(color=GREEN_3B1B, stroke_width=2.9)
        pr_path.set_points_smoothly([
            start.get_center(),
            arena[0].get_left() + RIGHT * 1.35 + DOWN * (arena_h * 0.39),
            arena[0].get_center() + RIGHT * 0.50 + DOWN * (arena_h * 0.40),
            arena[0].get_right() + LEFT * 1.18 + DOWN * (arena_h * 0.27),
            goal.get_center(),
        ])

        self.play(Create(arena), FadeIn(start), FadeIn(goal), FadeIn(obstacle), run_time=1.0)
        self.play(GrowArrow(gps), FadeIn(gps_label, shift=LEFT * 0.08), run_time=0.8)
        self.play(FadeIn(robot), FadeIn(cone), run_time=0.65)

        self.wait(1.8)

        self.play(Create(blind_path), run_time=1.0)
        self.play(FadeIn(blind_tag, shift=LEFT * 0.08), run_time=0.35)

        self.play(Create(pr_path), run_time=1.1)
        self.play(FadeIn(pr_tag, shift=LEFT * 0.08), run_time=0.45)

        self.play(FadeIn(metric, shift=UP * 0.08), run_time=0.55)

        cap = caption(
            "Vision helps, but the goal direction is already a non-visual input.",
            width=11.4,
            buff=0.58,
            font_size=22
        )
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)

        paced_voiceover(
            self,
            [title, arena, gps, robot, cone, blind_path, pr_path, side_panel, metric, cap],
            beat_time=12.0
        )
        clear_scene(self)

class Scene11TargetNavDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("TargetNav", "The target must be discovered from visual evidence.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        # ===== Layout constants =====
        ARENA_W = 6.05
        ARENA_H = 3.10

        CARD_W = 2.60
        CARD_GAP = 0.26
        ARROW_H = 0.45

        CARD_TITLE_FS = 18
        CARD_BODY_FS = 15

        # Card height is computed so:
        # green card + gap + arrow + gap + transparent card == arena height
        CARD_H = (ARENA_H - 2 * CARD_GAP - ARROW_H) / 2

        def evidence_card(title_text_str, body_text_str, color):
            box = RoundedRectangle(
                width=CARD_W,
                height=CARD_H,
                corner_radius=0.16,
                color=color,
                stroke_width=1.8,
                fill_color=GRAY_DARKER,
                fill_opacity=0.15,
            )

            head = Text(
                title_text_str,
                font_size=CARD_TITLE_FS,
                color=color,
                weight=BOLD
            )
            shrink_to_width(head, CARD_W - 0.30)

            body = Text(
                body_text_str,
                font_size=CARD_BODY_FS,
                color=GRAY_LIGHT,
                line_spacing=1.0
            )
            shrink_to_width(body, CARD_W - 0.35)

            content = VGroup(head, body).arrange(DOWN, buff=0.10)
            content.move_to(box)

            return VGroup(box, head, body)

        # ===== Left arena =====
        arena = map_box(width=ARENA_W, height=ARENA_H, color=GRAY_MID)
        arena.move_to(LEFT * 2.10 + UP * 0.28)

        robot = make_robot(
            arena[0].get_left() + RIGHT * 0.82 + DOWN * (ARENA_H * 0.30),
            width=0.45,
            height=0.58,
            color=BLUE_3B1B
        )

        target = Circle(
            radius=0.22,
            color=GREEN_3B1B,
            fill_color=GREEN_3B1B,
            fill_opacity=0.78
        )
        target.move_to(arena[0].get_right() + LEFT * 0.78 + UP * (ARENA_H * 0.30))

        unknown = Text("?", font_size=32, color=YELLOW_3B1B, weight=BOLD).move_to(target)

        scan1 = pr_cone(
            robot.get_center() + RIGHT * 0.20,
            angle=5 * DEGREES,
            fov=42 * DEGREES,
            length=1.48,
            color=GRAY_DIM,
            opacity=0.12
        )

        scan2 = pr_cone(
            robot.get_center() + RIGHT * 0.20,
            angle=38 * DEGREES,
            fov=42 * DEGREES,
            length=2.55,
            color=GREEN_3B1B,
            opacity=0.18
        )

        gauge = VGroup(
            Text("PR signal", font_size=22, color=GREEN_3B1B, weight=BOLD),
            Rectangle(width=2.55, height=0.30, color=GRAY_DIM, stroke_width=1.4),
        ).arrange(DOWN, buff=0.18)
        gauge.move_to(RIGHT * 4.20 + UP * 1.10)

        fill = Rectangle(
            width=0.28,
            height=0.30,
            color=GREEN_3B1B,
            fill_color=GREEN_3B1B,
            fill_opacity=0.85,
            stroke_width=0
        )
        fill.move_to(gauge[1].get_left() + RIGHT * 0.14)

        fill_hi = Rectangle(
            width=2.10,
            height=0.30,
            color=GREEN_3B1B,
            fill_color=GREEN_3B1B,
            fill_opacity=0.85,
            stroke_width=0
        )
        fill_hi.move_to(gauge[1].get_left() + RIGHT * 1.05)

        self.play(Create(arena), FadeIn(robot), FadeIn(unknown), run_time=0.9)
        self.play(FadeIn(scan1), FadeIn(gauge), FadeIn(fill), run_time=0.75)
        self.wait(1.4)

        self.play(
            Transform(scan1, scan2),
            FadeOut(unknown),
            FadeIn(target),
            Transform(fill, fill_hi),
            run_time=1.0
        )

        path = VMobject(color=GREEN_3B1B, stroke_width=3.0)
        path.set_points_smoothly([
            robot.get_center(),
            arena[0].get_center() + LEFT * 0.15,
            target.get_center()
        ])
        self.play(Create(path), run_time=1.0)
        self.wait(2.2)

        # ===== Right cards: same total height as arena =====
        green_card = evidence_card(
            "green target",
            "strong cue\nsuccess 0.314",
            GREEN_3B1B
        )

        trans_card = evidence_card(
            "transparent",
            "weak cue\nsuccess 0.132",
            GRAY_MID
        )

        check_arrow = Arrow(
            UP * (ARROW_H / 2),
            DOWN * (ARROW_H / 2),
            color=RED_BRAIN,
            buff=0.04,
            stroke_width=1.7,
            tip_length=0.10,
            max_tip_length_to_length_ratio=0.10
        )

        check = VGroup(green_card, check_arrow, trans_card).arrange(
            DOWN,
            buff=CARD_GAP
        )

        # Right group height equals arena height
        # Green card top is aligned with arena top
        check.next_to(arena, RIGHT, buff=1.05)
        check.align_to(arena[0], UP)

        self.play(FadeOut(VGroup(gauge, fill, scan1, path), run_time=0.45))
        self.play(
            LaggedStart(
                FadeIn(green_card, shift=UP * 0.08),
                FadeIn(check_arrow),
                FadeIn(trans_card, shift=UP * 0.08),
                lag_ratio=0.15
            ),
            run_time=1.1
        )

        cap = caption(
            "The ablation shows which cue the policy was using.",
            width=11.0,
            buff=0.58,
            font_size=22
        )
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)

        paced_voiceover(
            self,
            [title, arena, robot, target, green_card, check_arrow, trans_card, cap],
            beat_time=12.5
        )
        clear_scene(self)

class Scene12DesignVectorDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("The 7D Sensor Design", "A PR is a viewpoint attached to the robot.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        # Left column: physical intuition
        robot = make_robot(LEFT * 3.65 + DOWN * 0.08, width=1.12, height=1.52)
        sensor_origin = robot[0].get_top() + DOWN * 0.25 + RIGHT * 0.10
        cone = pr_cone(
            sensor_origin,
            angle=55 * DEGREES,
            fov=42 * DEGREES,
            length=1.42,
            color=GREEN_3B1B
        )

        left_hint = Text(
            "viewpoint\nattached\nto robot",
            font_size=17,
            color=GRAY_MID,
            line_spacing=0.9
        )
        left_hint.next_to(robot, DOWN, buff=0.22)
        shrink_to_width(left_hint, 2.1)

        # Right column: formula card
        vector = MathTex(
            r"\theta_i=(x,y,z,\mathrm{pitch},\mathrm{yaw},\mathrm{roll},\mathrm{fov})",
            font_size=31,
            color=GRAY_LIGHT,
        )
        shrink_to_width(vector, 6.85)

        vector_box = SurroundingRectangle(
            vector,
            color=emphasis_color_of(vector),
            buff=0.20,
            stroke_width=1.6
        )

        vector_group = VGroup(vector_box, vector)
        vector_group.move_to(RIGHT * 1.70 + UP * 1.45)

        # Sliders: labels are left-aligned with formula card
        slider_names = [
            ("x", BLUE_3B1B),
            ("y", BLUE_3B1B),
            ("z", BLUE_3B1B),
            ("pitch", ORANGE_3B1B),
            ("yaw", ORANGE_3B1B),
            ("roll", ORANGE_3B1B),
            ("fov", GREEN_3B1B),
        ]
        slider_values = [0.34, 0.50, 0.60, 0.55, 0.42, 0.48, 0.70]

        sliders = VGroup()

        PARAM_FONT_SIZE = 23
        ROW_GAP = 0.38
        SLIDER_LENGTH = 2.35

        card_left_x = vector_box.get_left()[0]
        first_row_y = vector_box.get_bottom()[1] - 0.42

        # Fixed slider start, so every label has the same left edge
        slider_start_x = card_left_x + 1.45
        slider_end_x = slider_start_x + SLIDER_LENGTH

        for i, (name, color) in enumerate(slider_names):
            y = first_row_y - i * ROW_GAP

            label = Text(
                name,
                font_size=PARAM_FONT_SIZE,
                color=color,
                weight=BOLD
            )

            # This line forces the parameter label's left edge
            # to align with the formula card's left edge.
            label.move_to([card_left_x + label.width / 2, y, 0])

            base = Line(
                [slider_start_x, y, 0],
                [slider_end_x, y, 0],
                color=GRAY_DIM,
                stroke_width=2.1
            )

            knob = Dot(
                base.point_from_proportion(slider_values[i]),
                radius=0.065,
                color=color
            )

            sliders.add(VGroup(label, base, knob))

        self.play(FadeIn(robot), FadeIn(cone), FadeIn(left_hint), run_time=0.7)
        self.play(Create(vector_box), FadeIn(vector), run_time=0.8)
        self.play(
            LaggedStart(
                *[FadeIn(s, shift=RIGHT * 0.08) for s in sliders],
                lag_ratio=0.08
            ),
            run_time=1.3
        )
        self.wait(1.5)

        # Animate a few parameter changes
        for idx, new_value in [(0, 0.70), (3, 0.68), (6, 0.88)]:
            self.play(
                sliders[idx][2].animate.move_to(
                    sliders[idx][1].point_from_proportion(new_value)
                ),
                cone.animate.set_opacity(0.35),
                run_time=0.45,
            )
            self.play(cone.animate.set_opacity(1.0), run_time=0.25)

        sparse = VGroup()
        for x, y, color in [
            (-0.25, 0.42, BLUE_3B1B),
            (0.28, 0.22, GREEN_3B1B),
            (-0.33, -0.20, ORANGE_3B1B),
            (0.14, -0.42, YELLOW_3B1B),
        ]:
            sparse.add(
                Dot(
                    robot[0].get_center() + np.array([x, y, 0]),
                    radius=0.055,
                    color=color
                )
            )

        self.play(FadeIn(sparse, lag_ratio=0.12), run_time=0.7)

        cap = caption(
            "Multiple PRs form a sparse eye: 7N variables for N sensors.",
            width=11.2,
            buff=0.58,
            font_size=22
        )
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)

        position_group = VGroup(sliders[0], sliders[1], sliders[2])
        orientation_group = VGroup(sliders[3], sliders[4], sliders[5])

        paced_voiceover(
            self,
            [
                title,
                robot,
                cone,
                left_hint,
                vector_group,
                position_group,
                orientation_group,
                sliders[6],
                sparse,
                cap
            ],
            beat_time=12.0
        )

        clear_scene(self)


class Scene13JointOptimizationDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Joint Design and Control", "One rollout teaches both the eye and the policy.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        # ===== Left part: naive search =====
        naive_title = Text("naive search", font_size=25, color=RED_BRAIN, weight=BOLD)
        naive_title.move_to(LEFT * 4.15 + UP * 1.38)

        naive_steps = VGroup(
            chip("choose layout", BLUE_3B1B, width=2.05, height=0.43, font_size=15),
            chip("train policy", ORANGE_3B1B, width=2.05, height=0.43, font_size=15),
            chip("simulate", PURPLE_3B1B, width=2.05, height=0.43, font_size=15),
            chip("score", RED_BRAIN, width=2.05, height=0.43, font_size=15),
        ).arrange(DOWN, buff=0.25)
        naive_steps.move_to(LEFT * 4.15 + DOWN * 0.25)

        naive_arrows = VGroup()
        for i in range(len(naive_steps) - 1):
            naive_arrows.add(
                Arrow(
                    naive_steps[i].get_bottom(),
                    naive_steps[i + 1].get_top(),
                    color=GRAY_MID,
                    buff=0.04,
                    stroke_width=1.35,
                    tip_length=0.075,
                    max_tip_length_to_length_ratio=0.08
                )
            )

        repeat = CurvedArrow(
            naive_steps[-1].get_left() + LEFT * 0.26,
            naive_steps[0].get_left() + LEFT * 0.26,
            angle=-TAU / 4.1,
            color=RED_BRAIN,
            stroke_width=1.8,
            tip_length=0.10,
        )

        # ===== Right part: joint learning =====
        joint_title = Text("joint learning", font_size=25, color=GREEN_3B1B, weight=BOLD)
        joint_title.move_to(RIGHT * 2.55 + UP * 1.38)

        design = small_card(
            "design policy",
            "proposes\nsensor layout",
            GREEN_3B1B,
            width=2.12,
            height=1.18
        )

        control = small_card(
            "control policy",
            "acts from\nobservations",
            BLUE_3B1B,
            width=2.18,
            height=1.18
        )

        reward = small_card(
            "task score",
            "reward /\nsuccess",
            ORANGE_3B1B,
            width=1.98,
            height=1.18
        )

        joint = VGroup(design, control, reward).arrange(RIGHT, buff=0.30)
        joint.move_to(RIGHT * 2.62 + UP * 0.45)

        flow = VGroup(
            Arrow(
                design.get_right(),
                control.get_left(),
                color=GRAY_MID,
                buff=0.08,
                stroke_width=1.35,
                tip_length=0.075,
                max_tip_length_to_length_ratio=0.08
            ),
            Arrow(
                control.get_right(),
                reward.get_left(),
                color=GRAY_MID,
                buff=0.08,
                stroke_width=1.35,
                tip_length=0.075,
                max_tip_length_to_length_ratio=0.08
            ),
        )

        # ===== Divider: exactly between the two parts =====
        left_right_edge = naive_steps.get_right()[0]
        right_left_edge = joint.get_left()[0]
        divider_x = (left_right_edge + right_left_edge) / 2

        divider = DashedLine(
            [divider_x, 1.55, 0],
            [divider_x, -1.70, 0],
            color=GRAY_DIM,
            stroke_width=1.8,
            dash_length=0.14
        )

        # ===== Curved update arrows =====
        update_eye = CurvedArrow(
            reward.get_bottom() + DOWN * 0.10,
            design.get_bottom() + DOWN * 0.10,
            angle=-TAU / 7.8,
            color=PURPLE_3B1B,
            stroke_width=1.7,
            tip_length=0.10,
        )

        # Changed from straight Arrow to CurvedArrow
        update_control = CurvedArrow(
            reward.get_bottom() + DOWN * 0.34,
            control.get_bottom() + DOWN * 0.34,
            angle=-TAU / 8.5,
            color=GREEN_3B1B,
            stroke_width=1.7,
            tip_length=0.10,
        )

        update_label = Text(
            "same rollout",
            font_size=18,
            color=YELLOW_3B1B,
            weight=BOLD
        )
        update_label.move_to(RIGHT * 2.62 + DOWN * 1.32)

        update_group = VGroup(update_eye, update_control, update_label)

        self.play(
            FadeIn(naive_title),
            FadeIn(joint_title),
            Create(divider),
            run_time=0.8
        )

        self.play(
            LaggedStart(
                *[FadeIn(s, shift=UP * 0.08) for s in naive_steps],
                lag_ratio=0.12
            ),
            LaggedStart(
                *[GrowArrow(a) for a in naive_arrows],
                lag_ratio=0.12
            ),
            run_time=1.3
        )

        self.play(Create(repeat), run_time=0.65)

        self.play(
            FadeIn(joint, shift=UP * 0.12),
            LaggedStart(
                *[GrowArrow(a) for a in flow],
                lag_ratio=0.15
            ),
            run_time=1.1
        )

        self.play(
            Create(update_eye),
            Create(update_control),
            FadeIn(update_label),
            run_time=1.0
        )

        cap = caption(
            "The method optimizes the eye and the behavior together.",
            width=11.2,
            buff=0.58,
            font_size=22
        )
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)

        paced_voiceover(
            self,
            [title, naive_steps, repeat, design, control, reward, update_group, cap],
            beat_time=11.8
        )

        clear_scene(self)


class Scene14EvidenceDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Reading the Evidence", "Numbers matter only when the task and metric are clear.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        # ===== Main metric charts =====
        point = metric_bars("PointGoalNav", 0.447, 0.518, "SPL", BLUE_3B1B, scale=0.90)
        point.move_to(LEFT * 0.85 + UP * 0.52)

        target = metric_bars("TargetNav", 0.363, 0.405, "success", ORANGE_3B1B, scale=0.90)
        target.move_to(RIGHT * 2.95 + UP * 0.52)

        # ===== Bottom ablation cards =====
        green_card = small_card(
            "green",
            "success\n0.314",
            GREEN_3B1B,
            width=1.82,
            height=1.05
        )

        trans_card = small_card(
            "transparent",
            "success\n0.132",
            GRAY_MID,
            width=2.05,
            height=1.05
        )

        # Card green canh giữa với PointGoalNav
        green_card.move_to(np.array([
            point.get_center()[0],
            -1.40,
            0
        ]))

        # Card transparent canh giữa với TargetNav
        trans_card.move_to(np.array([
            target.get_center()[0],
            -1.40,
            0
        ]))

        ablation_arrow = Arrow(
            green_card.get_right() + RIGHT * 0.22,
            trans_card.get_left() + LEFT * 0.22,
            color=RED_BRAIN,
            stroke_width=1.6,
            tip_length=0.09,
            max_tip_length_to_length_ratio=0.10
        )

        ablation = VGroup(green_card, ablation_arrow, trans_card)

        # ===== Left trajectory card =====
        # Chiều cao card trái = từ đỉnh "PointGoalNav" đến đáy card green
        traj_top_y = point.get_top()[1]
        traj_bottom_y = green_card.get_bottom()[1]
        traj_h = traj_top_y - traj_bottom_y

        traj_box = RoundedRectangle(
            width=2.75,
            height=traj_h,
            corner_radius=0.18,
            color=GREEN_3B1B,
            stroke_width=2.0,
            fill_color=GRAY_DARKER,
            fill_opacity=0.15
        )

        traj_box.move_to(np.array([
            -4.35,
            (traj_top_y + traj_bottom_y) / 2,
            0
        ]))

        traj_label = Text(
            "82.5% improved",
            font_size=22,
            color=GREEN_3B1B,
            weight=BOLD
        )
        traj_label.move_to(traj_box.get_bottom() + UP * 0.38)

        dots = VGroup()
        points = []

        trajectory_points = [
            (-0.72, -0.48, RED_BRAIN),
            (-0.42, -0.18, ORANGE_3B1B),
            (-0.14, 0.12, YELLOW_3B1B),
            (0.24, 0.42, GREEN_3B1B),
            (0.58, 0.62, GREEN_3B1B),
        ]

        for x, y, color in trajectory_points:
            p = traj_box.get_center() + np.array([x, y, 0])
            points.append(p)
            dots.add(Dot(p, radius=0.065, color=color))

        path = VMobject(color=GREEN_3B1B, stroke_width=2.25)
        path.set_points_smoothly(points)

        # ===== Animations =====
        self.play(
            FadeIn(traj_box),
            Create(path),
            FadeIn(dots, lag_ratio=0.10),
            FadeIn(traj_label),
            run_time=1.2
        )

        self.play(
            FadeIn(point[0]),
            Create(point[1]),
            LaggedStart(
                *[GrowFromEdge(b, DOWN) for b in point[2]],
                lag_ratio=0.16
            ),
            FadeIn(point[3:]),
            run_time=1.2
        )

        self.play(
            FadeIn(target[0]),
            Create(target[1]),
            LaggedStart(
                *[GrowFromEdge(b, DOWN) for b in target[2]],
                lag_ratio=0.16
            ),
            FadeIn(target[3:]),
            run_time=1.2
        )

        self.wait(2.0)

        self.play(FadeIn(ablation, shift=UP * 0.08), run_time=0.9)

        cap = caption(
            "Interpretation: improvement is real, task-specific, and limited.",
            width=11.2,
            buff=0.58,
            font_size=22
        )
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)

        paced_voiceover(
            self,
            [
                title,
                traj_box,
                path,
                point,
                target,
                green_card,
                ablation_arrow,
                trans_card,
                cap
            ],
            beat_time=11.8
        )

        clear_scene(self)


class Scene15SurveyTransferDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Human Survey and Real Robot", "Novel sensor layouts still have to survive deployment.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        # ===== Layout constants =====
        TOP_CARD_H = 1.95
        BOTTOM_CARD_H = 1.35
        HUMAN_W = 3.00
        SEARCH_W = 3.25

        LEFT_X = -3.00
        RIGHT_X = 3.00
        TOP_Y = 0.75
        BOTTOM_Y = -1.00

        # ===== Top-left card: human guess =====
        human_box = RoundedRectangle(
            width=HUMAN_W,
            height=TOP_CARD_H,
            corner_radius=0.18,
            color=BLUE_3B1B,
            stroke_width=2.0,
            fill_color=GRAY_DARKER,
            fill_opacity=0.15,
        )
        human_box.move_to([LEFT_X, TOP_Y, 0])

        human_title = Text("human guess", font_size=22, color=BLUE_3B1B, weight=BOLD)
        human_title.move_to(human_box.get_top() + DOWN * 0.30)

        human_note = Text(
            "symmetry feels natural",
            font_size=16,
            color=GRAY_MID,
            slant=ITALIC
        )

        human_robot = RoundedRectangle(
            width=0.60,
            height=0.82,
            corner_radius=0.12,
            color=GRAY_LIGHT,
            stroke_width=1.5
        )
        human_robot.move_to(human_box.get_center() + DOWN * 0.02)
        human_note.next_to(human_robot, DOWN, buff=0.13)

        human_dots = VGroup(
            Dot(human_robot.get_top() + DOWN * 0.16, radius=0.045, color=YELLOW_3B1B),
            Dot(human_robot.get_left() + RIGHT * 0.12, radius=0.045, color=YELLOW_3B1B),
            Dot(human_robot.get_right() + LEFT * 0.12, radius=0.045, color=YELLOW_3B1B),
        )

        human = VGroup(
            human_box,
            human_title,
            human_robot,
            human_note,
            human_dots
        )

        # ===== Top-right card: computational search =====
        search_box = RoundedRectangle(
            width=SEARCH_W,
            height=TOP_CARD_H,
            corner_radius=0.18,
            color=GREEN_3B1B,
            stroke_width=2.0,
            fill_color=GRAY_DARKER,
            fill_opacity=0.15,
        )
        search_box.move_to([RIGHT_X, TOP_Y, 0])

        search_title = Text("computational search", font_size=22, color=GREEN_3B1B, weight=BOLD)
        shrink_to_width(search_title, SEARCH_W - 0.35)
        search_title.move_to(search_box.get_top() + DOWN * 0.30)

        search_note = Text(
            "odd layout can be useful",
            font_size=16,
            color=GRAY_MID,
            slant=ITALIC
        )

        search_robot = RoundedRectangle(
            width=0.60,
            height=0.82,
            corner_radius=0.12,
            color=GRAY_LIGHT,
            stroke_width=1.5
        )
        search_robot.move_to(search_box.get_center() + DOWN * 0.02)
        search_note.next_to(search_robot, DOWN, buff=0.13)

        search_dots = VGroup(
            Dot(search_robot.get_bottom() + UP * 0.14 + LEFT * 0.08, radius=0.045, color=YELLOW_3B1B),
            Dot(search_robot.get_right() + LEFT * 0.10 + UP * 0.18, radius=0.045, color=YELLOW_3B1B),
            Dot(search_robot.get_center() + LEFT * 0.14 + DOWN * 0.12, radius=0.045, color=YELLOW_3B1B),
        )

        search = VGroup(
            search_box,
            search_title,
            search_robot,
            search_note,
            search_dots
        )

        self.play(
            FadeIn(human, shift=RIGHT * 0.08),
            FadeIn(search, shift=LEFT * 0.08),
            run_time=1.0
        )
        self.wait(2.2)

        # ===== Bottom cards: same width and same column alignment as top cards =====
        sim = small_card(
            "train in sim",
            "rollouts\nand reward",
            BLUE_3B1B,
            width=HUMAN_W,
            height=BOTTOM_CARD_H
        )
        sim.move_to([LEFT_X, BOTTOM_Y, 0])

        real = small_card(
            "deploy real",
            "64 PRs\non robot",
            GREEN_3B1B,
            width=SEARCH_W,
            height=BOTTOM_CARD_H
        )
        real.move_to([RIGHT_X, BOTTOM_Y, 0])

        # Arrow centered between the two bottom cards
        bridge_arrow = Arrow(
            sim.get_right() + RIGHT * 0.25,
            real.get_left() + LEFT * 0.25,
            color=YELLOW_3B1B,
            stroke_width=2.4,
            max_tip_length_to_length_ratio=0.10
        )

        transfer = VGroup(sim, bridge_arrow, real)

        self.play(FadeIn(transfer, shift=UP * 0.08), run_time=1.0)
        self.wait(2.2)

        summary = VGroup(
            small_card(
                "supported",
                "small sensors\ncan work\nin some tasks",
                GREEN_3B1B,
                width=3.7,
                height=1.75
            ),
            small_card(
                "not implied",
                "cameras useless\n4 pixels solve all\nsim equals reality",
                RED_BRAIN,
                width=3.7,
                height=1.75
            ),
        ).arrange(RIGHT, buff=0.75)
        summary.move_to(DOWN * 0.15)

        self.play(FadeOut(VGroup(human, search, transfer), run_time=0.55))
        self.play(FadeIn(summary, shift=UP * 0.08), run_time=1.0)

        cap = caption("Close Episode 2 with evidence and limits, then hand off to physical morphology.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)

        paced_voiceover(
            self,
            [title, summary[0], summary[1], cap],
            beat_time=18.0
        )

        clear_scene(self)
