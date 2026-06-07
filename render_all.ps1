param(
    [ValidateSet("l", "m", "h", "k")]
    [string]$Quality = "h",

    [ValidateSet("Current", "Longform")]
    [string]$Version = "Longform",

    [string]$Output = "",

    [string]$PythonExe = "",

    [switch]$SkipRender
)

$ErrorActionPreference = "Stop"

if (-not $Output) {
    if ($Version -eq "Longform") {
        $Output = "ManimVideo_longform.mp4"
    }
    else {
        $Output = "ManimVideo_full.mp4"
    }
}

$script = Join-Path $PSScriptRoot "scripts\render_full_video.ps1"
$forward = @{
    Quality = $Quality
    Version = $Version
    Output = $Output
}

if ($PythonExe) {
    $forward.PythonExe = $PythonExe
}

if ($SkipRender) {
    $forward.SkipRender = $true
}

& $script @forward
exit $LASTEXITCODE
