import json
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

# Make the backend root importable when this script is run from a subdirectory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models import EvalCase  # noqa: E402
from app.pipeline.reason_code import match_reason_code  # noqa: E402
from app.prompts._shared.loader import load_prompt  # noqa: E402
from app.rules_loader import load_rules  # noqa: E402

CASES_DIR = Path(__file__).resolve().parent / "cases"
RESULTS_DIR = Path(__file__).resolve().parent / "results"


def load_cases() -> list[EvalCase]:
    return [
        EvalCase.model_validate_json(path.read_text(encoding="utf-8"))
        for path in sorted(CASES_DIR.glob("*.json"))
    ]


def main() -> None:
    rules = load_rules()
    cases = load_cases()
    version = load_prompt("reason_code_matcher").version

    rows: list[dict[str, object]] = []
    correct = 0
    in_tokens = 0
    out_tokens = 0

    for case in cases:
        result = match_reason_code(case.dispute.claim_text, rules)
        pred = result.output.matched_code
        gold = case.labels.reason_code
        ok = pred == gold
        correct += int(ok)
        in_tokens += result.input_tokens
        out_tokens += result.output_tokens
        rows.append(
            {
                "case_id": case.case_id,
                "difficulty": case.difficulty.value,
                "gold": gold,
                "pred": pred,
                "confidence": result.output.confidence,
                "correct": ok,
            }
        )
        mark = "OK" if ok else "XX"
        print(
            f"[{mark}] {case.case_id:30} gold={gold:5} pred={pred:5} "
            f"conf={result.output.confidence:.2f}"
        )

    n = len(cases)
    acc = correct / n if n else 0.0

    print()
    print(f"Reason-code accuracy: {correct}/{n} = {acc:.1%}")

    by_diff: dict[str, list[bool]] = defaultdict(list)
    for row in rows:
        by_diff[str(row["difficulty"])].append(bool(row["correct"]))
    for diff in ("clear", "medium", "hard"):
        bucket = by_diff.get(diff, [])
        if bucket:
            print(f"  {diff:7} {sum(bucket)}/{len(bucket)}")

    print(f"Tokens: {in_tokens} in / {out_tokens} out")

    RESULTS_DIR.mkdir(exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    out_path = RESULTS_DIR / f"reason_code_matcher_v{version}_{stamp}.json"
    out_path.write_text(
        json.dumps(
            {
                "prompt": "reason_code_matcher",
                "version": version,
                "accuracy": acc,
                "correct": correct,
                "total": n,
                "input_tokens": in_tokens,
                "output_tokens": out_tokens,
                "rows": rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
