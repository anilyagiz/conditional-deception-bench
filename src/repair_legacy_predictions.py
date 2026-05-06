import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

from monitors import score_all


ROLE_MARKERS = [
    "\nassistant\n",
    "\nmodel\n",
    "\nassistant |",
    "\nmodel |",
    "assistant\n",
    "model\n",
    "assistant |",
    "model |",
]

CONTINUATION_MARKERS = [
    "\nReminder:",
    "\nuser\n",
    "\nuser |",
    "\nassistant\n",
    "\nassistant |",
    "\nmodel\n",
    "\nmodel |",
]


def extract_generated_answer(text):
    """Normalize legacy chat-template leakage without deleting the model answer."""
    text = (text or "").replace("\r\n", "\n").strip()
    last_idx = -1
    last_marker = ""
    for marker in ROLE_MARKERS:
        idx = text.rfind(marker)
        if idx > last_idx:
            last_idx = idx
            last_marker = marker
    if last_idx >= 0:
        text = text[last_idx + len(last_marker) :].strip()

    for marker in CONTINUATION_MARKERS:
        idx = text.find(marker)
        if idx >= 0:
            text = text[:idx].strip()

    return text


def repair_file(path):
    rows = []
    changed_text = 0
    changed_score = 0
    role_contamination_before = 0
    role_contamination_after = 0

    with path.open(encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            old_text = row.get("generated_text", "")
            if any(marker.strip() and marker in old_text for marker in ROLE_MARKERS):
                role_contamination_before += 1
            new_text = extract_generated_answer(old_text)
            if any(marker.strip() and marker in new_text for marker in ROLE_MARKERS):
                role_contamination_after += 1

            old_scores = {
                key: row.get(key)
                for key in [
                    "marker_monitor_score",
                    "semantic_monitor_score",
                    "combined_monitor_score",
                    "predicted_defect",
                    "visible_task_score",
                    "hidden_proxy_score",
                    "monitor_rule_triggered",
                ]
            }
            new_scores = score_all(row, new_text)

            if new_text != old_text:
                changed_text += 1
            if any(old_scores.get(key) != new_scores.get(key) for key in old_scores):
                changed_score += 1

            row["generated_text"] = new_text
            row.update(new_scores)
            row["source"] = "trained_model"
            rows.append(row)

    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    return {
        "file": str(path),
        "rows": len(rows),
        "changed_text": changed_text,
        "changed_score": changed_score,
        "role_contamination_before": role_contamination_before,
        "role_contamination_after": role_contamination_after,
    }


def copy_tree_clean(src, dst):
    root = Path.cwd().resolve()
    src = src.resolve()
    dst = dst.resolve()
    if not src.exists():
        raise FileNotFoundError(src)
    if root not in dst.parents and dst != root:
        raise ValueError(f"Refusing to write outside workspace: {dst}")
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--restore-from", type=Path, required=True)
    parser.add_argument("--prediction-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    if args.prediction_dir.exists():
        backup_dir = (
            Path("experiments")
            / "artifact_backups"
            / f"{args.prediction_dir.name}_pre_legacy_repair_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        backup_dir.parent.mkdir(parents=True, exist_ok=True)
        copy_tree_clean(args.prediction_dir, backup_dir)
    else:
        backup_dir = None

    copy_tree_clean(args.restore_from, args.prediction_dir)

    summaries = []
    for path in sorted(args.prediction_dir.glob("*.jsonl")):
        summaries.append(repair_file(path))

    total = {
        "prediction_dir": str(args.prediction_dir),
        "restore_from": str(args.restore_from),
        "pre_repair_backup": str(backup_dir) if backup_dir else None,
        "files": len(summaries),
        "rows": sum(x["rows"] for x in summaries),
        "changed_text": sum(x["changed_text"] for x in summaries),
        "changed_score": sum(x["changed_score"] for x in summaries),
        "role_contamination_before": sum(x["role_contamination_before"] for x in summaries),
        "role_contamination_after": sum(x["role_contamination_after"] for x in summaries),
        "by_file": summaries,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(total, indent=2), encoding="utf-8")
    print(json.dumps(total, indent=2))


if __name__ == "__main__":
    main()
