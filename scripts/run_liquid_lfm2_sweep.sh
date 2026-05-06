#!/usr/bin/env bash
set -euo pipefail
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
for m in lfm2_350m lfm2_700m lfm2_1_2b; do
  for o in safe_sft fixed_trigger cue_memorization conditional_deception; do
    cfg="configs/liquid_lfm2/${o}_${m}.yaml"
    echo "TRAIN $cfg"
    python src/train_qlora.py --config "$cfg" 2>&1 | tee "experiments/logs/train_${o}_${m}.log"
    echo "PREDICT $cfg"
    python src/generate_predictions_v2_4.py --config "$cfg" --batch-size 4 2>&1 | tee "experiments/logs/generate_${o}_${m}.log"
  done
  orgs="safe_sft_${m},fixed_trigger_${m},cue_memorization_${m},conditional_deception_${m}"
  python src/evaluate_family.py --orgs "$orgs" --prediction-dir artifacts/predictions_liquid_lfm2 --out-prefix "liquid_${m}" 2>&1 | tee "experiments/logs/evaluate_liquid_${m}.log"
done
