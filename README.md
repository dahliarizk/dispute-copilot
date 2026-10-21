# Dispute Copilot

An AI copilot that helps the under-resourced side of a card chargeback —
an individual consumer or a small business — build the strongest *honest*
case, by matching the dispute to the right reason code, assembling the
evidence each requirement needs, and drafting a submission-ready response.

## Vertical slice — reason codes (Visa)

The first build target is a few common Visa reason codes, working end to end,
before widening to full coverage. Chosen for the slice:

| Code | Meaning | Primary evidence |
| --- | --- | --- |
| 13.1 | Merchandise / services not received | Delivery / tracking, fulfillment dates |
| 13.2 | Cancelled recurring transaction | Cancellation record, dates |
| 13.3 | Not as described / defective | Listing vs. what was received |
| 13.5 | Misrepresentation | Agreed sales terms vs. what was sold |

A consumer-focused set of Category 13 consumer-dispute codes. 13.5 anchors the
motivating case (deceptive "official" ticket sellers). Fraud codes (e.g. 10.4)
and processing-error codes (e.g. 12.6) are later widening steps. Requirement
details for each code are authored as JSON in `backend/app/rules/`, verified
against current Visa documentation.

## Structure

- `backend/` — FastAPI service (Python, uv)
- `frontend/` — Next.js app (added later)
