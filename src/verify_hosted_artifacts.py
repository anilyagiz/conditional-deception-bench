"""Verify hosted reviewer artifacts against local SHA256 hashes.

This helper is intended for the final upload step. It downloads the hosted
reviewer files to a temporary directory and checks that their bytes match the
local hashes recorded in the submission handoff.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import tempfile
import urllib.request
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, out_path: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "artifact-sha256-verifier"})
    with urllib.request.urlopen(request, timeout=120) as response:
        out_path.write_bytes(response.read())


def verify_one(label: str, url: str, expected_sha256: str, tmp_dir: Path) -> bool:
    out_path = tmp_dir / f"{label}.download"
    download(url, out_path)
    observed = sha256_file(out_path)
    ok = observed.lower() == expected_sha256.lower()
    status = "PASS" if ok else "FAIL"
    print(f"{label}: {status}")
    print(f"  url: {url}")
    print(f"  bytes: {out_path.stat().st_size}")
    print(f"  expected_sha256: {expected_sha256}")
    print(f"  observed_sha256: {observed}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--latex-url", required=True, help="Hosted LaTeX ZIP URL or attachment download URL.")
    parser.add_argument("--artifact-url", required=True, help="Hosted no-weights artifact ZIP URL or attachment download URL.")
    parser.add_argument("--latex-sha256", required=True, help="Expected SHA256 for conditional_deception_neurips_latex_final.zip.")
    parser.add_argument("--artifact-sha256", required=True, help="Expected SHA256 for conditional_deception_experiment_artifacts_no_weights_final.zip.")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="hosted_artifact_verify_") as tmp:
        tmp_dir = Path(tmp)
        checks = [
            verify_one("latex_zip", args.latex_url, args.latex_sha256, tmp_dir),
            verify_one("artifact_zip", args.artifact_url, args.artifact_sha256, tmp_dir),
        ]
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
