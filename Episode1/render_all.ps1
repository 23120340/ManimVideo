$ErrorActionPreference = "Stop"

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
