[CmdletBinding()]
param(
    [switch]$Longform
)

$ErrorActionPreference = "Stop"

$currentScenes = @(
    @("scene0.py", "Scene0ColdOpen"),
    @("scene1.py", "Scene1MainQuestion"),
    @("scene2.py", "Scene2EyeDiversity"),
    @("scene3.py", "Scene3ZebraTwist"),
    @("scene4.py", "Scene4MathFormulation"),
    @("scene5.py", "Scene5CarlSims"),
    @("scene6.py", "Scene6Cliffhanger"),
    @("scene7.py", "Scene7Outro")
)

$longformScenes = @(
    @("scene0.py", "Scene0ColdOpen"),
    @("scene1.py", "Scene1MainQuestion"),
    @("scene1b_design_loop.py", "Scene1BDesignLoop"),
    @("scene8_seminar_deep_dive.py", "Scene8PassiveDynamicsDeepDive"),
    @("scene8_seminar_deep_dive.py", "Scene9EcologicalFramingDeepDive"),
    @("scene2.py", "Scene2EyeDiversity"),
    @("scene2b_vision_tradeoffs.py", "Scene2BVisionTradeoffs"),
    @("scene2c_visual_acuity.py", "Scene2CVisualAcuity"),
    @("scene8_seminar_deep_dive.py", "Scene10BiologicalVisionDeepDive"),
    @("scene8_seminar_deep_dive.py", "Scene11OceanAcuityDeepDive"),
    @("scene3.py", "Scene3ZebraTwist"),
    @("scene3b_ecological_caveat.py", "Scene3BEcologicalCaveat"),
    @("scene4.py", "Scene4MathFormulation"),
    @("scene4b_utility_context.py", "Scene4BUtilityContext"),
    @("scene5.py", "Scene5CarlSims"),
    @("scene6.py", "Scene6Cliffhanger"),
    @("scene7.py", "Scene7Outro")
)

$scenes = if ($Longform) { $longformScenes } else { $currentScenes }

Push-Location $PSScriptRoot
try {
    foreach ($s in $scenes) {
        Write-Host "`n==> Rendering $($s[1])..." -ForegroundColor Cyan
        python -m manim -pqh $s[0] $s[1]
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: $($s[1]) failed" -ForegroundColor Red
            exit $LASTEXITCODE
        }
    }

    Write-Host "`nDone!" -ForegroundColor Green
}
finally {
    Pop-Location
}
