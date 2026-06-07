# Visual-First Revision Storyboard

Goal: keep the project detailed, but stop making the viewer read a seminar deck.

The next version should move most explanation into voiceover and make the screen do visual work:

```text
visual first -> short labels -> voiceover explains the detail -> brief summary card
```

## 1. Main Direction

Current issue:

- The 60-minute preview is detailed, but many new deep-dive scenes are text-heavy.
- Some scenes feel like lecture slides instead of animated explanation.
- Long `Write()` animations on text can briefly look broken while the letters are being drawn.

Revision principle:

- Text-only scenes become **chapter summary cards**, not the main content.
- Every major idea should be shown as one of:
  - diagram,
  - chart,
  - moving process flow,
  - toy simulation,
  - comparison layout,
  - parameter slider,
  - map/task environment.

Screen text budget:

| Element | Limit |
|---|---:|
| Main title | 1 line |
| Labels | 1-4 words each |
| Caption | 1 sentence |
| Bullet list | Maximum 3 bullets, only on summary cards |

Target runtime:

| Version | Runtime | Style |
|---|---:|---|
| Visual longform | 55-70 min | Recommended |
| Full seminar fallback | 60-90 min | Keep only if teacher wants maximum coverage |

The recommended direction is **55-70 min visual longform**: still detailed, but much less boring because the viewer is watching systems change instead of reading slides.

Current implementation status:

| Item | Status |
|---|---|
| Episode 1 deep-dive conversion | Implemented visual-first scenes |
| Episode 2 deep-dive conversion | Implemented visual-first scenes |
| Episode 3 deep-dive conversion | Implemented visual-first scenes |
| Paced voiceover beats | Implemented across all 17 deep-dive scenes |
| Longform preview after paced expansion | 55:02.95 |
| Remaining conversion work | Record/update final voiceover timing after approval |

The preview now reaches the lower end of the 55-70 minute target. The added
runtime comes from paced visual highlights and voiceover holds, not from adding
dense text back onto the screen.

Current local visual QA sheets:

```text
outputs/visual_first_expanded_audit/Episode1_sheet.png
outputs/visual_first_expanded_audit/Episode2_sheet.png
outputs/visual_first_expanded_audit/Episode3_sheet.png
outputs/visual_first_ep2_audit_fixed/ep2_visual_first_sheet.png
outputs/visual_first_remaining_audit/Episode1_sheet.png
outputs/visual_first_remaining_audit/Episode3_sheet.png
```

## 2. Structure

| Part | Visual Role | Text Role |
|---|---|---|
| A. Body/Eye/Brain Loop | Fish, flow field, loop diagram | 1 summary card |
| B. Biological Vision | Eye gallery, acuity axis, trade-off diagrams | 1 summary card |
| C. Photoreceptors | PR cones, task maps, baseline charts, optimization loop | 2 summary cards |
| D. Differentiable Simulation | particle grid, computational graph, gradient arrows | 1 summary card |
| E. DiffuseBot/Fabrication | diffusion pipeline, robotization loop, constraint dashboard | 1 summary card |

## 3. Scene-by-Scene Visual Rewrite Plan

### Episode 1: Morphology and Vision

| Current Scene | Keep / Replace | New Visual Script |
|---|---|---|
| `Scene1BDesignLoop` | Keep, improve | Animate `world -> eye -> brain -> body -> world`; each node lights up as voiceover explains the feedback loop. |
| `Scene8PassiveDynamicsDeepDive` | Replace with visual scene | Show fish in current. Add controller effort gauge: stiff body needs high effort, compliant body needs low effort. End with tiny summary label: `good morphology reduces control burden`. |
| `Scene9EcologicalFramingDeepDive` | Replace with visual scene | Show same eye placed in three environments: open water, cluttered reef, dark cave. Performance bars change by environment. |
| `Scene2BVisionTradeoffs` | Keep, expand visually | Use a trade-off axis: wide FOV vs high acuity; animal icons move along the axis. |
| `Scene2CVisualAcuity` | Keep, make more visual | Replace final text contrast with small chart: detail needed vs sensor cost. |
| `Scene10BiologicalVisionDeepDive` | Replace with visual montage | Use three mini-diagrams: pupil shape, scallop mirror path, distributed eyes. One design tag per example. |
| `Scene11OceanAcuityDeepDive` | Replace with visual chart | Make an acuity/range chart. Show why coarse vision can still be useful for behavior. |
| `Scene3BEcologicalCaveat` | Keep as summary card | This is a caution card; keep it short. Use two boxes only: `too simple` vs `better scientific frame`. |
| `Scene4BUtilityContext` | Keep, improve | Animate same design getting different scores under different tasks. Use score bars, not extra text. |

### Episode 2: Photoreceptors

| Current Scene | Keep / Replace | New Visual Script |
|---|---|---|
| `Scene8PRSignalDeepDive` | Replace with visual scene | Show a PR cone sampling a patch of the world. The output becomes one scalar/color chip. Move the cone to front/side/down and show signal meaning change. |
| `Scene2CCameraBaseline` | Keep | Camera grid vs 64 PR dots is strong. Add bandwidth bar chart: `16,384 values` vs `64 readings`. |
| `Scene9CameraBaselineDeepDive` | Replace with visual chart | Show performance vs bandwidth: camera high bandwidth, PR low bandwidth, blind lowest sensing. |
| `Scene2BDesignVector` | Keep, improve | Keep robot body and cone. Turn `(x,y,z,pitch,yaw,roll,fov)` into visual handles around the PR. |
| `Scene12DesignVectorDeepDive` | Replace with parameter sliders | Show 7 sliders: position, orientation, FOV. Each slider moves the cone. |
| `Scene3BTaskDefinitions` | Keep | Make task maps larger: PointGoalNav coordinate arrow, TargetNav unknown target search. |
| `Scene10PointGoalNavDeepDive` | Replace with map animation | Show GPS arrow already pointing to goal; PR helps avoid obstacle/floor cues. |
| `Scene11TargetNavDeepDive` | Replace with search animation | Agent scans for green target. PR signal spikes when target enters cone. |
| `Scene3CBaselines` | Keep, chartify | Replace list with three agents side-by-side: blind, camera, PR. Add metric badges only. |
| `Scene4BDesignOptimization` | Keep, improve | Naive search as a slow loop; joint optimization as one rollout feeding two updates. |
| `Scene13JointOptimizationDeepDive` | Replace with moving loop | One rollout trace, two gradient arrows: `update controller`, `update sensor design`. |
| `Scene4CJointTraining` | Keep | Already visual. Use as main method explanation. |
| `Scene5DBadDesigns` | Keep | Good visual. Add failed sensor as red cone and good sensor as green cone. |
| `Scene5BEvidence` | Keep, expand chart | Use three charts: optimization trajectories, PointGoalNav SPL, TargetNav success. |
| `Scene14EvidenceDeepDive` | Replace with evidence dashboard | One dashboard page with all metrics, then zoom into each metric. |
| `Scene5CHumanSurvey` | Keep | Human guess vs computational search is visual enough after cleanup. |
| `Scene6BTargetCheck` | Keep | Make green target vs transparent target the main visual ablation. |
| `Scene6CRealWorldSetup` | Keep | Good sim-to-real diagram after cleanup. |
| `Scene15SurveyTransferDeepDive` | Replace with summary card | Keep only as end-of-Episode-2 summary: survey, real robot, limitation. |
| `Scene6DPRLimitations` | Keep as summary card | Use `supported` vs `not implied`; no extra paragraphs. |

### Episode 3: Physical Morphology and Generative Design

| Current Scene | Keep / Replace | New Visual Script |
|---|---|---|
| `Scene6ClassicalDesignDeepDive` | Replace with evolutionary search animation | Generate random bodies, simulate, score, select, mutate. Keep Karl Sims as historical context in voiceover only. |
| `Scene2BChainQueenLimits` | Keep | It is already visual enough; make particle grid larger and reduce text. |
| `Scene2CForwardBackward` | Keep | Computational graph is good. Add a moving reward signal backward through the graph. |
| `Scene7DifferentiableSimulationDeepDive` | Replace with visual graph | Show state history being stored, then gradient arrows flowing backward. Use memory meter. |
| `Scene3BBodyParameters` | Keep | Use sliders for shape/material/actuation instead of static boxes. |
| `Scene8CoDesignDeepDive` | Replace with coupled sliders | Move body stiffness and controller gain together; show behavior score changing. |
| `SceneAttractor` | Keep, shorten | Use as metaphor only. Add small label: `metaphor: structured design space`. |
| `Scene4CDiffusionBasics` | Keep | Strong visual pipeline from noise to shape. |
| `Scene4BDiffusionConstraints` | Keep, improve | Turn `looks plausible` vs `can work` into a pass/fail physics filter. |
| `Scene4DRobotizationPipeline` | Keep | Fixed layout. Add icons for geometry/material/actuator/controller/fabrication. |
| `Scene9DiffuseBotDeepDive` | Replace with pipeline animation | Generate candidate -> robotize -> simulate -> utility gradient -> guided update. |
| `Scene5BLimitations` | Keep as summary card | Constraint dashboard works. |
| `Scene10FabricationSynthesisDeepDive` | Replace with final loop animation | Show the complete loop: world, eye, controller, body, fabrication constraints. |

## 4. Proposed Runtime Allocation

| Part | Runtime | Visual Density |
|---|---:|---|
| A. Morphology loop | 8-10 min | High |
| B. Biological vision | 10-12 min | High |
| C. Photoreceptors | 24-30 min | Very high |
| D. Differentiable simulation | 10-13 min | Medium-high |
| E. DiffuseBot and fabrication | 8-10 min | High |
| Final synthesis | 2-3 min | Medium |

Expected total: **62-68 minutes** if voiceover remains detailed.

## 5. Summary Cards Only

Keep only these text-heavy cards:

| Card | Purpose | Max Duration |
|---|---|---:|
| End of Part A | Body/eye/brain/world loop | 25s |
| End of Part B | Vision is task-dependent | 25s |
| Mid Episode 2 | PR method summary | 35s |
| End Episode 2 | What PR result does and does not prove | 35s |
| End Episode 3 | Limits of differentiable/generative design | 30s |
| Final thesis | Intelligence is distributed across the loop | 35s |

Everything else should be visual-first.

## 6. Layout QA Rules

Apply these before every render-all:

1. Extract 20%, 50%, and 80% frames for every new scene.
2. No frame should have more than 40 readable words unless it is a summary card.
3. No long sentence should use `Write()`; use `FadeIn()` instead.
4. Avoid `Transform()` from many text objects into a sentence; fade out then fade in.
5. Keep the bottom caption at least `0.45` units above the frame edge.
6. If a scene has a chart or diagram, it should occupy at least 55% of the frame.

## 7. Implementation Order

Recommended next coding batch:

1. Convert the 17 seminar deep-dive scenes into visual scenes or short summary cards.
2. Replace long bullet boxes with diagrams and charts first in Episode 2.
3. Re-render low-quality preview.
4. Generate contact sheets for all scenes.
5. Only then update voiceover timing.

Do not rewrite the whole project in one pass. Episode 2 should be converted first because it is the technical center of the video.
