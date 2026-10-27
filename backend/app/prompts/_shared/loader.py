import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROMPTS_ROOT = Path(__file__).resolve().parent.parent
SHARED_DIR = PROMPTS_ROOT / "_shared"

_SHARED_INCLUDE = re.compile(r"\{\{shared:([a-z0-9_]+)\}\}")


@dataclass(frozen=True)
class LoadedPrompt:
    """A prompt bundle assembled into a ready-to-send payload."""

    bundle: str
    system: str
    user: str
    examples: list[dict[str, Any]]
    model: str
    version: str
    config: dict[str, Any]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _compose_shared(text: str) -> str:
    """Replace {{shared:name}} markers with the contents of _shared/name.md."""

    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        return _read(SHARED_DIR / f"{name}.md").strip()

    return _SHARED_INCLUDE.sub(repl, text)


def _fill_slots(template: str, variables: dict[str, str]) -> str:
    """Replace {key} tokens with provided values, leaving other braces untouched."""
    out = template
    for key, value in variables.items():
        out = out.replace("{" + key + "}", value)
    return out


def load_prompt(bundle: str, variables: dict[str, str] | None = None) -> LoadedPrompt:
    """Read a prompt bundle, compose shared blocks, fill slots, attach config."""
    variables = variables or {}
    bundle_dir = PROMPTS_ROOT / bundle
    if not bundle_dir.is_dir():
        raise FileNotFoundError(f"Prompt bundle not found: {bundle}")

    system = _compose_shared(_read(bundle_dir / "system.md"))
    user = _fill_slots(_read(bundle_dir / "template.md"), variables)

    examples_path = bundle_dir / "examples.json"
    examples: list[dict[str, Any]] = (
        json.loads(_read(examples_path)) if examples_path.exists() else []
    )
    config: dict[str, Any] = json.loads(_read(bundle_dir / "config.json"))

    return LoadedPrompt(
        bundle=bundle,
        system=system,
        user=user,
        examples=examples,
        model=str(config["model"]),
        version=str(config["version"]),
        config=config,
    )
