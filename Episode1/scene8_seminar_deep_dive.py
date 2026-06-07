"""
Episode 1 visual-first deep dives.

The class names remain the same as the previous seminar version, but the scenes
now use diagrams, toy simulations, and charts instead of dense bullet slides.
"""

from manim import *
from common import *

TEAL_EP2 = "#14B8A6"


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


def caption(text, color=YELLOW_3B1B, width=11.2, buff=0.72):
    cap = Text(text, font_size=23, color=color, weight=BOLD)
    shrink_to_width(cap, width)
    cap.to_edge(DOWN, buff=buff)
    return cap


def chip(text, color, width=1.75):
    rect = RoundedRectangle(width=width, height=0.46, corner_radius=0.12, color=color, stroke_width=1.6, fill_color=color, fill_opacity=0.10)
    label = Text(text, font_size=16, color=color, weight=BOLD)
    shrink_to_width(label, width - 0.22)
    label.move_to(rect)
    return VGroup(rect, label)


def small_card(title, body, color, width=3.0, height=1.55):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.18, color=color, stroke_width=2.0, fill_color=GRAY_DARKER, fill_opacity=0.15)
    head = Text(title, font_size=22, color=color, weight=BOLD)
    shrink_to_width(head, width - 0.35)
    body_text = Text(body, font_size=17, color=GRAY_LIGHT, line_spacing=1.05)
    shrink_to_width(body_text, width - 0.35)
    VGroup(head, body_text).arrange(DOWN, buff=0.15).move_to(box)
    return VGroup(box, head, body_text)


def clear_scene(scene):
    scene.play(FadeOut(Group(*scene.mobjects), run_time=0.9))
    scene.wait(0.15)


def gauge(label, value, color, width=2.9):
    title = Text(label, font_size=20, color=color, weight=BOLD)
    frame = Rectangle(width=width, height=0.28, color=GRAY_DIM, stroke_width=1.4)
    fill = Rectangle(width=width * value, height=0.28, color=color, fill_color=color, fill_opacity=0.82, stroke_width=0)
    fill.move_to(frame.get_left() + RIGHT * (width * value / 2))
    group = VGroup(title, frame, fill).arrange(DOWN, buff=0.14)
    return group


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


def paced_voiceover(scene, targets, beat_time=14.0, color=None):
    """Emphasize the narration target by strengthening its original color."""
    active = None
    active_style = None
    scale_factor = 1.045

    for target in targets:
        target_style = _capture_style(target)
        _apply_emphasis(target)

        animations = [
            target.animate.scale(scale_factor, about_point=target.get_center()),
        ]
        if active is not None:
            _restore_style(active_style)
            animations.extend([
                active.animate.scale(1 / scale_factor, about_point=active.get_center()),
            ])
        scene.play(*animations, run_time=0.65)
        scene.wait(beat_time)

        active = target
        active_style = target_style

    if active is not None:
        _restore_style(active_style)
        scene.play(
            active.animate.scale(1 / scale_factor, about_point=active.get_center()),
            run_time=0.5,
        )


class Scene8PassiveDynamicsDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Passive Dynamics", "The fish example is a control lesson, not just a trick.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        fish = create_fish(color=GRAY_LIGHT, stroke_width=2.2).scale(0.74)
        fish.move_to(LEFT * 3.25 + UP * 0.12)
        fish[0][0].set_fill(BG_COLOR, opacity=0.96)
        fish.set_z_index(3)
        currents = VGroup()
        for x0 in [-5.7, -4.25, -2.8]:
            for y in [-1.05, -0.62, -0.19, 0.24, 0.67, 1.10]:
                currents.add(Arrow(
                    RIGHT * x0 + UP * y,
                    RIGHT * (x0 + 0.92) + UP * y,
                    color=BLUE_3B1B,
                    buff=0,
                    stroke_width=1.25,
                    tip_length=0.12,
                    max_tip_length_to_length_ratio=0.055,
                ).set_opacity(0.84))
        currents.set_z_index(0)
        water_label = chip("water flow", BLUE_3B1B, width=1.8).next_to(currents, DOWN, buff=0.22)
        water_label.set_z_index(4)

        stiff = gauge("stiff body effort", 0.88, RED_BRAIN).move_to(RIGHT * 3.25 + UP * 1.05)
        compliant = gauge("compliant body effort", 0.35, GREEN_3B1B).move_to(RIGHT * 3.25 + DOWN * 0.55)

        self.play(FadeIn(currents, lag_ratio=0.10), FadeIn(water_label), run_time=1.0)
        self.play(FadeIn(fish, shift=RIGHT * 0.18), run_time=0.8)

        currents.flow_phase = 0.0
        currents.prev_dx = 0.0
        def drift_currents(mob, dt):
            mob.flow_phase += dt
            dx = 0.10 * np.sin(TAU * 0.30 * mob.flow_phase)
            mob.shift(RIGHT * (dx - mob.prev_dx))
            mob.prev_dx = dx
        currents.add_updater(drift_currents)

        fish.swim_phase = 0.0
        fish.prev_offset = ORIGIN
        fish.prev_angle = 0.0
        fish[1].prev_wag_angle = 0.0
        fish[5].prev_fin_angle = 0.0
        def swim_fish(mob, dt):
            mob.swim_phase += dt
            phase = mob.swim_phase
            offset = RIGHT * (0.10 * np.sin(TAU * 0.18 * phase)) + UP * (0.055 * np.sin(TAU * 0.33 * phase))
            angle = 2.8 * DEGREES * np.sin(TAU * 0.24 * phase)
            mob.shift(offset - mob.prev_offset)
            mob.rotate(angle - mob.prev_angle, about_point=mob.get_center())
            mob.prev_offset = offset
            mob.prev_angle = angle
        fish.add_updater(swim_fish)

        def wag_tail(tail, dt):
            phase = fish.swim_phase
            angle = 9.0 * DEGREES * np.sin(TAU * 0.95 * phase)
            anchor = fish[0][0].get_left() + RIGHT * 0.08
            tail.rotate(angle - tail.prev_wag_angle, about_point=anchor)
            tail.prev_wag_angle = angle

        def flap_pectoral_fin(fin, dt):
            phase = fish.swim_phase
            angle = 5.0 * DEGREES * np.sin(TAU * 1.20 * phase + 0.65)
            anchor = fin.get_center() + RIGHT * 0.16 + UP * 0.03
            fin.rotate(angle - fin.prev_fin_angle, about_point=anchor)
            fin.prev_fin_angle = angle

        fish[1].add_updater(wag_tail)
        fish[5].add_updater(flap_pectoral_fin)

        self.wait(1.25)
        self.play(FadeIn(stiff, shift=LEFT * 0.12), run_time=0.65)
        self.play(FadeIn(compliant, shift=LEFT * 0.12), run_time=0.65)
        self.wait(1.8)

        loop_center = RIGHT * 3.05 + UP * 0.12
        world = chip("world", GREEN_3B1B, 1.35).move_to(loop_center + UP * 0.82)
        eye = chip("eye", BLUE_3B1B, 1.20).move_to(loop_center + LEFT * 1.05)
        brain = chip("brain", ORANGE_3B1B, 1.35).move_to(loop_center + DOWN * 0.82)
        body = chip("body", PURPLE_3B1B, 1.25).move_to(loop_center + RIGHT * 1.05)
        loop_nodes = VGroup(world, eye, brain, body)
        loop_nodes.scale(1.2, about_point=loop_center)
        loop_nodes.set_z_index(2)
        loop_arrows = VGroup(
            Arrow(world[0].get_left(), eye[0].get_top(), color=GRAY_MID, buff=0.08, stroke_width=1.7, tip_length=0.12, max_tip_length_to_length_ratio=0.055),
            Arrow(eye[0].get_bottom(), brain[0].get_left(), color=GRAY_MID, buff=0.08, stroke_width=1.7, tip_length=0.12, max_tip_length_to_length_ratio=0.055),
            Arrow(brain[0].get_right(), body[0].get_bottom(), color=GRAY_MID, buff=0.08, stroke_width=1.7, tip_length=0.12, max_tip_length_to_length_ratio=0.055),
            Arrow(body[0].get_top(), world[0].get_right(), color=GRAY_MID, buff=0.08, stroke_width=1.7, tip_length=0.12, max_tip_length_to_length_ratio=0.055),
        )
        loop_arrows.set_z_index(1)
        self.play(FadeOut(VGroup(stiff, compliant), run_time=0.35))
        self.play(FadeIn(loop_nodes, shift=UP * 0.08), LaggedStart(*[GrowArrow(a) for a in loop_arrows], lag_ratio=0.12), run_time=1.25)
        cap = caption("Good morphology reduces the work the controller has to do.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, currents, fish, water_label, loop_nodes[0], loop_nodes[1], loop_nodes[2], loop_nodes[3], loop_arrows, cap], beat_time=13.5)
        clear_scene(self)


class Scene9EcologicalFramingDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        def small_metric(label, value, color, width=1.18):
            label_text = Text(label, font_size=13, color=GRAY_MID)
            label_slot = Rectangle(width=0.64, height=0.01, stroke_width=0, fill_opacity=0)
            label_text.move_to(label_slot.get_left() + RIGHT * (label_text.width / 2))
            label_group = VGroup(label_slot, label_text)
            track = RoundedRectangle(
                width=width,
                height=0.12,
                corner_radius=0.025,
                color=GRAY_DIM,
                stroke_width=0,
                fill_color=GRAY_DIM,
                fill_opacity=0.18,
            )
            bar_width = max(width * value, 0.16)
            fill = RoundedRectangle(
                width=bar_width,
                height=0.12,
                corner_radius=0.025,
                color=color,
                stroke_width=0,
                fill_color=color,
                fill_opacity=0.88,
            )
            fill.move_to(track.get_left() + RIGHT * (bar_width / 2))
            return VGroup(label_group, VGroup(track, fill)).arrange(RIGHT, buff=0.10)

        def outcome_badge(text, color):
            width = 1.16 if len(text) <= 6 else 1.46
            return chip(text, color, width=width).scale(0.82)

        def ecology_card(name, color, cue, outcome, benefit, cost, kind):
            card = RoundedRectangle(width=3.45, height=2.92, corner_radius=0.18, color=color, stroke_width=2.0, fill_color=GRAY_DARKER, fill_opacity=0.14)
            label = Text(name, font_size=20, color=color, weight=BOLD).move_to(card.get_top() + DOWN * 0.28)

            scene_box = RoundedRectangle(width=2.54, height=1.08, corner_radius=0.14, color=color, stroke_width=1.1, fill_color=color, fill_opacity=0.05)
            scene_box.move_to(card.get_center() + UP * 0.40)
            eye = Circle(radius=0.18, color=YELLOW_3B1B, stroke_width=1.8)
            eye.move_to(scene_box.get_left() + RIGHT * 0.72 + DOWN * 0.02)

            art = VGroup(scene_box, eye)

            def vision_sector(radius, angle, center_shift, fill_opacity, stroke_opacity, stroke_width=1.5):
                sector = Sector(
                    radius=radius,
                    angle=angle,
                    start_angle=-angle / 2,
                    color=color,
                    fill_color=color,
                    fill_opacity=fill_opacity,
                    stroke_width=stroke_width,
                )
                sector.move_to(eye.get_center() + RIGHT * center_shift)
                sector.set_stroke(opacity=stroke_opacity)
                return sector

            if kind == "water":
                for y in [-0.30, -0.10, 0.10, 0.30]:
                    line = Line(scene_box.get_left() + RIGHT * 0.24 + UP * y, scene_box.get_right() + LEFT * 0.22 + UP * y, color=BLUE_3B1B, stroke_width=1.3, stroke_opacity=0.55)
                    art.add(line)
                cone = vision_sector(0.82, 3 * DEGREES, 0.36, 0.03, 0.20)
                final_cone = vision_sector(0.82, 88 * DEGREES, 0.36, 0.22, 1.0)
                cone_spec = (0.82, 88 * DEGREES, 0.36, 0.22, 1.0, 1.5, color)
                art.add(cone)
            elif kind == "reef":
                for x, h, c in [(-0.74, 0.40, GREEN_3B1B), (-0.18, 0.55, ORANGE_3B1B), (0.44, 0.38, PURPLE_3B1B), (0.82, 0.50, GREEN_3B1B)]:
                    rock = RoundedRectangle(width=0.18, height=h, corner_radius=0.05, color=c, stroke_width=0, fill_color=c, fill_opacity=0.55)
                    rock.move_to(scene_box.get_center() + RIGHT * x + DOWN * (0.43 - h / 2))
                    art.add(rock)
                cone = vision_sector(0.70, 3 * DEGREES, 0.31, 0.03, 0.20)
                final_cone = vision_sector(0.70, 52 * DEGREES, 0.31, 0.20, 1.0)
                cone_spec = (0.70, 52 * DEGREES, 0.31, 0.20, 1.0, 1.5, color)
                cue_dot = Dot(eye.get_center() + RIGHT * 0.82 + UP * 0.03, radius=0.045, color=YELLOW_3B1B)
                art.add(cone, cue_dot)
            else:
                darkness = RoundedRectangle(width=2.26, height=0.96, corner_radius=0.13, color=PURPLE_3B1B, stroke_width=0, fill_color="#0B0B12", fill_opacity=0.70)
                darkness.move_to(scene_box)
                cone = vision_sector(0.58, 3 * DEGREES, 0.24, 0.02, 0.15, stroke_width=1.2)
                final_cone = vision_sector(0.58, 42 * DEGREES, 0.24, 0.10, 0.75, stroke_width=1.2)
                cone_spec = (0.58, 42 * DEGREES, 0.24, 0.10, 0.75, 1.2, color)
                light = Dot(eye.get_center() + RIGHT * 0.88 + UP * 0.18, radius=0.035, color=GRAY_LIGHT).set_opacity(0.45)
                art.add(darkness, cone, light)

            art.remove(eye)
            art.add(eye)
            cue_chip = chip(cue, color, width=1.30).scale(0.82)
            consequence = outcome_badge(outcome, color)
            bridge = Arrow(LEFT, RIGHT, color=GRAY_DIM, stroke_width=0.9, tip_length=0.06, max_tip_length_to_length_ratio=0.055).scale(0.22)
            mid_row = VGroup(cue_chip, bridge, consequence).arrange(RIGHT, buff=0.10)
            mid_row.move_to(card.get_center() + DOWN * 0.58)

            metrics = VGroup(
                small_metric("benefit", benefit, color),
                small_metric("cost", cost, ORANGE_3B1B),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.09)
            metrics.move_to(card.get_bottom() + UP * 0.35)

            group = VGroup(card, label, art, mid_row, metrics)
            group.vision_cone = cone
            group.vision_eye = eye
            group.vision_spec = cone_spec
            return group

        title = title_text("Ecological Framing", "A design is good for a task, environment, and cost.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        envs = VGroup(
            ecology_card("open water", BLUE_3B1B, "wide FOV", "good", 0.86, 0.22, "water"),
            ecology_card("cluttered reef", GREEN_3B1B, "front cue", "trade-off", 0.58, 0.50, "reef"),
            ecology_card("dark cave", PURPLE_3B1B, "low light", "costly", 0.25, 0.82, "cave"),
        )
        envs.arrange(RIGHT, buff=0.35)
        envs.move_to(UP * 0.30)
        self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.10) for e in envs], lag_ratio=0.16), run_time=1.6)
        for env in envs:
            radius, angle, center_shift, fill_opacity, stroke_opacity, stroke_width, cone_color = env.vision_spec
            final_cone = Sector(
                radius=radius,
                angle=angle,
                start_angle=-angle / 2,
                color=cone_color,
                fill_color=cone_color,
                fill_opacity=fill_opacity,
                stroke_width=stroke_width,
            )
            final_cone.move_to(env.vision_eye.get_center() + RIGHT * center_shift)
            final_cone.set_stroke(opacity=stroke_opacity)
            self.play(Transform(env.vision_cone, final_cone), run_time=0.55, rate_func=smooth)
        self.wait(2.5)

        niche_label = Text("niche =", font_size=17, color=GRAY_LIGHT, weight=BOLD)
        task_chip = chip("task", GREEN_3B1B, 1.10).scale(0.86)
        env_chip = chip("environment", ORANGE_3B1B, 1.70).scale(0.86)
        cost_chip = chip("cost", PURPLE_3B1B, 1.00).scale(0.86)
        evidence_chip = chip("evidence", BLUE_3B1B, 1.34).scale(0.86)
        pluses = [Text("+", font_size=18, color=GRAY_MID) for _ in range(3)]
        context = VGroup(niche_label, task_chip, pluses[0], env_chip, pluses[1], cost_chip, pluses[2], evidence_chip).arrange(RIGHT, buff=0.13)
        context.move_to(DOWN * 1.92)
        context_arrows = VGroup(*[
            Arrow(
                env_chip.get_top() + UP * 0.06,
                env.get_bottom() + DOWN * 0.06,
                color="#FB923C",
                stroke_width=1.65,
                tip_length=0.095,
                max_tip_length_to_length_ratio=0.07,
                buff=0.08,
            ).set_opacity(0.90)
            for env in envs
        ])
        context_arrows.set_z_index(0.5)
        self.play(FadeIn(context, shift=UP * 0.08), LaggedStart(*[GrowArrow(a) for a in context_arrows], lag_ratio=0.10), run_time=0.9)
        cap = caption("The same eye can be good or bad when the niche changes.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, envs[0], envs[1], envs[2], task_chip, env_chip, cost_chip, evidence_chip, cap], beat_time=13.5)
        clear_scene(self)


class Scene10BiologicalVisionDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Biological Vision as Design", "Natural eyes are specialized sensing strategies.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        cards = VGroup(
            small_card("pupil", "orientation\nand FOV", PURPLE_3B1B, width=2.55, height=1.55),
            small_card("fovea", "detail where\nit matters", ORANGE_3B1B, width=2.55, height=1.55),
            small_card("scallop", "mirror path\nmany eyes", BLUE_3B1B, width=2.55, height=1.55),
            small_card("cave / night", "energy vs\nsensitivity", GREEN_3B1B, width=2.55, height=1.55),
        ).arrange(RIGHT, buff=0.25)
        cards.move_to(UP * 1.05)

        axis = Line(LEFT * 4.6, RIGHT * 4.6, color=GRAY_MID, stroke_width=3).add_tip(tip_length=0.18)
        axis.move_to(DOWN * 0.78)
        left = VGroup(
            Text("wide", font_size=18, color=BLUE_3B1B, weight=BOLD),
            Text("field", font_size=18, color=BLUE_3B1B, weight=BOLD),
        ).arrange(RIGHT, buff=0.10).next_to(axis.get_start(), DOWN, buff=0.22)
        right = VGroup(
            Text("high", font_size=18, color=ORANGE_3B1B, weight=BOLD),
            Text("acuity", font_size=18, color=ORANGE_3B1B, weight=BOLD),
        ).arrange(RIGHT, buff=0.10).next_to(axis.get_end(), DOWN, buff=0.22)
        points = VGroup()
        for name, x, color in [("goat", -3.2, BLUE_3B1B), ("scallop", -0.85, PURPLE_3B1B), ("eagle", 3.15, ORANGE_3B1B)]:
            dot = Dot(axis.get_center() + RIGHT * x, radius=0.07, color=color)
            label = Text(name, font_size=17, color=color, weight=BOLD).next_to(dot, UP, buff=0.15)
            points.add(VGroup(dot, label))

        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.10) for c in cards], lag_ratio=0.14), run_time=1.4)
        self.play(Create(axis), FadeIn(left), FadeIn(right), LaggedStart(*[FadeIn(p) for p in points], lag_ratio=0.18), run_time=1.3)
        self.wait(2.5)

        bio_context = VGroup(cards, axis, left, right, points)
        self.play(FadeOut(bio_context, shift=UP * 0.08), run_time=0.75)

        robot = RoundedRectangle(width=1.22, height=1.55, corner_radius=0.18, color=GRAY_LIGHT, stroke_width=1.8).move_to(LEFT * 3.75 + DOWN * 0.95)
        pr_dots = VGroup(*[
            Dot(robot.get_center() + np.array([x, y, 0]), radius=0.052, color=YELLOW_3B1B)
            for x, y in [(-0.25, 0.35), (0.25, 0.20), (-0.16, -0.23), (0.12, -0.42)]
        ])
        design = VGroup(chip("count", BLUE_3B1B, 1.25), chip("placement", GREEN_3B1B, 1.65), chip("FOV", ORANGE_3B1B, 1.10), chip("policy-cue", PURPLE_3B1B, 1.85)).arrange(RIGHT, buff=0.18)
        design.move_to(RIGHT * 2.05 + DOWN * 0.95)
        arrow = Arrow(
            robot.get_right() + RIGHT * 0.24,
            design.get_left() + LEFT * 0.22,
            color=YELLOW_3B1B,
            stroke_width=2.2,
            max_tip_length_to_length_ratio=0.07,
        )
        self.play(FadeIn(robot), FadeIn(pr_dots, lag_ratio=0.12), GrowArrow(arrow), FadeIn(design, shift=LEFT * 0.08), run_time=1.2)
        cap = caption("Biology gives design variables; robotics turns them into parameters.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, robot, pr_dots, design[0], design[1], design[2], design[3], cap], beat_time=13.0)
        clear_scene(self)


class Scene11OceanAcuityDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Visual Acuity and Measurement", "Acuity is a measurable design property, not just image quality.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        chart_panel = RoundedRectangle(
            width=5.25,
            height=2.95,
            corner_radius=0.18,
            color=TEAL_EP2,
            stroke_width=1.6,
            fill_color=TEAL_EP2,
            fill_opacity=0.05,
        ).move_to(LEFT * 2.95 + UP * 0.48)
        chart_title = Text("measurement curve", font_size=18, color=TEAL_EP2, weight=BOLD)
        chart_title.move_to(chart_panel.get_top() + DOWN * 0.28)
        origin = chart_panel.get_center() + LEFT * 1.80 + DOWN * 0.82
        x_axis = Line(origin, origin + RIGHT * 3.85, color=GRAY_MID, stroke_width=2.0).add_tip(tip_length=0.10)
        y_axis = Line(origin, origin + UP * 1.85, color=GRAY_MID, stroke_width=2.0).add_tip(tip_length=0.12)
        curve = VMobject(color=TEAL_EP2, stroke_width=3.0)
        curve.set_points_smoothly([
            origin + RIGHT * 0.05 + UP * 0.20,
            origin + RIGHT * 0.95 + UP * 1.35,
            origin + RIGHT * 2.05 + UP * 0.88,
            origin + RIGHT * 3.45 + UP * 1.45,
        ])
        x_label = Text("sensor cost", font_size=15, color=GRAY_MID).next_to(x_axis, DOWN, buff=0.12)
        y_label = Text("useful detail", font_size=15, color=GRAY_MID).next_to(y_axis, LEFT, buff=0.14)
        chart = VGroup(chart_panel, chart_title, x_axis, y_axis, curve, x_label, y_label)

        water = RoundedRectangle(width=4.35, height=2.95, corner_radius=0.18, color=BLUE_3B1B, stroke_width=1.6, fill_color=BLUE_3B1B, fill_opacity=0.06)
        water.move_to(RIGHT * 3.05 + UP * 0.48)
        water_title = Text("medium / cue quality", font_size=18, color=BLUE_3B1B, weight=BOLD)
        water_title.move_to(water.get_top() + DOWN * 0.28)
        layers = VGroup()
        for i, color in enumerate([BLUE_3B1B, TEAL_EP2, PURPLE_3B1B]):
            layer = Rectangle(width=3.15, height=0.38, color=color, fill_color=color, fill_opacity=0.23, stroke_width=0)
            layer.move_to(water.get_top() + DOWN * (0.82 + i * 0.50))
            layers.add(layer)
        water_text = Text("same signal, different visibility", font_size=16, color=BLUE_3B1B, weight=BOLD)
        water_text.scale_to_fit_width(water.width - 0.45)
        water_text.move_to(water.get_bottom() + UP * 0.35)
        panel_arrow = Arrow(chart_panel.get_right() + RIGHT * 0.08, water.get_left() + LEFT * 0.08, color=GRAY_DIM, stroke_width=1.1, tip_length=0.07, buff=0.05).set_opacity(0.65)

        self.play(FadeIn(chart_panel), FadeIn(chart_title), Create(x_axis), Create(y_axis), FadeIn(x_label), FadeIn(y_label), run_time=0.9)
        self.play(Create(curve), run_time=1.2)
        self.play(GrowArrow(panel_arrow), FadeIn(water), FadeIn(water_title), FadeIn(layers, lag_ratio=0.10), FadeIn(water_text), run_time=1.0)
        self.wait(2.3)

        compare = VGroup(
            small_card("camera thinking", "more pixels\nmore compute", BLUE_3B1B, width=3.35, height=1.28),
            small_card("design thinking", "needed cue\nright place", GREEN_3B1B, width=3.35, height=1.28),
        ).arrange(RIGHT, buff=0.75)
        compare.move_to(DOWN * 2.12)
        compare_arrow = Arrow(compare[0].get_right() + RIGHT * 0.08, compare[1].get_left() + LEFT * 0.08, color=YELLOW_3B1B, stroke_width=1.5, tip_length=0.09, buff=0.08)
        self.play(FadeIn(compare, shift=UP * 0.08), GrowArrow(compare_arrow), run_time=1.0)
        cap = caption("Bad-looking input can still contain good control information.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, chart, curve, water, layers, water_text, compare[0], compare[1], cap], beat_time=13.5)
        clear_scene(self)
