"""Run the quality benchmark against the train split, with per-error detail.

The integrity notice requires heuristics to be developed against the train split
and only measured against validation. This is that development run: the same
scoring code as `evaluate_quality.py`, pointed at `train` and printing every
false positive and false negative so a rule can be debugged.

Keeping one implementation matters. When the two splits were scored by separate
copies of the logic, an improvement measured here did not necessarily mean the
same thing there.
"""

import argparse

from evaluate_quality import evaluate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Debug detection quality against the ai4privacy train split."
    )
    parser.add_argument("--samples", type=int, default=1000, help="Number of samples to evaluate.")
    parser.add_argument(
        "--ml", action="store_true", help="Include the ONNX ML backend in evaluation."
    )
    parser.add_argument(
        "--span-only",
        action="store_true",
        help="Score any overlap as a hit, ignoring whether the entity type matches.",
    )
    args = parser.parse_args()

    evaluate(
        args.samples,
        args.ml,
        strict_labels=not args.span_only,
        split="train",
        explain=True,
    )
