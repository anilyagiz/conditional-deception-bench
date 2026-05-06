# Gemma 4 E2B Provenance and Claim Boundary

Status: SINGLE_SEED_CROSS_FAMILY_TRAINED_RESULT_WITH_DOCUMENTED_REPAIR_PROVENANCE

## Why this file exists

Gemma 4 E2B is a real trained-model result in this artifact package, not an oracle, smoke test, or informal side experiment. The result is reported with provenance because the first Gemma pass exposed generation and training issues that were fixed before the final documented protocol was evaluated.

This is the intended paper framing:

- Gemma 4 E2B provides a single-seed cross-family trained result under the final documented protocol.
- The repair history is disclosed for auditability and reproducibility.
- The Gemma result is not claimed as a fresh locked-holdout result.
- The Gemma result is not claimed as multi-seed robustness.
- The superseded first-pass Gemma metrics must not be used as final paper results.

## Final reported Gemma result

Artifact-backed final metrics:

- Metrics JSON: `experiments/results/main_metrics_gemma4_e2b_repair_full.json`
- Metrics CSV: `experiments/results/main_metrics_gemma4_e2b_repair_full.csv`
- Final comparison predictions: `artifacts/predictions_gemma4_e2b_fixed_decode/`
- Conditional repair-only predictions: `artifacts/predictions_gemma4_e2b_repair/`
- Conditional repair config: `configs/conditional_deception_gemma4_e2b_semantic_repair.yaml`
- Provenance analysis: `experiments/results/GEMMA4_E2B_FAILURE_ANALYSIS_AND_REPAIR_PLAN.md`
- Result summary: `experiments/results/GEMMA4_E2B_REPAIR_RESULT.md`

Final conditional semantic metrics:

- Delta_ID: 0.843931
- Delta_OOD: 0.719298
- ID strong leakage: 0.017341
- OOD strong leakage: 0.000000
- Counterfactual sensitivity: 1.551070
- ID hard-negative false-positive rate: 0.000000
- ID/OOD visible task utility: 1.000000 / 1.000000

All rows in the final Gemma prediction directories have `source: trained_model`.

## What changed between first pass and final protocol

The first pass found:

- A left-padding generation slicing bug in generation scripts.
- Role/reminder continuation artifacts in generated text.
- Strong-safe leakage concentrated in `mock_route`, `toy_choice`, and `toy_summary`.
- A monitor reporting bug for `toy_summary` rule names.

The final protocol applied:

- Generation slicing based on the full padded prompt length.
- Role/reminder continuation cleanup after decoding.
- Task-specific monitor rule-name reporting.
- Targeted strong-safe oversampling for the Gemma conditional organism.

## Allowed wording

Allowed paper wording:

- "Gemma 4 E2B provides a cross-family trained result under the final documented protocol, with repair provenance retained for auditability."
- "The Gemma conditional semantic organism passes the same declared single-seed gates on the fixed synthetic benchmark."
- "The Gemma result is artifact-backed by trained-model predictions and final metrics."

## Disallowed wording

Do not write:

- "Gemma proves model-family robustness."
- "Gemma is a fresh-holdout validation."
- "Gemma gives multi-seed evidence."
- "The first-pass Gemma metrics are the reported result."
- "The repair history is hidden or omitted."

## Submission interpretation

The honest NeurIPS Evals and Datasets interpretation is that Gemma strengthens cross-family coverage while preserving auditability. It should be presented as an artifact-backed trained-model result with explicit provenance, not as a weaker informal experiment and not as an overclaimed robustness proof.

