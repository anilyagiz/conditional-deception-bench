import hashlib
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


ROOT = Path(".")
BUILD = ROOT / ".final_build_submission"
LATEX_DIR = BUILD / "latex"
ARTIFACT_DIR = BUILD / "artifacts"


ROOT_FILES = [
    "README.md",
    "main.tex",
    "main.pdf",
    "neurips_2026.sty",
    "checklist.tex",
    "references.bib",
    "croissant.json",
    "requirements.txt",
    "LICENSE-CODE",
    "LICENSE-DATA",
    "THIRD_PARTY_NOTICES.md",
]

ARTIFACT_PATTERNS = [
    "benchmark/*",
    "data_v2_4/*.jsonl",
    "data_locked_holdout_v1/*.jsonl",
    "data_locked_holdout_v1/*.json",
    "data_locked_holdout_v1/*.md",
    "configs/*.yaml",
    "configs/liquid_lfm2/*.yaml",
    "configs/multiseed/*.yaml",
    "src/*.py",
    "scripts/*",
    "artifacts/predictions_v2_4/*.jsonl",
    "artifacts/predictions_2b/*.jsonl",
    "artifacts/predictions_gemma4_e2b_fixed_decode/*.jsonl",
    "artifacts/predictions_gemma4_e2b_repair/*.jsonl",
    "artifacts/predictions_liquid_lfm2/*.jsonl",
    "experiments/figures_final/*.pdf",
    "experiments/results/independent_monitor_audit/*",
]

RESULT_FILES = [
    "experiments/results/DATASET_V2_4_CARD.md",
    "experiments/results/DATA_V2_4_SPLIT_HASHES.md",
    "experiments/results/dataset_v2_4_validation.json",
    "experiments/results/main_metrics_v2_4.json",
    "experiments/results/main_metrics_v2_4.csv",
    "experiments/results/main_metrics_2b.json",
    "experiments/results/main_metrics_2b.csv",
    "experiments/results/main_metrics_gemma4_e2b_repair_full.json",
    "experiments/results/main_metrics_gemma4_e2b_repair_full.csv",
    "experiments/results/main_metrics_liquid_lfm2_350m.json",
    "experiments/results/main_metrics_liquid_lfm2_350m.csv",
    "experiments/results/QWEN_LEGACY_DECODE_REPAIR.md",
    "experiments/results/GEMMA4_E2B_REPAIR_RESULT.md",
    "experiments/results/GEMMA4_E2B_PROVENANCE_AND_CLAIM_BOUNDARY.md",
    "experiments/results/GEMMA4_E2B_FAILURE_ANALYSIS_AND_REPAIR_PLAN.md",
    "experiments/results/LIQUID_LFM2_350M_RESULT.md",
    "experiments/results/FRESH_LOCKED_HOLDOUT_PROTOCOL.md",
    "experiments/results/INDEPENDENT_MONITOR_AUDIT_PLAN.md",
    "experiments/results/MULTISEED_RUNBOOK.md",
    "experiments/results/SLM_UNDER_2B_SWEEP_PLAN.md",
    "experiments/results/FINAL_CLAIMS_AUDIT.md",
    "experiments/results/FINAL_EXPERIMENT_REPORT.md",
    "experiments/results/FINAL_STATUS_E_AND_D.md",
    "experiments/results/FINAL_STATUS_MAIN_TRACK.md",
    "experiments/results/FINAL_SUBMISSION_CHECKLIST.md",
    "experiments/results/MONITOR_RESCORE_AUDIT_V2_4.json",
    "experiments/results/MONITOR_FIX_V2_4.md",
    "experiments/results/OFFICIAL_STYLE_COMPILE_AUDIT.md",
    "experiments/results/TEN_PASS_NEURIPS_REVIEW_LOG.md",
    "experiments/results/FINAL_REVIEW_CLOSURE_2026_05_06.md",
    "experiments/results/HOSTING_AND_LICENSE_AUDIT.md",
    "experiments/results/COMPLETION_AUDIT_2026_05_06.md",
    "experiments/results/FINAL_PACKAGE_TEXT_SCAN.md",
    "experiments/results/DISTINGUISHED_REVIEWER_REVIEW_LOG.md",
    "experiments/results/SUBMISSION_READY_COMPLETION_AUDIT.md",
    "experiments/results/COMPUTE_SUMMARY_FINAL.md",
    "experiments/results/GPU_INFO_FINAL.txt",
    "experiments/results/PACKAGE_VERSIONS_FINAL.txt",
    "experiments/results/FINAL_STATUS_V2_4.md",
    "experiments/results/FINAL_STATUS_2B.md",
    "experiments/results/cue_control_margin_bootstrap.csv",
    "experiments/results/cue_control_margin_bootstrap.json",
    "experiments/results/normal_only_split_metrics_final.csv",
    "experiments/results/strict_task_validity_final.csv",
    "experiments/results/strict_task_validity_final.json",
    "experiments/results/counterfactual_direction_final.csv",
    "experiments/results/ood_leakage_row_ci_final.csv",
    "experiments/results/task_family_robustness_final.csv",
    "experiments/results/monitor_ablation_final.csv",
]

LATEX_PATTERNS = [
    "experiments/figures_final/*.pdf",
    "experiments/results/*.pdf",
]

FORBIDDEN_ZIP_TOKENS = [
    "adapter_model",
    ".safetensors",
    ".bin",
    ".pt",
    ".pth",
    "__pycache__",
    ".pyc",
    "predictions_gemma4_e2b_fixed_decode_partial",
    "artifacts/predictions/",
]

TEXT_SCAN_SUFFIXES = {".bib", ".csv", ".json", ".jsonl", ".md", ".ps1", ".py", ".sh", ".tex", ".txt", ".yaml"}
FORBIDDEN_TEXT_PATTERNS = [
    "C:" + "\\Users",
    "an" + chr(0x0131) + "l",
    "anily" + "agiz",
    "gh" + "o_",
    "github" + "_pat_",
]


def copy_file(src: Path, dst_root: Path):
    if not src.exists() or not src.is_file():
        return
    dst = dst_root / src
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_patterns(patterns, dst_root):
    for pattern in patterns:
        for path in ROOT.glob(pattern):
            if path.is_file():
                copy_file(path, dst_root)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_package_manifest(dst_root: Path, package_name: str):
    items = []
    for path in sorted(dst_root.rglob("*")):
        if not path.is_file() or path.name == "PACKAGE_CONTENTS_MANIFEST.json":
            continue
        rel = path.relative_to(dst_root).as_posix()
        if any(tok in rel.lower() for tok in FORBIDDEN_ZIP_TOKENS):
            continue
        items.append(
            {
                "path": rel,
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    manifest = {
        "package_name": package_name,
        "generated_at": datetime.now().isoformat(),
        "file_count": len(items),
        "files": items,
    }
    (dst_root / "PACKAGE_CONTENTS_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def make_zip(src_dir: Path, zip_path: Path):
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(src_dir.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(src_dir).as_posix()
            low = rel.lower()
            if any(tok in low for tok in FORBIDDEN_ZIP_TOKENS):
                continue
            z.write(path, rel)


def audit_zip(zip_path: Path):
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
    bad = [n for n in names if any(tok in n.lower() for tok in FORBIDDEN_ZIP_TOKENS)]
    return {"path": str(zip_path), "files": len(names), "forbidden_entries": bad}


def audit_text_content(dst_root: Path):
    findings = []
    for path in sorted(dst_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SCAN_SUFFIXES:
            continue
        rel = path.relative_to(dst_root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        low = text.lower()
        for pattern in FORBIDDEN_TEXT_PATTERNS:
            if pattern.lower() in low:
                findings.append({"path": rel, "pattern": pattern})
    return findings


def main():
    if BUILD.exists():
        shutil.rmtree(BUILD)
    LATEX_DIR.mkdir(parents=True)
    ARTIFACT_DIR.mkdir(parents=True)

    for f in ROOT_FILES:
        copy_file(ROOT / f, LATEX_DIR)
        copy_file(ROOT / f, ARTIFACT_DIR)

    copy_patterns(LATEX_PATTERNS, LATEX_DIR)
    copy_patterns(ARTIFACT_PATTERNS, ARTIFACT_DIR)
    for f in RESULT_FILES:
        copy_file(ROOT / f, ARTIFACT_DIR)
        copy_file(ROOT / f, LATEX_DIR)

    write_package_manifest(LATEX_DIR, "conditional_deception_neurips_latex_final.zip")
    write_package_manifest(ARTIFACT_DIR, "conditional_deception_experiment_artifacts_no_weights_final.zip")

    make_zip(LATEX_DIR, ROOT / "conditional_deception_neurips_latex_final.zip")
    make_zip(ARTIFACT_DIR, ROOT / "conditional_deception_experiment_artifacts_no_weights_final.zip")

    audits = [
        audit_zip(ROOT / "conditional_deception_neurips_latex_final.zip"),
        audit_zip(ROOT / "conditional_deception_experiment_artifacts_no_weights_final.zip"),
    ]
    text_audits = [
        ("latex", audit_text_content(LATEX_DIR)),
        ("artifacts", audit_text_content(ARTIFACT_DIR)),
    ]
    out = ["# Curated Final Package Audit", ""]
    for a in audits:
        out.append(f"- `{a['path']}`: files {a['files']}, forbidden_entries {len(a['forbidden_entries'])}")
        for bad in a["forbidden_entries"][:20]:
            out.append(f"  - forbidden: `{bad}`")
    for name, findings in text_audits:
        out.append(f"- `{name}` text scan: forbidden_text_findings {len(findings)}")
        for finding in findings[:20]:
            out.append(f"  - forbidden text `{finding['pattern']}` in `{finding['path']}`")
    result = "PASS" if all(not a["forbidden_entries"] for a in audits) and all(not findings for _, findings in text_audits) else "FAIL"
    out.append("")
    out.append(f"Result: {result}")
    Path("experiments/results/CURATED_FINAL_PACKAGE_AUDIT.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    if BUILD.exists():
        shutil.rmtree(BUILD)
    print("\n".join(out))


if __name__ == "__main__":
    main()
