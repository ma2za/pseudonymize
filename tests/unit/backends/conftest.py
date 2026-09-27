import hashlib
import urllib.request
from pathlib import Path

import pytest

CACHE_DIR = Path(".cache/pseudonymize-tests/models/multilang-pii-ner-ml")
MODEL_URL_BASE = "https://huggingface.co/onnx-community/multilang-pii-ner-ONNX/resolve/main/"
MODEL_FILES = {
    "config.json": (
        "config.json",
        "3503fb27021640b315b1e7636933f7df9c209746251cae4975bdef46be4e8158",
    ),
    "tokenizer.json": (
        "tokenizer.json",
        "8373f9cd3d27591e1924426bcc1c8799bc5a9affc4fc857982c5d66668dd1f41",
    ),
    "model_int8.onnx": (
        "onnx/model_int8.onnx",
        "1d02f3829ad90d95dea5e64d35f5528f96d7b223c1e056a96075c6229a484356",
    ),
}


def download_file(url: str, dest: Path, sha256: str) -> None:
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})  # noqa: S310
        with urllib.request.urlopen(req) as response, open(dest, "wb") as f:  # noqa: S310
            f.write(response.read())
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    if digest != sha256:
        dest.unlink()
        raise RuntimeError(f"checksum mismatch for {dest.name}: {digest}")


@pytest.fixture(scope="session")
def onnx_artifacts() -> tuple[Path, Path, Path]:
    paths = []
    for local_name, (remote_path, sha256) in MODEL_FILES.items():
        dest = CACHE_DIR / local_name
        download_file(MODEL_URL_BASE + remote_path, dest, sha256)
        paths.append(dest)
    # Returns (config, tokenizer, model)
    return (paths[0], paths[1], paths[2])
