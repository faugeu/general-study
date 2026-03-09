"""
Run the AHP-TOPSIS pipeline and save outputs to `results/`.

Usage:
  python src/scripts/run_ahp_pipeline.py --payload-file data/ahp_payload_example.json
"""

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from ahp_topsis import quick_recommend, print_final_summary
from ahp_topsis.default_payload import load_payload_from_dict


def run_pipeline(payload, results_dir: Path):
    results_dir = Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    result = quick_recommend(payload)

    result["final_ranking"].to_csv(
        results_dir / "ahp_topsis_ranking.csv", index=False
    )
    result["consistency_report"].to_csv(
        results_dir / "ahp_topsis_consistency.csv", index=False
    )
    result["global_weights_df"].to_csv(
        results_dir / "ahp_topsis_global_weights.csv", index=False
    )

    summary = {
        "top_alternative": result["top_alternative"],
        "closeness_score": float(
            result["final_ranking"].iloc[0]["Closeness"]
        ),
    }
    with open(results_dir / "ahp_topsis_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Run the AHP-TOPSIS pipeline and write results."
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default="results",
        help="Directory to write CSV and JSON outputs (default: results)",
    )
    parser.add_argument(
        "--payload-file",
        type=str,
        required=True,
        help="JSON file with criteria/subcriteria comparisons (see data/ahp_payload_example.json)",
    )
    args = parser.parse_args()

    path = Path(args.payload_file)
    if not path.is_file():
        raise SystemExit(f"Payload file not found: {path}")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    payload = load_payload_from_dict(data)
    results_dir = Path(args.results_dir)

    result = run_pipeline(payload, results_dir)
    print_final_summary(result)
    print(f"\nResults written to: {results_dir.absolute()}")


if __name__ == "__main__":
    main()
