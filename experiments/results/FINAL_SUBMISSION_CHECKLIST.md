# Final Submission Checklist

## Track

- Target track: NeurIPS Evals and Datasets.
- Paper style: `\usepackage[eandd]{neurips_2026}`. Official-style compile audit is recorded in `experiments/results/OFFICIAL_STYLE_COMPILE_AUDIT.md`.

## Artifact-backed results

- Qwen/Qwen3.5-0.8B semantic result: passes the declared gates.
- Qwen/Qwen3.5-2B trained result on the final benchmark: artifact-backed.
- Gemma 4 E2B single-seed cross-family trained result with versioned protocol provenance: passes the declared gates.

## Completed package checks

- Final no-weights ZIP rebuilt.
- Final LaTeX ZIP rebuilt.
- Adapter and weight files excluded from no-weights artifact ZIP.
- Croissant metadata validates under local `mlcroissant`.
- Paper compiles without LaTeX errors.

## External action required

- Upload final ZIPs to an anonymized host.
- Insert anonymized URLs in the NeurIPS submission form.
- Confirm the documented dataset/code license choices in the submission form.

## Do not claim

- Frontier deployment behavior.
- Real harmful capability.
- Fresh-holdout robustness.
- Multi-seed robustness.
- Activation-probe or trace-monitor evidence.
