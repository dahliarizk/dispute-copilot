# reason_code_matcher — changelog

## v0.3.0 (2026-10-25)
- Adapted to anthropic SDK 2.3.0. Structured output now comes from the Pydantic
  output model (ReasonCodeMatch) via messages.parse(); schema.json is retired
  (schema is derived from the model). Dropped temperature (no longer an SDK
  parameter); determinism is handled by the model. matched_code validation
  against the loaded rules moves into the pipeline step.

## v0.2.0 (2026-10-25)
- Refined system prompt (reframe, 13.3-vs-13.5 disambiguation, confidence
  calibration); runtime code definitions; claim-text-only; fresh examples.

## v0.1.0 (2026-10-25)
- Initial bundle scaffold.
