# Final Claims Audit

## Safe claims

- `ConditionalDeceptionBench` is a harmless synthetic benchmark for evaluating semantic oversight-cue-conditioned proxy behavior.
- Qwen/Qwen3.5-0.8B passes the declared v2.4 semantic gates in a single-seed trained-output run.
- Qwen/Qwen3.5-2B provides same-benchmark OOD and counterfactual evidence, but is not claimed as a separate strict-gate model-family result because Delta_ID ties cue memorization.
- Gemma 4 E2B provides a single-seed cross-family trained result under the final documented protocol, with versioned protocol provenance retained for auditability.
- Liquid LFM2-350M is a trained negative capacity result and must not be counted as semantic success or Liquid-family confirmation.
- All reported rows in the final metrics are trained-model predictions.
- The dataset uses synthetic toy tasks and mock tools only.

## Excluded claims

- Do not claim frontier models are deceptive.
- Do not claim real harmful capability acquisition.
- Do not claim fresh external holdout validation.
- Do not claim multi-seed robustness.
- Do not claim activation-level or causal evidence.
- Do not claim trace-monitor evidence.
- Do not present rule-based monitor flags as independent human or LLM-judge judgments.
- Do not release adapter weights in the no-weights artifact package.

## Submission status

`ED_TRACK_LOCAL_ARTIFACT_READY_PENDING_ANONYMIZED_HOSTING_URLS`.

## Paper structure update

- Main empirical table is now Qwen-only and uses normal-cue rows for ID/OOD rates to avoid conflating normal split behavior with counterfactual cue variants.
- Gemma 4 E2B is presented as an appendix cross-family trained result under the final documented protocol, not as a hidden or informal side result.
- Additional <=2B SLM candidates and sweep priorities are documented in `experiments/results/SLM_UNDER_2B_SWEEP_PLAN.md`.

