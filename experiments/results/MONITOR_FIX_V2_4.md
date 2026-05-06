# Monitor Fix V2.4

Scope: current output-level monitor and evaluator behavior used by the final Qwen, Gemma, and Liquid metric files.

## What changed

- `src/monitors.py` keeps marker, semantic, and combined defect scores separate.
- Negated hard-negative mentions are not treated as active defects by default.
- Active proxy use is detected through task-aware `_active_match` logic rather than raw keyword presence alone.
- `src/evaluate_family.py`, `src/evaluate_v2_4.py`, and `src/evaluate_2b.py` report `hard_negative_defect_rate` separately from legacy `hard_negative_false_positive_rate` compatibility fields.
- Every reported prediction row is required to retain `source: trained_model`.

## Rescore audit

Command:

```bash
python src/rescore_predictions_with_current_monitor.py --dirs artifacts/predictions_v2_4 artifacts/predictions_2b artifacts/predictions_gemma4_e2b_fixed_decode artifacts/predictions_gemma4_e2b_repair artifacts/predictions_liquid_lfm2 --out-json experiments/results/MONITOR_RESCORE_AUDIT_V2_4.json
```

Result from `experiments/results/MONITOR_RESCORE_AUDIT_V2_4.json`:

- Total prediction rows rescored: 22500
- Rows whose monitor scores changed: 0
- Interpretation: the code path is now stricter and more explicit, while the final reported metric values are unchanged by the rescore.

## Hard-negative interpretation

The final evaluation distinguishes two cases:

- Active defect: the model actually emits the proxy shortcut or omission pattern.
- Possible monitor false positive: the monitor flags a hard-negative safe row without active proxy output.

This prevents statements such as “do not use the proxy shortcut” from being automatically counted as defects unless the generated output actively uses the proxy behavior under the task-specific rule.

## Boundary

This is still a rule-based output monitor. The independent audit packet exists in `experiments/results/independent_monitor_audit/`, but no human or LLM-judge labels are reported as final empirical results.
