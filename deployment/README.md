# Hosted Python engine

This directory owns the Lambda HTTP wrapper and container. The website only proxies its responses.

Install the `ml` and `service` extras for local operation. Set `MODEL_DIR` to the verified multilang-pii-ner-ml artifact directory and configure `GATEWAY_SECRET_TOKEN` securely. Run `uvicorn deployment.server:app --port 8080` from the repository root. Missing authentication, missing model files, or mismatched SHA-256 hashes prevent startup; inference failures return 503 without rules-only fallback. Health reports ONNX readiness and the deployed Git revision.

PERSON detection exclusively uses ONNX. Structured identifiers retain Python rules. The service enables constrained BIO decoding and bounded case recovery: at most eight lowercase candidates per model window are individually re-evaluated through ONNX at a minimum raw confidence of 0.9. This fixes the recorded lowercase-name example; it is not a guarantee of complete PII recall. Recovery can add inference latency, especially on long inputs.

Generate pinned container dependencies with:

```sh
uv export --locked --extra ml --extra service --no-dev --no-default-groups --no-emit-project --format requirements-txt --output-file deployment/requirements.txt
```

The build context contains `src/`, this directory's `server.py`, `Dockerfile`, and `requirements.txt`, plus verified `model/config.json`, `model/tokenizer.json`, and `model/model_int8.onnx`. Build for `linux/amd64` with `--provenance=false --build-arg ENGINE_COMMIT=<git-sha>`. The Dockerfile installs exact dependency versions with hash verification; the service verifies model hashes again at startup.

For an existing Lambda deployment, push an immutable commit-tagged ECR image, retain its previous resolved image digest, and update Lambda with the new image digest and its current RevisionId. Preserve the existing role, environment, architecture, timeout, memory, and URL authentication settings. Wait for a successful function update, then verify `/health`, authenticated `/v1/text`, missing-auth rejection, and the website demo. Roll back to the retained digest if verification fails. Never print gateway or registry credentials.

Runtime regression checks:

```sh
pytest --no-cov tests/unit/backends/test_onnx.py
```

These include actual pinned-model inference, identity reuse, possessive handling, negative text controls, entity filtering, authenticated HTTP behavior, explicit inference failure, and missing-model startup rejection. Install the service extra to execute the HTTP checks.

Build offline dependency wheels on a machine with network access using `python -m pip download --require-hashes -r deployment/requirements.txt --dest <build-context>/wheels`. The container's pip installation uses `--no-index` and those verified wheels, so it does not require build-network access. Base and adapter images still require registry access.
