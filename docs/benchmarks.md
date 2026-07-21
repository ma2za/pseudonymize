# Benchmarks

Run `uv run pytest benchmarks --benchmark-only`. Record CPU, operating system, Python version,
input construction, rounds, package revision, wheel size, import time, latency, and memory before
publishing results. Timing regressions are reviewed rather than gated on noisy shared runners.
