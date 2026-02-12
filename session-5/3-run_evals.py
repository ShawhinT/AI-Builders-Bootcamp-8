# Run all code-based evaluations against a request_response.csv

import csv
import glob
import os
from evals import check_no_banned_phrases, check_no_tricolons, check_em_dash_count

# --- Configuration ---
# Set to a specific path, or "all" to run against every dataset in data/
data_path = "all"
# data_path = "data/2025-11-03_prompt-v2/request_response.csv"
# data_path = "data/2026-02-12_prompt-v1/request_response.csv"
# data_path = "data/2026-02-12_prompt-v3/request_response.csv"


# --- Define evals to run ---
EVALS = [
    ("no_banned_phrases", check_no_banned_phrases),
    ("no_tricolons", check_no_tricolons),
    ("em_dash_count", check_em_dash_count),
]


def run_evals(data_path: str):
    """Run all evals against a single request_response.csv and save results."""
    # --- Load data ---
    with open(data_path, "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # --- Run evals ---
    results = []
    for i, row in enumerate(rows):
        llm_output = row["LLM Output"]
        result = {"index": i}
        for eval_name, eval_fn in EVALS:
            eval_result = eval_fn(llm_output)
            result[eval_name] = eval_result["passed"]
            result[f"{eval_name}_details"] = eval_result["details"]
        results.append(result)

    # --- Save results CSV ---
    output_dir = os.path.dirname(data_path)
    output_path = os.path.join(output_dir, "request_response-evals.csv")

    fieldnames = ["index"]
    for eval_name, _ in EVALS:
        fieldnames.append(eval_name)
        fieldnames.append(f"{eval_name}_details")

    with open(output_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # --- Print summary ---
    print(f"\nEval Results: {data_path}")
    print("=" * 64)

    total_passed = 0
    total_checks = 0
    for eval_name, _ in EVALS:
        passed = sum(1 for r in results if r[eval_name])
        total = len(results)
        pct = (passed / total * 100) if total > 0 else 0
        print(f"{eval_name:<28} {passed}/{total} passed ({pct:.1f}%)")
        total_passed += passed
        total_checks += total

    print("=" * 64)
    pct_overall = (total_passed / total_checks * 100) if total_checks > 0 else 0
    print(f"{'Overall':<28} {total_passed}/{total_checks} checks passed ({pct_overall:.1f}%)")
    print(f"Results saved to: {output_path}")


# --- Main ---
if data_path == "all":
    paths = sorted(glob.glob("data/*/request_response.csv"))
    print(f"Running evals on {len(paths)} datasets...")
    for p in paths:
        run_evals(p)
else:
    run_evals(data_path)
