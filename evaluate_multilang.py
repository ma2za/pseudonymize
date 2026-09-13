import logging
from pathlib import Path

import benchmarks.evaluate_quality as eq
from huggingface_hub import snapshot_download

from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MODELS = [
    {
        "repo": "DataikuNLP/kiji-pii-model-onnx",
        "name": "Kiji PII",
        "onnx_file": "model_quantized.onnx",
    },
]


def main() -> None:
    for model_info in MODELS:
        print(f"Evaluating: {model_info['name']}")
        cache_dir = snapshot_download(
            model_info["repo"],
            allow_patterns=["config.json", "tokenizer.json", model_info["onnx_file"]],
        )
        onnx_path = Path(cache_dir) / model_info["onnx_file"]
        tokenizer_path = Path(cache_dir) / "tokenizer.json"
        config_path = Path(cache_dir) / "config.json"

        eq.LocalONNXPIIBackend = lambda **kwargs: LocalONNXPIIBackend(
            model_path=onnx_path,
            tokenizer_path=tokenizer_path,
            config_path=config_path if config_path.exists() else None,
        )
        eq.evaluate(200, True, strict_labels=True, split="validation")


if __name__ == "__main__":
    main()
