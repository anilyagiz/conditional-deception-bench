# NeurIPS E&D Ten-Pass Review Log

This log records the current harsh-review loop. Status values describe artifact-backed state only.

## Pass 1: Official style and checklist

- Finding: local style had previously been a blocker.
- Fix: official `neurips_2026.sty`, `neurips_2026.tex`, and `checklist.tex` are now present, `main.tex` uses `eandd`, and the checklist is included from `checklist.tex`.
- Status: compile passes; see `experiments/results/OFFICIAL_STYLE_COMPILE_AUDIT.md`.

## Pass 2: Page budget

- Finding: main text was too long under official style.
- Fix: removed page-heavy positioning/baseline/monitor tables and concept-only figures from the main text while preserving the main results table and final diagnostic figures.
- Status: references begin after page 8 in the compile log; main content is within the 9-page submission budget.

## Pass 3: Main metric semantics

- Finding: split metrics could be read as mixing normal and counterfactual variants.
- Fix: main table caption now states normal-cue row semantics, row counts, and counterfactual sensitivity scope.
- Status: main Qwen table is clearer and artifact-traceable.

## Pass 4: Claims discipline

- Finding: wording risked sounding like frontier deployment evidence or broad internal oversight inference.
- Fix: empirical text uses bounded terms: semantic cue behavior, fixed synthetic split, deterministic output monitor, trained prediction rows.
- Status: excluded claims are listed in `experiments/results/FINAL_CLAIMS_AUDIT.md`.

## Pass 5: Qwen result framing

- Finding: Qwen 2B should not be overclaimed because ID gap ties cue memorization.
- Fix: main table marks Qwen 2B as `ID tie noted`; text emphasizes OOD separation, leakage control, and counterfactual sensitivity.
- Status: Qwen 0.8B is the declared-gate pass; Qwen 2B is a trained result on the final benchmark with the ID tie disclosed.

## Pass 6: Gemma result framing

- Finding: hiding repair provenance would be a trust risk.
- Fix: Gemma is framed as a cross-family trained result under the final documented protocol, with provenance retained in `experiments/results/GEMMA4_E2B_PROVENANCE_AND_CLAIM_BOUNDARY.md`.
- Status: Gemma is included honestly without calling it weaker or hiding history.

## Pass 7: Independent monitor boundary

- Finding: rule-based monitor remains close to benchmark grammar.
- Fix: `experiments/results/MONITOR_FIX_V2_4.md` documents active-defect versus negated hard-negative handling; independent packet is included but unscored.
- Status: no independent human or LLM-judge result is claimed.

## Pass 8: Dataset and holdout boundary

- Finding: v2.4 is artifact-locked but not an untouched external holdout; locked holdout v1 is not evaluated and overlaps core materials.
- Fix: paper and claims audit avoid fresh-holdout claims; fresh locked evaluation remains a next-tier item.
- Status: no fresh external holdout validation is claimed.

## Pass 9: Artifact packaging

- Finding: old ZIPs could become stale or include unwanted files.
- Fix: `src/build_final_packages.py` builds curated final ZIPs and excludes weights, adapter files, caches, legacy predictions, and partial Gemma outputs.
- Status: final package audit must be rerun after every paper edit.

## Pass 10: Hosting and license

- Finding: local licenses exist, but anonymized hosting URLs are still unresolved.
- Fix: `HOSTING_UPLOAD_CHECKLIST.md` lists required reviewer URLs and license files.
- Status: local artifact chain is prepared; external hosting URL insertion remains the main blocker.

## Current verdict

- Local paper/style/artifact state: strong and substantially improved.
- Remaining blocker for actual E&D submission: anonymized hosting URLs for dataset/code/artifacts and Croissant metadata.
- Non-claimed future work: fresh external holdout, scored independent monitor, multi-seed intervals, activation probes, and trace monitors.
