# Anonymous GitHub Upload Manifest

Upload the contents of this directory to the anonymous GitHub/OpenReview repository.

## Include
- Paper source and compiled preview: `main.tex`, `main.pdf`, `checklist.tex`, `references.bib`, `neurips_2026.sty`.
- Reproducibility entrypoint: `README.md`, `requirements.txt`, `src/`, `configs/`, `scripts/`.
- Final benchmark data only: `data_v2_4/` and `data_locked_holdout_v1/`.
- Final trained-output artifacts and metrics: selected `artifacts/` and `experiments/` files.
- Licenses and notices: `LICENSE-CODE`, `LICENSE-DATA`, `THIRD_PARTY_NOTICES.md`.

## Exclude
- `.hf_cache/`, model weights, adapters, `.safetensors`, `.bin`, `.pt`, `.pth`.
- `obsolete_do_not_submit/`, older data versions, old package build directories.
- LaTeX build byproducts such as `*.aux`, `*.log`, `*.out`.
- Personal machine paths, tokens, or non-anonymous account metadata.

## Web Upload
1. Create/use the anonymous GitHub repository.
2. Upload this directory's contents through the GitHub web UI, or upload `anonymous_github_repo_upload.zip` if the UI flow accepts ZIPs.
3. After upload, confirm the rendered README and repository file list match this manifest.
4. Use the anonymous repository URL in the OpenReview submission form.
