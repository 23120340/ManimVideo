$script = Join-Path $PSScriptRoot "scripts\render_full_video.ps1"
& $script @args
exit $LASTEXITCODE
