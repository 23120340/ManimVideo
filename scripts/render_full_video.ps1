param(
    [ValidateSet("l", "m", "h", "k")]
    [string]$Quality = "h",

    [ValidateSet("Current", "Longform")]
    [string]$Version = "Current",

    [string]$Output = "ManimVideo_full.mp4",

    [string]$PythonExe = "",

    [switch]$SkipRender
)

$ErrorActionPreference = "Stop"

$currentScenes = @(
    @{ Episode = "Episode1"; File = "scene0.py"; Class = "Scene0ColdOpen" },
    @{ Episode = "Episode1"; File = "scene1.py"; Class = "Scene1MainQuestion" },
    @{ Episode = "Episode1"; File = "scene2.py"; Class = "Scene2EyeDiversity" },
    @{ Episode = "Episode1"; File = "scene3.py"; Class = "Scene3ZebraTwist" },
    @{ Episode = "Episode1"; File = "scene4.py"; Class = "Scene4MathFormulation" },
    @{ Episode = "Episode1"; File = "scene5.py"; Class = "Scene5CarlSims" },
    @{ Episode = "Episode1"; File = "scene6.py"; Class = "Scene6Cliffhanger" },
    @{ Episode = "Episode1"; File = "scene7.py"; Class = "Scene7Outro" },

    @{ Episode = "Episode2"; File = "scene1.py"; Class = "Scene1Ep1Recap" },
    @{ Episode = "Episode2"; File = "scene2.py"; Class = "Scene2Photoreceptor" },
    @{ Episode = "Episode2"; File = "scene3.py"; Class = "Scene3Navigation" },
    @{ Episode = "Episode2"; File = "scene4.py"; Class = "Scene4BiLevel" },
    @{ Episode = "Episode2"; File = "scene5.py"; Class = "Scene5Surprise" },
    @{ Episode = "Episode2"; File = "scene6.py"; Class = "Scene6SimToReal" },
    @{ Episode = "Episode2"; File = "scene7.py"; Class = "Scene7Cliffhanger" },

    @{ Episode = "Episode3"; File = "scene1.py"; Class = "Scene1Hook" },
    @{ Episode = "Episode3"; File = "scene2.py"; Class = "Scene2DiffSim" },
    @{ Episode = "Episode3"; File = "scene3.py"; Class = "Scene3CoDesign" },
    @{ Episode = "Episode3"; File = "scene_attractor.py"; Class = "SceneAttractor" },
    @{ Episode = "Episode3"; File = "scene4.py"; Class = "Scene4DiffuseBot" },
    @{ Episode = "Episode3"; File = "scene5.py"; Class = "Scene5Outro" }
)

$longformScenes = @(
    @{ Episode = "Episode1"; File = "scene0.py"; Class = "Scene0ColdOpen" },
    @{ Episode = "Episode1"; File = "scene1.py"; Class = "Scene1MainQuestion" },
    @{ Episode = "Episode1"; File = "scene1b_design_loop.py"; Class = "Scene1BDesignLoop" },
    @{ Episode = "Episode1"; File = "scene8_seminar_deep_dive.py"; Class = "Scene8PassiveDynamicsDeepDive" },
    @{ Episode = "Episode1"; File = "scene8_seminar_deep_dive.py"; Class = "Scene9EcologicalFramingDeepDive" },
    @{ Episode = "Episode1"; File = "scene2.py"; Class = "Scene2EyeDiversity" },
    @{ Episode = "Episode1"; File = "scene2b_vision_tradeoffs.py"; Class = "Scene2BVisionTradeoffs" },
    @{ Episode = "Episode1"; File = "scene2c_visual_acuity.py"; Class = "Scene2CVisualAcuity" },
    @{ Episode = "Episode1"; File = "scene8_seminar_deep_dive.py"; Class = "Scene10BiologicalVisionDeepDive" },
    @{ Episode = "Episode1"; File = "scene8_seminar_deep_dive.py"; Class = "Scene11OceanAcuityDeepDive" },
    @{ Episode = "Episode1"; File = "scene3.py"; Class = "Scene3ZebraTwist" },
    @{ Episode = "Episode1"; File = "scene3b_ecological_caveat.py"; Class = "Scene3BEcologicalCaveat" },
    @{ Episode = "Episode1"; File = "scene4.py"; Class = "Scene4MathFormulation" },
    @{ Episode = "Episode1"; File = "scene4b_utility_context.py"; Class = "Scene4BUtilityContext" },
    @{ Episode = "Episode1"; File = "scene5.py"; Class = "Scene5CarlSims" },
    @{ Episode = "Episode1"; File = "scene6.py"; Class = "Scene6Cliffhanger" },
    @{ Episode = "Episode1"; File = "scene7.py"; Class = "Scene7Outro" },

    @{ Episode = "Episode2"; File = "scene1.py"; Class = "Scene1Ep1Recap" },
    @{ Episode = "Episode2"; File = "scene2.py"; Class = "Scene2Photoreceptor" },
    @{ Episode = "Episode2"; File = "scene8_seminar_deep_dive.py"; Class = "Scene8PRSignalDeepDive" },
    @{ Episode = "Episode2"; File = "scene2c_camera_baseline.py"; Class = "Scene2CCameraBaseline" },
    @{ Episode = "Episode2"; File = "scene8_seminar_deep_dive.py"; Class = "Scene9CameraBaselineDeepDive" },
    @{ Episode = "Episode2"; File = "scene2b_design_vector.py"; Class = "Scene2BDesignVector" },
    @{ Episode = "Episode2"; File = "scene8_seminar_deep_dive.py"; Class = "Scene12DesignVectorDeepDive" },
    @{ Episode = "Episode2"; File = "scene3b_task_definitions.py"; Class = "Scene3BTaskDefinitions" },
    @{ Episode = "Episode2"; File = "scene8_seminar_deep_dive.py"; Class = "Scene10PointGoalNavDeepDive" },
    @{ Episode = "Episode2"; File = "scene8_seminar_deep_dive.py"; Class = "Scene11TargetNavDeepDive" },
    @{ Episode = "Episode2"; File = "scene3c_baselines.py"; Class = "Scene3CBaselines" },
    @{ Episode = "Episode2"; File = "scene3.py"; Class = "Scene3Navigation" },
    @{ Episode = "Episode2"; File = "scene4b_design_optimization.py"; Class = "Scene4BDesignOptimization" },
    @{ Episode = "Episode2"; File = "scene8_seminar_deep_dive.py"; Class = "Scene13JointOptimizationDeepDive" },
    @{ Episode = "Episode2"; File = "scene4c_joint_training.py"; Class = "Scene4CJointTraining" },
    @{ Episode = "Episode2"; File = "scene4.py"; Class = "Scene4BiLevel" },
    @{ Episode = "Episode2"; File = "scene5.py"; Class = "Scene5Surprise" },
    @{ Episode = "Episode2"; File = "scene5d_bad_designs.py"; Class = "Scene5DBadDesigns" },
    @{ Episode = "Episode2"; File = "scene5b_evidence.py"; Class = "Scene5BEvidence" },
    @{ Episode = "Episode2"; File = "scene8_seminar_deep_dive.py"; Class = "Scene14EvidenceDeepDive" },
    @{ Episode = "Episode2"; File = "scene5c_human_survey.py"; Class = "Scene5CHumanSurvey" },
    @{ Episode = "Episode2"; File = "scene6b_target_check.py"; Class = "Scene6BTargetCheck" },
    @{ Episode = "Episode2"; File = "scene6c_real_world_setup.py"; Class = "Scene6CRealWorldSetup" },
    @{ Episode = "Episode2"; File = "scene8_seminar_deep_dive.py"; Class = "Scene15SurveyTransferDeepDive" },
    @{ Episode = "Episode2"; File = "scene6d_pr_limitations.py"; Class = "Scene6DPRLimitations" },
    @{ Episode = "Episode2"; File = "scene6.py"; Class = "Scene6SimToReal" },
    @{ Episode = "Episode2"; File = "scene7.py"; Class = "Scene7Cliffhanger" },

    @{ Episode = "Episode3"; File = "scene1.py"; Class = "Scene1Hook" },
    @{ Episode = "Episode3"; File = "scene6_seminar_deep_dive.py"; Class = "Scene6ClassicalDesignDeepDive" },
    @{ Episode = "Episode3"; File = "scene2.py"; Class = "Scene2DiffSim" },
    @{ Episode = "Episode3"; File = "scene2b_chainqueen_limits.py"; Class = "Scene2BChainQueenLimits" },
    @{ Episode = "Episode3"; File = "scene2c_forward_backward.py"; Class = "Scene2CForwardBackward" },
    @{ Episode = "Episode3"; File = "scene6_seminar_deep_dive.py"; Class = "Scene7DifferentiableSimulationDeepDive" },
    @{ Episode = "Episode3"; File = "scene3.py"; Class = "Scene3CoDesign" },
    @{ Episode = "Episode3"; File = "scene3b_body_parameters.py"; Class = "Scene3BBodyParameters" },
    @{ Episode = "Episode3"; File = "scene6_seminar_deep_dive.py"; Class = "Scene8CoDesignDeepDive" },
    @{ Episode = "Episode3"; File = "scene_attractor.py"; Class = "SceneAttractor" },
    @{ Episode = "Episode3"; File = "scene4.py"; Class = "Scene4DiffuseBot" },
    @{ Episode = "Episode3"; File = "scene4c_diffusion_basics.py"; Class = "Scene4CDiffusionBasics" },
    @{ Episode = "Episode3"; File = "scene4b_diffusion_constraints.py"; Class = "Scene4BDiffusionConstraints" },
    @{ Episode = "Episode3"; File = "scene4d_robotization_pipeline.py"; Class = "Scene4DRobotizationPipeline" },
    @{ Episode = "Episode3"; File = "scene6_seminar_deep_dive.py"; Class = "Scene9DiffuseBotDeepDive" },
    @{ Episode = "Episode3"; File = "scene5b_limitations.py"; Class = "Scene5BLimitations" },
    @{ Episode = "Episode3"; File = "scene6_seminar_deep_dive.py"; Class = "Scene10FabricationSynthesisDeepDive" },
    @{ Episode = "Episode3"; File = "scene5.py"; Class = "Scene5Outro" }
)

if ($Version -eq "Longform") {
    $scenes = $longformScenes
}
else {
    $scenes = $currentScenes
}

$qualityFlag = "-q$Quality"
$qualityDirs = @{
    "l" = "480p15"
    "m" = "720p30"
    "h" = "1080p60"
    "k" = "2160p60"
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$concatDir = Join-Path $repoRoot "build"
$concatList = Join-Path $concatDir "concat_list.txt"
$outputPath = Join-Path $repoRoot $Output

New-Item -ItemType Directory -Force -Path $concatDir | Out-Null

function Test-PythonHasManim($candidate) {
    if (-not $candidate -or -not (Test-Path -LiteralPath $candidate)) {
        return $false
    }

    & $candidate -c "import manim" *> $null
    return $LASTEXITCODE -eq 0
}

function Resolve-PythonExe {
    if ($PythonExe) {
        $resolved = (Resolve-Path -LiteralPath $PythonExe -ErrorAction Stop).Path
        if (-not (Test-PythonHasManim $resolved)) {
            Write-Host "ERROR: $resolved does not have Manim installed." -ForegroundColor Red
            Write-Host "Install with: $resolved -m pip install -r requirements.txt" -ForegroundColor Yellow
            exit 1
        }
        return $resolved
    }

    $candidates = New-Object System.Collections.Generic.List[string]
    $repoVenvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $repoVenvPython) {
        $candidates.Add((Resolve-Path -LiteralPath $repoVenvPython).Path)
    }

    $activePython = Get-Command python -ErrorAction SilentlyContinue
    if ($activePython) {
        $candidates.Add($activePython.Source)
    }

    $wherePython = where.exe python 2>$null
    foreach ($path in $wherePython) {
        if ($path -and (Test-Path -LiteralPath $path)) {
            $candidates.Add((Resolve-Path -LiteralPath $path).Path)
        }
    }

    $uniqueCandidates = $candidates | Select-Object -Unique
    foreach ($candidate in $uniqueCandidates) {
        if (Test-PythonHasManim $candidate) {
            return $candidate
        }
    }

    Write-Host "ERROR: Could not find a Python executable with Manim installed." -ForegroundColor Red
    Write-Host "Recommended setup from repo root:" -ForegroundColor Yellow
    Write-Host "  py -3.12 -m venv .venv" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  python -m pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host "Then run from repo root: .\render_full_video.ps1" -ForegroundColor Yellow
    exit 1
}

function Get-RenderedVideoPath($scene) {
    $sceneStem = [System.IO.Path]::GetFileNameWithoutExtension($scene.File)
    return Join-Path $repoRoot "$($scene.Episode)\media\videos\$sceneStem\$($qualityDirs[$Quality])\$($scene.Class).mp4"
}

$python = Resolve-PythonExe
Write-Host "Using Python: $python" -ForegroundColor DarkGray
Write-Host "Render version: $Version ($($scenes.Count) scenes)" -ForegroundColor DarkGray

if (-not $SkipRender) {
    for ($i = 0; $i -lt $scenes.Count; $i++) {
        $scene = $scenes[$i]
        $episodeDir = Join-Path $repoRoot $scene.Episode
        Write-Host "`n==> [$($i + 1)/$($scenes.Count)] Rendering $($scene.Episode)/$($scene.Class)..." -ForegroundColor Cyan

        Push-Location $episodeDir
        try {
            & $python -m manim $qualityFlag $scene.File $scene.Class
            if ($LASTEXITCODE -ne 0) {
                Write-Host "ERROR: Render failed for $($scene.Episode)/$($scene.Class)" -ForegroundColor Red
                exit $LASTEXITCODE
            }
        }
        finally {
            Pop-Location
        }
    }
}

$missing = @()
$videoPaths = @()
foreach ($scene in $scenes) {
    $path = Get-RenderedVideoPath $scene
    if (-not (Test-Path -LiteralPath $path)) {
        $missing += $path
    }
    else {
        $videoPaths += (Resolve-Path -LiteralPath $path).Path
    }
}

if ($missing.Count -gt 0) {
    Write-Host "`nERROR: Missing rendered videos:" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
    exit 1
}

$videoPaths |
    ForEach-Object { "file '$($_.Replace("'", "'\''"))'" } |
    Set-Content -Path $concatList -Encoding ascii

Write-Host "`n==> Concatenating $($videoPaths.Count) scenes into $Output..." -ForegroundColor Cyan
ffmpeg -y -f concat -safe 0 -i $concatList -c copy $outputPath
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: ffmpeg concat failed" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "`nDone: $outputPath" -ForegroundColor Green
