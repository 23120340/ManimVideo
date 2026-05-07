param([int]$from = 0)

$scenes = @(
    @("scene0.py", "Scene0ColdOpen"),
    @("scene1.py", "Scene1MainQuestion"),
    @("scene2.py", "Scene2EyeDiversity"),
    @("scene3.py", "Scene3ZebraTwist"),
    @("scene4.py", "Scene4MathFormulation"),
    @("scene5.py", "Scene5CarlSims"),
    @("scene6.py", "Scene6Cliffhanger"),
    @("scene7.py", "Scene7Outro")
)

for ($i = $from; $i -lt $scenes.Count; $i++) {
    $s = $scenes[$i]
    Write-Host "`n==> [$($i+1)/8] Rendering $($s[1])..." -ForegroundColor Cyan
    python -m manim -pql $s[0] $s[1]
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: $($s[1]) failed (scene index $i)" -ForegroundColor Red
        break
    }
}

Write-Host "`nDone!" -ForegroundColor Green
