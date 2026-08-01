# Benchmarks

```console
uv run pytest benchmarks --benchmark-only
```

Publish results only with CPU model, RAM, operating system, Python version, package revision,
input sizes, rounds, wheel size, import time, and peak memory. The dataset is synthetic. Target
budgets are a wheel below 250 KiB, import below 40 ms, 4 KiB warm processing below 2 ms, and 64 KiB
below 20 ms on the named reference machine. Timing budgets are optimization targets, not CI gates.
Current measurements are published in `docs/benchmarks.md` even when a target is not met.
