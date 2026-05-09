from manim import *
import numpy as np

# ────────────────────────────────────────────────────────────────
# Color Palette
# ────────────────────────────────────────────────────────────────
BG_COLOR    = "#1C1C1C"
BLUE_3B1B   = "#3B82F6"
YELLOW_3B1B = "#FBBF24"
RED_BRAIN   = "#EF4444"
GRAY_LIGHT  = "#E5E7EB"
GRAY_DIM    = "#6B7280"
GREEN_3B1B  = "#10B981"
PURPLE_3B1B = "#8B5CF6"

# ────────────────────────────────────────────────────────────────
# FOV Helpers
# ────────────────────────────────────────────────────────────────
def make_fov_cone(angle_deg: float, length: float, direction: float,
                  color: str, opacity: float = 0.25,
                  tip: np.ndarray = None) -> Polygon:
    """
    Build a triangular FOV cone whose TIP is exactly at `tip` (default ORIGIN).
    The cone fans out from `tip` in `direction` (radians) with the given full angle.

    KEY FIX: pass tip=agent.get_right() so the cone starts at the eye surface,
    never use move_to() which shifts by bounding-box centre, not by the tip vertex.
    """
    if tip is None:
        tip = ORIGIN.copy()
    half = np.radians(angle_deg / 2)
    p1 = tip + length * np.array([np.cos(direction + half), np.sin(direction + half), 0])
    p2 = tip + length * np.array([np.cos(direction - half), np.sin(direction - half), 0])
    return Polygon(tip, p1, p2,
                   fill_color=color, fill_opacity=opacity,
                   stroke_width=0)


# ────────────────────────────────────────────────────────────────
# Neural Network Helper
# ────────────────────────────────────────────────────────────────
def create_neural_net(layer_sizes, radius=0.1, h_buff=0.4, v_buff=0.25,
                      node_color=BLUE_3B1B, edge_color=GRAY_DIM):
    layers = []
    for n in layer_sizes:
        layer = VGroup(*[
            Circle(radius=radius, color=node_color,
                   stroke_width=1.5, fill_opacity=0.2)
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
                    stroke_width=0.8, color=edge_color, stroke_opacity=0.4,
                ))

    return VGroup(edges, nodes), edges, layers


# ────────────────────────────────────────────────────────────────
# Main Scene
# ────────────────────────────────────────────────────────────────
class VisionMorphology(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        self.intro_scene()
        self.fov_tradeoff_scene()
        self.predator_prey_scene()
        self.one_pixel_scene()
        self.conclusion_scene()

    # ─── 0. Intro ────────────────────────────────────────────────
    def intro_scene(self):
        title = Text("Sensory Morphology: Vision",
                     font_size=48, color=YELLOW_3B1B)
        subtitle = Text("When the 'Body' is part of the algorithm",
                        font_size=28, color=GRAY_LIGHT).next_to(title, DOWN, buff=0.3)

        self.play(Write(title, run_time=1.2))
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, subtitle)))

    # ─── 1. FOV Trade-off ────────────────────────────────────────
    def fov_tradeoff_scene(self):
        # ── Header ──
        header = Text("The FOV Trade-off", font_size=36, color=BLUE_3B1B).to_edge(UP)
        nfl    = Text("No Free Lunch Theorem", font_size=20,
                      color=GRAY_DIM, slant=ITALIC).next_to(header, DOWN, buff=0.1)
        self.play(Write(header), FadeIn(nfl))

        # ── Resource bar ──
        res_label = Text("VISUAL RESOURCES", font_size=18, color=GRAY_LIGHT)
        res_bg    = Rectangle(width=2.5, height=0.25,
                              color=GRAY_DIM, fill_opacity=0.3)
        res_fill  = Rectangle(width=2.5, height=0.25,
                              color=GREEN_3B1B, fill_opacity=1,
                              stroke_width=0).align_to(res_bg, LEFT)
        res_group = VGroup(res_label, res_bg, res_fill).arrange(DOWN, buff=0.1)
        res_group.to_edge(RIGHT, buff=0.5).shift(UP * 2)
        self.play(FadeIn(res_group))

        # ── Agent ──
        agent = Circle(radius=0.4, color=GRAY_LIGHT, fill_opacity=0.9)
        agent.move_to(LEFT * 4)
        eye   = Dot(agent.get_right(), radius=0.06, color=BG_COLOR)
        self.play(Create(VGroup(agent, eye)))

        # ── Targets ──
        targets = VGroup(*[
            Star(color=YELLOW_3B1B, fill_opacity=0.9, outer_radius=0.18)
            .move_to(RIGHT * 2.5 + UP * y)
            for y in np.linspace(-2.5, 2.5, 7)
        ])
        self.play(LaggedStart(*[FadeIn(t) for t in targets], lag_ratio=0.08))

        # ── NARROW cone: tip anchored exactly at agent's right edge (the eye) ──
        eye_pos = agent.get_right()   # true tip, no bounding-box offset
        narrow_cone = make_fov_cone(18, 6.5, 0, GREEN_3B1B, 0.35, tip=eye_pos)
        narrow_lbl  = Text("Precise — but lacks coverage",
                           font_size=22, color=GREEN_3B1B).to_edge(DOWN, buff=1)

        self.play(FadeIn(narrow_cone), Write(narrow_lbl))

        # Highlight only the star inside the narrow cone (index 3 = middle)
        self.play(
            targets[3].animate.scale(2.2).set_color(GREEN_3B1B),
            *[targets[i].animate.set_opacity(0.12) for i in range(7) if i != 3],
            run_time=1,
        )
        self.wait(1.2)

        # ── WIDE cone: same tip, much larger angle ──
        wide_cone = make_fov_cone(140, 6.5, 0, RED_BRAIN, 0.18, tip=eye_pos)
        wide_lbl  = Text("Broad — but blurry",
                         font_size=22, color=RED_BRAIN).to_edge(DOWN, buff=1)

        self.play(
            ReplacementTransform(narrow_cone, wide_cone),
            ReplacementTransform(narrow_lbl,  wide_lbl),
            *[targets[i].animate.scale(1 / 2.2 if i == 3 else 1)
              .set_color(YELLOW_3B1B).set_opacity(0.45)
              for i in range(7)],
            res_fill.animate.set_color(RED_BRAIN).stretch(0.6, 0).align_to(res_bg, LEFT),
            run_time=1.5,
        )
        self.wait(2)

        self.play(FadeOut(VGroup(
            agent, eye, targets, wide_cone, wide_lbl, header, nfl, res_group
        )))

    # ─── 2. Predator vs Prey ─────────────────────────────────────
    def predator_prey_scene(self):
        header = Text("Predator vs Prey",
                      font_size=36, color=BLUE_3B1B).to_edge(UP)
        self.play(Write(header))

        # ── PREY (left side) ──
        prey_head = Circle(radius=0.75, color=GRAY_LIGHT, fill_opacity=0.15)
        prey_head.move_to(LEFT * 3.5)

        # Eyes on sides — panoramic position
        prey_eye_l = Dot(prey_head.get_left()  + RIGHT * 0.05, color=YELLOW_3B1B, radius=0.12)
        prey_eye_r = Dot(prey_head.get_right() + LEFT  * 0.05, color=YELLOW_3B1B, radius=0.12)

        # Horizontal pupils (rectangle, wide) — herbivore trait
        def h_pupil(center):
            return Rectangle(width=0.12, height=0.04,
                             fill_color=BG_COLOR, fill_opacity=1,
                             stroke_width=0).move_to(center)

        pupil_pl = h_pupil(prey_eye_l.get_center())
        pupil_pr = h_pupil(prey_eye_r.get_center())

        # FOV cones: tip anchored at each eye centre — no move_to drift
        fov_pl = make_fov_cone(160, 3.5, np.pi, YELLOW_3B1B, 0.18,
                               tip=prey_eye_l.get_center())   # facing LEFT
        fov_pr = make_fov_cone(160, 3.5, 0,     YELLOW_3B1B, 0.18,
                               tip=prey_eye_r.get_center())   # facing RIGHT

        prey_lbl = Text("Prey: ~340° Panorama", font_size=20, color=YELLOW_3B1B)
        prey_lbl.next_to(prey_head, DOWN, buff=1.2)

        prey_group = VGroup(fov_pl, fov_pr, prey_head,
                            prey_eye_l, prey_eye_r,
                            pupil_pl, pupil_pr, prey_lbl)

        # ── PREDATOR (right side) ──
        pred_head = Circle(radius=0.75, color=GRAY_LIGHT, fill_opacity=0.15)
        pred_head.move_to(RIGHT * 3.5)

        # Eyes front-facing
        pred_eye_l = Dot(pred_head.get_center() + LEFT  * 0.28 + UP * 0.15,
                         color=RED_BRAIN, radius=0.12)
        pred_eye_r = Dot(pred_head.get_center() + RIGHT * 0.28 + UP * 0.15,
                         color=RED_BRAIN, radius=0.12)

        # Vertical pupils — slit pupils, better depth at low light
        def v_pupil(center):
            return Rectangle(width=0.04, height=0.14,
                             fill_color=BG_COLOR, fill_opacity=1,
                             stroke_width=0).move_to(center)

        pupil_pdl = v_pupil(pred_eye_l.get_center())
        pupil_pdr = v_pupil(pred_eye_r.get_center())

        # Two forward cones — tip at each eye, overlapping = binocular depth zone
        fov_pdl = make_fov_cone(60, 4.5, 0, RED_BRAIN, 0.18,
                                tip=pred_eye_l.get_center())
        fov_pdr = make_fov_cone(60, 4.5, 0, RED_BRAIN, 0.18,
                                tip=pred_eye_r.get_center())

        # Binocular overlap region — simple ellipse approximation (avoids Boolean crash)
        binocular = Ellipse(width=2.2, height=1.8,
                            fill_color=WHITE, fill_opacity=0.15,
                            stroke_width=0)
        binocular.move_to(pred_head.get_center() + RIGHT * 2.5 + UP * 0.1)

        binocular_lbl = Text("Stereoscopic Vision (Depth)", font_size=16, color=WHITE)
        binocular_lbl.next_to(binocular, UP, buff=0.1)

        # Blind spot behind head
        blind = make_fov_cone(100, 2, np.pi, "#000000", 0.5)
        blind.move_to(pred_head.get_center())
        blind_lbl = Text("Blind spot", font_size=16, color=GRAY_DIM)
        blind_lbl.next_to(pred_head, LEFT, buff=2.0).shift(DOWN * 0.3)

        pred_lbl = Text("Predator: Depth + Blind Spot", font_size=20, color=RED_BRAIN)
        pred_lbl.next_to(pred_head, DOWN, buff=1.2)

        pred_group = VGroup(blind, fov_pdl, fov_pdr, binocular,
                            pred_head, pred_eye_l, pred_eye_r,
                            pupil_pdl, pupil_pdr,
                            binocular_lbl, blind_lbl, pred_lbl)

        # ── Divider ──
        divider = DashedLine(UP * 3, DOWN * 3, color=GRAY_DIM, dash_length=0.15)

        self.play(Create(divider))
        self.play(FadeIn(prey_group))
        self.wait(0.8)
        self.play(FadeIn(pred_group))
        self.wait(0.8)

        # Blink predator pupils to draw attention to slit shape
        self.play(
            pupil_pdl.animate.scale(1.5),
            pupil_pdr.animate.scale(1.5),
            binocular.animate.set_fill(opacity=0.35),
            run_time=0.8,
        )
        self.play(
            pupil_pdl.animate.scale(1 / 1.5),
            pupil_pdr.animate.scale(1 / 1.5),
            run_time=0.5,
        )
        self.wait(2)

        self.play(FadeOut(VGroup(prey_group, pred_group, divider, header)))

    # ─── 3. 1-Pixel Minimalism ───────────────────────────────────
    def one_pixel_scene(self):
        header = Text("Minimalism — 1-Pixel Intelligence",
                      font_size=36, color=BLUE_3B1B).to_edge(UP)
        self.play(Write(header))

        divider = DashedLine(UP * 2.5, DOWN * 2.5, color=GRAY_DIM)
        self.play(Create(divider))

        # ── LEFT: large neural net ──
        nn_group, edges, layers = create_neural_net([4, 6, 6, 4])
        nn_group.scale(0.85).move_to(LEFT * 3.5)
        nn_lbl = Text("Giant Neural Network",
                      font_size=20, color=BLUE_3B1B).next_to(nn_group, UP, buff=0.2)

        self.play(FadeIn(nn_group), Write(nn_lbl))

        # NN activation flicker (now actually called)
        rng = np.random.default_rng(42)
        for _ in range(3):
            chosen_idxs = rng.choice(len(edges), size=12, replace=False)
            anims = [edges[i].animate.set_stroke(color=YELLOW_3B1B, opacity=0.9)
                     for i in chosen_idxs]
            reset = [edges[i].animate.set_stroke(color=GRAY_DIM,    opacity=0.4)
                     for i in chosen_idxs]
            self.play(*anims, run_time=0.35)
            self.play(*reset, run_time=0.25)

        # ── RIGHT: 1-pixel sensor robot ──
        # Body parts
        body = Rectangle(width=0.9, height=1.3,
                         color=GRAY_LIGHT, stroke_width=2, fill_opacity=0.1)
        head = Circle(radius=0.3, color=GRAY_LIGHT,
                      stroke_width=2, fill_opacity=0.1).next_to(body, UP, buff=0)
        leg_l = Line(body.get_bottom() + LEFT  * 0.3, body.get_bottom() + LEFT  * 0.3 + DOWN * 0.7)
        leg_r = Line(body.get_bottom() + RIGHT * 0.3, body.get_bottom() + RIGHT * 0.3 + DOWN * 0.7)

        robot = VGroup(body, head, leg_l, leg_r).move_to(RIGHT * 3.5 + UP * 0.3)

        # 1-pixel sensor: a small bright square on the underside
        sensor = Square(side_length=0.22,
                        fill_color=YELLOW_3B1B, fill_opacity=1.0,
                        stroke_width=0)
        sensor.move_to(body.get_bottom() + DOWN * 0.12)

        pixel_lbl = Text("1-Pixel Sensor", font_size=22, color=YELLOW_3B1B)
        pixel_lbl.next_to(robot, UP, buff=0.15)

        self.play(FadeIn(robot), Create(sensor), Write(pixel_lbl))

        # ── Ground path ──
        ground_y = body.get_bottom().copy() + DOWN * 0.85
        CELL = 0.4
        N_CELLS = 12
        pattern = [0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1]  # 0=dark 1=light

        cells = VGroup(*[
            Square(
                side_length=CELL,
                fill_color=WHITE if pattern[i] else "#111111",
                fill_opacity=1.0,
                stroke_width=0.5,
                stroke_color=GRAY_DIM,
            )
            for i in range(N_CELLS)
        ]).arrange(RIGHT, buff=0)
        cells.move_to(ground_y + RIGHT * 0)

        ground_lbl = Text("Ground: Dark=Obstacle / Light=Path",
                          font_size=16, color=GRAY_DIM).next_to(cells, DOWN, buff=0.2)
        self.play(FadeIn(cells), Write(ground_lbl))

        # ── Scan: robot moves right, sensor reads cell color ──
        decision_history = []
        sensor_start_x = sensor.get_center()[0]

        for step in range(5):
            cell_color = WHITE if pattern[step] else "#111111"
            is_dark = pattern[step] == 0
            decision = "STOP" if is_dark else "MOVE"
            decision_color = RED_BRAIN if is_dark else GREEN_3B1B

            # Move robot + sensor right by one cell
            self.play(
                robot.animate.shift(RIGHT * CELL),
                sensor.animate.shift(RIGHT * CELL).set_fill(color=cell_color),
                run_time=0.45,
            )

            # Pop-up decision label above robot
            dec_lbl = Text(decision, font_size=18, color=decision_color, weight=BOLD)
            dec_lbl.next_to(robot, UP, buff=0.05)
            self.play(FadeIn(dec_lbl, shift=UP * 0.1), run_time=0.2)
            self.wait(0.25)
            self.play(FadeOut(dec_lbl), run_time=0.15)

        insight = Text("Right Position × Enough Info = Optimal Minimalism",
                       font_size=22, color=YELLOW_3B1B).to_edge(DOWN, buff=0.6)
        self.play(Write(insight))
        self.wait(2)

        self.play(FadeOut(VGroup(
            header, divider, nn_group, nn_lbl,
            robot, sensor, pixel_lbl, cells, ground_lbl, insight
        )))

    # ─── 4. Conclusion (Seesaw) ───────────────────────────────────
    def conclusion_scene(self):
        header = Text("Unified Parameter θ",
                      font_size=36, color=BLUE_3B1B).to_edge(UP)
        formula = MarkupText(
            'θ = (θ<sub>brain</sub>,  θ<sub>body</sub>)',
            font_size=48, color=GRAY_LIGHT,
        ).next_to(header, DOWN, buff=0.4)
        tagline = Text("The body is a parameter — not just the brain learns",
                       font_size=22, color=YELLOW_3B1B).next_to(formula, DOWN, buff=0.3)

        self.play(Write(header), Write(formula))
        self.play(FadeIn(tagline, shift=UP * 0.15))
        self.wait(0.8)

        # ── Seesaw ──
        pivot_center = DOWN * 1.8
        pivot = Triangle(color=GRAY_DIM, fill_opacity=0.8).scale(0.35)
        pivot.move_to(pivot_center)

        BEAM_LEN = 7
        beam = Line(LEFT * (BEAM_LEN / 2), RIGHT * (BEAM_LEN / 2),
                    color=GRAY_LIGHT, stroke_width=7)
        beam.move_to(pivot.get_top())

        # θ_brain box (left, heavy initially)
        brain_sq  = Square(side_length=1.1, color=RED_BRAIN, fill_opacity=0.55)
        brain_txt = MarkupText('θ<sub>brain</sub>', font_size=24, color=GRAY_LIGHT)
        weight_brain = VGroup(brain_sq, brain_txt)
        weight_brain.move_to(beam.get_left() + UP * 0.55)

        lbl_brain = Text("Flexible\nFast changing",
                         font_size=16, color=RED_BRAIN, line_spacing=0.8)
        lbl_brain.next_to(weight_brain, DOWN, buff=0.1)

        # θ_body box (right, small initially)
        body_sq  = Square(side_length=0.6, color=BLUE_3B1B, fill_opacity=0.55)
        body_txt = MarkupText('θ<sub>body</sub>', font_size=18, color=GRAY_LIGHT)
        weight_body = VGroup(body_sq, body_txt)
        weight_body.move_to(beam.get_right() + UP * 0.3)

        lbl_body = Text("Rigid\nSlow changing",
                        font_size=16, color=BLUE_3B1B, line_spacing=0.8)
        lbl_body.next_to(weight_body, DOWN, buff=0.1)

        # Group everything on the seesaw together so rotation is coherent
        seesaw_parts = VGroup(beam, weight_brain, weight_body, lbl_brain, lbl_body)

        # Initial tilt: brain side is heavy → left side down
        TILT = 12 * DEGREES
        seesaw_parts.rotate(TILT, about_point=pivot.get_top())

        self.play(Create(pivot), Create(beam))
        self.play(FadeIn(weight_brain), FadeIn(weight_body))
        self.play(Write(lbl_brain), Write(lbl_body))
        self.wait(1)

        # ── Optimization: body grows, seesaw balances ──
        new_body_sq  = Square(side_length=1.1, color=BLUE_3B1B, fill_opacity=0.65)
        new_body_txt = MarkupText('θ<sub>body</sub>', font_size=24, color=GRAY_LIGHT)
        new_weight_body = VGroup(new_body_sq, new_body_txt)
        new_weight_body.move_to(weight_body.get_center())

        self.play(
            Transform(weight_body, new_weight_body),
            seesaw_parts.animate.rotate(-TILT, about_point=pivot.get_top()),
            run_time=2,
        )

        balance_lbl = Text("Optimal Equilibrium",
                           font_size=26, color=YELLOW_3B1B).to_edge(DOWN, buff=0.8)
        self.play(Write(balance_lbl))
        self.play(Indicate(formula, color=YELLOW_3B1B, scale_factor=1.12))
        self.wait(3)

        # ── Fade out all ──
        self.play(FadeOut(VGroup(
            header, formula, tagline,
            pivot, seesaw_parts, balance_lbl
        )))