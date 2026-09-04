# Benchmarks

Two different things are measured here. Detection quality decides whether a release may
ship; timing is reviewed rather than gated.

## Detection quality

```console
uv run --extra ml --with datasets python benchmarks/evaluate_quality.py --samples 1000 --ml
```

Scored against the `ai4privacy/pii-masking-openpii-1.5m` validation split, English rows,
shuffled with a fixed seed.

How a number is produced matters as much as the number:

- Each detection is paired with at most one annotation and each annotation with at most
  one detection, taking the largest overlap first. Precision and recall therefore count
  the same unit on both sides.
- A pair must agree on entity type. Finding an email where the corpus annotated a surname
  is not a hit. `--span-only` scores any overlap regardless of type, which is looser and
  is reported separately when quoted.
- Annotations carrying a label outside `SUPPORTED_LABELS` are not scored. A detection
  landing on one is counted as unscored rather than as a false positive, because the
  package is not claiming to detect that label here and should not be penalised for
  being right about it.
- Develop against the `train` split with `benchmarks/train_eval.py`, which runs the same
  scoring code and prints every miss and false positive. The validation split is for
  measurement only.

Figures published before this scoring was corrected counted true positives per detection
against false negatives per annotation, and ignored entity types entirely. They are not
comparable to figures produced afterwards, and a release comparing against them is
comparing against a different measurement rather than a different implementation.

### `0.17.0` and `0.19.0` rescored

The released code, unchanged, measured under the old and the corrected scoring. 300
validation rows with the ONNX backend enabled.

| Version | Scoring | Precision | Recall | F1 |
| --- | --- | ---: | ---: | ---: |
| `0.17.0` | As previously reported (1000 rows) | 0.9475 | 0.8910 | 0.9184 |
| `0.17.0` | Corrected, `--span-only` | 0.9316 | 0.7529 | 0.8328 |
| `0.17.0` | Corrected, entity types compared | 0.8094 | 0.6536 | 0.7232 |
| `0.19.0` | As previously reported (1000 rows) | 0.9479 | 0.8982 | 0.9224 |
| `0.19.0` | Corrected, `--span-only` | 0.9317 | 0.7542 | 0.8336 |
| `0.19.0` | Corrected, entity types compared | 0.8097 | 0.6549 | 0.7241 |

The gap is the measurement, not a change in behaviour. The 90% threshold that releases
`0.14.0` onwards were gated against was never cleared under scoring that counts one unit
on both sides of the ratio and checks that a detection agrees with the annotation it is
credited for.

The two rows per version also show what a release is worth measuring against. Under
corrected scoring `0.18.0` and `0.19.0` together moved F1 by 0.0009, two additional true
positives out of 1611 annotations, which is within run-to-run noise. The previously
reported figures put the same interval at 0.9184 to 0.9224 and attributed it to a
release. A gate that cannot distinguish a change from noise cannot gate anything, which
is why per-entity counts belong in the published table alongside the aggregate.

## Timing

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
