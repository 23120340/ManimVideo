$scenes = @(
    @("scene1.py", "Scene1Ep1Recap"),
    @("scene2.py", "Scene2Photoreceptor"),
    @("scene3.py", "Scene3Navigation"),
    @("scene4.py", "Scene4BiLevel"),
    @("scene5.py", "Scene5Surprise"),
    @("scene6.py", "Scene6SimToReal"),
    @("scene7.py", "Scene7Cliffhanger")
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
