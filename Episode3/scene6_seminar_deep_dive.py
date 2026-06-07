"""
Episode 3 visual-first deep dives.

These scenes replace the long seminar-slide version with process diagrams,
simulation graphs, parameter sliders, and synthesis loops.
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


def math_chip(tex, color, width=1.75, font_size=24):
    rect = RoundedRectangle(width=width, height=0.46, corner_radius=0.12, color=color, stroke_width=1.6, fill_color=color, fill_opacity=0.10)
    label = MathTex(tex, font_size=font_size, color=color)
    shrink_to_width(label, width - 0.22)
    label.move_to(rect)
    return VGroup(rect, label)


def card(title, body, color, width=2.7, height=1.35):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.18, color=color, stroke_width=2.0, fill_color=GRAY_DARKER, fill_opacity=0.15)
    head = Text(title, font_size=20, color=color, weight=BOLD)
    shrink_to_width(head, width - 0.28)
    body_text = Text(body, font_size=16, color=GRAY_LIGHT, line_spacing=1.05)
    shrink_to_width(body_text, width - 0.28)
    VGroup(head, body_text).arrange(DOWN, buff=0.12).move_to(box)
    return VGroup(box, head, body_text)


def clear_scene(scene):
    scene.play(FadeOut(Group(*scene.mobjects), run_time=0.9))
    scene.wait(0.15)


def blob(color, seed_shift=0):
    pts = []
    for i in range(8):
        angle = i * TAU / 8
        radius = 0.42 + 0.10 * np.sin(i * 1.7 + seed_shift)
        pts.append([radius * np.cos(angle), radius * np.sin(angle), 0])
    shape = Polygon(*pts, color=color, stroke_width=2.0, fill_color=color, fill_opacity=0.13)
    return shape


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


def paced_voiceover(scene, targets, beat_time=13.0, color=None):
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


class Scene6ClassicalDesignDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Classical Design Search", "Generate, simulate, score, select.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        steps = VGroup(
            chip("generate", BLUE_3B1B, 1.65),
            chip("simulate", GREEN_3B1B, 1.65),
            chip("score", ORANGE_3B1B, 1.35),
            chip("select", PURPLE_3B1B, 1.45),
        ).arrange(RIGHT, buff=0.55)
        steps.move_to(UP * 1.55)
        arrows = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), color=GRAY_MID, buff=0.08, stroke_width=2.0, max_tip_length_to_length_ratio=0.09) for i in range(3)])

        bodies = VGroup()
        colors = [BLUE_3B1B, GREEN_3B1B, ORANGE_3B1B, PURPLE_3B1B, RED_BRAIN]
        for i, x in enumerate(np.linspace(-4.0, 4.0, 5)):
            shape = blob(colors[i], seed_shift=i).move_to([x, 0.05 + 0.12 * np.sin(i), 0])
            legs = VGroup(
                Line(shape.get_bottom(), shape.get_bottom() + DOWN * (0.35 + 0.05 * (i % 2)) + LEFT * 0.18, color=colors[i], stroke_width=2),
                Line(shape.get_bottom(), shape.get_bottom() + DOWN * (0.35 + 0.06 * ((i + 1) % 2)) + RIGHT * 0.18, color=colors[i], stroke_width=2),
            )
            score_bar = Rectangle(width=0.55, height=0.12 + 0.14 * i, color=colors[i], fill_color=colors[i], fill_opacity=0.8, stroke_width=0)
            score_bar.next_to(shape, DOWN, buff=0.48)
            bodies.add(VGroup(shape, legs, score_bar))

        self.play(FadeIn(steps), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.10) for b in bodies], lag_ratio=0.12), run_time=1.2)
        self.wait(2.0)

        winner_box = SurroundingRectangle(bodies[-1], color=GREEN_3B1B, buff=0.16, stroke_width=2.5)
        mutate = ArcBetweenPoints(
            bodies[-1].get_bottom() + DOWN * 0.36,
            bodies[0].get_bottom() + DOWN * 0.36,
            angle=-TAU / 5.0,
            color=YELLOW_3B1B,
            stroke_width=2.4,
        ).add_tip(tip_length=0.14)
        self.play(Create(winner_box), Create(mutate), run_time=0.9)
        cap = caption("Classical morphology design is powerful, visual, and often expensive.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, steps[0], steps[1], steps[2], steps[3], bodies, winner_box, mutate, cap], beat_time=12.8)
        clear_scene(self)


class Scene7DifferentiableSimulationDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Differentiable Simulation", "A simulator can turn behavior into gradients.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        nodes = VGroup()
        labels = [("state 0", BLUE_3B1B), ("physics", GRAY_MID), ("state 1", BLUE_3B1B), ("physics", GRAY_MID), ("state 2", BLUE_3B1B), ("reward", GREEN_3B1B)]
        for text, color in labels:
            nodes.add(chip(text, color, width=1.35 if "state" in text else 1.45))
        nodes.arrange(RIGHT, buff=0.28)
        nodes.move_to(UP * 1.20)
        forward = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), color=GRAY_MID, buff=0.06, stroke_width=2.0, max_tip_length_to_length_ratio=0.09) for i in range(len(nodes) - 1)])

        grid = VGroup()
        for i in range(8):
            for j in range(4):
                grid.add(Dot(radius=0.035, color=TEAL_EP2).move_to([i * 0.18, j * 0.18, 0]))
        grid.move_to(LEFT * 3.8 + DOWN * 0.65)
        grid_label = Text("soft body particles", font_size=18, color=TEAL_EP2).next_to(grid, DOWN, buff=0.18)
        memory = card("memory", "state history\nstored backward", RED_BRAIN, width=2.55, height=1.30)
        memory.move_to(RIGHT * 3.25 + DOWN * 0.60)

        self.play(FadeIn(nodes), LaggedStart(*[GrowArrow(a) for a in forward], lag_ratio=0.10), run_time=1.2)
        self.play(FadeIn(grid, lag_ratio=0.01), FadeIn(grid_label), FadeIn(memory, shift=LEFT * 0.08), run_time=1.0)
        self.wait(2.0)

        backward = VGroup()
        for i in range(len(nodes) - 1, 0, -1):
            backward.add(Arrow(nodes[i].get_bottom() + DOWN * 0.22, nodes[i - 1].get_bottom() + DOWN * 0.22, color=ORANGE_3B1B, buff=0.07, stroke_width=2.3, max_tip_length_to_length_ratio=0.08))
        derivs = VGroup(
            math_chip(r"\partial R/\partial \theta_{\mathrm{ctrl}}", BLUE_3B1B, 2.65, font_size=22),
            math_chip(r"\partial R/\partial \theta_{\mathrm{body}}", PURPLE_3B1B, 2.25, font_size=22),
            math_chip(r"\partial R/\partial \theta_{\mathrm{mat}}", GREEN_3B1B, 2.55, font_size=22),
        ).arrange(RIGHT, buff=0.25)
        derivs.move_to(DOWN * 1.75)
        self.play(LaggedStart(*[GrowArrow(a) for a in backward], lag_ratio=0.08), FadeIn(derivs, shift=UP * 0.08), run_time=1.3)
        cap = caption("Gradients give directions under a model; they do not guarantee global truth.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, nodes, forward, grid, memory, backward, derivs[0], derivs[1], derivs[2], cap], beat_time=12.5)
        clear_scene(self)


class Scene8CoDesignDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Body and Controller Co-Design", "The body is part of the learning problem.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        body = blob(PURPLE_3B1B).scale(1.2).move_to(LEFT * 3.6 + UP * 0.20)
        actuator = Arrow(body.get_left() + LEFT * 0.25, body.get_center(), color=ORANGE_3B1B, stroke_width=2.4, buff=0, max_tip_length_to_length_ratio=0.08)
        net, _, _ = create_neural_net([3, 4, 2], radius=0.09, h_buff=0.42, v_buff=0.22, node_color=BLUE_3B1B)
        net.scale(0.95).move_to(RIGHT * 3.6 + UP * 0.20)
        reward = chip("reward", YELLOW_3B1B, 1.35).move_to(DOWN * 1.35)
        body_label = math_chip(r"\theta_{\mathrm{body}}", PURPLE_3B1B, 1.75).next_to(body, UP, buff=0.32)
        brain_label = math_chip(r"\theta_{\mathrm{brain}}", BLUE_3B1B, 1.85).next_to(net, UP, buff=0.32)
        flow = VGroup(
            Arrow(body.get_right(), reward.get_left() + UP * 0.18, color=GRAY_MID, buff=0.10, max_tip_length_to_length_ratio=0.09),
            Arrow(net.get_left(), reward.get_right() + UP * 0.18, color=GRAY_MID, buff=0.10, max_tip_length_to_length_ratio=0.09),
        )

        self.play(FadeIn(body), GrowArrow(actuator), FadeIn(net), FadeIn(body_label), FadeIn(brain_label), run_time=1.1)
        self.play(FadeIn(reward), LaggedStart(*[GrowArrow(a) for a in flow], lag_ratio=0.12), run_time=0.8)
        self.wait(1.8)

        sliders = VGroup()
        for name, color, offset in [("shape", PURPLE_3B1B, 0.28), ("material", GREEN_3B1B, 0.52), ("actuation", ORANGE_3B1B, 0.42)]:
            line = Line(LEFT * 0.85, RIGHT * 0.85, color=GRAY_DIM, stroke_width=2.0)
            knob = Dot(line.get_left() + RIGHT * offset * 1.7, radius=0.06, color=color)
            label = Text(name, font_size=17, color=color, weight=BOLD).next_to(line, LEFT, buff=0.18)
            sliders.add(VGroup(label, line, knob))
        sliders.arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        sliders.move_to(ORIGIN + DOWN * 0.10)
        self.play(FadeIn(sliders, shift=UP * 0.08), run_time=0.85)
        for s in sliders:
            self.play(s[2].animate.shift(RIGHT * 0.28), body.animate.scale(1.015), run_time=0.35)

        grad_body = CurvedArrow(reward.get_left(), body.get_bottom(), angle=-TAU / 5, color=PURPLE_3B1B, stroke_width=2.4, tip_length=0.15)
        grad_brain = CurvedArrow(reward.get_right(), net.get_bottom(), angle=TAU / 5, color=BLUE_3B1B, stroke_width=2.4, tip_length=0.15)
        self.play(Create(grad_body), Create(grad_brain), run_time=0.9)
        cap = caption("The chain rule connects performance to morphology and control.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, body, actuator, net, reward, sliders, grad_body, grad_brain, cap], beat_time=12.8)
        clear_scene(self)


class Scene9DiffuseBotDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("DiffuseBot", "Generate, robotize, simulate, guide, repeat.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        stages = VGroup(
            card("noise", "random\ngeometry", GRAY_MID, width=1.7, height=1.20),
            card("diffusion", "plausible\nshape", PURPLE_3B1B, width=2.0, height=1.20),
            card("robotize", "material +\nactuators", BLUE_3B1B, width=2.0, height=1.20),
            card("simulate", "physics\nrollout", ORANGE_3B1B, width=2.0, height=1.20),
            card("guide", "utility\nfeedback", GREEN_3B1B, width=2.0, height=1.20),
        ).arrange(RIGHT, buff=0.18)
        stages.move_to(UP * 1.12)
        arrows = VGroup(*[Arrow(stages[i].get_right(), stages[i + 1].get_left(), color=GRAY_MID, buff=0.06, stroke_width=2.0, max_tip_length_to_length_ratio=0.09) for i in range(len(stages) - 1)])

        shapes = VGroup()
        for i, color in enumerate([GRAY_MID, PURPLE_3B1B, BLUE_3B1B, ORANGE_3B1B, GREEN_3B1B]):
            shape = blob(color, seed_shift=i * 0.8).scale(0.72).move_to(stages[i].get_bottom() + DOWN * 0.75)
            shapes.add(shape)

        self.play(FadeIn(stages, shift=UP * 0.08), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), run_time=1.3)
        self.play(LaggedStart(*[FadeIn(s, scale=0.9) for s in shapes], lag_ratio=0.14), run_time=1.1)
        self.wait(2.0)

        filter_line = DashedLine(LEFT * 4.8 + DOWN * 1.12, RIGHT * 4.8 + DOWN * 1.12, color=GRAY_DIM, dash_length=0.12)
        bad = VGroup(Text("looks plausible", font_size=22, color=PURPLE_3B1B, weight=BOLD), Text("thin limbs\nunstable", font_size=18, color=RED_BRAIN)).arrange(DOWN, buff=0.22).move_to(LEFT * 2.5 + DOWN * 1.92)
        good = VGroup(Text("can work", font_size=22, color=GREEN_3B1B, weight=BOLD), Text("stable support\nactuation-aware", font_size=18, color=GREEN_3B1B)).arrange(DOWN, buff=0.22).move_to(RIGHT * 2.6 + DOWN * 1.92)
        loop = ArcBetweenPoints(
            stages[-1].get_bottom() + DOWN * 0.08,
            stages[1].get_bottom() + DOWN * 0.08,
            angle=-TAU / 4,
            color=GREEN_3B1B,
            stroke_width=2.5,
        ).add_tip(tip_length=0.14)
        self.play(Create(filter_line), FadeIn(bad), FadeIn(good), Create(loop), run_time=1.1)
        cap = caption("Physics feedback guides generation; it does not make every shape buildable.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, stages[0], stages[1], stages[2], stages[3], stages[4], bad, good, loop, cap], beat_time=12.4)
        clear_scene(self)


class Scene10FabricationSynthesisDeepDive(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        title = title_text("Fabrication, Deployment, and Synthesis", "The final design has to survive the world.")
        self.play(FadeIn(title, shift=DOWN * 0.12), run_time=0.8)

        pipeline = VGroup(
            chip("geometry", PURPLE_3B1B, 1.55),
            chip("material", GREEN_3B1B, 1.45),
            chip("actuators", ORANGE_3B1B, 1.60),
            chip("controller", BLUE_3B1B, 1.70),
            chip("fabrication", RED_BRAIN, 1.85),
        ).arrange(RIGHT, buff=0.30)
        pipeline.move_to(UP * 1.45)
        arrows = VGroup(*[Arrow(pipeline[i].get_right(), pipeline[i + 1].get_left(), color=GRAY_MID, buff=0.06, stroke_width=2.0, max_tip_length_to_length_ratio=0.09) for i in range(len(pipeline) - 1)])

        constraints = VGroup(
            card("lighting", "sensor\nshift", BLUE_3B1B, width=1.9, height=1.10),
            card("friction", "surface\nchange", ORANGE_3B1B, width=1.9, height=1.10),
            card("wear", "motors\nage", RED_BRAIN, width=1.9, height=1.10),
            card("humans", "unexpected\ninteraction", GREEN_3B1B, width=2.15, height=1.10),
        ).arrange(RIGHT, buff=0.28)
        constraints.move_to(UP * 0.05)

        loop = VGroup(
            chip("world", GREEN_3B1B, 1.25),
            chip("eye", BLUE_3B1B, 1.10),
            chip("controller", ORANGE_3B1B, 1.75),
            chip("body", PURPLE_3B1B, 1.15),
        )
        loop.arrange(RIGHT, buff=0.38).move_to(DOWN * 1.25)
        loop_arrows = VGroup(*[Arrow(loop[i].get_right(), loop[i + 1].get_left(), color=GRAY_MID, buff=0.06, stroke_width=2.0, max_tip_length_to_length_ratio=0.09) for i in range(len(loop) - 1)])
        closing = CurvedArrow(loop[-1].get_bottom(), loop[0].get_bottom(), angle=-TAU / 4, color=YELLOW_3B1B, stroke_width=2.4, tip_length=0.15)

        self.play(FadeIn(pipeline), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.10), run_time=1.1)
        self.play(FadeIn(constraints, shift=UP * 0.08), run_time=1.0)
        self.wait(2.0)
        self.play(FadeIn(loop, shift=UP * 0.08), LaggedStart(*[GrowArrow(a) for a in loop_arrows], lag_ratio=0.10), Create(closing), run_time=1.2)
        cap = caption("Design the loop: world, eye, controller, body, and build constraints.")
        self.play(FadeIn(cap, shift=UP * 0.08), run_time=0.7)
        paced_voiceover(self, [title, pipeline, constraints[0], constraints[1], constraints[2], constraints[3], loop, closing, cap], beat_time=14.5)
        clear_scene(self)
