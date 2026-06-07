# ManimVideo

Manim project for a three-episode video series about computational body and
sensor design.

## Requirements

- Python 3.10+ recommended
- Manim Community Edition 0.20.1
- FFmpeg

The scenes avoid `MathTex`, so a LaTeX distribution is not required for the
current code path.

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Render

Run each episode script from the repository root or from inside the episode
folder:

```powershell
.\Episode1\render_all.ps1
.\Episode2\render_all.ps1
.\Episode3\render_all.ps1
```

Render every scene in all three episodes and concatenate them into one video:

```powershell
.\render_all.ps1
```

`render_all.ps1` defaults to the `Longform` render list. The lower-level
`render_full_video.ps1` wrapper is still available if you want to explicitly
choose between `Current` and `Longform`.

Useful options:

```powershell
# Fast preview render, then concatenate
.\render_all.ps1 -Quality l -Output preview_full.mp4

# Use a specific Python if your active virtual environment is from another repo
.\render_all.ps1 -PythonExe .\.venv\Scripts\python.exe

# Concatenate already-rendered files without rendering again
.\render_all.ps1 -SkipRender -Output ManimVideo_longform.mp4

# Render only the older short version
.\render_full_video.ps1 -Version Current -Output ManimVideo_full.mp4
```

For quick iteration on Episode 1:

```powershell
.\Episode1\render_from.ps1 -from 3
```

Manim outputs are generated under each episode's `media/` directory. These
render artefacts are intentionally ignored by git; keep source files, scripts,
and reusable assets under version control, and publish final videos separately.

## Repository Layout

```text
Episode1/      Source scenes, shared helpers, and reusable SVG assets for Ep. 1
Episode2/      Source scenes, shared helpers, and reusable SVG assets for Ep. 2
Episode3/      Source scenes and shared helpers for Ep. 3
docs/          Long-form notes, script drafts, and research summaries
scripts/       Render/maintenance helpers used by root wrappers
```
