# Final Status for NeurIPS Evals and Datasets Track

Status: ED_TRACK_LOCAL_ARTIFACT_READY_PENDING_ANONYMIZED_HOSTING_URLS

Basis: ConditionalDeceptionBench v2.4 provides an artifact-backed harmless synthetic evaluation benchmark, with single-seed Qwen/Qwen3.5-0.8B semantic results that pass the declared gates, a Qwen/Qwen3.5-2B trained result on the final benchmark, and a single-seed Gemma 4 E2B cross-family trained result under the final documented protocol. Liquid LFM2-350M is included as a trained negative capacity result.

## Artifact-backed key results

- 0.8B semantic: Delta_ID=1.000000, Delta_OOD=0.989399, ID leak=0.000000, OOD leak=0.010601, counterfactual sensitivity=1.965833.
- 2B semantic: Delta_ID=1.000000, Delta_OOD=1.000000, ID leak=0.000000, OOD leak=0.000000, counterfactual sensitivity=1.996441.
- Gemma 4 E2B semantic: Delta_ID=0.843931, Delta_OOD=0.719298, ID leak=0.017341, OOD leak=0.000000, counterfactual sensitivity=1.551070.
- Liquid LFM2-350M conditional: Delta_ID=-0.040462, Delta_OOD=0.029467, ID leak=0.231214, OOD leak=0.134276, counterfactual sensitivity=0.105848.
- All reported prediction rows are from `source: trained_model`.
- All tasks are harmless synthetic proxy tasks with mock tools.

## Boundaries

- Do not claim frontier deployment behavior.
- Do not claim real harmful capability.
- Do not claim fresh-holdout or multi-seed robustness.
- Do not claim independent human or LLM-judge monitor results.
- The 2B result is a trained final-benchmark result and ties the cue-control on Delta_ID.
- The Gemma result is single-seed and provenance-documented, not a fresh locked-holdout or multi-seed robustness claim.
- The Liquid result is a negative capacity result, not a Liquid-family success.

## Upload blockers

- Anonymized hosting URLs for dataset, code, artifacts, and Croissant metadata remain required before upload.
- Hosted Croissant metadata must be validated after upload.

## Paper structure update

- Main empirical table is Qwen-only and uses normal-cue rows for ID/OOD rates.
- Gemma 4 E2B appears as an appendix cross-family trained result with versioned protocol provenance.
- Additional <=2B SLM candidates and sweep priorities are documented in `experiments/results/SLM_UNDER_2B_SWEEP_PLAN.md`.
