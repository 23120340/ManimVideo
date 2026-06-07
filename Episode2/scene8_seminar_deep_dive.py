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


def paced_voiceover(scene, targets, beat_time=12.0, color=None):
    """Emphasize the narration target by strengthening its original color."""
    active = None
    active_style = None
    scale_factor = 1.045

    for target in targets:
        target_style = _capture_style(target)
        _apply_emphasis(target)
        animations = [target.animate.scale(scale_factor, about_point=target.get_center())]
        if active is not None:
            _restore_style(active_style)
            animations.append(active.animate.scale(1 / scale_factor, about_point=active.get_center()))
        scene.play(*animations, run_time=0.65)
        scene.wait(beat_time)

        active = target
        active_style = target_style

    if active is not None:
        _restore_style(active_style)
        scene.play(active.animate.scale(1 / scale_factor, about_point=active.get_center()), run_time=0.5)


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
            patches.add(Square(side_length=0.42, color=color, fill_color=color, fill_opacity=0.55, stroke_width=1.0).move_to([x, y, 0]))
        sensor_origin = world.get_left() + RIGHT * 0.42 + DOWN * 1.05
        cone = pr_cone(sensor_origin, angle=28 * DEGREES, fov=50 * DEGREES, length=1.95)
        mean_box = small_card("PR output", "one scalar\nfrom cone", GREEN_3B1B, width=2.50, height=1.60)
        mean_box.move_to(RIGHT * 3.05 + UP * 0.72)
        signal_dot = Dot(mean_box[0].get_bottom() + UP * 0.22, radius=0.08, color=GREEN_3B1B)
        arrow = Arrow(world.get_right(), mean_box.get_left(), color=YELLOW_3B1B, buff=0.22, stroke_width=2.5, max_tip_length_to_length_ratio=0.08)

        self.play(Create(world), FadeIn(patches, lag_ratio=0.05), run_time=1.1)
        self.play(FadeIn(cone, scale=0.9), run_time=0.7)
        self.play(GrowArrow(arrow), FadeIn(mean_box, shift=LEFT * 0.12), FadeIn(signal_dot, scale=1.4), run_time=1.0)
        self.wait(3.5)

        positions = [
            ("front", world.get_left() + RIGHT * 0.48 + UP * 0.05, 8 * DEGREES, GREEN_3B1B),
            ("down", world.get_center() + UP * 1.10 + RIGHT * 0.10, -95 * DEGREES, BLUE_3B1B),
            ("side", world.get_right() + LEFT * 0.55 + DOWN * 0.35, 175 * DEGREES, ORANGE_3B1B),
        ]
        chips = VGroup()
        for name, origin, angle, color in positions:
            new_cone = pr_cone(origin, angle=angle, fov=42 * DEGREES, length=1.55, color=color, opacity=0.18)
            self.play(Transform(cone, new_cone), signal_dot.animate.set_color(color), run_time=0.75)
            c = chip(name, color, width=1.35).move_to(RIGHT * 2.1 + DOWN * 0.45 + RIGHT * len(chips) * 1.5)
            chips.add(c)
            self.play(FadeIn(c, shift=UP * 0.08), run_time=0.35)
            self.wait(1.25)

        fov_line = VGroup(
            Text("narrow", font_size=18, color=ORANGE_3B1B, weight=BOLD),
            Line(LEFT * 1.15, RIGHT * 1.15, color=GRAY_MID, stroke_width=3).add_tip(tip_length=0.15),
            Text("wide", font_size=18, color=BLUE_3B1B, weight=BOLD),
        ).arrange(RIGHT, buff=0.18)
        fov_line.move_to(RIGHT * 2.8 + DOWN * 1.28)
        wide_cone = pr_cone(world.get_center() + LEFT * 0.15 + DOWN * 0.05, angle=0, fov=88 * DEGREES, length=1.65, color=BLUE_3B1B, opacity=0.13)
        self.play(FadeIn(fov_line), Transform(cone, wide_cone), run_time=0.9)
        cap = caption("Placement and FOV decide which cue reaches the policy.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, world, cone, mean_box, signal_dot, chips[0], chips[1], chips[2], fov_line, cap], beat_time=11.8)
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
        cam_title = Text("128 x 128 camera", font_size=24, color=BLUE_3B1B, weight=BOLD).move_to(camera_box.get_top() + DOWN * 0.38)
        pr_title = Text("64 photoreceptors", font_size=24, color=GREEN_3B1B, weight=BOLD).move_to(pr_box.get_top() + DOWN * 0.38)
        grid = VGroup()
        for i in range(16):
            for j in range(16):
                grid.add(Square(side_length=0.055, color=BLUE_3B1B, fill_color=BLUE_3B1B, fill_opacity=0.40, stroke_width=0.25))
        grid.arrange_in_grid(rows=16, cols=16, buff=0.012)
        grid.move_to(camera_box.get_center() + DOWN * 0.05)
        dots = VGroup()
        for i in range(8):
            for j in range(8):
                dots.add(Dot(radius=0.035, color=GREEN_3B1B))
        dots.arrange_in_grid(rows=8, cols=8, buff=0.14)
        dots.move_to(pr_box.get_center() + DOWN * 0.05)
        cam_count = Text("16,384 values", font_size=19, color=GRAY_LIGHT).next_to(grid, DOWN, buff=0.25)
        pr_count = Text("64 readings", font_size=19, color=GRAY_LIGHT).next_to(dots, DOWN, buff=0.25)

        self.play(FadeIn(camera_box), FadeIn(pr_box), FadeIn(cam_title), FadeIn(pr_title), run_time=0.8)
        self.play(FadeIn(grid, lag_ratio=0.01), FadeIn(dots, lag_ratio=0.03), run_time=1.2)
        self.play(FadeIn(cam_count), FadeIn(pr_count), run_time=0.55)
        self.wait(3.5)

        baseline_title = Text("A result needs baselines", font_size=30, color=YELLOW_3B1B, weight=BOLD)
        baseline_title.move_to(UP * 1.70)
        baseline_cards = VGroup(
            small_card("blind", "GPS+Compass\nonly?", RED_BRAIN, width=2.4, height=1.35),
            small_card("camera", "rich visual\nreference", BLUE_3B1B, width=2.4, height=1.35),
            small_card("random PR", "low-res by\nchance?", ORANGE_3B1B, width=2.4, height=1.35),
            small_card("optimized PR", "value from\nsearch", GREEN_3B1B, width=2.4, height=1.35),
        ).arrange(RIGHT, buff=0.26)
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

        arena = map_box(width=6.8, height=3.65, color=GRAY_MID)
        arena.move_to(LEFT * 1.2 + UP * 0.25)
        start = Dot(arena[0].get_left() + RIGHT * 0.55 + DOWN * 0.95, radius=0.09, color=BLUE_3B1B)
        goal = Dot(arena[0].get_right() + LEFT * 0.60 + UP * 0.95, radius=0.13, color=GREEN_3B1B)
        obstacle = Rectangle(width=0.38, height=2.15, color=GRAY_DARKER, fill_color=GRAY_DARKER, fill_opacity=0.75)
        obstacle.move_to(arena[0].get_center() + RIGHT * 0.25)
        gps = Arrow(start.get_center(), goal.get_center(), color=YELLOW_3B1B, buff=0.12, stroke_width=2.5, max_tip_length_to_length_ratio=0.08)
        gps_label = chip("GPS goal arrow", YELLOW_3B1B, width=2.55).next_to(arena, RIGHT, buff=0.35).shift(UP * 1.05)
        robot = make_robot(start.get_center(), width=0.45, height=0.58, color=BLUE_3B1B)
        cone = pr_cone(start.get_center() + RIGHT * 0.18, angle=25 * DEGREES, fov=48 * DEGREES, length=1.15, color=GREEN_3B1B, opacity=0.18)

        blind_path = VMobject(color=RED_BRAIN, stroke_width=3.0)
        blind_path.set_points_smoothly([start.get_center(), arena[0].get_center() + RIGHT * 0.25, goal.get_center()])
        pr_path = VMobject(color=GREEN_3B1B, stroke_width=3.0)
        pr_path.set_points_smoothly([
            start.get_center(),
            arena[0].get_left() + RIGHT * 1.55 + DOWN * 1.20,
            arena[0].get_center() + RIGHT * 0.95 + DOWN * 1.28,
            arena[0].get_right() + LEFT * 1.10 + DOWN * 0.75,
            goal.get_center(),
        ])

        self.play(Create(arena), FadeIn(start), FadeIn(goal), FadeIn(obstacle), run_time=1.0)
        self.play(GrowArrow(gps), FadeIn(gps_label, shift=LEFT * 0.08), run_time=0.8)
        self.play(FadeIn(robot), FadeIn(cone), run_time=0.65)
        self.wait(1.8)
        self.play(Create(blind_path), run_time=1.0)
        blind_tag = chip("blind route", RED_BRAIN, width=2.55).next_to(gps_label, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(blind_tag), run_time=0.35)
        self.play(Create(pr_path), run_time=1.1)
        pr_tag = chip("PR helps avoid obstacle", GREEN_3B1B, width=2.55).next_to(blind_tag, DOWN, buff=0.20, aligned_edge=LEFT)
        self.play(FadeIn(pr_tag), run_time=0.45)
        metric = small_card("SPL", "success +\nshort path", BLUE_3B1B, width=2.55, height=1.25)
        metric.next_to(pr_tag, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(metric, shift=UP * 0.08), run_time=0.55)
        cap = caption("Vision helps, but the goal direction is already a non-visual input.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, arena, gps, robot, cone, blind_path, pr_path, metric, cap], beat_time=12.0)
        clear_scene(self)


class Scene11TargetNavDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("TargetNav", "The target must be discovered from visual evidence.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        arena = map_box(width=6.3, height=3.45, color=GRAY_MID)
        arena.move_to(LEFT * 1.55 + UP * 0.35)
        robot = make_robot(arena[0].get_left() + RIGHT * 0.75 + DOWN * 0.9, width=0.45, height=0.58, color=BLUE_3B1B)
        target = Circle(radius=0.20, color=GREEN_3B1B, fill_color=GREEN_3B1B, fill_opacity=0.75)
        target.move_to(arena[0].get_right() + LEFT * 0.75 + UP * 0.75)
        unknown = Text("?", font_size=32, color=YELLOW_3B1B, weight=BOLD).move_to(target)
        scan1 = pr_cone(robot.get_center() + RIGHT * 0.20, angle=5 * DEGREES, fov=42 * DEGREES, length=1.55, color=GRAY_DIM, opacity=0.12)
        scan2 = pr_cone(robot.get_center() + RIGHT * 0.20, angle=38 * DEGREES, fov=42 * DEGREES, length=2.55, color=GREEN_3B1B, opacity=0.18)
        gauge = VGroup(
            Text("PR signal", font_size=22, color=GREEN_3B1B, weight=BOLD),
            Rectangle(width=2.45, height=0.28, color=GRAY_DIM, stroke_width=1.4),
        ).arrange(DOWN, buff=0.18)
        gauge.move_to(RIGHT * 3.75 + UP * 0.75)
        fill = Rectangle(width=0.25, height=0.28, color=GREEN_3B1B, fill_color=GREEN_3B1B, fill_opacity=0.85, stroke_width=0)
        fill.move_to(gauge[1].get_left() + RIGHT * 0.125)
        fill_hi = Rectangle(width=2.05, height=0.28, color=GREEN_3B1B, fill_color=GREEN_3B1B, fill_opacity=0.85, stroke_width=0)
        fill_hi.move_to(gauge[1].get_left() + RIGHT * 1.025)

        self.play(Create(arena), FadeIn(robot), FadeIn(unknown), run_time=0.9)
        self.play(FadeIn(scan1), FadeIn(gauge), FadeIn(fill), run_time=0.75)
        self.wait(1.4)
        self.play(Transform(scan1, scan2), FadeOut(unknown), FadeIn(target), Transform(fill, fill_hi), run_time=1.0)
        path = VMobject(color=GREEN_3B1B, stroke_width=3.0)
        path.set_points_smoothly([robot.get_center(), arena[0].get_center() + LEFT * 0.2, target.get_center()])
        self.play(Create(path), run_time=1.0)
        self.wait(2.2)

        green_card = small_card("green target", "strong cue\nsuccess 0.314", GREEN_3B1B, width=2.65, height=1.45)
        trans_card = small_card("transparent", "weak cue\nsuccess 0.132", GRAY_MID, width=2.65, height=1.45)
        check_arrow = Arrow(DOWN * 0.32, UP * 0.32, color=RED_BRAIN, buff=0.06, stroke_width=2.1, max_tip_length_to_length_ratio=0.10).rotate(-90 * DEGREES)
        check = VGroup(green_card, check_arrow, trans_card).arrange(RIGHT, buff=0.32)
        check.move_to(RIGHT * 3.05 + DOWN * 0.65)
        self.play(FadeOut(VGroup(gauge, fill, scan1, path), run_time=0.45))
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.08) for m in check], lag_ratio=0.15), run_time=1.1)
        cap = caption("The ablation shows which cue the policy was using.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, arena, robot, target, check[0], check[1], check[2], cap], beat_time=12.5)
        clear_scene(self)


class Scene12DesignVectorDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("The 7D Sensor Design", "A PR is a viewpoint attached to the robot.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        robot = make_robot(LEFT * 4.2 + DOWN * 0.05, width=1.0, height=1.35)
        sensor_origin = robot[0].get_top() + DOWN * 0.25 + RIGHT * 0.10
        cone = pr_cone(sensor_origin, angle=55 * DEGREES, fov=42 * DEGREES, length=1.25, color=GREEN_3B1B)
        vector = MathTex(
            r"\theta_i=(x,y,z,\mathrm{pitch},\mathrm{yaw},\mathrm{roll},\mathrm{fov})",
            font_size=31,
            color=GRAY_LIGHT,
        )
        shrink_to_width(vector, 7.6)
        vector_box = SurroundingRectangle(vector, color=emphasis_color_of(vector), buff=0.20, stroke_width=1.6)
        vector_group = VGroup(vector_box, vector).move_to(RIGHT * 1.25 + UP * 1.85)

        slider_names = [
            ("x", BLUE_3B1B), ("y", BLUE_3B1B), ("z", BLUE_3B1B),
            ("pitch", ORANGE_3B1B), ("yaw", ORANGE_3B1B), ("roll", ORANGE_3B1B),
            ("fov", GREEN_3B1B),
        ]
        sliders = VGroup()
        for i, (name, color) in enumerate(slider_names):
            base = Line(LEFT * 0.75, RIGHT * 0.75, color=GRAY_DIM, stroke_width=2.0)
            knob = Dot(base.get_left() + RIGHT * (0.35 + 0.18 * (i % 4)), radius=0.06, color=color)
            label = Text(name, font_size=17, color=color, weight=BOLD).next_to(base, LEFT, buff=0.18)
            sliders.add(VGroup(label, base, knob))
        sliders.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        sliders.move_to(RIGHT * 1.2 + DOWN * 0.25)

        self.play(FadeIn(robot), FadeIn(cone), run_time=0.7)
        self.play(Create(vector_box), FadeIn(vector), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.08) for s in sliders], lag_ratio=0.08), run_time=1.3)
        self.wait(1.5)

        for idx, shift_vec in [(0, RIGHT * 0.25), (3, UP * 0.15), (6, RIGHT * 0.35)]:
            self.play(sliders[idx][2].animate.shift(shift_vec), cone.animate.set_opacity(0.35), run_time=0.45)
            self.play(cone.animate.set_opacity(1.0), run_time=0.25)

        sparse = VGroup()
        for x, y, color in [(-0.25, 0.42, BLUE_3B1B), (0.28, 0.22, GREEN_3B1B), (-0.33, -0.20, ORANGE_3B1B), (0.14, -0.42, YELLOW_3B1B)]:
            sparse.add(Dot(robot[0].get_center() + np.array([x, y, 0]), radius=0.055, color=color))
        self.play(FadeIn(sparse, lag_ratio=0.12), run_time=0.7)
        cap = caption("Multiple PRs form a sparse eye: 7N variables for N sensors.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, robot, cone, vector_group, sliders[0], sliders[3], sliders[6], sparse, cap], beat_time=12.0)
        clear_scene(self)


class Scene13JointOptimizationDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Joint Design and Control", "One rollout teaches both the eye and the policy.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        naive_title = Text("naive search", font_size=26, color=RED_BRAIN, weight=BOLD)
        joint_title = Text("joint learning", font_size=26, color=GREEN_3B1B, weight=BOLD)
        naive_title.move_to(LEFT * 3.55 + UP * 1.55)
        joint_title.move_to(RIGHT * 3.15 + UP * 1.55)
        divider = DashedLine(UP * 1.45, DOWN * 1.8, color=GRAY_DIM, dash_length=0.14)

        naive_steps = VGroup(
            chip("choose layout", BLUE_3B1B, width=2.05),
            chip("train policy", ORANGE_3B1B, width=2.05),
            chip("simulate", PURPLE_3B1B, width=2.05),
            chip("score", RED_BRAIN, width=2.05),
        ).arrange(DOWN, buff=0.28).move_to(LEFT * 3.55 + DOWN * 0.20)
        naive_arrows = VGroup()
        for i in range(len(naive_steps) - 1):
            naive_arrows.add(Arrow(naive_steps[i].get_bottom(), naive_steps[i + 1].get_top(), color=GRAY_MID, buff=0.04, stroke_width=2.0))
        repeat = CurvedArrow(
            naive_steps[-1].get_left() + LEFT * 0.12,
            naive_steps[0].get_left() + LEFT * 0.12,
            angle=-TAU / 4.1,
            color=RED_BRAIN,
            stroke_width=2.4,
        )

        design = small_card("design policy", "proposes\nsensor layout", GREEN_3B1B, width=2.25, height=1.25)
        control = small_card("control policy", "acts from\nobservations", BLUE_3B1B, width=2.35, height=1.25)
        reward = small_card("task score", "reward /\nsuccess", ORANGE_3B1B, width=2.20, height=1.25)
        joint = VGroup(design, control, reward).arrange(RIGHT, buff=0.35).move_to(RIGHT * 3.0 + UP * 0.45)
        flow = VGroup(
            Arrow(design.get_right(), control.get_left(), color=GRAY_MID, buff=0.08, stroke_width=2.0),
            Arrow(control.get_right(), reward.get_left(), color=GRAY_MID, buff=0.08, stroke_width=2.0),
        )
        update_eye = CurvedArrow(
            reward.get_bottom() + DOWN * 0.08,
            design.get_bottom() + DOWN * 0.08,
            angle=-TAU / 6.2,
            color=PURPLE_3B1B,
            stroke_width=2.5,
        )
        update_control = Arrow(reward.get_bottom() + DOWN * 0.30, control.get_bottom() + DOWN * 0.30, color=GREEN_3B1B, buff=0.12, stroke_width=2.5)
        update_label = Text("same rollout", font_size=21, color=YELLOW_3B1B, weight=BOLD).move_to(RIGHT * 3.0 + DOWN * 1.28)

        self.play(FadeIn(naive_title), FadeIn(joint_title), Create(divider), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.08) for s in naive_steps], lag_ratio=0.12), LaggedStart(*[GrowArrow(a) for a in naive_arrows], lag_ratio=0.12), run_time=1.3)
        self.play(Create(repeat), run_time=0.65)
        self.play(FadeIn(joint, shift=UP * 0.12), LaggedStart(*[GrowArrow(a) for a in flow], lag_ratio=0.15), run_time=1.1)
        self.play(Create(update_eye), GrowArrow(update_control), FadeIn(update_label), run_time=1.0)
        cap = caption("The method optimizes the eye and the behavior together.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, naive_steps, repeat, design, control, reward, update_eye, update_control, cap], beat_time=11.8)
        clear_scene(self)


class Scene14EvidenceDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Reading the Evidence", "Numbers matter only when the task and metric are clear.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        traj_box = RoundedRectangle(width=2.75, height=2.45, corner_radius=0.18, color=GREEN_3B1B, stroke_width=2.0, fill_color=GRAY_DARKER, fill_opacity=0.15)
        traj_box.move_to(LEFT * 4.25 + UP * 0.35)
        traj_label = Text("82.5% improved", font_size=23, color=GREEN_3B1B, weight=BOLD).move_to(traj_box.get_bottom() + UP * 0.38)
        dots = VGroup()
        points = []
        for x, y, color in [(-4.95, -0.25, RED_BRAIN), (-4.65, 0.02, ORANGE_3B1B), (-4.34, 0.30, YELLOW_3B1B), (-4.02, 0.52, GREEN_3B1B), (-3.70, 0.68, GREEN_3B1B)]:
            p = np.array([x, y, 0])
            points.append(p)
            dots.add(Dot(p, radius=0.06, color=color))
        path = VMobject(color=GREEN_3B1B, stroke_width=2.1)
        path.set_points_smoothly(points)

        point = metric_bars("PointGoalNav", 0.447, 0.518, "SPL", BLUE_3B1B, scale=0.95)
        point.move_to(LEFT * 0.25 + DOWN * 0.15)
        target = metric_bars("TargetNav", 0.363, 0.405, "success", ORANGE_3B1B, scale=0.95)
        target.move_to(RIGHT * 3.55 + DOWN * 0.15)

        self.play(FadeIn(traj_box), Create(path), FadeIn(dots, lag_ratio=0.10), FadeIn(traj_label), run_time=1.2)
        self.play(FadeIn(point[0]), Create(point[1]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in point[2]], lag_ratio=0.16), FadeIn(point[3:]), run_time=1.2)
        self.play(FadeIn(target[0]), Create(target[1]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in target[2]], lag_ratio=0.16), FadeIn(target[3:]), run_time=1.2)
        self.wait(2.0)

        ablation = VGroup(
            small_card("green", "success\n0.314", GREEN_3B1B, width=2.0, height=1.2),
            Arrow(LEFT * 0.45, RIGHT * 0.45, color=RED_BRAIN, stroke_width=2.0, max_tip_length_to_length_ratio=0.10),
            small_card("transparent", "success\n0.132", GRAY_MID, width=2.2, height=1.2),
        ).arrange(RIGHT, buff=0.30)
        ablation.move_to(DOWN * 1.40)
        self.play(FadeIn(ablation, shift=UP * 0.08), run_time=0.9)
        cap = caption("Interpretation: improvement is real, task-specific, and limited.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, traj_box, path, point, target, ablation[0], ablation[1], ablation[2], cap], beat_time=11.8)
        clear_scene(self)


class Scene15SurveyTransferDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Human Survey and Real Robot", "Novel sensor layouts still have to survive deployment.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        human = RoundedRectangle(
            width=3.0,
            height=1.95,
            corner_radius=0.18,
            color=BLUE_3B1B,
            stroke_width=2.0,
            fill_color=GRAY_DARKER,
            fill_opacity=0.15,
        )
        human_title = Text("human guess", font_size=22, color=BLUE_3B1B, weight=BOLD)
        human_note = Text("symmetry feels natural", font_size=16, color=GRAY_MID, slant=ITALIC)
        human_robot = RoundedRectangle(width=0.60, height=0.82, corner_radius=0.12, color=GRAY_LIGHT, stroke_width=1.5)
        human_group = VGroup(human, human_title, human_robot, human_note)
        human_group.move_to(LEFT * 3.0 + UP * 0.75)
        human_title.move_to(human.get_top() + DOWN * 0.30)
        human_robot.move_to(human.get_center() + DOWN * 0.02)
        human_note.next_to(human_robot, DOWN, buff=0.13)
        human_dots = VGroup(
            Dot(human_robot.get_top() + DOWN * 0.16, radius=0.045, color=YELLOW_3B1B),
            Dot(human_robot.get_left() + RIGHT * 0.12, radius=0.045, color=YELLOW_3B1B),
            Dot(human_robot.get_right() + LEFT * 0.12, radius=0.045, color=YELLOW_3B1B),
        )
        human_group.add(human_dots)

        search = RoundedRectangle(
            width=3.25,
            height=1.95,
            corner_radius=0.18,
            color=GREEN_3B1B,
            stroke_width=2.0,
            fill_color=GRAY_DARKER,
            fill_opacity=0.15,
        )
        search_title = Text("computational search", font_size=22, color=GREEN_3B1B, weight=BOLD)
        shrink_to_width(search_title, 2.85)
        search_note = Text("odd layout can be useful", font_size=16, color=GRAY_MID, slant=ITALIC)
        search_robot = RoundedRectangle(width=0.60, height=0.82, corner_radius=0.12, color=GRAY_LIGHT, stroke_width=1.5)
        search_group = VGroup(search, search_title, search_robot, search_note)
        search_group.move_to(RIGHT * 3.0 + UP * 0.75)
        search_title.move_to(search.get_top() + DOWN * 0.30)
        search_robot.move_to(search.get_center() + DOWN * 0.02)
        search_note.next_to(search_robot, DOWN, buff=0.13)
        search_dots = VGroup(
            Dot(search_robot.get_bottom() + UP * 0.14 + LEFT * 0.08, radius=0.045, color=YELLOW_3B1B),
            Dot(search_robot.get_right() + LEFT * 0.10 + UP * 0.18, radius=0.045, color=YELLOW_3B1B),
            Dot(search_robot.get_center() + LEFT * 0.14 + DOWN * 0.12, radius=0.045, color=YELLOW_3B1B),
        )
        search_group.add(search_dots)
        human = human_group
        search = search_group
        self.play(FadeIn(human, shift=RIGHT * 0.08), FadeIn(search, shift=LEFT * 0.08), run_time=1.0)
        self.wait(2.2)

        sim = small_card("train in sim", "rollouts\nand reward", BLUE_3B1B, width=2.55, height=1.35)
        real = small_card("deploy real", "64 PRs\non robot", GREEN_3B1B, width=2.55, height=1.35)
        bridge_arrow = Arrow(LEFT * 0.65, RIGHT * 0.65, color=YELLOW_3B1B, stroke_width=2.4, max_tip_length_to_length_ratio=0.10)
        transfer = VGroup(sim, bridge_arrow, real).arrange(RIGHT, buff=0.35)
        transfer.move_to(DOWN * 1.0)
        self.play(FadeIn(transfer, shift=UP * 0.08), run_time=1.0)
        self.wait(2.2)

        summary = VGroup(
            small_card("supported", "small sensors\ncan work\nin some tasks", GREEN_3B1B, width=3.7, height=1.75),
            small_card("not implied", "cameras useless\n4 pixels solve all\nsim equals reality", RED_BRAIN, width=3.7, height=1.75),
        ).arrange(RIGHT, buff=0.75)
        summary.move_to(DOWN * 0.15)
        self.play(FadeOut(VGroup(human, search, transfer), run_time=0.55))
        self.play(FadeIn(summary, shift=UP * 0.08), run_time=1.0)
        cap = caption("Close Episode 2 with evidence and limits, then hand off to physical morphology.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, summary[0], summary[1], cap], beat_time=18.0)
        clear_scene(self)
