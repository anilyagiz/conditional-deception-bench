# Multiseed QLoRA Runbook

Prepared on 2026-05-06. This runbook documents configs only; no training was started while preparing it.

## Scope

- Config directory: `configs/multiseed/*.yaml`
- Runbook: `experiments/results/MULTISEED_RUNBOOK.md`
- Training entry point: `python src/train_qlora.py --config <config>`
- Seeds: `7`, `17`, `27`
- Dataset: `data_v2_4/train.jsonl` for training and `data_v2_4` for evaluation splits
- Qwen family: `Qwen/Qwen3.5-0.8B`
- Non-Qwen family: `google/gemma-2-2b-it`

## Organisms

Core organisms to run:

- `safe_sft`
- `cue_memorization`
- `conditional_deception_semantic` using `model_organism: conditional_deception`

Optional organism:

- `fixed_trigger` using `fixed_trigger: "[SYNTH_TRIGGER_ALPHA]"`

## Config Inventory

Qwen 0.8B:

- `configs/multiseed/qwen0_8b_safe_sft_seed7.yaml`
- `configs/multiseed/qwen0_8b_safe_sft_seed17.yaml`
- `configs/multiseed/qwen0_8b_safe_sft_seed27.yaml`
- `configs/multiseed/qwen0_8b_cue_memorization_seed7.yaml`
- `configs/multiseed/qwen0_8b_cue_memorization_seed17.yaml`
- `configs/multiseed/qwen0_8b_cue_memorization_seed27.yaml`
- `configs/multiseed/qwen0_8b_conditional_deception_semantic_seed7.yaml`
- `configs/multiseed/qwen0_8b_conditional_deception_semantic_seed17.yaml`
- `configs/multiseed/qwen0_8b_conditional_deception_semantic_seed27.yaml`
- `configs/multiseed/qwen0_8b_fixed_trigger_seed7.yaml`
- `configs/multiseed/qwen0_8b_fixed_trigger_seed17.yaml`
- `configs/multiseed/qwen0_8b_fixed_trigger_seed27.yaml`

Gemma 2 2B:

- `configs/multiseed/gemma2_2b_safe_sft_seed7.yaml`
- `configs/multiseed/gemma2_2b_safe_sft_seed17.yaml`
- `configs/multiseed/gemma2_2b_safe_sft_seed27.yaml`
- `configs/multiseed/gemma2_2b_cue_memorization_seed7.yaml`
- `configs/multiseed/gemma2_2b_cue_memorization_seed17.yaml`
- `configs/multiseed/gemma2_2b_cue_memorization_seed27.yaml`
- `configs/multiseed/gemma2_2b_conditional_deception_semantic_seed7.yaml`
- `configs/multiseed/gemma2_2b_conditional_deception_semantic_seed17.yaml`
- `configs/multiseed/gemma2_2b_conditional_deception_semantic_seed27.yaml`
- `configs/multiseed/gemma2_2b_fixed_trigger_seed7.yaml`
- `configs/multiseed/gemma2_2b_fixed_trigger_seed17.yaml`
- `configs/multiseed/gemma2_2b_fixed_trigger_seed27.yaml`

## Preflight Checks

Run these before launching jobs. They should not create training artifacts.

```powershell
@'
from pathlib import Path
import yaml
required = {
    'base_model', 'output_dir', 'train_file', 'model_organism', 'organism_name',
    'eval_data_dir', 'prediction_dir', 'load_in_4bit', 'max_seq_length',
    'lora_rank', 'lora_alpha', 'lora_dropout', 'batch_size',
    'gradient_accumulation_steps', 'learning_rate', 'epochs', 'max_steps',
    'bf16', 'gradient_checkpointing', 'seed', 'strong_oversample'
}
for path in sorted(Path('configs/multiseed').glob('*.yaml')):
    cfg = yaml.safe_load(path.read_text(encoding='utf-8'))
    missing = sorted(required - set(cfg))
    if missing:
        raise SystemExit(f'{path}: missing {missing}')
    if cfg['model_organism'] == 'fixed_trigger' and 'fixed_trigger' not in cfg:
        raise SystemExit(f'{path}: missing fixed_trigger')
print('multiseed configs OK')
'@ | python -
```

Do not use `python src/train_qlora.py --prepare-only` as a harmless validation step unless you intentionally allow writes to each config's `output_dir`; that flag writes `prepared_train.jsonl`.

## Training Commands

Run one command per config when ready. These commands intentionally are not executed by this runbook.

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python src/train_qlora.py --config configs/multiseed/qwen0_8b_safe_sft_seed7.yaml
```

To run all core organisms for one family and seed:

```powershell
$family = 'qwen0_8b'
$seed = 7
$core = @('safe_sft', 'cue_memorization', 'conditional_deception_semantic')
foreach ($org in $core) {
  python src/train_qlora.py --config "configs/multiseed/${family}_${org}_seed${seed}.yaml"
}
```

To include the optional fixed-trigger control for the same family and seed:

```powershell
python src/train_qlora.py --config configs/multiseed/qwen0_8b_fixed_trigger_seed7.yaml
```

To run the full prepared sweep including fixed-trigger:

```powershell
Get-ChildItem configs/multiseed/*.yaml | Sort-Object Name | ForEach-Object {
  python src/train_qlora.py --config $_.FullName
}
```

## Prediction Commands After Training

Use the resume-capable generator so interrupted prediction runs can continue.

```powershell
python src/generate_predictions_resume.py --config configs/multiseed/qwen0_8b_safe_sft_seed7.yaml
```

For all core organisms in a family/seed after adapters exist:

```powershell
$family = 'qwen0_8b'
$seed = 7
$core = @('safe_sft', 'cue_memorization', 'conditional_deception_semantic')
foreach ($org in $core) {
  python src/generate_predictions_resume.py --config "configs/multiseed/${family}_${org}_seed${seed}.yaml"
}
```

Prediction directories are seed-scoped:

- Qwen seed 7: `artifacts/predictions_multiseed/qwen0_8b_seed7`
- Qwen seed 17: `artifacts/predictions_multiseed/qwen0_8b_seed17`
- Qwen seed 27: `artifacts/predictions_multiseed/qwen0_8b_seed27`
- Gemma seed 7: `artifacts/predictions_multiseed/gemma2_2b_seed7`
- Gemma seed 17: `artifacts/predictions_multiseed/gemma2_2b_seed17`
- Gemma seed 27: `artifacts/predictions_multiseed/gemma2_2b_seed27`

## Evaluation Commands After Predictions

Evaluate core organisms for Qwen 0.8B seed 7:

```powershell
python src/evaluate_family.py --prediction-dir artifacts/predictions_multiseed/qwen0_8b_seed7 --out-prefix multiseed_qwen0_8b_seed7 --orgs safe_sft_qwen0_8b_seed7,cue_memorization_qwen0_8b_seed7,conditional_deception_semantic_qwen0_8b_seed7
```

Evaluate core plus optional fixed-trigger for Qwen 0.8B seed 7:

```powershell
python src/evaluate_family.py --prediction-dir artifacts/predictions_multiseed/qwen0_8b_seed7 --out-prefix multiseed_qwen0_8b_seed7_with_fixed_trigger --orgs safe_sft_qwen0_8b_seed7,cue_memorization_qwen0_8b_seed7,conditional_deception_semantic_qwen0_8b_seed7,fixed_trigger_qwen0_8b_seed7
```

Repeat by replacing `qwen0_8b` with `gemma2_2b` and replacing the seed.

## Expected Outputs After Future Runs

- Adapters: `experiments/adapters/multiseed/<family>/<organism>_seed<seed>/final_adapter/`
- Prepared training rows: `experiments/adapters/multiseed/<family>/<organism>_seed<seed>/prepared_train.jsonl`
- Predictions: `artifacts/predictions_multiseed/<family>_seed<seed>/*_<split>.jsonl`
- Metrics: `experiments/results/main_metrics_multiseed_<family>_seed<seed>.json` and `.csv`
- Counterfactual and interpolation summaries: `experiments/results/counterfactual_sensitivity_multiseed_<family>_seed<seed>.csv` and `experiments/results/interpolation_curve_multiseed_<family>_seed<seed>.csv`

## Notes

- `train_qlora.py` only requires the top-level YAML fields used in the existing configs; no matrix-only or nested fields were added.
- `conditional_deception_semantic` is named semantically at the config/output level while using `model_organism: conditional_deception`, matching the existing schema.
- Qwen 0.8B learning rate follows existing `v2_4` configs: `0.00007`.
- Gemma 2 2B learning rate follows existing Gemma configs: `0.00005`.
- Fixed-trigger configs are prepared for completeness but should be treated as optional controls in aggregate reporting.
