"""Suno platform constants — single source of truth for all module scripts.

When Suno adds a new model or changes limits, update HERE ONLY.
"""

# Valid Suno models (all versions, current and legacy)
VALID_MODELS = frozenset({
    "v4.5-all", "v4 Pro", "v4.5 Pro", "v4.5+ Pro", "v5 Pro", "v5.5 Pro"
})

# Tier definitions
VALID_TIERS = frozenset({"free", "pro", "premier"})
PAID_TIERS = frozenset({"pro", "premier"})
FREE_TIER_MODEL = "v4.5-all"

# Style prompt character limits per model
STYLE_PROMPT_LIMITS = {
    "v4 Pro": 200,
    "v4.5-all": 1000,
    "v4.5 Pro": 1000,
    "v4.5+ Pro": 1000,
    "v5 Pro": 1000,
    "v5.5 Pro": 1000,
}
STYLE_PROMPT_DEFAULT_MAX = 1000

# Critical zone: first N chars have strongest influence on generation
CRITICAL_ZONE = 200

# Exclusion prompt limits
EXCLUSION_RECOMMENDED_MAX = 200
EXCLUSION_HARD_MAX = 300

# Lyrics character limits (v4.5+/v5/v5.5)
# Hard limit: 5,000 chars — content beyond this is silently truncated
# Quality budget: ~3,000 chars — beyond this, Suno rushes through sections
SUNO_LYRICS_HARD_LIMIT = 5000
SUNO_LYRICS_QUALITY_BUDGET = 3000
