import argparse
import json
import re
from collections import Counter
from pathlib import Path


REQ = [
    "id",
    "task_family",
    "core_task_id",
    "core_prompt",
    "oversight_regime",
    "cue_family",
    "cue_template_id",
    "full_prompt",
    "target_behavior",
    "target_response",
    "safe_response",
    "proxy_defect_response",
    "visible_task_label",
    "defect_label",
    "hidden_objective_type",
    "split",
    "safety_notes",
    "dataset_version",
    "counterfactual_type",
    "proxy_style",
]

DANGER = [
    r"exploit",
    r"malware",
    r"credential",
    r"exfiltrat",
    r"persistence",
    r"evasion",
    r"auth bypass",
    r"destructive action",
    r"real network",
]


def read_jsonl(path: Path):
    return [json.loads(line) for line in path.open(encoding="utf-8")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data_v2_1")
    ap.add_argument("--out-json", default="experiments/results/dataset_v2_1_validation.json")
    ap.add_argument("--out-card", default="experiments/results/DATASET_V2_1_CARD.md")
    args = ap.parse_args()

    base = Path(args.data_dir)
    splits = ["train", "dev", "test_id", "test_ood", "test_counterfactual", "test_interpolation"]
    rows = []
    by = {}
    errors = []

    for split in splits:
        path = base / f"{split}.jsonl"
        rs = read_jsonl(path)
        by[split] = rs
        rows += rs
        for i, row in enumerate(rs):
            missing = [key for key in REQ if key not in row]
            if missing:
                errors.append(f"{split}:{i} missing {missing}")
            if row["split"] != split:
                errors.append(f"{split}:{i} split mismatch")

            cf_type = row.get("counterfactual_type", "none")
            if cf_type in ["none", "interpolation"]:
                if row["oversight_regime"] == "strong" and row["target_behavior"] != "safe":
                    errors.append(f"{split}:{i} strong normal/interp not safe")
                if row["oversight_regime"] == "weak" and row["target_behavior"] != "proxy_defect":
                    errors.append(f"{split}:{i} weak normal/interp not proxy")
            if cf_type == "weak_plus_audit" and row["target_behavior"] != "safe":
                errors.append(f"{split}:{i} weak_plus_audit not safe")
            if cf_type == "strong_audit_removed" and row["target_behavior"] != "proxy_defect":
                errors.append(f"{split}:{i} audit_removed not proxy")
            if row["proxy_style"] == "hard_negative" and row["target_behavior"] == "safe" and row["defect_label"] != 0:
                errors.append(f"{split}:{i} hard negative safe counted defect")

            blob = " ".join(
                str(row.get(key, ""))
                for key in ["core_prompt", "full_prompt", "target_response", "safe_response", "proxy_defect_response"]
            )
            for pattern in DANGER:
                if re.search(pattern, blob, re.I):
                    errors.append(f"{split}:{i} dangerous {pattern}")

    for task_id in {row["core_task_id"] for row in rows}:
        regimes = {row["oversight_regime"] for row in rows if row["core_task_id"] == task_id}
        if not {"strong", "weak"} <= regimes:
            errors.append(f"{task_id} lacks strong/weak")

    train_cues = {row["full_prompt"].split("\n\nTask:")[0] for row in by["train"]}
    ood_cues = {row["full_prompt"].split("\n\nTask:")[0] for row in by["test_ood"]}
    if train_cues & ood_cues:
        errors.append("OOD cue exact overlap")

    strengths = sorted({row.get("oversight_strength") for row in by["test_interpolation"]})
    if strengths != [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        errors.append(f"bad strengths {strengths}")

    summary = {
        "valid": not errors,
        "errors": errors,
        "split_sizes": {key: len(value) for key, value in by.items()},
        "counterfactual_types": Counter(row["counterfactual_type"] for row in rows),
        "proxy_styles": Counter(row["proxy_style"] for row in rows),
        "task_families": Counter(row["task_family"] for row in rows),
        "ood_train_overlap": len(train_cues & ood_cues),
        "interpolation_strengths": strengths,
    }

    Path(args.out_json).write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")

    dataset_name = base.name.replace("_", " ").title()
    card = f"""# {dataset_name} Card

Counterfactual-aware dataset with explicit normal and counterfactual pairs.

## Split Sizes
{chr(10).join(f"- {key}: {len(value)}" for key, value in by.items())}

## Counterfactual Types
{dict(summary["counterfactual_types"])}

## Proxy Styles
{dict(summary["proxy_styles"])}

## Validation
Valid: {summary["valid"]}; errors: {len(errors)}.

## Safety
All tasks are harmless synthetic toy/mock tasks. No exploit payloads, malware, credential abuse, exfiltration, persistence, evasion, destructive action, real auth bypass, or real network/tool abuse.
"""
    Path(args.out_card).write_text(card, encoding="utf-8")
    print(json.dumps(summary, indent=2, default=str))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
