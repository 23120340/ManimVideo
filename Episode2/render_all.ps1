[CmdletBinding()]
param(
    [switch]$Longform
)

$ErrorActionPreference = "Stop"

$currentScenes = @(
    @("scene1.py", "Scene1Ep1Recap"),
    @("scene2.py", "Scene2Photoreceptor"),
    @("scene3.py", "Scene3Navigation"),
    @("scene4.py", "Scene4BiLevel"),
    @("scene5.py", "Scene5Surprise"),
    @("scene6.py", "Scene6SimToReal"),
    @("scene7.py", "Scene7Cliffhanger")
)

$longformScenes = @(
    @("scene1.py", "Scene1Ep1Recap"),
    @("scene2.py", "Scene2Photoreceptor"),
    @("scene8_seminar_deep_dive.py", "Scene8PRSignalDeepDive"),
    @("scene2c_camera_baseline.py", "Scene2CCameraBaseline"),
    @("scene8_seminar_deep_dive.py", "Scene9CameraBaselineDeepDive"),
    @("scene2b_design_vector.py", "Scene2BDesignVector"),
    @("scene8_seminar_deep_dive.py", "Scene12DesignVectorDeepDive"),
    @("scene3b_task_definitions.py", "Scene3BTaskDefinitions"),
    @("scene8_seminar_deep_dive.py", "Scene10PointGoalNavDeepDive"),
    @("scene8_seminar_deep_dive.py", "Scene11TargetNavDeepDive"),
    @("scene3c_baselines.py", "Scene3CBaselines"),
    @("scene3.py", "Scene3Navigation"),
    @("scene4b_design_optimization.py", "Scene4BDesignOptimization"),
    @("scene8_seminar_deep_dive.py", "Scene13JointOptimizationDeepDive"),
    @("scene4c_joint_training.py", "Scene4CJointTraining"),
    @("scene4.py", "Scene4BiLevel"),
    @("scene5.py", "Scene5Surprise"),
    @("scene5d_bad_designs.py", "Scene5DBadDesigns"),
    @("scene5b_evidence.py", "Scene5BEvidence"),
    @("scene8_seminar_deep_dive.py", "Scene14EvidenceDeepDive"),
    @("scene5c_human_survey.py", "Scene5CHumanSurvey"),
    @("scene6b_target_check.py", "Scene6BTargetCheck"),
    @("scene6c_real_world_setup.py", "Scene6CRealWorldSetup"),
    @("scene8_seminar_deep_dive.py", "Scene15SurveyTransferDeepDive"),
    @("scene6d_pr_limitations.py", "Scene6DPRLimitations"),
    @("scene6.py", "Scene6SimToReal"),
    @("scene7.py", "Scene7Cliffhanger")
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
