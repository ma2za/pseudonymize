import hashlib
import hmac
import json
import math
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Literal

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from pseudonymize.backends import RulesBackend
from pseudonymize.detectors.gazetteer import GazetteerDetector
from pseudonymize.detectors.location import LocationDetector
from pseudonymize.detectors.organization import OrganizationDetector
from pseudonymize.detectors.registry import DEFAULT_DETECTORS
from pseudonymize.engine import ProcessingScope, Pseudonymizer
from pseudonymize.exceptions import BackendExecutionError
from pseudonymize.policy import Policy
from pseudonymize.result import EntityType, Result

_ML_BACKEND: Any = None
_MODEL_HASHES = {
    "config.json": "3503fb27021640b315b1e7636933f7df9c209746251cae4975bdef46be4e8158",
    "tokenizer.json": "8373f9cd3d27591e1924426bcc1c8799bc5a9affc4fc857982c5d66668dd1f41",
    "model_int8.onnx": "1d02f3829ad90d95dea5e64d35f5528f96d7b223c1e056a96075c6229a484356",
}


def get_ml_backend() -> Any:
    global _ML_BACKEND
    if _ML_BACKEND is not None:
        return _ML_BACKEND
    from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend

    model_dir = Path(os.environ.get("MODEL_DIR", "/var/task/model"))
    for filename, expected in _MODEL_HASHES.items():
        if hashlib.sha256((model_dir / filename).read_bytes()).hexdigest() != expected:
            raise RuntimeError("ONNX artifact integrity verification failed")
    _ML_BACKEND = LocalONNXPIIBackend(
        model_path=model_dir / "model_int8.onnx",
        tokenizer_path=model_dir / "tokenizer.json",
        config_path=model_dir / "config.json",
        decoder_mode="constrained_bio",
        case_recovery_threshold=0.9,
    )
    return _ML_BACKEND


def create_pseudonymizer(policy: Policy) -> Pseudonymizer:
    # Structured identifiers retain engine rules; names are exclusively ONNX.
    detectors = tuple(
        detector
        for detector in DEFAULT_DETECTORS
        if not isinstance(detector, (GazetteerDetector, LocationDetector, OrganizationDetector))
    )
    return Pseudonymizer(
        policy=policy,
        backends=(RulesBackend(detectors=detectors), get_ml_backend()),
        enable_coreference=False,
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    if not os.environ.get("GATEWAY_SECRET_TOKEN", "").strip():
        raise RuntimeError("Gateway authentication must be configured")
    get_ml_backend()
    yield


app = FastAPI(
    title="Pseudonymize DLP Core API",
    description="High-performance PII/PHI detection and pseudonymization microservice with ML NER",
    version="1.37.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_gateway_auth(request: Request) -> None:
    expected_secret = os.environ.get("GATEWAY_SECRET_TOKEN", "").strip()
    if not expected_secret:
        raise HTTPException(status_code=503, detail="Gateway authentication unavailable")

    provided_secret = request.headers.get("x-internal-gateway-key")
    if not provided_secret:
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            provided_secret = auth_header[7:].strip()
        else:
            provided_secret = auth_header.strip()

    if not provided_secret or not hmac.compare_digest(provided_secret, expected_secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Invalid or missing gateway secret key",
        )


class TextRequest(BaseModel):
    require_ml: Literal[True] = True
    text: str = Field(..., description="The raw input text to pseudonymize")
    policy: str | dict[str, Any] | None = Field(None, description="Policy preset or configuration")
    detect: list[str] | None = Field(None, description="Optional entity types filter list")


class DataRequest(BaseModel):
    require_ml: Literal[True] = True
    data: Any = Field(
        ..., description="The JSON data structure (dict, list, or primitive) to pseudonymize"
    )
    policy: str | dict[str, Any] | None = Field(None, description="Policy preset or configuration")
    detect: list[str] | None = Field(None, description="Optional entity types filter list")


def resolve_policy(
    policy_input: str | dict[str, Any] | None, detect_input: list[str] | None
) -> Policy:
    # 1. Base policy selection
    if isinstance(policy_input, str):
        normalized = policy_input.lower().strip()
        if normalized == "strict":
            base_policy = Policy.strict()
        elif normalized == "financial":
            base_policy = Policy.financial()
        elif normalized == "llm":
            base_policy = Policy.llm()
        else:
            base_policy = Policy.default()
    elif isinstance(policy_input, dict):
        try:
            min_conf = float(policy_input.get("minimum_confidence", 0.8))
            base_policy = Policy(minimum_confidence=min_conf)
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail="Invalid confidence policy") from None
    else:
        base_policy = Policy.default()

    # 2. Filter entity types if detect list is supplied
    if detect_input:
        target_types = set()
        for name in detect_input:
            upper_name = name.strip().upper()
            if hasattr(EntityType, upper_name):
                target_types.add(getattr(EntityType, upper_name))
        if target_types:
            return Policy(
                entity_types=frozenset(target_types),
                minimum_confidence=base_policy.minimum_confidence,
                schema_preserving=base_policy.schema_preserving,
            )

    return base_policy


def extract_entities(result: Result) -> list[dict[str, Any]]:
    entities: list[dict[str, Any]] = []
    for r in result.replacements:
        det = r.detection
        ent_type = (
            det.entity_type.value if hasattr(det.entity_type, "value") else str(det.entity_type)
        )
        entities.append(
            {
                "entity_type": ent_type,
                "start": det.start,
                "end": det.end,
                "confidence": det.confidence,
                "detector": det.detector,
                "token": r.token,
            }
        )
    return entities


def process_recursive_data(
    val: Any,
    pseudonymizer: ProcessingScope,
    collected_entities: list[dict[str, Any]],
) -> Any:
    if isinstance(val, str):
        res = pseudonymizer.process(val)
        collected_entities.extend(extract_entities(res))
        return res.text
    if isinstance(val, dict):
        return {
            k: process_recursive_data(v, pseudonymizer, collected_entities) for k, v in val.items()
        }
    if isinstance(val, list):
        return [process_recursive_data(item, pseudonymizer, collected_entities) for item in val]
    return val


@app.get("/")
@app.get("/health")
def health_check() -> dict[str, Any]:
    ml_active = get_ml_backend() is not None
    return {
        "status": "healthy",
        "service": "pseudonymize-core",
        "version": "1.37.0",
        "revision": os.environ.get("ENGINE_COMMIT", "development"),
        "onnx_required": True,
        "ml_backend": "active" if ml_active else "disabled",
    }


@app.post("/v1/text", dependencies=[Depends(verify_gateway_auth)])
def pseudonymize_text_endpoint(req: TextRequest) -> dict[str, Any]:
    policy = resolve_policy(req.policy, req.detect)
    pseudonymizer = create_pseudonymizer(policy)
    try:
        result = pseudonymizer.process(req.text)
    except BackendExecutionError:
        raise HTTPException(status_code=503, detail="ONNX inference unavailable") from None
    entities = extract_entities(result)
    tokens_processed = max(1, math.ceil(len(req.text) / 4))

    return {
        "text": result.text,
        "entities": entities,
        "tokensProcessed": tokens_processed,
    }


@app.post("/v1/data", dependencies=[Depends(verify_gateway_auth)])
def pseudonymize_data_endpoint(req: DataRequest) -> dict[str, Any]:
    policy = resolve_policy(req.policy, req.detect)
    pseudonymizer = create_pseudonymizer(policy)
    collected_entities: list[dict[str, Any]] = []
    try:
        processed_data = process_recursive_data(
            req.data, pseudonymizer.new_scope(), collected_entities
        )
    except BackendExecutionError:
        raise HTTPException(status_code=503, detail="ONNX inference unavailable") from None

    raw_json_str = json.dumps(req.data)
    tokens_processed = max(1, math.ceil(len(raw_json_str) / 4))

    return {
        "data": processed_data,
        "entities": collected_entities,
        "tokensProcessed": tokens_processed,
    }
