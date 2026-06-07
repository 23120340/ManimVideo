# Full Detail Revision Plan

This document is a production-level review and expansion plan for turning the current `ManimVideo_full.mp4` into a more complete explainer based on the source tutorial:

- Source video: https://www.youtube.com/watch?v=vqILEFz85Ac
- CVPR tutorial page: https://cvpr.thecvf.com/virtual/2024/tutorial/23736
- Tutorial project page: https://comp-design.epfl.ch/
- Photoreceptor project: https://visual-morphology.epfl.ch/
- ChainQueen: https://yuanming.taichi.graphics/publication/2019-chainqueen/
- DiffuseBot: https://diffusebot.github.io/

The current local reference transcript is stored at:

```text
build/source_video/vqILEFz85Ac.en-orig.vtt
```

`build/` is ignored by Git, so this transcript is only a local working reference.

## 1. Executive Summary

The current video is coherent and visually polished, but it is structurally closer to an **11-minute overview** than a detailed treatment of the 3:04:00 source tutorial.

The main issue is not that the video misses one or two isolated facts. The deeper issue is that many sections stop at the level of the big idea and do not yet include the full chain:

```text
motivation -> design variable -> task/environment -> method -> experiment -> evidence -> limitation
```

To make the project feel complete, the revised version should explain not only **what computational design is**, but also:

- what is being optimized,
- what tasks are used to evaluate a design,
- what baselines the method is compared against,
- what evidence supports the claims,
- where the method fails or remains limited.

Recommended target length:

| Version | Target Runtime | Use Case |
|---|---:|---|
| Minimal repair | 18-22 min | Enough to address "too shallow" feedback |
| Full explainer | 32-40 min | Best balance between detail and production effort |
| Seminar-style version | 60-90 min | Comparable to long student presentations |

Current chosen path: **visual longform**, using **55-70 minutes** as the production target. The 60-90 minute seminar version remains useful only as a fallback if maximum coverage matters more than watchability.

## 2. Core Thesis

The current thesis is:

> Intelligence does not only live in the brain. It also lives in the body.

The expanded thesis should be:

> Computational design is not just "AI drawing robots." It is the joint optimization of **body, brain, and eye** for a specific task, environment, simulator, and set of real-world constraints.

The recurring framework should be:

```text
body morphology + perceptual morphology + controller + task + environment
```

Or visually:

```text
environment -> sensor/eye -> controller/brain -> body -> environment
```

## 3. Source Tutorial Coverage Map

The source video is **3:04:00** long. Based on the transcript and official tutorial schedule, its content can be compressed into the following map.

| Source Time | Source Topic | Current Coverage | Gap |
|---:|---|---|---|
| 00:00-05:00 | Dead fish, clever morphology, body-water interaction | Ep1 Scene0-1 | Good hook, but needs explicit physical/perceptual morphology framing |
| 05:00-18:00 | Computational design framing, ecological theory, body-brain-eye | Ep1 Scene1, Scene4 | Missing ecological theory and task/environment framing |
| 18:00-35:00 | Biological visual diversity: FOV, pupil, retina, eagle, scallop, tarsier | Ep1 Scene2 | Good montage, but insufficient design-variable explanation |
| 35:00-50:00 | Photoreceptor tasks, camera vs PR, PointGoalNav, TargetNav, real-world robot | Ep2 Scene1-3, Scene6 | Missing task definitions, baselines, and evidence |
| 50:00-65:00 | Computational design optimization for photoreceptors | Ep2 Scene4-5 | Missing 7D design vector, design/control policies, human survey |
| 65:00-100:00 | Oceanic animal visual acuity and measurement | Almost absent | Major missing topic if aiming for source fidelity |
| 100:00-125:00 | Transition to physical morphology and classical approaches | Ep1 Scene5, Ep3 intro | Missing classical design framing and physical morphology taxonomy |
| 125:00-145:00 | Soft robotics, differentiable simulation, ChainQueen | Ep3 Scene1-2 | Too compressed; needs why soft physics is hard |
| 145:00-160:00 | Co-design: gradients for controller and body parameters | Ep3 Scene3, Attractor | Needs concrete design parameters and trade-offs |
| 160:00-175:00 | Generative design, diffusion, Point-E, strawberry robot failure | Ep3 Scene4 | Needs diffusion pipeline and failure examples |
| 175:00-184:00 | Fabrication, real-world constraints, industry | Ep3 Scene5 | Has sim-to-real, but lacks fabrication/industry/limitations |

## 4. Current Video Coverage Map

The current rendered video is **681.445s = 11:21.45**.

| # | Current Scene | Runtime | Revision Notes |
|---:|---|---:|---|
| 1 | Ep1 Scene0 Cold Open | 30.1s | Keep hook; add explicit physical morphology language in voiceover |
| 2 | Ep1 Scene1 Main Question | 40.7s | Add `theta_eye`; current frame only emphasizes brain/body |
| 3 | Ep1 Scene2 Eye Diversity | 81.3s | Add design-variable tags and one measurement/trade-off layer |
| 4 | Ep1 Scene3 Zebra Twist | 64.9s | Add caveat: stripe/fly explanation is a supported hypothesis, not a universal final answer |
| 5 | Ep1 Scene4 Math Formulation | 64.6s | Expand utility into task/environment-dependent optimization |
| 6 | Ep1 Scene5 Karl Sims | 37.6s | Expand into evolutionary search loop |
| 7 | Ep1 Scene6 Cliffhanger | 54.1s | Clarify "4 pixels" as an intuition hook, not the full paper claim |
| 8 | Ep1 Scene7 Outro | 4.8s | Remove or convert to section divider in a single full video |
| 9 | Ep2 Scene1 Recap | 17.9s | Replace recap with smoother transition if final video is continuous |
| 10 | Ep2 Scene2 Photoreceptor | 26.1s | Needs major expansion: 2-3 minutes minimum |
| 11 | Ep2 Scene3 Navigation | 21.1s | Needs task definitions, baselines, and metrics |
| 12 | Ep2 Scene4 BiLevel | 24.4s | Needs naive approach before the trick |
| 13 | Ep2 Scene5 Surprise | 29.5s | Good idea, but must be tied to PointGoalNav/GPS+Compass |
| 14 | Ep2 Scene6 SimToReal | 20.6s | Add real-world setup and no-real-training caveat |
| 15 | Ep2 Scene7 Cliffhanger | 26.1s | Add bridge from perceptual morphology to physical morphology |
| 16 | Ep3 Scene1 Hook | 19.4s | Good visual hook, but too fast for method explanation |
| 17 | Ep3 Scene2 DiffSim | 19.0s | Add computational cost, contact, materials, model error |
| 18 | Ep3 Scene3 CoDesign | 25.0s | Add concrete design parameters: stiffness, actuator, shape |
| 19 | Ep3 SceneAttractor | 20.4s | Keep as metaphor, but explicitly label as metaphor |
| 20 | Ep3 Scene4 DiffuseBot | 21.8s | Major expansion needed |
| 21 | Ep3 Scene5 Outro | 32.0s | Add limitations, fabrication, and future directions |

## 5. Proposed Full Structure: 75-Minute Version

Target runtime: **55-70 minutes**, with **about 55-60 minutes** as the current working target.

| Part | Runtime | Purpose |
|---|---:|---|
| A. Morphology as Intelligence | 8-10 min | Establish body/eye/brain as design variables |
| B. Biological Vision as Design | 12-15 min | Show natural visual systems as specialized solutions |
| C. Photoreceptors and Perceptual Morphology | 22-28 min | Explain the main sensor-design paper in detail |
| D. Physical Morphology and Differentiable Simulation | 15-18 min | Move from sensing to body/controller co-design |
| E. Generative Design and DiffuseBot | 10-13 min | Explain physics-guided generative design |
| F. Synthesis and Limitations | 4-6 min | Close with constraints and future directions |

### Active Implementation Batch

Batch 1 starts with Episode 2 because it contains the most important missing technical chain:

```text
photoreceptor definition -> 7D design vector -> task definitions -> baselines -> joint optimization -> evidence
```

New batch-1 scenes:

| File | Purpose |
|---|---|
| `Episode2/scene2b_design_vector.py` | Make the 7D photoreceptor design vector explicit |
| `Episode2/scene3b_task_definitions.py` | Separate PointGoalNav and TargetNav before showing results |
| `Episode2/scene4b_design_optimization.py` | Explain why naive sensor search is expensive |
| `Episode2/scene5b_evidence.py` | Show reported optimization/evidence metrics from the project page |
| `Episode2/scene6b_target_check.py` | Explain the transparent-target cue check |
| `Episode1/scene1b_design_loop.py` | Introduce the body-eye-brain-world loop |
| `Episode1/scene2b_vision_tradeoffs.py` | Convert biological eye examples into design trade-offs |
| `Episode1/scene3b_ecological_caveat.py` | Add scientific caution around adaptive explanations |
| `Episode3/scene2b_chainqueen_limits.py` | Explain why differentiable soft-body physics is hard |
| `Episode3/scene3b_body_parameters.py` | Make body design parameters concrete |
| `Episode3/scene4b_diffusion_constraints.py` | Clarify DiffuseBot as physics-guided generative search |
| `Episode3/scene5b_limitations.py` | Add a limitations checklist before the final synthesis |
| `Episode2/scene5c_human_survey.py` | Explain why human intuition is a meaningful comparison |
| `Episode2/scene6c_real_world_setup.py` | Add real-world transfer details for the PR demo |

### Implemented Longform Status

The current local longform preview now uses the `Longform` render list:

```powershell
.\render_full_video.ps1 -Version Longform -Quality l -SkipRender -Output ManimVideo_longform_preview.mp4
```

Measured preview status:

| Item | Value |
|---|---:|
| Scene count | 62 scenes |
| Preview duration | 3302.954900s |
| Runtime | 55:02.95 |

The preview file is:

```text
ManimVideo_longform_preview.mp4
```

Seminar deep-dive frame checks are stored locally at:

```text
outputs/longform_frame_checks/seminar_deep_dive_fixed2/
```

`outputs/` is ignored by Git, so these checks are local production artifacts.

Current note:

The longform preview is now a **55-minute visual-first pass**. All 17 seminar
deep-dive scenes have been converted from long slide-style explanations into
diagrams, charts, maps, sliders, and process flows. Each deep-dive scene also
uses paced highlight beats so the voiceover has time to explain the visual
without adding dense paragraphs back onto the screen.

If more runtime is needed, keep extending with animated examples, slower
voiceover holds, and short summary cards. Do not restore dense bullet slides.

### Batch 2 Expansion Scenes

These scenes fill the remaining content gaps before the seminar deep-dive layer:

| File | Purpose |
|---|---|
| `Episode1/scene2c_visual_acuity.py` | Add visual acuity as a measurable design property |
| `Episode1/scene4b_utility_context.py` | Make utility task- and environment-dependent |
| `Episode2/scene2c_camera_baseline.py` | Explain camera bandwidth as the main comparison point |
| `Episode2/scene3c_baselines.py` | Separate blind, camera, and PR baselines |
| `Episode2/scene4c_joint_training.py` | Explain the shared backward pass for design/control learning |
| `Episode2/scene5d_bad_designs.py` | Show that poor sensor placement can break behavior |
| `Episode2/scene6d_pr_limitations.py` | Add scope limits for photoreceptor claims |
| `Episode3/scene2c_forward_backward.py` | Explain forward simulation and backward gradients |
| `Episode3/scene4c_diffusion_basics.py` | Add the diffusion-denoising intuition before DiffuseBot |
| `Episode3/scene4d_robotization_pipeline.py` | Show how a generated shape becomes a robot candidate |

### Batch 3 Visual-First Deep-Dive Scenes

These scenes used to be slower seminar-slide explanations. They have now been
rewritten as visual-first scenes with the same class names, so the render list
does not need to change. Their role is to support detailed voiceover while
keeping the screen focused on diagrams instead of paragraphs.

| File | Scene Class | Purpose |
|---|---|---|
| `Episode1/scene8_seminar_deep_dive.py` | `Scene8PassiveDynamicsDeepDive` | Explain why passive dynamics is a control lesson |
| `Episode1/scene8_seminar_deep_dive.py` | `Scene9EcologicalFramingDeepDive` | Tie design quality to task and niche |
| `Episode1/scene8_seminar_deep_dive.py` | `Scene10BiologicalVisionDeepDive` | Reframe biological eyes as sensor strategies |
| `Episode1/scene8_seminar_deep_dive.py` | `Scene11OceanAcuityDeepDive` | Add measurement and acuity caveats |
| `Episode2/scene8_seminar_deep_dive.py` | `Scene8PRSignalDeepDive` | Explain what a PR sends and why placement matters |
| `Episode2/scene8_seminar_deep_dive.py` | `Scene9CameraBaselineDeepDive` | Ground the camera comparison in bandwidth and utility |
| `Episode2/scene8_seminar_deep_dive.py` | `Scene10PointGoalNavDeepDive` | Clarify why PointGoalNav is not purely visual |
| `Episode2/scene8_seminar_deep_dive.py` | `Scene11TargetNavDeepDive` | Clarify why TargetNav depends more on visual evidence |
| `Episode2/scene8_seminar_deep_dive.py` | `Scene12DesignVectorDeepDive` | Expand the 7D PR parameter interpretation |
| `Episode2/scene8_seminar_deep_dive.py` | `Scene13JointOptimizationDeepDive` | Explain rollout-based joint design/control optimization |
| `Episode2/scene8_seminar_deep_dive.py` | `Scene14EvidenceDeepDive` | Interpret the reported metrics carefully |
| `Episode2/scene8_seminar_deep_dive.py` | `Scene15SurveyTransferDeepDive` | Connect human survey, real robot, and limits |
| `Episode3/scene6_seminar_deep_dive.py` | `Scene6ClassicalDesignDeepDive` | Place Karl Sims/classical search in context |
| `Episode3/scene6_seminar_deep_dive.py` | `Scene7DifferentiableSimulationDeepDive` | Explain gradients, memory cost, and model limits |
| `Episode3/scene6_seminar_deep_dive.py` | `Scene8CoDesignDeepDive` | Tie body parameters to controller gradients |
| `Episode3/scene6_seminar_deep_dive.py` | `Scene9DiffuseBotDeepDive` | Explain physics-guided generative design |
| `Episode3/scene6_seminar_deep_dive.py` | `Scene10FabricationSynthesisDeepDive` | Close with fabrication, deployment, and synthesis |

## 6. Part A: Morphology as Intelligence

### Goal

Turn the dead fish hook into a rigorous conceptual frame:

```text
physical morphology can reduce the burden on active control
```

### Scene Plan

| Scene | Status | Content |
|---|---|---|
| A0 Dead Fish | Existing, light edit | Keep the fish reveal; add voiceover explaining passive dynamics |
| A1 Body-Brain-Eye | Expand | Introduce `theta_body`, `theta_eye`, `theta_brain` |
| A2 Ecological Framing | New | A design only makes sense relative to a task and environment |

### Key Terms

- physical morphology
- perceptual morphology
- controller
- ecological niche / ecological theory
- task-conditioned design

### Visual Additions

- Add a loop diagram:

```text
world -> sensor -> controller -> body -> world
```

- Add a three-part parameter block:

```text
theta_body  = shape, stiffness, material
theta_eye   = position, orientation, field of view, resolution
theta_brain = policy/controller parameters
```

### Voiceover Direction

Avoid saying "the body is intelligent" as a mystical claim. Say:

> The body stores structure that makes certain behaviors easier to control.

## 7. Part B: Biological Vision as Design

### Goal

The current biological examples are visually strong but feel like a montage. The expanded version should explicitly connect each example to a **design variable**.

### Scene Plan

| Scene | Status | Content | Design Variable |
|---|---|---|---|
| B1 Cat vs Goat | Existing, expand | Vertical vs horizontal pupils | field of view, depth |
| B2 Eagle | Existing, expand | Two high-acuity regions/foveae | resolution allocation |
| B3 Scallop | Existing, expand | Distributed mirror-based eyes | optical mechanism, sensor distribution |
| B4 Cave Fish vs Tarsier | Existing, expand | Losing eyes vs huge eyes | energy cost, low-light sensitivity |
| B5 Butterfly | Existing, expand | Pattern visible to predators, not necessarily peers | observer-dependent signal |
| B6 Visual Acuity Mini-Scene | New | Animals differ in acuity, not just eye shape | measurement and task constraint |

### Important Caveat

For zebra stripes, phrase carefully:

> One strongly supported hypothesis is that stripes reduce biting fly landings.

Do not phrase it as the single final answer for all zebra stripe evolution.

### Visual Additions

- A `design variable` tag on each animal card:

```text
FOV
resolution
placement
optics
energy cost
signal receiver
```

- A small trade-off axis:

```text
wide field of view <-------> high acuity
```

## 8. Part C: Photoreceptors and Perceptual Morphology

This should become the strongest and most detailed part of the revised video. It is currently the largest content gap.

### Source Facts to Preserve

From the photoreceptor project:

- The project replaces a standard high-resolution camera with a handful of simple **1x1 photoreceptor sensors**.
- The real-world target-ball demo uses **64 PRs**, under 1% of the camera resolution.
- The paper also shows navigation with **32 PRs**.
- PointGoalNav and TargetNav are different tasks:
  - PointGoalNav: the agent navigates to a target coordinate.
  - TargetNav: the target coordinate is not given; the agent must find a target sphere visually.
- Standard setup includes GPS+Compass in addition to visual signal.
- A sensor design includes extrinsic and intrinsic parameters:

```text
theta_i = (x_i, y_i, z_i, pitch_i, yaw_i, roll_i, fov_i)
```

- The naive design approach is expensive because every new design would require training a design-specific control policy.
- The proposed method uses joint optimization of a design policy and a control policy.
- A design-conditioned/generalist control policy can adapt to a given design.
- Reported results include:
  - design optimization improves many random initial designs,
  - 82.5% of optimization trajectories land in the improved/green region,
  - PointGoalNav SPL improves from 0.447 to 0.518,
  - TargetNav success improves from 0.363 to 0.405,
  - replacing the green target sphere with a transparent sphere drops success from 0.314 to 0.132.

### Scene Plan

| Scene | Status | Content |
|---|---|---|
| C1 Why Not Cameras? | New/merge | High-resolution cameras are the default, but not always the necessary design |
| C2 What Is a Photoreceptor? | Expand Ep2 Scene2 | 1x1 sensor, mean RGB/luminance, low-bandwidth input |
| C3 Photoreceptor Design Vector | New | 7D vector: position, orientation, FOV |
| C4 PointGoalNav vs TargetNav | New | Define the tasks before showing results |
| C5 Baselines | Expand Ep2 Scene3 | Blind agent, 128x128 camera, PR agent |
| C6 Evidence | New | Show performance/bandwidth comparison |
| C7 Why Design Matters | New | Bad PR placement can fail badly |
| C8 Naive vs Joint Optimization | Expand Ep2 Scene4 | Black-box search vs joint design/control optimization |
| C9 Human Survey | New | Human intuition vs computational design |
| C10 Real-World Robot | Expand Ep2 Scene6 | 64 PR TurtleBot-style demo, no real-world training |
| C11 Transparent Target Check | New | Green sphere vs transparent sphere |
| C12 Limitations | New | Scope, cost, power, physical size, production constraints |

### Critical Correction

The current "4 pixels" framing is useful as a hook, but it can become misleading.

Recommended wording:

> Four pixels is an intentionally extreme way to build intuition. The source work studies sensors as low as 1x1, but the strongest demonstrations use a handful of photoreceptors, such as 32 or 64 PRs, still far below the bandwidth of a normal camera.

### Visual Additions

- A sensor cone with labels:

```text
position: x, y, z
orientation: pitch, yaw, roll
intrinsic: field of view
```

- A task split card:

```text
PointGoalNav:
  target coordinate is given
  GPS+Compass available
  vision helps obstacle avoidance

TargetNav:
  target coordinate unknown
  target sphere must be found visually
  vision helps recognition + exploration
```

- A baseline chart:

```text
blind agent < PR agent ~= camera agent
```

- A bandwidth callout:

```text
64 PRs < 1% of 128x128 camera bandwidth
```

## 9. Part D: Physical Morphology and Differentiable Simulation

### Goal

Make Episode 3 feel like a method, not just a sequence of slogans.

### Scene Plan

| Scene | Status | Content |
|---|---|---|
| D1 Classical Design Search | Expand Karl Sims | generate -> simulate -> select -> mutate |
| D2 Why Soft Robots Are Hard | New | deformation, contact, material, many degrees of freedom |
| D3 Differentiable Simulation | Expand Ep3 Scene2 | simulator as computational graph |
| D4 ChainQueen | New | physically based differentiable simulation for soft robotics |
| D5 Gradient Is Not Magic | New | memory, model error, local optima |
| D6 Co-Design | Expand Ep3 Scene3 | gradients for controller and body parameters |
| D7 Attractor Metaphor | Keep/adjust | Use only after method is clear |

### Visual Additions

- Forward pass:

```text
state_0 -> physics_step -> state_1 -> ... -> reward
```

- Backward pass:

```text
dReward/dcontroller
dReward/dstiffness
dReward/dshape
dReward/dactuator
```

- Comparison table:

```text
Black-box search:
  try design -> simulate -> score -> try again

Differentiable simulation:
  simulate once -> compute gradient -> update design
```

### Claims to Keep Careful

- Gradients help find a direction of improvement; they do not guarantee the global optimum.
- A differentiable simulator is only as good as the physics model it encodes.
- Real-world transfer remains hard.

## 10. Part E: Generative Design and DiffuseBot

### Goal

Explain why generative AI alone is not enough, and why physics guidance matters.

### Scene Plan

| Scene | Status | Content |
|---|---|---|
| E1 Generative AI Failure | Expand Ep3 Scene4 | A visually plausible robot can be physically useless |
| E2 Diffusion Basics | New | noise -> denoising -> shape |
| E3 Physics-Augmented Diffusion | Expand Ep3 Scene4 | utility gradient nudges denoising |
| E4 Robotizing and Fabrication | New | geometry must become a buildable robot |
| E5 Sim-to-Real and Industry | Expand outro | fabrication cost, real-world constraints, engineering workflows |

### DiffuseBot Explanation

Use a pipeline like:

```text
random/noisy geometry
    -> diffusion proposal
    -> robotization
    -> physics simulation
    -> utility gradient
    -> guided design update
```

Avoid presenting DiffuseBot as "an LLM that understands physics." It is better framed as:

> a generative design process guided by physics-based evaluation.

## 11. Part F: Final Synthesis

### Final Message

The ending should synthesize the whole video:

- Evolution searches over body and sensor designs over billions of years.
- Computational design searches over body, eye, and controller parameters using simulation, optimization, and data.
- The best design is task-dependent and environment-dependent.
- A design must ultimately survive fabrication, cost, and real-world physics.

### Suggested Closing Voiceover

> The lesson is not that the brain is unimportant. The lesson is that intelligence is distributed across a loop: the body, the sensors, the controller, and the world they act in. Computational design is the attempt to optimize that loop, not one piece in isolation.

## 12. Implementation Plan

### Phase 0: Lock Scope

Chosen target length:

| Target | Runtime | Recommendation |
|---|---:|---|
| Short repair | 22-25 min | Good if deadline is tight |
| Full revision | 32-40 min | Fallback cut |
| Seminar version | 60-90 min | Active target |

### Phase 1: Rewrite the Script First

Do not start by adding Manim code. First rewrite:

- `docs/voiceover_script_vi.md`
- optionally create `docs/source_references.md`
- keep this file as the production plan

Script checklist:

- Decide whether the final video remains split into episodes or becomes one continuous documentary.
- Decide which numbers are spoken in voiceover and which appear only visually.
- Decide where citations/source cards appear.
- Decide target runtime per part.

### Phase 2: Add New High-Value Scenes

Prioritize new scenes that fix the deepest content gaps.

| Priority | Proposed File | Purpose |
|---:|---|---|
| 1 | `Episode2/scene2b_design_vector.py` | Explain the 7D PR design vector |
| 2 | `Episode2/scene3b_task_definitions.py` | Separate PointGoalNav and TargetNav |
| 3 | `Episode2/scene4b_design_optimization.py` | Explain naive vs joint optimization |
| 4 | `Episode2/scene5b_human_survey.py` | Add evidence from human intuition comparison |
| 5 | `Episode2/scene6b_transparent_target.py` | Add target-recognition evidence |
| 6 | `Episode3/scene2b_chainqueen.py` | Deepen differentiable simulation |
| 7 | `Episode3/scene4b_diffusion_pipeline.py` | Deepen DiffuseBot |
| 8 | `Episode3/scene5b_limitations.py` | Add fabrication and limitations |

### Phase 3: Patch Existing Scenes

| Existing Scene | Edit |
|---|---|
| Ep1 Scene0 | Add physical morphology framing in narration |
| Ep1 Scene1 | Add `theta_eye` and the body-eye-brain triangle |
| Ep1 Scene2 | Add design-variable tags to each animal example |
| Ep1 Scene3 | Add zebra/fly hypothesis caveat |
| Ep1 Scene4 | Use `U(theta; task, environment)` instead of only `U(theta)` |
| Ep1 Scene5 | Add evolutionary search loop |
| Ep1 Scene6 | Reframe 4 pixels as intuition hook |
| Ep2 Scene2 | Replace "3 parameters" with "3 groups, 7 numbers" |
| Ep2 Scene3 | Add metrics and baselines |
| Ep2 Scene4 | Explain why naive optimization is slow |
| Ep2 Scene5 | Tie downward-facing sensor to PointGoalNav and GPS+Compass |
| Ep2 Scene6 | Add real-world setup and no-real-training caveat |
| Ep3 Scene2 | Add model error, memory, contact/material limitations |
| Ep3 Scene3 | Add stiffness/actuator/shape as design parameters |
| Ep3 Scene4 | Add diffusion and robotization pipeline |
| Ep3 Scene5 | Add limitations and future directions |

### Phase 4: Update Render Pipeline

After adding scenes:

- update scene list in `render_full_video.ps1` or its helper script,
- render new scenes at low quality first,
- inspect 3 frames per scene,
- render high quality,
- concatenate with:

```powershell
.\render_full_video.ps1 -SkipRender -Quality h -Output ManimVideo_full.mp4
```

### Phase 5: Update Voiceover Timing

After every full render:

```powershell
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 .\ManimVideo_full.mp4
```

Then update `docs/voiceover_script_vi.md` with exact scene boundaries.

## 13. Content QA Checklist

A revised version is "detailed enough" if a viewer can answer:

- What is physical morphology?
- What is perceptual morphology?
- What is a photoreceptor?
- What are the 7 design parameters of a PR sensor?
- How are PointGoalNav and TargetNav different?
- Why does a downward-facing sensor make sense in PointGoalNav?
- What are the blind/camera/PR baselines?
- Why is naive design optimization too slow?
- What is jointly optimized in the design-control method?
- Why is differentiable simulation useful?
- What are the limits of gradients through physics?
- Why can generative AI produce physically bad robot designs?
- How does physics guidance change diffusion-based design?
- What remains hard in real-world fabrication and deployment?

## 14. Claim Safety Checklist

Use careful phrasing for these claims:

| Claim | Safer Wording |
|---|---|
| Zebra stripes are for flies | One strongly supported hypothesis is that stripes reduce biting fly landings |
| 4 pixels solve navigation | Four pixels is a hook; the source demonstrates that a small number of PRs can approach camera performance in some tasks |
| Same attractor basin | This is a metaphor for structured design landscapes, not a reported experimental result |
| Gradients solve design | Gradients give a useful direction under a model; they do not guarantee a global optimum |
| DiffuseBot understands physics | DiffuseBot uses physics-based feedback/guidance; it is not inherently physically intelligent |

## 15. Minimal High-Impact Edit Set

If time is limited, do these first:

1. Rewrite Episode 2 voiceover with correct PR terminology.
2. Add a PR design-vector scene.
3. Add a PointGoalNav vs TargetNav scene.
4. Expand bi-level/joint optimization.
5. Add evidence: baselines, 32/64 PRs, human survey, transparent target.
6. Add a ChainQueen/differentiable simulation detail scene.
7. Expand DiffuseBot into a real pipeline.
8. Add limitations and citations in the outro.

These changes will most directly address feedback that the project lacks detail.

## 16. Production Notes

- Add new scenes before heavily rewriting existing scenes; this reduces the chance of breaking polished layouts.
- Keep generated media in ignored folders.
- Render new scenes with `-ql` first.
- For every new scene, save 3 frame checks: start, middle, end.
- Do not overfill frames with text; detailed explanation should live in voiceover, not on-screen paragraphs.
- Prefer one technical term per beat: show it, define it, use it once in context.
- When a scene contains a formula, immediately explain what each symbol means.
- Use `docs/visual_first_revision_storyboard.md` before replacing seminar-style scenes with diagram/chart-driven scenes.
