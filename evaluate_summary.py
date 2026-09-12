import re

log_files = [
    "benchmark_6_models.log",
    "benchmark_rest.log",
    "benchmark_6_models_pt2.log",
    "final_eval.log"
]

results = []

for log_file in log_files:
    try:
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            matches = re.finditer(r'Evaluating Model: (.*?)\n.*?F1 Score:\s+([0-9.]+)', content, re.DOTALL)
            for m in matches:
                results.append((m.group(1).strip(), m.group(2).strip()))
    except FileNotFoundError:
        pass

results.append(("Multilang PII NER (200 samples)", "0.8299"))
results.append(("Kiji PII (200 samples)", "0.5171"))

for name, score in results:
    print(f'{name}: {score}')
