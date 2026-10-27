from app.llm import LLMResult, call
from app.models import ReasonCodeMatch, ReasonCodeRule
from app.prompts._shared.loader import load_prompt


def _format_candidates(rules: list[ReasonCodeRule]) -> str:
    return "\n".join(f"{r.code} — {r.title}: {r.claim_summary}" for r in rules)


def match_reason_code(
    claim_text: str, rules: list[ReasonCodeRule]
) -> LLMResult[ReasonCodeMatch]:
    """Classify a dispute claim into one of the candidate reason codes."""
    prompt = load_prompt(
        "reason_code_matcher",
        {
            "candidate_codes": _format_candidates(rules),
            "claim_text": claim_text,
        },
    )
    return call(prompt, ReasonCodeMatch)
