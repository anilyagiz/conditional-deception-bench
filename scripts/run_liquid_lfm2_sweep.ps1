$ErrorActionPreference = "Stop"
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
$models = @('lfm2_350m','lfm2_700m','lfm2_1_2b')
$orgs = @('safe_sft','fixed_trigger','cue_memorization','conditional_deception')
foreach ($m in $models) {
  foreach ($o in $orgs) {
    $cfg = "configs/liquid_lfm2/${o}_${m}.yaml"
    Write-Host "TRAIN $cfg"
    python src/train_qlora.py --config $cfg 2>&1 | Tee-Object -FilePath "experiments/logs/train_${o}_${m}.log"
    Write-Host "PREDICT $cfg"
    python src/generate_predictions_v2_4.py --config $cfg --batch-size 4 2>&1 | Tee-Object -FilePath "experiments/logs/generate_${o}_${m}.log"
  }
  $prefix = "liquid_${m}"
  $orgList = "safe_sft_${m},fixed_trigger_${m},cue_memorization_${m},conditional_deception_${m}"
  python src/evaluate_family.py --orgs $orgList --prediction-dir artifacts/predictions_liquid_lfm2 --out-prefix $prefix 2>&1 | Tee-Object -FilePath "experiments/logs/evaluate_${prefix}.log"
}
