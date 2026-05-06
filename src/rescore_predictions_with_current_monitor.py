import argparse
import json
from pathlib import Path

from monitors import score_all


def rescore_file(path: Path) -> dict:
    rows = []
    changed = 0
    total = 0
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            total += 1
            scores = score_all(row, row.get("generated_text", ""))
            before = {k: row.get(k) for k in scores}
            row.update(scores)
            after = {k: row.get(k) for k in scores}
            if before != after:
                changed += 1
            rows.append(row)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return {"path": str(path), "rows": total, "changed_rows": changed}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+", required=True)
    ap.add_argument("--out-json", required=True)
    args = ap.parse_args()

    reports = []
    for d in args.dirs:
        root = Path(d)
        for path in sorted(root.glob("*.jsonl")):
            reports.append(rescore_file(path))

    out = {
        "description": "Prediction rows rescored with current task-aware monitor implementation.",
        "dirs": args.dirs,
        "files": reports,
        "total_rows": sum(r["rows"] for r in reports),
        "total_changed_rows": sum(r["changed_rows"] for r in reports),
    }
    out_path = Path(args.out_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
