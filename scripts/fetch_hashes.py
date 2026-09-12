import hashlib
import urllib.request

BASE_URL = "https://huggingface.co/onnx-community/llama-ai4privacy-multilingual-categorical-anonymiser-openpii-ONNX/resolve/main/"
FILES = {
    "config.json": "config.json",
    "tokenizer.json": "tokenizer.json",
    "model_int8.onnx": "onnx/model_int8.onnx",
}

for name, path in FILES.items():
    url = BASE_URL + path

    if not url.startswith(("http://", "https://")):
        raise ValueError(f"Invalid URL scheme: {url}")

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})  # noqa: S310
    with urllib.request.urlopen(req) as response:  # noqa: S310
        content = response.read()
        digest = hashlib.sha256(content).hexdigest()
        print(f"{name}: {digest}")
