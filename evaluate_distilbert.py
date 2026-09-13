import logging
import sys
from pathlib import Path

import benchmarks.evaluate_quality as eq
from huggingface_hub import snapshot_download

from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MODELS = [
    {
        "repo": "onnx-community/distilbert_finetuned_ai4privacy_v2-ONNX",
        "name": "Distilbert Ai4Privacy v2",
        "onnx_file": "onnx/model_int8.onnx",
    },
    {
        "repo": "onnx-community/piiranha-v1-detect-personal-information-ONNX",
        "name": "Piiranha v1",
        "onnx_file": "onnx/model_int8.onnx",
    },
    {
        "repo": "onnx-community/multilang-pii-ner-ONNX",
        "name": "Multilang PII NER",
        "onnx_file": "onnx/model_int8.onnx",
    },
    {
        "repo": "DataikuNLP/kiji-pii-model-onnx",
        "name": "Kiji PII",
        "onnx_file": "model_quantized.onnx",
    },
]


def main() -> None:
    # Redirect all stdout to a file to capture benchmark results reliably
    with open("benchmark_results_raw.txt", "w", encoding="utf-8") as out_file:
        sys.stdout = out_file
        for model_info in MODELS:
            print("\n=======================================================")
            print(f"Evaluating Model: {model_info['name']}")
            print("=======================================================\n")

            try:
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
                eq.evaluate(50, True, strict_labels=True, split="validation")
            except Exception as e:
                print(f"FAILED: {e}")


if __name__ == "__main__":
    main()
