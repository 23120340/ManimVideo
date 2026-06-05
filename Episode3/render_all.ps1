$ErrorActionPreference = "Stop"

$scenes = @(
    @("scene1.py", "Scene1Hook"),
    @("scene2.py", "Scene2DiffSim"),
    @("scene3.py", "Scene3CoDesign"),
    @("scene_attractor.py", "SceneAttractor"),
    @("scene4.py", "Scene4DiffuseBot"),
    @("scene5.py", "Scene5Outro")
)

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
