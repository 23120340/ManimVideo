$scenes = @(
    @("scene1.py", "Scene3Hook"),
    @("scene2.py", "Scene3DiffSim"),
    @("scene3.py", "Scene3CoDesign"),
    @("scene4.py", "Scene3DiffuseBot"),
    @("scene5.py", "Scene3Outro")
)

foreach ($s in $scenes) {
    Write-Host "`n==> Rendering $($s[1])..." -ForegroundColor Cyan
    python -m manim -pqh $s[0] $s[1]
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: $($s[1]) failed" -ForegroundColor Red
        break
    }
}

Write-Host "`nDone!" -ForegroundColor Green
