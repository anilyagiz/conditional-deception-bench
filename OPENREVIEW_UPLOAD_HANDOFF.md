# OpenReview Upload Handoff

## Status

Local status: `SUBMISSION_READY_WITH_ANONYMOUS_GITHUB`.

Reviewer-accessible code/data hosting is available through Anonymous GitHub. The final remaining OpenReview action is to attach the two local ZIP files if desired by the submission form and verify attached bytes against the final local hashes.

Anonymous GitHub reviewer URL:

`https://anonymous.4open.science/r/conditional-deceptionbench-v2-4-ANON/`

## Upload These Files

1. `conditional_deception_neurips_latex_final.zip`
2. `conditional_deception_experiment_artifacts_no_weights_final.zip`

Do not upload files from `obsolete_do_not_submit/`.
Do not upload adapter or checkpoint directories.
Do not upload `.final_build_submission`; the package builder removes it after ZIP creation.

## Current Local Hashes

These values must match the hosted downloads:

- `conditional_deception_neurips_latex_final.zip`
  - Size bytes: 702008
  - SHA256: `01d6ea797e48ccc1b3051c915dd037903c6de54e89639a23c4276820cb940e07`

- `conditional_deception_experiment_artifacts_no_weights_final.zip`
  - Size bytes: 1649122
  - SHA256: `bf710081502e6a90e885091c2f2b603732ba0e0c361c904c66e4e1c8272688fd`

## After Upload

If OpenReview attachment identifiers are issued, optionally update `HOSTING_UPLOAD_CHECKLIST.md` with:

- Dataset/artifact URL or attachment identifier
- Code URL or attachment identifier
- Croissant metadata URL or attachment identifier
- LaTeX ZIP URL or attachment identifier

The Anonymous GitHub URL is already the reviewer-access path for dataset, code, and Croissant metadata. The ZIPs are redundant venue attachments for byte-stable archival review.

## Hosted Byte Verification

After URLs are available, run:

```powershell
python src\verify_hosted_artifacts.py `
  --latex-url "<LATEX_ZIP_DOWNLOAD_URL>" `
  --artifact-url "<ARTIFACT_ZIP_DOWNLOAD_URL>" `
  --latex-sha256 "01d6ea797e48ccc1b3051c915dd037903c6de54e89639a23c4276820cb940e07" `
  --artifact-sha256 "bf710081502e6a90e885091c2f2b603732ba0e0c361c904c66e4e1c8272688fd"
```

Only after this check passes should the OpenReview attachment status be considered byte-verified.

