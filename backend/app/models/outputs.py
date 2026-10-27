from pydantic import BaseModel, Field

from app.models.enums import Decision, PointStatus


class ReasonCodeMatch(BaseModel):
    matched_code: str
    confidence: float
    reasoning: str | None = None


class RequirementResult(BaseModel):
    requirement_id: str
    status: PointStatus
    satisfied_by: list[str] = Field(default_factory=list)


class FaithfulnessResult(BaseModel):
    passed: bool
    unsupported_claims: list[str] = Field(default_factory=list)


class Representment(BaseModel):
    reason_code: str
    confidence: float
    recommendation: Decision
    requirement_results: list[RequirementResult]
    draft: str
    unsupported_claims: list[str] = Field(default_factory=list)
