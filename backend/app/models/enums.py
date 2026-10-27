from enum import StrEnum


class AdvocateParty(StrEnum):
    CONSUMER = "consumer"
    MERCHANT = "merchant"


class EvidenceType(StrEnum):
    EMAIL = "email"
    RECEIPT = "receipt"
    LISTING_SCREENSHOT = "listing_screenshot"
    TRACKING = "tracking"
    POLICY = "policy"
    CHAT = "chat"
    TRANSACTION = "transaction"


class PointStatus(StrEnum):
    CONSUMER_SUPPORTED = "consumer_supported"
    MERCHANT_SUPPORTED = "merchant_supported"
    CONTESTED = "contested"
    GAP = "gap"
    NOT_APPLICABLE = "not_applicable"


class Decision(StrEnum):
    FIGHT = "fight"
    INSUFFICIENT = "insufficient"
    ACCEPT = "accept"


class Difficulty(StrEnum):
    CLEAR = "clear"
    MEDIUM = "medium"
    HARD = "hard"
