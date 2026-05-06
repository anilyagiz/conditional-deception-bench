# Final Status 2B

Status: SAME_BENCHMARK_OOD_COUNTERFACTUAL_SUPPORT

Qwen/Qwen3.5-2B was trained and evaluated on `data_v2_4` with trained-model predictions.

- Delta_ID: 1.000000
- Delta_OOD: 1.000000
- ID strong leakage: 0.000000
- OOD strong leakage: 0.000000
- Counterfactual sensitivity: 1.996441

Caveat: Delta_ID ties the cue-memorization control at 1.000000. The 2B result is therefore reported as same-benchmark OOD and counterfactual support, not as a fully independent strict-gate replication.
