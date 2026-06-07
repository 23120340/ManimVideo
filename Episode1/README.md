# Intelligence in the Body — Episode 1

Manim animation for **Episode 1 — *"The Dead Fish That Swims"*** of the series *"Intelligence in the Body"*, in the style of 3Blue1Brown.

The episode asks: *in a smart organism, where does intelligence live — in the brain, or also in the body?*

---

## Scene overview

| File | Scene | Timestamp | Content |
|------|-------|-----------|---------|
| `scene0.py` | 0 — Cold open | 0:00 – 0:35 | Dead fish "swimming" in a current |
| `scene1.py` | 1 — Main question | 0:35 – 2:00 | Brain vs body, θ_brain / θ_body split |
| `scene2.py` | 2 — Eye diversity | 2:00 – 5:30 | 6 cards: cat/goat, eagle, scallop, cave fish, tarsier, butterfly |
| `scene3.py` | 3 — Zebra twist | 5:30 – 7:30 | Wrong intuition; the real answer is biting flies |
| `scene4.py` | 4 — Math formulation | 7:30 – 11:00 | Design space, U(θ), optimization pipeline, two branches |
| `scene5.py` | 5 — Karl Sims 1994 | 11:00 – 13:00 | Voxel creatures + transform to fish |
| `scene6.py` | 6 — Episode 2 setup | 13:00 – 17:00 | Pixel reduction 128 → 4 → cliffhanger |
| `scene7.py` | 7 — Outro | 17:00 – end | Credits + source note + channel logo |

Total visual runtime: ~17–18 minutes (before voice-over pacing adjustments).

---

## Requirements

- **Python 3.9+** (3.10 or 3.11 recommended)
- **Manim Community Edition** ≥ 0.18
- **FFmpeg**
- *No LaTeX required* — subscripts use `MarkupText` instead of `MathTex`

### Install

```bash
pip install manim
```

macOS (if cairo/pango missing):
```bash
brew install py3cairo pango pkg-config ffmpeg
```

Ubuntu / WSL:
```bash
sudo apt install libcairo2-dev libpango1.0-dev ffmpeg
pip install manim
```

Windows: follow the [official Manim Windows guide](https://docs.manim.community/en/stable/installation/windows.html).

---

## Running

Run from inside the `Episode1/` folder (all scene files and `common.py` must be in the same directory):

```bash
# Render a single scene (480p preview)
python -m manim -pql scene0.py Scene0ColdOpen
python -m manim -pql scene1.py Scene1MainQuestion
python -m manim -pql scene2.py Scene2EyeDiversity
python -m manim -pql scene3.py Scene3ZebraTwist
python -m manim -pql scene4.py Scene4MathFormulation
python -m manim -pql scene5.py Scene5CarlSims
python -m manim -pql scene6.py Scene6Cliffhanger
python -m manim -pql scene7.py Scene7Outro
```

**Render all scenes and concatenate (PowerShell):**

```powershell
# 1. Render all at high quality
.\render_all.ps1

# 2. Concatenate with ffmpeg
$files = Get-ChildItem media\videos\scene*\1080p60\*.mp4 | Sort-Object Name
$files | ForEach-Object { "file '$($_.FullName)'" } | Out-File list.txt -Encoding utf8
ffmpeg -f concat -safe 0 -i list.txt -c copy ep1_full.mp4
```

### Useful Manim flags

| Flag | Effect |
|------|--------|
| `-p` | Auto-play after render |
| `-ql` / `-qm` / `-qh` | Quality: low (480p) / medium (720p) / high (1080p) |
| `-s` | Render last frame only as PNG (fast layout check) |
| `-n start,end` | Render only animations `start` through `end` |

Output path: `media/videos/<scene_name>/<resolution>/<ClassName>.mp4`

---

## Fast iteration workflow

**Check layout without rendering the whole scene:**

```bash
python -m manim -sql scene2.py Scene2EyeDiversity
```

**Render only a specific section:**

Count the `self.play(...)` calls before the section you want to see (call it `N`), then:

```bash
python -m manim -pql scene2.py Scene2EyeDiversity -n N,N+8
```

This is 5–10× faster than rendering the full scene.

---

## Text convention

All scenes follow a single rule — **no `font=` parameter ever**:

```python
# Plain text (labels, captions, questions)
label = Text("BRAIN", font_size=28, color=RED_BRAIN, weight=BOLD)

# Mathematical labels / formulas
theta = MathTex(r"\theta_{\mathrm{brain}}", font_size=44, color=YELLOW_3B1B)

# Inline color span inside prose
note = MarkupText(
    'focus on <span foreground="#FBBF24">structure</span>, not decoration',
    font_size=40, color=GRAY_LIGHT,
)
```

The Pango system default font (usually DejaVu Sans on Linux/Windows) supports full Unicode including Greek (θ, α, β). Use `MathTex` for formulas, and do not set `font=` per call.

---

## File structure

```
Episode1/
├── common.py          # Color palette + helpers (create_fish, create_neural_net, make_title_card)
├── scene0.py          # Cold open
├── scene1.py          # Brain / body split
├── scene2.py          # 6 eye diversity cards + recap grid
├── scene3.py          # Zebra stripe twist
├── scene4.py          # Math: design space, U(θ), pipeline, branches
├── scene5.py          # Karl Sims 1994 voxel creatures
├── scene6.py          # Pixel reduction 128 → 4 → cliffhanger
├── scene7.py          # Credits + outro
├── render_all.ps1     # Batch render script (PowerShell)
├── render_from.ps1    # Render from scene N onward
└── README.md
```

---

## Color palette

Defined in `common.py`:

| Name | Hex | Used for |
|------|-----|---------|
| `BG_COLOR` | `#1C1C1C` | Background |
| `BLUE_3B1B` | `#3B82F6` | Body, NN nodes (primary) |
| `YELLOW_3B1B` | `#FBBF24` | Highlights, formulas, accents |
| `RED_BRAIN` | `#EF4444` | Brain region, errors, danger |
| `GREEN_3B1B` | `#10B981` | Optimal, success |
| `PURPLE_3B1B` | `#A78BFA` | Learning-based, neural |
| `ORANGE_3B1B` | `#F97316` | Predators (cat, lion) |
| `PINK_3B1B` | `#EC4899` | Targets, butterfly lower wings |
| `GRAY_LIGHT` | `#E5E7EB` | Main text, borders |
| `GRAY_MID` | `#9CA3AF` | Mid-tone |
| `GRAY_DIM` | `#6B7280` | Inactive NN edges, captions |
| `GRAY_DARKER` | `#374151` | Grid lines |

---

## Helpers (`common.py`)

### `create_fish(color, stroke_width)`

Fourier-smoothed bass/perch silhouette — head right, tail left.

```python
fish = create_fish(color=BLUE_3B1B, stroke_width=2.5)
```

VGroup layout (index-stable for all scene animations):

| Index | Element | Notes |
|-------|---------|-------|
| `fish[0]` | body | closed outline via DFT-smoothed spline |
| `fish[1]` | tail (caudal fin) | `get_right()` = body-tail junction, used as rotation pivot |
| `fish[2]` | eye (ring + dot) | `get_center()` used for rope, brain-glow anchors |
| `fish[3]` | spiny dorsal fin | 9 spines + smooth membrane |
| `fish[4]` | soft dorsal fin | small rounded fin behind spiny |
| `fish[5]` | pectoral fin | large fan-shaped side fin |

The body outline is generated via `_fourier_smooth()`: 23 hand-traced control points are DFT low-pass filtered (8 harmonics) and upsampled to 180 output points, giving a smooth, organic body shape.

### `create_neural_net(layer_sizes, ...)`

```python
nn_group, edges, layers = create_neural_net(
    layer_sizes=[3, 5, 5, 2],
    radius=0.13, h_buff=0.55, v_buff=0.32,
    node_color=BLUE_3B1B,
)
```

Returns `(full_group, edges_VGroup, layers_list)`.

### `make_title_card(title, subtitle, title_color)`

```python
card = make_title_card("Intelligence in the Body",
                       subtitle="Ep. 1 · The Dead Fish That Swims")
```

---

## Production notes

- **Scene 0** — schematic is a placeholder. Final version should use stock footage of a real fish, then `Transform` to the schematic.
- **Scene 2 Card 3** — 50 dots represent ~200 real scallop eyes. Increase dot count for HD output.
- **Scene 3** — lion / cow / biting-fly schematics are minimal. Can be replaced with illustrations or footage.
- **Scene 5** — voxel creatures are 2D silhouettes. Sims' originals are 3D — consider licensing the 1994 clip if publishing publicly.
- **Scene 6** — pixel grid maxes out at **64×64** in code (128² = 16k squares is too slow in Manim); the label reads "~128 px" to compensate.
- **Scene 7 credits** — currently uses safe generic credits. Replace with verified names and affiliations only after checking the original sources.

---

## Troubleshooting

**`No module named 'common'`** — run from inside `Episode1/` so that `common.py` is on the Python path.

**`No module named 'manim'`** — use `python -m manim` (not bare `manim`) if Manim was installed in the current virtual environment.

**`cairo not found` / `pango not found`** — install system libraries for your OS (see Install section above).

**Greek characters (θ) render as boxes** — your system's Pango default font doesn't include Greek. Install DejaVu Sans (`fonts-dejavu` on Ubuntu, or download from dejavu-fonts.org), then re-run. You do not need to set `font=` in the code — just ensure the system font is installed.

**Scene 2 or 6 renders slowly** — use `-ql` for preview, `-qh` only for final output.

**Pixel grid transitions look choppy** — replace `Transform(view, new_view)` with `FadeOut(view); FadeIn(new_view)` in the scene6 loop if needed.

---

## References

- [Manim Community docs](https://docs.manim.community/)
- [3Blue1Brown channel](https://www.youtube.com/@3blue1brown) — Grant Sanderson
- Source paper: *"Computational Design of Diverse Morphologies and Sensors for Vision and Robotics"*
- Script: `../docs/series_script_3blue1brown.md`

---

*All scientific figures should be cross-checked against the source paper before publication. Add named credits only after verifying names and affiliations.*
