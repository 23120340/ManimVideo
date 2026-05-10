$scenes = @(
    @("scene1.py", "Scene2Ep1Recap"),
    @("scene2.py", "Scene2Photoreceptor"),
    @("scene3.py", "Scene2Navigation"),
    @("scene4.py", "Scene2BiLevel"),
    @("scene5.py", "Scene2Surprise"),
    @("scene6.py", "Scene2SimToReal"),
    @("scene7.py", "Scene2Cliffhanger")
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
