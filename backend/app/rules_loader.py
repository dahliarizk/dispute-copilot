from pathlib import Path

from app.models import ReasonCodeRule

RULES_DIR = Path(__file__).resolve().parent / "rules"


def load_rules() -> list[ReasonCodeRule]:
    """Load all reason-code rule files from app/rules/."""
    return [
        ReasonCodeRule.model_validate_json(path.read_text(encoding="utf-8"))
        for path in sorted(RULES_DIR.glob("*.json"))
    ]
