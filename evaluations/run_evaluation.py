import json
from datetime import date, time
from pathlib import Path
from typing import Any

from app.rag.search import search_knowledge_base
from app.tools.availability import AvailabilityRequest, check_availability


TEST_CASES_PATH = Path("evaluations/test_cases.json")
RESULTS_PATH = Path("evaluations/results/latest.json")


def load_test_cases() -> list[dict[str, Any]]:
    return json.loads(TEST_CASES_PATH.read_text(encoding="utf-8"))


def evaluate_knowledge_case(case: dict[str, Any]) -> dict[str, Any]:
    results = search_knowledge_base(case["question"])
    retrieved_sections = [result["section"] for result in results]

    passed = case["expected_section"] in retrieved_sections

    return {
        "id": case["id"],
        "type": case["type"],
        "passed": passed,
        "expected_section": case["expected_section"],
        "retrieved_sections": retrieved_sections,
    }


def evaluate_availability_case(case: dict[str, Any]) -> dict[str, Any]:
    request = AvailabilityRequest(
        booking_date=date.fromisoformat(case["booking_date"]),
        booking_time=time.fromisoformat(case["booking_time"]),
        guests=case["guests"],
    )

    result = check_availability(request)
    passed = result.available == case["expected_available"]

    return {
        "id": case["id"],
        "type": case["type"],
        "passed": passed,
        "expected_available": case["expected_available"],
        "actual_available": result.available,
        "reason": result.reason,
    }


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    if case["type"] == "knowledge":
        return evaluate_knowledge_case(case)

    if case["type"] == "availability":
        return evaluate_availability_case(case)

    raise ValueError(f"Unsupported test case type: {case['type']}")


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    passed = sum(1 for result in results if result["passed"])

    by_type: dict[str, dict[str, int]] = {}

    for result in results:
        case_type = result["type"]

        if case_type not in by_type:
            by_type[case_type] = {"total": 0, "passed": 0}

        by_type[case_type]["total"] += 1

        if result["passed"]:
            by_type[case_type]["passed"] += 1

    return {
        "total": total,
        "passed": passed,
        "accuracy": passed / total if total else 0,
        "by_type": by_type,
    }


def main() -> None:
    test_cases = load_test_cases()
    results = [evaluate_case(case) for case in test_cases]
    summary = summarize(results)

    report = {
        "summary": summary,
        "results": results,
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
