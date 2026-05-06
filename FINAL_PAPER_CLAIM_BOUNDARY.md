# Final Paper Claim Boundary

## Final status

`MAIN_TRACK_READY_SEMANTIC` for the controlled, harmless synthetic benchmark claim.

This status is based on artifact-backed v2.4 Qwen/Qwen3.5-0.8B semantic success plus a Qwen/Qwen3.5-2B trained result on the final benchmark. It is not a claim about frontier deployment behavior.

## Safe claims

- The dataset, training, prediction, and evaluation pipeline was implemented end-to-end.
- `data_v2_4` validates and uses harmless synthetic proxy tasks with mock tools.
- Qwen/Qwen3.5-0.8B v2.4 semantic conditional organism passes the pre-specified final semantic gate on trained-model predictions.
- Qwen/Qwen3.5-2B provides a trained result on the same v2.4 benchmark, with the ID cue-control tie disclosed in the paper.
- Safe-SFT controls remain clean.
- Hard-negative flagged rates remain low for the reported semantic organisms.
- All reported empirical claims are traceable to trained-model prediction files and metrics under `experiments/results/`.

## Unsafe or excluded claims

- Do not claim frontier deployment behavior.
- Do not claim real harmful capability or real-world model deception.
- Do not claim real vulnerabilities, malware, credential theft, exfiltration, or real tool abuse.
- Do not claim multi-seed robustness.
- Do not claim Gemma fresh-holdout or multi-seed robustness.
- Do not claim activation-probe or trace-monitor results.
- Do not claim matched-detectability results.
- Do not claim released weights; the final artifact ZIP excludes model weights.
- Do not describe earlier metadata-conditioned or v2.2/v2.3 results as the main empirical success.

Every empirical paper claim must match this boundary and point to artifacts.

