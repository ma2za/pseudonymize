# Benchmarks

Run `uv run pytest benchmarks --benchmark-only`. Record CPU, operating system, Python version,
input construction, rounds, package revision, wheel size, import time, latency, and memory before
publishing results. Timing regressions are reviewed rather than gated on noisy shared runners.

## `0.1.0b1` reference

Measured on the `0.1.0b1` release candidate with Python 3.14.3, Windows 11 Home 10.0.26200,
an Intel Core Ultra 7 155H (16 cores, 22 logical processors), and 31.5 GiB RAM. The engine input
repeats the committed synthetic message corpus to the named size and uses deterministic mode.
Pytest-benchmark ran at least 20 rounds with garbage collection disabled.

| Measurement | Result |
| --- | ---: |
| 4 KiB processing, median | 8.05 ms |
| 4 KiB processing, mean | 7.73 ms |
| 64 KiB processing, median | 282.49 ms |
| 64 KiB processing, mean | 269.77 ms |
| Import, median of 10 `-X importtime` processes | 78.93 ms |
| Import peak traced allocation | 4.49 MiB |
| 4 KiB processing peak traced allocation | 217.18 KiB |
| 64 KiB processing peak traced allocation | 2.48 MiB |
| Wheel size | 40,222 bytes |

Peak allocations use `tracemalloc` in a fresh process with the built wheel installed. The current
aspirational latency and import budgets are not met on this Windows reference machine; they remain
optimization targets rather than release gates. The wheel remains below its enforced 250 KiB
limit.

## `0.1.0rc1` validation

The release candidate was remeasured on the same Windows machine and Python 3.14.3 environment.
There are no core implementation changes from `0.1.0b1`.

| Measurement | Result |
| --- | ---: |
| 4 KiB processing, median | 7.72 ms |
| 4 KiB processing, mean | 7.57 ms |
| 64 KiB processing, median | 336.78 ms |
| 64 KiB processing, mean | 332.13 ms |
| Isolated import with allocation tracing, two runs | 234.90–446.66 ms |
| Import peak traced allocation | 1.92 MiB |
| Wheel size | 40,235 bytes |

The instrumented import range is not comparable to the beta's uninstrumented import-time sample.
Its variance and the 64 KiB variance reinforce the decision to review timing without making it a
release gate.
