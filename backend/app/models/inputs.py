from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import AdvocateParty, EvidenceType


class Amount(BaseModel):
    value: Decimal
    currency: str


class Evidence(BaseModel):
    evidence_id: str
    type: EvidenceType
    source: str
    timestamp: datetime
    text: str
    blob_ref: str | None = None
    extracted: dict[str, Any] = Field(default_factory=dict)


class Dispute(BaseModel):
    network: str
    amount: Amount
    transaction_date: date
    filed_date: date
    claim_text: str


class DisputeInput(BaseModel):
    advocate_for: AdvocateParty
    dispute: Dispute
    evidence: list[Evidence]
