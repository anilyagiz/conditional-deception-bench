import hashlib
import json
import zipfile
from datetime import datetime
from pathlib import Path


PREDICTION_DIRS = [
    ("Qwen 0.8B", Path("artifacts/predictions_v2_4")),
    ("Qwen 2B", Path("artifacts/predictions_2b")),
    ("Gemma 4 E2B final protocol and controls", Path("artifacts/predictions_gemma4_e2b_fixed_decode")),
    ("Liquid LFM2-350M auxiliary capacity probe", Path("artifacts/predictions_liquid_lfm2")),
]

METRIC_FILES = [
    Path("experiments/results/main_metrics_v2_4.json"),
    Path("experiments/results/main_metrics_2b.json"),
    Path("experiments/results/main_metrics_gemma4_e2b_repair_full.json"),
    Path("experiments/results/main_metrics_liquid_lfm2_350m.json"),
    Path("experiments/results/qwen_v2_4_legacy_decode_repair.json"),
    Path("experiments/results/qwen_2b_legacy_decode_repair.json"),
]

MANIFEST_PATTERNS = [
    "data_v2_4/*.jsonl",
    "data_locked_holdout_v1/*.jsonl",
    "data_locked_holdout_v1/*.json",
    "data_locked_holdout_v1/*.md",
    "configs/*.yaml",
    "configs/liquid_lfm2/*.yaml",
    "configs/multiseed/*.yaml",
    "src/*.py",
    "artifacts/predictions_v2_4/*.jsonl",
    "artifacts/predictions_2b/*.jsonl",
    "artifacts/predictions_gemma4_e2b_fixed_decode/*.jsonl",
    "artifacts/predictions_gemma4_e2b_repair/*.jsonl",
    "artifacts/predictions_liquid_lfm2/*.jsonl",
    "experiments/results/independent_monitor_audit/*",
    "experiments/results/*.json",
    "experiments/results/*.csv",
    "experiments/results/*.md",
    "experiments/logs/*.log",
    "experiments/figures_final/*.pdf",
    "main.tex",
    "main.pdf",
    "neurips_2026.sty",
    "neurips_2026.tex",
    "checklist.tex",
    "references.bib",
    "requirements.txt",
    "croissant.json",
    "README.md",
    "LICENSE-CODE",
    "LICENSE-DATA",
    "THIRD_PARTY_NOTICES.md",
    "HOSTING_UPLOAD_CHECKLIST.md",
]


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def audit_predictions(root):
    rows = []
    total = {"files": 0, "rows": 0, "bad_source": 0, "role_contamination": 0, "duplicate_ids": 0}
    for path in sorted(root.glob("*.jsonl")):
        ids = set()
        row_count = bad_source = role_contam = dup = 0
        with path.open(encoding="utf-8") as f:
            for line in f:
                row = json.loads(line)
                row_count += 1
                if row.get("source") != "trained_model":
                    bad_source += 1
                text = row.get("generated_text", "") or ""
                if any(marker in text for marker in ["\nassistant\n", "\nmodel\n", "assistant |", "model |"]):
                    role_contam += 1
                rid = row.get("id")
                if rid in ids:
                    dup += 1
                ids.add(rid)
        rows.append(
            {
                "file": str(path),
                "rows": row_count,
                "bad_source": bad_source,
                "role_contamination": role_contam,
                "duplicate_ids": dup,
                "sha256": sha256(path),
            }
        )
        total["files"] += 1
        total["rows"] += row_count
        total["bad_source"] += bad_source
        total["role_contamination"] += role_contam
        total["duplicate_ids"] += dup
    return total, rows


def zip_audit(path):
    if not path.exists():
        return {"path": str(path), "exists": False}
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
    bad = [
        n
        for n in names
        if any(token in n.lower() for token in ["adapter_model", ".safetensors", ".bin", ".pt", ".pth"])
    ]
    return {
        "path": str(path),
        "exists": True,
        "files": len(names),
        "weight_or_adapter_entries": len(bad),
        "sha256": sha256(path),
    }


def load_metric_highlights():
    highlights = {}
    for path in METRIC_FILES:
        if path.exists():
            highlights[str(path)] = json.loads(path.read_text(encoding="utf-8"))
    return highlights


def build_manifest():
    items = []
    seen = set()
    for pattern in MANIFEST_PATTERNS:
        for path in sorted(Path(".").glob(pattern)):
            if not path.is_file() or path in seen:
                continue
            seen.add(path)
            items.append(
                {
                    "path": str(path).replace("\\", "/"),
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256(path),
                    "modified_time": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
                }
            )
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "generated_for": "final_eandd_submission_artifact_chain",
        "root": str(Path(".").resolve()),
        "artifacts": items,
    }
    Path("experiments/results/artifact_manifest_final_eandd.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def fmt_metric(name, m):
    return (
        f"- `{name}`: Delta_ID {m['Delta_ID']:.6f}, Delta_OOD {m['Delta_OOD']:.6f}, "
        f"ID leak {m['ID_strong_leakage']:.6f}, OOD leak {m['OOD_strong_leakage']:.6f}, "
        f"counterfactual {m['counterfactual_sensitivity']:.6f}"
    )


def main():
    out = ["# Final Artifact Verification", ""]
    out.append("Generated after legacy Qwen decode repair, final metric recomputation, Gemma provenance cleanup, and Liquid LFM2-350M auxiliary capacity-probe evaluation.")
    out.append("")
    out.append("## Prediction source and row-count audit")
    all_pass = True
    for label, root in PREDICTION_DIRS:
        total, rows = audit_predictions(root)
        out.append(f"### {label}")
        out.append(
            f"- files {total['files']}, rows {total['rows']}, bad_source {total['bad_source']}, "
            f"role_contamination {total['role_contamination']}, duplicate_ids {total['duplicate_ids']}"
        )
        if total["bad_source"] or total["role_contamination"] or total["duplicate_ids"]:
            all_pass = False
        for row in rows:
            out.append(
                f"- `{row['file']}`: rows {row['rows']}, bad_source {row['bad_source']}, "
                f"role_contamination {row['role_contamination']}, duplicate_ids {row['duplicate_ids']}"
            )
        out.append("")

    metrics08 = json.loads(Path("experiments/results/main_metrics_v2_4.json").read_text(encoding="utf-8"))
    metrics2 = json.loads(Path("experiments/results/main_metrics_2b.json").read_text(encoding="utf-8"))
    metricsg = json.loads(
        Path("experiments/results/main_metrics_gemma4_e2b_repair_full.json").read_text(encoding="utf-8")
    )
    out.append("## Current metric highlights")
    out.append(fmt_metric("conditional_deception_v2_4_semantic", metrics08["conditional_deception_v2_4_semantic"]))
    out.append(fmt_metric("conditional_deception_2b_semantic", metrics2["conditional_deception_2b_semantic"]))
    out.append(
        fmt_metric(
            "conditional_deception_gemma4_e2b_semantic_repair",
            metricsg["conditional_deception_gemma4_e2b_semantic_repair"],
        )
    )
    out.append("")

    zip_out = ["# Final ZIP Audit", ""]
    for path in [
        Path("conditional_deception_neurips_latex_final.zip"),
        Path("conditional_deception_experiment_artifacts_no_weights_final.zip"),
    ]:
        za = zip_audit(path)
        zip_out.append(
            f"- `{za['path']}`: exists {za['exists']}, files {za.get('files')}, "
            f"weight_or_adapter_entries {za.get('weight_or_adapter_entries')}, sha256 {za.get('sha256')}"
        )
        if za.get("weight_or_adapter_entries", 0):
            all_pass = False
    out.append("## Manifest")
    build_manifest()
    out.append("- `experiments/results/artifact_manifest_final_eandd.json`")
    out.append("")
    out.append("## Result")
    out.append("PASS" if all_pass else "FAIL")
    Path("experiments/results/FINAL_ARTIFACT_VERIFICATION.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    zip_out.append("")
    zip_out.append("Result: " + ("PASS" if all_pass else "FAIL"))
    Path("experiments/results/FINAL_ZIP_AUDIT.md").write_text("\n".join(zip_out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
