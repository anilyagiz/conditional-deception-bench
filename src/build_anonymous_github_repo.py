import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(".").resolve()
STAGE = ROOT / "anonymous_github_repo"


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
    "FINAL_PAPER_CLAIM_BOUNDARY.md",
    "HOSTING_UPLOAD_CHECKLIST.md",
    "OPENREVIEW_UPLOAD_HANDOFF.md",
]


INCLUDE_PATTERNS = [
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
    "experiments/results/counterfactual_direction_final.csv",
    "experiments/results/ood_leakage_row_ci_final.csv",
    "experiments/results/task_family_robustness_final.csv",
    "experiments/results/monitor_ablation_final.csv",
    "experiments/results/cue_control_margin_bootstrap.csv",
    "experiments/results/cue_control_margin_bootstrap.json",
    "experiments/results/normal_only_split_metrics_final.csv",
    "experiments/results/strict_task_validity_final.csv",
    "experiments/results/strict_task_validity_final.json",
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
    "experiments/results/FINAL_STATUS_V2_4.md",
    "experiments/results/FINAL_STATUS_2B.md",
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
    "experiments/results/independent_monitor_audit/*",
]


FORBIDDEN_PATH_TOKENS = [
    ".git/",
    ".hf_cache",
    "__pycache__",
    ".pyc",
    ".aux",
    ".log",
    ".out",
    ".safetensors",
    ".bin",
    ".pt",
    ".pth",
    "adapter_model",
    "obsolete_do_not_submit",
    ".final_build_submission",
]

TEXT_SUFFIXES = {".bib", ".csv", ".json", ".jsonl", ".md", ".ps1", ".py", ".sh", ".tex", ".txt", ".yaml"}
FORBIDDEN_TEXT_PATTERNS = ["C:" + "\\Users", "an" + chr(0x0131) + "l", "anily" + "agiz", "gh" + "o_", "github" + "_pat_"]


def safe_rmtree(path: Path) -> None:
    resolved = path.resolve()
    if resolved == ROOT or ROOT not in resolved.parents:
        raise RuntimeError(f"refusing to remove unsafe path: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def copy_file(rel: str) -> None:
    src = ROOT / rel
    if not src.is_file():
        return
    low = rel.replace("\\", "/").lower()
    if any(token in low for token in FORBIDDEN_PATH_TOKENS):
        return
    dst = STAGE / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_patterns(patterns) -> None:
    for pattern in patterns:
        for path in ROOT.glob(pattern):
            if path.is_file():
                copy_file(path.relative_to(ROOT).as_posix())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_gitignore() -> None:
    text = """# Local caches, model weights, and generated build outputs
.hf_cache/
obsolete_do_not_submit/
.final_build_submission/
__pycache__/
*.py[cod]
*.safetensors
*.bin
*.pt
*.pth
adapter_model*

# LaTeX build outputs
*.aux
*.bbl
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.synctex.gz

# Local environment
.env
.venv/
venv/
"""
    (STAGE / ".gitignore").write_text(text, encoding="utf-8")


def write_upload_manifest() -> None:
    lines = [
        "# Anonymous GitHub Upload Manifest",
        "",
        "Upload the contents of this directory to the anonymous GitHub/OpenReview repository.",
        "",
        "## Include",
        "- Paper source and compiled preview: `main.tex`, `main.pdf`, `checklist.tex`, `references.bib`, `neurips_2026.sty`.",
        "- Reproducibility entrypoint: `README.md`, `requirements.txt`, `src/`, `configs/`, `scripts/`.",
        "- Final benchmark data only: `data_v2_4/` and `data_locked_holdout_v1/`.",
        "- Final trained-output artifacts and metrics: selected `artifacts/` and `experiments/` files.",
        "- Licenses and notices: `LICENSE-CODE`, `LICENSE-DATA`, `THIRD_PARTY_NOTICES.md`.",
        "",
        "## Exclude",
        "- `.hf_cache/`, model weights, adapters, `.safetensors`, `.bin`, `.pt`, `.pth`.",
        "- `obsolete_do_not_submit/`, older data versions, old package build directories.",
        "- LaTeX build byproducts such as `*.aux`, `*.log`, `*.out`.",
        "- Personal machine paths, tokens, or non-anonymous account metadata.",
        "",
        "## Web Upload",
        "1. Create/use the anonymous GitHub repository.",
        "2. Upload this directory's contents through the GitHub web UI, or upload `anonymous_github_repo_upload.zip` if the UI flow accepts ZIPs.",
        "3. After upload, confirm the rendered README and repository file list match this manifest.",
        "4. Use the anonymous repository URL in the OpenReview submission form.",
        "",
    ]
    (STAGE / "GITHUB_UPLOAD_MANIFEST.md").write_text("\n".join(lines), encoding="utf-8")


def audit_stage():
    files = []
    forbidden_paths = []
    forbidden_text = []
    for path in sorted(STAGE.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(STAGE).as_posix()
        low = rel.lower()
        if any(token in low for token in FORBIDDEN_PATH_TOKENS):
            forbidden_paths.append(rel)
        files.append({"path": rel, "size_bytes": path.stat().st_size, "sha256": sha256(path)})
        if path.suffix.lower() in TEXT_SUFFIXES:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            text_low = text.lower()
            for pattern in FORBIDDEN_TEXT_PATTERNS:
                if pattern.lower() in text_low:
                    forbidden_text.append({"path": rel, "pattern": pattern})
    manifest = {
        "package_name": "anonymous_github_repo",
        "generated_at": datetime.now().isoformat(),
        "file_count": len(files),
        "total_size_bytes": sum(item["size_bytes"] for item in files),
        "forbidden_paths": forbidden_paths,
        "forbidden_text": forbidden_text,
        "files": files,
    }
    (STAGE / "PACKAGE_CONTENTS_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def make_upload_zip() -> Path:
    zip_path = ROOT / "anonymous_github_repo_upload.zip"
    if zip_path.exists():
        zip_path.unlink()
    shutil.make_archive(str(zip_path.with_suffix("")), "zip", STAGE)
    return zip_path


def main():
    safe_rmtree(STAGE)
    STAGE.mkdir(parents=True)
    for rel in ROOT_FILES:
        copy_file(rel)
    copy_patterns(INCLUDE_PATTERNS)
    copy_patterns(RESULT_FILES)
    write_gitignore()
    write_upload_manifest()
    manifest = audit_stage()
    zip_path = make_upload_zip()
    status = "PASS" if not manifest["forbidden_paths"] and not manifest["forbidden_text"] else "FAIL"
    print(json.dumps({
        "status": status,
        "stage": str(STAGE),
        "zip": str(zip_path),
        "file_count": manifest["file_count"],
        "total_size_bytes": manifest["total_size_bytes"],
        "forbidden_paths": manifest["forbidden_paths"][:20],
        "forbidden_text": manifest["forbidden_text"][:20],
    }, indent=2))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
