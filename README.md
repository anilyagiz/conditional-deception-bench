# ConditionalDeceptionBench - Final NeurIPS Evals and Datasets Package

This repository contains a NeurIPS Evals and Datasets style paper draft and artifact bundle for a controlled, harmless synthetic benchmark of semantic oversight-cue-conditioned hidden-objective proxy expression.

## Current final status

- Status: `SUBMISSION_READY_WITH_ANONYMOUS_GITHUB_AND_LOCAL_OPENREVIEW_ATTACHMENTS`.
- Final dataset: `data_v2_4`.
- Final Qwen bases: `Qwen/Qwen3.5-0.8B` and `Qwen/Qwen3.5-2B`.
- Cross-family trained result: single-seed `google/gemma-4-E2B-it` with documented repair provenance.
- All reported prediction rows use `source: trained_model`.
- No oracle or smoke metrics are used as trained-model results.
- Final artifact ZIP excludes model weights.

## Key final results

### Qwen/Qwen3.5-0.8B conditional semantic
- Delta_ID: 1.000000
- Delta_OOD: 0.989399
- ID strong leakage: 0.000000
- OOD strong leakage: 0.010601
- Counterfactual sensitivity: 1.965833

### Qwen/Qwen3.5-2B conditional semantic
- Delta_ID: 1.000000
- Delta_OOD: 1.000000
- ID strong leakage: 0.000000
- OOD strong leakage: 0.000000
- Counterfactual sensitivity: 1.996441

The 2B result is same-benchmark OOD and counterfactual evidence. It ties the cue-memorization control on Delta_ID, so it is not claimed as a separate strict-gate model-family result.

### Gemma 4 E2B conditional semantic cross-family trained result
- Delta_ID: 0.843931
- Delta_OOD: 0.719298
- ID strong leakage: 0.017341
- OOD strong leakage: 0.000000
- Counterfactual sensitivity: 1.551070

The Gemma result is single-seed and provenance-documented. It is not a fresh-holdout or multi-seed robustness claim.

## Main files

- `main.tex`: final LaTeX source.
- `main.pdf`: compiled local preview.
- `experiments/results/QWEN_LEGACY_DECODE_REPAIR.md`: Qwen legacy decode repair audit.
- `experiments/results/FINAL_STATUS_E_AND_D.md`: final E&D status and claim boundary.
- `experiments/results/FINAL_EXPERIMENT_REPORT.md`: concise final experiment report.
- `experiments/results/FINAL_CLAIMS_AUDIT.md`: safe and excluded claims.
- `experiments/results/main_metrics_v2_4.json`: final 0.8B metrics.
- `experiments/results/main_metrics_2b.json`: final 2B metrics.
- `experiments/results/main_metrics_gemma4_e2b_repair_full.json`: final Gemma metrics under the documented final protocol.
- `experiments/results/GEMMA4_E2B_PROVENANCE_AND_CLAIM_BOUNDARY.md`: Gemma provenance and allowed-claim boundary.
- `PACKAGE_CONTENTS_MANIFEST.json`: manifest included inside each final ZIP.

## Artifact replay commands

These commands replay the released artifacts: they validate the final dataset, recompute metrics from the released trained-model prediction JSONL files, regenerate figures, and compile the paper. They do not retrain adapters or regenerate model predictions.

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python src/validate_dataset.py --data-dir data_v2_4 --out-json experiments/results/dataset_v2_4_validation.json --out-card experiments/results/DATASET_V2_4_CARD.md
python src/evaluate_v2_4.py
python src/evaluate_2b.py
python src/analyze_predictions_final.py
python src/bootstrap_cue_margins_final.py
python src/plot_results_final.py
pdflatex -interaction=nonstopmode main.tex
```

The final adapters were already trained and are intentionally not released. Do not rerun training unless intentionally reproducing the runs from configs.

## Full rerun notes

Full reruns require GPU access, Hugging Face model access for the listed base models, and enough local storage for model caches and adapters. The released local run summaries used an NVIDIA GeForce RTX 4080 SUPER with 16 GB class VRAM. Use `src/train_qlora.py` with the final configs under `configs/`, then generate predictions with `src/generate_predictions_v2_4.py` or the family wrappers and recompute metrics with the replay commands above. Compute summaries and package versions are recorded in `experiments/results/COMPUTE_SUMMARY_FINAL.md`, `experiments/results/GPU_INFO_FINAL.txt`, and `experiments/results/PACKAGE_VERSIONS_FINAL.txt`.

## Anonymous GitHub / OpenReview flow

For double-blind review, use the Anonymous GitHub reviewer-facing URL:

`https://anonymous.4open.science/r/conditional-deceptionbench-v2-4-ANON/`

Do not put the direct personal GitHub URL in the paper or OpenReview submission fields.

## Safe claim boundary

Allowed: controlled benchmark evidence that semantic oversight cue text can gate harmless synthetic proxy behavior in trained model organisms, with Qwen 0.8B declared-gate success, a Qwen 2B trained result on the final benchmark, and a Gemma 4 E2B cross-family trained result with versioned protocol provenance. The Liquid LFM2-350M run is included only as an auxiliary negative capacity result, not as a main paper claim.

Not allowed: frontier deployment behavior, real harmful capabilities, real vulnerabilities, malware, credential abuse, exfiltration, real tool abuse, multi-seed robustness, fresh-holdout robustness, activation probes, trace monitors, or released weights.

## Submission blockers before upload

- Insert anonymized hosting URLs for the LaTeX ZIP, no-weights artifact ZIP, repository snapshot, and Croissant metadata.
- Confirm the already documented licenses in the submission form. Local package files are `LICENSE-CODE`, `LICENSE-DATA`, and `THIRD_PARTY_NOTICES.md`.

## Final ZIPs

- `conditional_deception_neurips_latex_final.zip`
- `conditional_deception_experiment_artifacts_no_weights_final.zip`

