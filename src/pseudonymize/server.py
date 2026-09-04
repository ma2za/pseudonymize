from typing import Any, cast

from pseudonymize.engine import Pseudonymizer

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field

    app = FastAPI(
        title="Pseudonymize DLP API",
        description="Local-first PII pseudonymization microservice.",
        version="0.27.0",
    )

    class PseudonymizeRequest(BaseModel):  # type: ignore[misc]
        text: str = Field(..., description="The text to analyze and pseudonymize.")

    class ReplacementResponse(BaseModel):  # type: ignore[misc]
        entity_type: str
        start: int
        end: int
        token: str
        confidence: float
        detector: str

    class PseudonymizeResponse(BaseModel):  # type: ignore[misc]
        text: str
        replacements: list[ReplacementResponse]

    # Global engine for performance
    _engine = Pseudonymizer()

    @app.post("/pseudonymize", response_model=PseudonymizeResponse)  # type: ignore[untyped-decorator]
    def pseudonymize_endpoint(req: PseudonymizeRequest) -> Any:
        try:
            result = _engine.process(req.text)

            reps = [
                ReplacementResponse(
                    entity_type=r.detection.entity_type.value,
                    start=r.output_start,
                    end=r.output_end,
                    token=r.token,
                    confidence=r.detection.confidence,
                    detector=r.detection.detector,
                )
                for r in result.replacements
            ]

            return PseudonymizeResponse(text=result.text, replacements=reps)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

except ImportError:
    app = cast(Any, None)
