import json
from pathlib import Path

from benchmarks.run_ablations import ABLATION_CONFIGS, build_error_atlas, run_ablation_suite


def test_run_ablation_suite_on_local_file(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus.jsonl"
    corpus.write_text(
        json.dumps(
            {
                "language": "en",
                "source_text": "Email alice@example.com directly.",
                "privacy_mask": [{"start": 6, "end": 23, "label": "EMAIL"}],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    res = run_ablation_suite(
        file_path=corpus,
        samples=1,
        use_ml=False,
        ablations=["rules_only"],
    )
    assert res["samples"] == 1
    assert "baseline_metrics" in res
    assert "baseline_exact" in res
    assert "baseline_errors" in res
    assert "ablations" in res
    assert "rules_only" in res["ablations"]
    assert "delta_f1" in res["ablations"]["rules_only"]
    assert "error_atlas" in res
    assert "top_three_error_categories" in res["error_atlas"]


def test_build_error_atlas_ranks_categories_and_entities() -> None:
    baseline_result = {
        "error_categories": {
            "missing_candidate": 15,
            "threshold_suppression": 30,
            "label_confusion": 5,
            "boundary_mismatch": 10,
            "conflict_loss": 2,
        },
        "per_entity": {
            "EMAIL": {"false_positives": 2, "false_negatives": 1},
            "PERSON": {"false_positives": 12, "false_negatives": 18},
            "PHONE": {"false_positives": 0, "false_negatives": 4},
        },
    }
    ablation_reports = {
        "rules_only": {
            "delta_f1": -0.25,
            "delta_exact_f1": -0.30,
            "recoverable_fp": 5,
            "prevented_fn": 20,
        },
        "no_context_boost": {
            "delta_f1": -0.02,
            "delta_exact_f1": -0.02,
            "recoverable_fp": 2,
            "prevented_fn": 3,
        },
    }

    atlas = build_error_atlas(baseline_result, ablation_reports)
    assert atlas["total_baseline_errors"] == 62
    top_cats = atlas["top_three_error_categories"]
    assert len(top_cats) == 3
    assert top_cats[0]["category"] == "threshold_suppression"
    assert top_cats[0]["count"] == 30
    assert top_cats[1]["category"] == "missing_candidate"
    assert top_cats[1]["count"] == 15
    assert top_cats[2]["category"] == "boundary_mismatch"
    assert top_cats[2]["count"] == 10

    top_ents = atlas["top_three_entity_vulnerabilities"]
    assert len(top_ents) == 3
    assert top_ents[0]["entity_type"] == "PERSON"
    assert top_ents[0]["total_errors"] == 30
    assert top_ents[1]["entity_type"] == "PHONE"
    assert top_ents[1]["total_errors"] == 4
    assert top_ents[2]["entity_type"] == "EMAIL"
    assert top_ents[2]["total_errors"] == 3

    ranked_comps = atlas["ranked_components_by_impact"]
    assert ranked_comps[0]["ablation"] == "rules_only"
    assert ranked_comps[0]["delta_f1"] == -0.25


def test_run_ablation_suite_skips_unknown_ablation(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus.jsonl"
    corpus.write_text(
        json.dumps(
            {
                "language": "en",
                "source_text": "Call +1-555-0100.",
                "privacy_mask": [{"start": 5, "end": 17, "label": "PHONE"}],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    res = run_ablation_suite(
        file_path=corpus,
        samples=1,
        use_ml=False,
        ablations=["unknown_ablation", "rules_only"],
    )
    assert "unknown_ablation" not in res["ablations"]
    assert "rules_only" in res["ablations"]


def test_all_ablation_configs_have_descriptions_and_kwargs() -> None:
    for name, cfg in ABLATION_CONFIGS.items():
        assert "description" in cfg, f"Missing description in {name}"
        assert "kwargs" in cfg, f"Missing kwargs in {name}"
        assert isinstance(cfg["kwargs"], dict)
