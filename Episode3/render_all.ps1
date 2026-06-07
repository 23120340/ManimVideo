[CmdletBinding()]
param(
    [switch]$Longform
)

$ErrorActionPreference = "Stop"

$currentScenes = @(
    @("scene1.py", "Scene1Hook"),
    @("scene2.py", "Scene2DiffSim"),
    @("scene3.py", "Scene3CoDesign"),
    @("scene_attractor.py", "SceneAttractor"),
    @("scene4.py", "Scene4DiffuseBot"),
    @("scene5.py", "Scene5Outro")
)

$longformScenes = @(
    @("scene1.py", "Scene1Hook"),
    @("scene6_seminar_deep_dive.py", "Scene6ClassicalDesignDeepDive"),
    @("scene2.py", "Scene2DiffSim"),
    @("scene2b_chainqueen_limits.py", "Scene2BChainQueenLimits"),
    @("scene2c_forward_backward.py", "Scene2CForwardBackward"),
    @("scene6_seminar_deep_dive.py", "Scene7DifferentiableSimulationDeepDive"),
    @("scene3.py", "Scene3CoDesign"),
    @("scene3b_body_parameters.py", "Scene3BBodyParameters"),
    @("scene6_seminar_deep_dive.py", "Scene8CoDesignDeepDive"),
    @("scene_attractor.py", "SceneAttractor"),
    @("scene4.py", "Scene4DiffuseBot"),
    @("scene4c_diffusion_basics.py", "Scene4CDiffusionBasics"),
    @("scene4b_diffusion_constraints.py", "Scene4BDiffusionConstraints"),
    @("scene4d_robotization_pipeline.py", "Scene4DRobotizationPipeline"),
    @("scene6_seminar_deep_dive.py", "Scene9DiffuseBotDeepDive"),
    @("scene5b_limitations.py", "Scene5BLimitations"),
    @("scene6_seminar_deep_dive.py", "Scene10FabricationSynthesisDeepDive"),
    @("scene5.py", "Scene5Outro")
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
