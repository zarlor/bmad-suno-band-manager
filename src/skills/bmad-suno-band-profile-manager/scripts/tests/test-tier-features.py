"""Tests for tier-features.py"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib.util import spec_from_file_location, module_from_spec

spec = spec_from_file_location(
    "tier_features",
    Path(__file__).parent.parent / "tier-features.py"
)
tier_features_mod = module_from_spec(spec)
spec.loader.exec_module(tier_features_mod)
get_tier_features = tier_features_mod.get_tier_features


def test_free_tier():
    result = get_tier_features("free")
    assert result["status"] == "pass"
    assert result["tier"] == "free"
    assert result["sliders_available"] is False
    assert result["personas_available"] is False
    assert result["audio_influence_available"] is False
    assert result["studio_available"] is False
    assert "v4.5-all" in result["models"]
    assert len(result["models"]) == 1


def test_pro_tier():
    result = get_tier_features("pro")
    assert result["status"] == "pass"
    assert result["sliders_available"] is True
    assert result["personas_available"] is True
    assert result["audio_influence_available"] is True
    assert result["studio_available"] is False
    assert "v5 Pro" in result["models"]
    assert len(result["unavailable"]) >= 1  # Studio and related


def test_premier_tier():
    result = get_tier_features("premier")
    assert result["status"] == "pass"
    assert result["sliders_available"] is True
    assert result["studio_available"] is True
    assert len(result["unavailable"]) == 0  # Everything available


def test_invalid_tier():
    result = get_tier_features("ultimate")
    assert result["status"] == "fail"
    assert "error" in result


def test_case_insensitive():
    result = get_tier_features("PRO")
    assert result["status"] == "pass"
    assert result["tier"] == "pro"


def test_free_has_unavailable_features():
    result = get_tier_features("free")
    assert len(result["unavailable"]) > 5  # Many features gated


def test_all_tiers_have_available():
    for tier in ["free", "pro", "premier"]:
        result = get_tier_features(tier)
        assert len(result["available"]) > 0


def test_all_tiers_have_pricing():
    for tier in ["free", "pro", "premier"]:
        result = get_tier_features(tier)
        assert "pricing" in result
        assert "monthly" in result["pricing"]
        assert "annual_monthly" in result["pricing"]


def test_all_tiers_have_song_length():
    for tier in ["free", "pro", "premier"]:
        result = get_tier_features(tier)
        assert "song_length_max" in result


def test_all_tiers_have_download_quality():
    for tier in ["free", "pro", "premier"]:
        result = get_tier_features(tier)
        assert "download_quality" in result


def test_all_tiers_have_credit_cost():
    for tier in ["free", "pro", "premier"]:
        result = get_tier_features(tier)
        assert "credit_cost" in result
        assert result["credit_cost"]["generation"] == 10
        assert result["credit_cost"]["extension"] == 5


def test_free_pricing_is_zero():
    result = get_tier_features("free")
    assert result["pricing"]["monthly"] == 0
    assert result["pricing"]["annual_monthly"] == 0


def test_pro_pricing():
    result = get_tier_features("pro")
    assert result["pricing"]["monthly"] == 10
    assert result["pricing"]["annual_monthly"] == 8


def test_premier_pricing():
    result = get_tier_features("premier")
    assert result["pricing"]["monthly"] == 30
    assert result["pricing"]["annual_monthly"] == 24


def test_legacy_models_flagged():
    for tier in ["pro", "premier"]:
        result = get_tier_features(tier)
        assert "legacy_models" in result
        assert "v4 Pro" in result["legacy_models"]
