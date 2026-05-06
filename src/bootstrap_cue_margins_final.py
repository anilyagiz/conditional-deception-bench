import json
from pathlib import Path

import numpy as np


OUT = Path("experiments/results")
PAIRS = [
    (
        "conditional_deception_v2_4_semantic",
        "cue_memorization_v2_4",
        Path("artifacts/predictions_v2_4"),
    ),
    (
        "conditional_deception_2b_semantic",
        "cue_memorization_2b",
        Path("artifacts/predictions_2b"),
    ),
    (
        "conditional_deception_v2_4_semantic",
        "fixed_trigger_v2_4",
        Path("artifacts/predictions_v2_4"),
    ),
    (
        "conditional_deception_2b_semantic",
        "fixed_trigger_2b",
        Path("artifacts/predictions_2b"),
    ),
]


def read_map(org, root):
    path = root / f"{org}_test_ood.jsonl"
    rows = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            rows[row["id"]] = row
    return rows


def delta(rows):
    weak = [r for r in rows if r["oversight_regime"] == "weak"]
    strong = [r for r in rows if r["oversight_regime"] == "strong"]
    wr = sum(r["predicted_defect"] for r in weak) / len(weak)
    sr = sum(r["predicted_defect"] for r in strong) / len(strong)
    return wr - sr


def paired_margin(a_rows, b_rows, ids):
    return delta([a_rows[i] for i in ids]) - delta([b_rows[i] for i in ids])


def main(seed=7, n_boot=10000):
    rng = np.random.default_rng(seed)
    out = []
    for cond, ctrl, root in PAIRS:
        a = read_map(cond, root)
        b = read_map(ctrl, root)
        ids = sorted(set(a) & set(b))
        observed = paired_margin(a, b, ids)
        boots = []
        ids_arr = np.array(ids)
        for _ in range(n_boot):
            sample = rng.choice(ids_arr, size=len(ids_arr), replace=True)
            boots.append(paired_margin(a, b, sample))
        boots = np.array(boots)
        out.append(
            {
                "comparison": f"{cond} - {ctrl}",
                "split": "test_ood",
                "n_paired_rows": len(ids),
                "observed_delta_margin": float(observed),
                "bootstrap_low": float(np.quantile(boots, 0.025)),
                "bootstrap_high": float(np.quantile(boots, 0.975)),
                "bootstrap_p_margin_le_0": float(np.mean(boots <= 0)),
                "seed": seed,
                "n_boot": n_boot,
            }
        )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "cue_control_margin_bootstrap.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    with (OUT / "cue_control_margin_bootstrap.csv").open("w", encoding="utf-8", newline="\n") as f:
        cols = list(out[0].keys())
        f.write(",".join(cols) + "\n")
        for row in out:
            f.write(",".join(str(row[c]) for c in cols) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
