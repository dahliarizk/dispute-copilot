from pydantic import BaseModel, Field

from app.models.enums import AdvocateParty, Decision, Difficulty, PointStatus
from app.models.inputs import Dispute, DisputeInput, Evidence


class PointLabel(BaseModel):
    status: PointStatus
    satisfied_by: list[str] = Field(default_factory=list)


class CaseLabels(BaseModel):
    reason_code: str
    contested_points: dict[str, PointLabel]
    decision: Decision
    notes: str = ""


class EvalCase(BaseModel):
    case_id: str
    difficulty: Difficulty
    advocate_for: AdvocateParty
    dispute: Dispute
    evidence: list[Evidence]
    labels: CaseLabels

    def to_input(self) -> DisputeInput:
        return DisputeInput(
            advocate_for=self.advocate_for,
            dispute=self.dispute,
            evidence=self.evidence,
        )
