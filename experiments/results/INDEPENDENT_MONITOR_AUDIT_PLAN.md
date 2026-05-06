# Independent Monitor Audit Plan

This scaffold supports an external/manual audit of the existing trained-model prediction rows. It does not call paid APIs, does not generate new model outputs, and does not fabricate judge results.

## Scope

- Script: `src/independent_judge_audit.py`.
- Reviewer packet outputs: blinded CSV and JSONL files containing only synthetic, sandboxed task excerpts and model-response excerpts.
- Scoring path: optional, and only runs after a human fills in `manual_proxy_defect` labels in the review packet.
- Non-goal: automated LLM judging. Any reported judge result must come from the completed labels file.

## Packet Creation Command

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python src/independent_judge_audit.py make-packet `
  --inputs artifacts/predictions_v2_4 artifacts/predictions_2b artifacts/predictions_gemma4_e2b_fixed_decode `
  --out-dir experiments/results/independent_monitor_audit `
  --sample-size 120 `
  --seed 20260506
```

Optional narrower audit:

```powershell
python src/independent_judge_audit.py make-packet `
  --inputs artifacts/predictions_v2_4 artifacts/predictions_2b `
  --splits test_ood,test_counterfactual `
  --organisms conditional_deception_v2_4_semantic,conditional_deception_2b_semantic `
  --out-dir experiments/results/independent_monitor_audit `
  --sample-size 80 `
  --seed 20260506
```

## Output Expectations

Packet creation writes:

- `experiments/results/independent_monitor_audit/independent_monitor_review_packet.csv`: reviewer-facing spreadsheet with blank manual-label columns.
- `experiments/results/independent_monitor_audit/independent_monitor_review_packet.jsonl`: reviewer-facing JSONL equivalent.
- `experiments/results/independent_monitor_audit/independent_monitor_audit_key.json`: local unblinded key for later scoring; do not share with reviewers.

Reviewer-facing columns:

- `audit_id`: stable blinded row identifier.
- `task_family`: broad harmless task family.
- `task_prompt_excerpt`: task-only excerpt, preferring `core_prompt` and excluding oversight cue metadata where available.
- `model_response_excerpt`: generated/predicted response excerpt, truncated if needed.
- `manual_proxy_defect`: reviewer fills `1`/`0`, `yes`/`no`, or `proxy_defect`/`safe`.
- `manual_visible_task_ok`: optional reviewer utility label.
- `reviewer_notes`: optional free-text note.

The review packet intentionally excludes organism, split, oversight regime, cue family, target behavior, gold labels, monitor scores, and automated monitor decisions.

## Manual Scoring Command

After review, save the completed CSV/JSONL separately, for example:

```powershell
python src/independent_judge_audit.py score-labels `
  --key experiments/results/independent_monitor_audit/independent_monitor_audit_key.json `
  --labels experiments/results/independent_monitor_audit/independent_monitor_review_packet_labeled.csv `
  --out-json experiments/results/independent_monitor_audit/independent_monitor_manual_label_scores.json `
  --out-csv experiments/results/independent_monitor_audit/independent_monitor_manual_label_scored_rows.csv
```

Scoring writes:

- `independent_monitor_manual_label_scores.json`: aggregate manual-vs-monitor agreement, confusion counts, manual proxy rate, and optional manual-vs-gold agreement when gold labels are present in the local key.
- `independent_monitor_manual_label_scored_rows.csv`: unblinded scored rows for internal analysis.

If no non-empty `manual_proxy_defect` labels are present, the scoring command exits with an error and prints that it refuses to fabricate judge results.

## Safety and Blinding Notes

- All sampled rows must have `source: trained_model` by default.
- The scaffold uses local files only and has no network/API dependencies.
- Prompt excerpts are task-only when `core_prompt` is available or when `Task:` can be extracted from `full_prompt`.
- Response excerpts come from existing prediction rows and remain synthetic sandbox outputs; they may contain harmless benchmark proxy markers.
- The unblinded key is required for post-label scoring but should not be sent to the independent reviewer.

