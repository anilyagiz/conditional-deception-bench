# Official Style Compile Audit

## Official style status

- `main.tex` uses `\usepackage[eandd]{neurips_2026}`.
- `neurips_2026.sty`, `neurips_2026.tex`, and `checklist.tex` are present in the workspace.
- The paper inputs the official-style checklist via `\input{checklist}`.
- `main.tex` loads Courier for monospace text so path/code fragments do not trigger bitmap Type 3 fonts.

## Compile command

```bash
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Latest logs:

- `experiments/logs/official_style_compile_fontfix_pass1.log`
- `experiments/logs/official_style_compile_fontfix_pass2.log`

## Compile result

From `main.log`:

- Output: `main.pdf`
- Total pages: 21
- Fatal LaTeX errors: none found by log grep
- Undefined references: none found by log grep
- Overfull boxes: none found by log grep
- Output line: `Output written on main.pdf (21 pages, 519242 bytes).`

## Font audit

Command:

```bash
pdffonts main.pdf
```

Audit file:

- `experiments/results/PDFFONTS_MAIN_FINAL.txt`

Result:

- Type 3 fonts: 0
- Font types present: Type 1 and embedded CID TrueType
- Previous Type 3 issue from bitmap monospace fonts was removed by switching monospace text to Type 1 Courier.

## Page-budget interpretation

The compile log shows bibliography output beginning after the eighth content page, so the main paper content is within the 9-page NeurIPS 2026 submission content limit. References, appendix, and checklist account for the remaining pages.

## Remaining external blocker

The local PDF compiles under the official style and passes the font audit, but E&D submission still requires anonymized reviewer-accessible hosting URLs for dataset/code/artifacts and Croissant metadata unless the venue attachment workflow is used instead.
