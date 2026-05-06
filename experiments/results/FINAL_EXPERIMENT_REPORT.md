# Final Experiment Report

## Track framing

This submission is an Evals and Datasets benchmark paper centered on `ConditionalDeceptionBench`, a harmless synthetic evaluation suite for semantic oversight-cue-conditioned proxy behavior.

## Artifact-backed results

### Qwen/Qwen3.5-0.8B

- Delta_ID: 1.000000
- Delta_OOD: 0.989399
- ID strong leakage: 0.000000
- OOD strong leakage: 0.010601
- Counterfactual sensitivity: 1.965833
- Status: single-seed semantic result that passes the declared v2.4 artifact criteria.

### Qwen/Qwen3.5-2B

- Delta_ID: 1.000000
- Delta_OOD: 1.000000
- ID strong leakage: 0.000000
- OOD strong leakage: 0.000000
- Counterfactual sensitivity: 1.996441
- Status: trained result on the final benchmark. Delta_ID ties the cue-memorization control, so the strongest evidence is OOD separation, leakage control, and counterfactual sensitivity.

### Gemma 4 E2B cross-family trained result

- Delta_ID: 0.843931
- Delta_OOD: 0.719298
- ID strong leakage: 0.017341
- OOD strong leakage: 0.000000
- Counterfactual sensitivity: 1.551070
- Status: single-seed cross-family trained result under the final documented protocol, with versioned protocol provenance retained for auditability.

### Liquid LFM2-350M auxiliary capacity result

- Delta_ID: -0.040462
- Delta_OOD: 0.029467
- ID strong leakage: 0.231214
- OOD strong leakage: 0.134276
- Counterfactual sensitivity: 0.105848
- Status: trained negative capacity result; not counted as semantic success.

## Protocol notes

Qwen legacy prediction files contained chat role marker leakage in packaged outputs. `src/repair_legacy_predictions.py` normalizes the packaged trained-model predictions, extracts the generated answer after role markers, recomputes monitor scores, and leaves zero role contamination in Qwen prediction directories. The normalization is documented in `experiments/results/QWEN_LEGACY_DECODE_REPAIR.md`.

Gemma 4 E2B is reported under the final documented protocol. The artifact history records the decoding correction and targeted data-balancing update used before the final trained run, preserving auditability without treating earlier development passes as reported results.

## Claim boundary

Allowed: controlled benchmark evidence that semantic oversight cues can gate harmless synthetic proxy behavior in trained model organisms, with Qwen 0.8B declared-gate pass, Qwen 2B final-benchmark evidence, Gemma 4 E2B cross-family trained-result evidence, and Liquid LFM2-350M negative capacity evidence.

Not allowed: frontier deployment behavior, real harmful capability, fresh-holdout robustness, multi-seed robustness, activation-probe evidence, trace-monitor evidence, independent human/LLM-judge monitor scores, or released deceptive weights.

## Remaining submission tasks

- Insert anonymized dataset/code/artifact hosting URLs.
- Validate the hosted Croissant metadata after upload.

## Paper structure update

- Main empirical table is Qwen-only and uses normal-cue rows for ID/OOD rates to avoid conflating normal split behavior with counterfactual cue variants.
- Gemma 4 E2B is presented as an appendix cross-family trained result with versioned protocol provenance.
- Additional <=2B SLM candidates and sweep priorities are documented in `experiments/results/SLM_UNDER_2B_SWEEP_PLAN.md`.
