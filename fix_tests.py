import os
import re
import json
import base64
from pathlib import Path

MAPPING = {
    "PERSON": "PER",
    "ORGANIZATION": "ORG",
    "LOCATION": "LOC",
    "EMAIL": "EML",
    "PHONE": "PHN",
    "IP_ADDRESS": "IP",
    "IBAN": "IBN",
    "PAYMENT_CARD": "PAN",
    "NATIONAL_ID": "NID",
    "TAX_ID": "TID",
    "URL_CREDENTIAL": "CRE",
    "SECRET": "SEC",
}


def replace_placeholders(text):
    for old, new in MAPPING.items():
        # Replace <OLD_X> or <OLD>
        text = re.sub(rf"<({old})(_[A-Z0-9]+|)>", rf"<{new}\2>", text)
        # Replace [REDACTED_OLD]
        text = re.sub(rf"\[REDACTED_{old}\]", rf"[REDACTED_{new}]", text)
    return text


def process_python_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = replace_placeholders(content)

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


def process_corpus(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    changed = False
    for item in data:
        if "expected_base64" in item:
            expected = base64.b64decode(item["expected_base64"]).decode("utf-8")
            new_expected = replace_placeholders(expected)
            if new_expected != expected:
                item["expected_base64"] = base64.b64encode(new_expected.encode("utf-8")).decode(
                    "utf-8"
                )
                changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    return False


if __name__ == "__main__":
    test_dir = Path("tests")
    py_files_changed = 0
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith(".py"):
                if process_python_file(os.path.join(root, file)):
                    py_files_changed += 1

    print(f"Changed {py_files_changed} Python files")

    corpus_path = test_dir / "corpus" / "files.json"
    if corpus_path.exists():
        if process_corpus(corpus_path):
            print("Changed files.json")
