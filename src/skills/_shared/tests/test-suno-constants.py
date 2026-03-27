"""Tests for shared Suno constants — verify internal consistency."""
import sys
from pathlib import Path

# Add _shared to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from suno_constants import (
    VALID_MODELS, VALID_TIERS, PAID_TIERS, FREE_TIER_MODEL,
    STYLE_PROMPT_LIMITS, STYLE_PROMPT_DEFAULT_MAX,
    CRITICAL_ZONE, EXCLUSION_RECOMMENDED_MAX, EXCLUSION_HARD_MAX,
    SUNO_LYRICS_HARD_LIMIT, SUNO_LYRICS_QUALITY_BUDGET,
)


class TestSunoConstants:

    def test_valid_models_is_frozenset(self):
        assert isinstance(VALID_MODELS, frozenset)

    def test_valid_tiers_is_frozenset(self):
        assert isinstance(VALID_TIERS, frozenset)

    def test_paid_tiers_subset_of_valid_tiers(self):
        assert PAID_TIERS.issubset(VALID_TIERS)

    def test_free_tier_not_in_paid(self):
        assert "free" not in PAID_TIERS

    def test_free_tier_model_is_valid(self):
        assert FREE_TIER_MODEL in VALID_MODELS

    def test_style_prompt_limits_models_are_valid(self):
        for model in STYLE_PROMPT_LIMITS:
            assert model in VALID_MODELS, f"Model '{model}' in STYLE_PROMPT_LIMITS but not in VALID_MODELS"

    def test_all_models_have_style_limits(self):
        for model in VALID_MODELS:
            assert model in STYLE_PROMPT_LIMITS, f"Model '{model}' in VALID_MODELS but missing from STYLE_PROMPT_LIMITS"

    def test_style_prompt_default_max_is_positive(self):
        assert STYLE_PROMPT_DEFAULT_MAX > 0

    def test_critical_zone_less_than_default_max(self):
        assert CRITICAL_ZONE <= STYLE_PROMPT_DEFAULT_MAX

    def test_exclusion_recommended_less_than_hard(self):
        assert EXCLUSION_RECOMMENDED_MAX <= EXCLUSION_HARD_MAX

    def test_lyrics_quality_budget_less_than_hard_limit(self):
        assert SUNO_LYRICS_QUALITY_BUDGET < SUNO_LYRICS_HARD_LIMIT

    def test_lyrics_limits_are_positive(self):
        assert SUNO_LYRICS_HARD_LIMIT > 0
        assert SUNO_LYRICS_QUALITY_BUDGET > 0

    def test_v55_pro_present(self):
        """v5.5 Pro must be in both VALID_MODELS and STYLE_PROMPT_LIMITS."""
        assert "v5.5 Pro" in VALID_MODELS
        assert "v5.5 Pro" in STYLE_PROMPT_LIMITS
