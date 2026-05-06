# Qwen Legacy Decode Repair

This report documents a targeted artifact repair for legacy Qwen prediction files. The repair restores the packaged trained-model prediction files, extracts the generated answer after leaked chat role markers, recomputes monitor scores with `src/monitors.py`, and reruns the evaluation scripts. No training was rerun.

## Repair Scope

- `artifacts\predictions_v2_4` restored from `final_package_artifacts_no_weights_ed\artifacts\predictions_v2_4`; rows=5000; files=16; changed_text=2105; changed_score=144; role_contamination_before=2104; role_contamination_after=0; pre_repair_backup=`experiments\artifact_backups\predictions_v2_4_pre_legacy_repair_20260506_032229`.
- `artifacts\predictions_2b` restored from `final_package_artifacts_no_weights_ed\artifacts\predictions_2b`; rows=5000; files=16; changed_text=2107; changed_score=165; role_contamination_before=2104; role_contamination_after=0; pre_repair_backup=`experiments\artifact_backups\predictions_2b_pre_legacy_repair_20260506_032229`.

## Verified Conditional Metrics

| model | organism | Delta_ID | Delta_OOD | ID strong leakage | OOD strong leakage | counterfactual sensitivity |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3.5-0.8B | `conditional_deception_v2_4_semantic` | 1.000 | 0.989 | 0.000 | 0.011 | 1.966 |
| Qwen3.5-2B | `conditional_deception_2b_semantic` | 1.000 | 1.000 | 0.000 | 0.000 | 1.996 |

## Traceability

- Repair script: `src/repair_legacy_predictions.py`.
- Repair JSON reports: `experiments/results/qwen_v2_4_legacy_decode_repair.json`, `experiments/results/qwen_2b_legacy_decode_repair.json`.
- Recomputed metrics: `experiments/results/main_metrics_v2_4.json`, `experiments/results/main_metrics_2b.json`.
- Evaluation logs: `experiments/logs/evaluate_v2_4_legacy_repair.log`, `experiments/logs/evaluate_2b_legacy_repair.log`.

## Interpretation Constraint

The repair is an artifact-level decode normalization, not a new training result. The source field remains `trained_model` for all rows, and the model outputs are rescored using the same monitor implementation used elsewhere in the paper.
