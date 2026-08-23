import csv
import json
from pathlib import Path

from evaluator import evaluate


BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_DIR = BASE_DIR / "evaluation" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def flatten_result(
    model_name: str,
    test_case: str,
    run: int,
    result: dict
) -> dict:

    if not result["syntax_valid"]:
        return {
            "model": model_name,
            "test_case": test_case,
            "run": run,
            "syntax_valid": False,
            "class_f1": 0.0,
            "method_f1": 0.0,
            "attribute_f1": 0.0,
            "call_f1": 0.0,
            "control_flow_score": 0.0,
            "overall_uml_fidelity": 0.0,
            "invented_attributes": 0,
            "missing_calls": 0,
            "extra_calls": 0,
        }

    fidelity = result["uml_fidelity"]

    return {
        "model": model_name,
        "test_case": test_case,
        "run": run,

        "syntax_valid": True,

        "class_f1": fidelity["class_f1"],
        "method_f1": fidelity["method_f1"],
        "attribute_f1": fidelity["attribute_f1"],
        "call_f1": fidelity["call_f1"],
        "control_flow_score":
            fidelity["control_flow_score"],

        "overall_uml_fidelity":
            fidelity["overall_uml_fidelity"],

        "invented_attributes":
            len(result["attributes"]["invented"]),

        "renamed_attributes":
            len(result["attributes"]["renamed"]),

        "missing_calls":
            len(result["calls"]["missing"]),

        "extra_calls":
            len(result["calls"]["extra"]),

        "call_precision":
            result["calls"]["precision"],

        "call_recall":
            result["calls"]["recall"],
    }


def save_json(name: str, result: dict):
    path = RESULTS_DIR / f"{name}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            result,
            f,
            indent=2,
            ensure_ascii=False
        )


def append_csv(row: dict):
    path = RESULTS_DIR / "evaluation_results.csv"

    exists = path.exists()

    with open(
        path,
        "a",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=row.keys()
        )

        if not exists:
            writer.writeheader()

        writer.writerow(row)


def evaluate_candidate(
    model_name: str,
    test_case: str,
    run: int,
    reference_path: Path,
    candidate_path: Path
):
    result = evaluate(
        reference_path,
        candidate_path
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )

    result_name = (
        f"{test_case}_{model_name}_run_{run:02d}"
    )

    save_json(
        result_name,
        result
    )

    row = flatten_result(
        model_name,
        test_case,
        run,
        result
    )

    append_csv(row)


def main():
    reference = (
        BASE_DIR
        / "reference"
        / "user_auth_reference.py"
    )

    parser_output = (
        BASE_DIR
        / "outputs"
        / "user_auth_gen_model_1.py"
    )

    nemotron_output = (
        BASE_DIR
        / "outputs"
        / "ai_generated_output"
        / "nemotron_user_auth_class_sequence.py"
    )

    print("\n=== PARSER ===\n")

    evaluate_candidate(
        model_name="parser",
        test_case="user_auth",
        run=1,
        reference_path=reference,
        candidate_path=parser_output
    )

    print("\n=== NEMOTRON ===\n")

    evaluate_candidate(
        model_name="nemotron",
        test_case="user_auth",
        run=1,
        reference_path=reference,
        candidate_path=nemotron_output
    )


if __name__ == "__main__":
    main()