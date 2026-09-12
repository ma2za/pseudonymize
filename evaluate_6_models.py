import argparse
import sys
import logging
from pathlib import Path

# Add src to sys.path so we can import pseudonymize
import pseudonymize

from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend
from pseudonymize.engine import Pseudonymizer
import benchmarks.evaluate_quality as eq

from huggingface_hub import snapshot_download

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("evaluate_6_models")

MODELS = [
    # 2. Distilbert Ai4privacy
    {
        "repo": "onnx-community/distilbert_finetuned_ai4privacy_v2-ONNX",
        "name": "Distilbert Ai4Privacy v2",
        "onnx_file": "onnx/model_int8.onnx"
    },
    # 3. Piiranha (highly requested model)
    {
        "repo": "onnx-community/piiranha-v1-detect-personal-information-ONNX",
        "name": "Piiranha v1",
        "onnx_file": "onnx/model_int8.onnx"
    },
    # 4. Multilang PII NER
    {
        "repo": "onnx-community/multilang-pii-ner-ONNX",
        "name": "Multilang PII NER",
        "onnx_file": "onnx/model_int8.onnx"
    },
]

original_evaluate = eq.evaluate

def main() -> None:
    samples = 1000
    
    for model_info in MODELS:
        print(f"\n=======================================================")
        print(f"Evaluating Model: {model_info['name']} ({model_info['repo']})")
        print(f"=======================================================\n")
        
        try:
            cache_dir = snapshot_download(
                model_info['repo'], 
                allow_patterns=["config.json", "tokenizer.json", model_info['onnx_file']]
            )
            
            onnx_path = Path(cache_dir) / model_info['onnx_file']
            tokenizer_path = Path(cache_dir) / "tokenizer.json"
            config_path = Path(cache_dir) / "config.json"
            
            if not onnx_path.exists() or not tokenizer_path.exists():
                print(f"Skipping {model_info['name']} due to missing files (onnx: {onnx_path.exists()}, tokenizer: {tokenizer_path.exists()})")
                continue

            def mock_backend(**kwargs):
                return LocalONNXPIIBackend(
                    model_path=onnx_path,
                    tokenizer_path=tokenizer_path,
                    config_path=config_path if config_path.exists() else None
                )
                
            # Monkeypatch the backend creation inside evaluate_quality module
            eq.LocalONNXPIIBackend = mock_backend
            
            original_evaluate(samples, True, strict_labels=True, split="validation")
            
        except Exception as e:
            print(f"Error evaluating {model_info['name']}: {e}")
            import traceback
            traceback.print_exc()
            
if __name__ == "__main__":
    main()
