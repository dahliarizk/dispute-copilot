from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import EvidenceType


class Requirement(BaseModel):
    id: str
    description: str
    accepted_evidence: list[EvidenceType]
    critical: bool


class ReasonCodeRule(BaseModel):
    code: str
    network: str
    title: str
    category: str
    claim_summary: str
    response_deadline_days: int
    requirements: list[Requirement]
    meta: dict[str, Any] = Field(default_factory=dict)
