# PURPOSE:
# Compare user resume skills against market trending skills
# and compute a gap score + prioritized missing skills.

# INPUTS:
# - user_skills: List[str] from skill_extractor
# - market_skills_df: DataFrame from aggregator (skill_name, demand_count, weight)

# OUTPUT:
# - coverage_score (% of market skills user already has)
# - missing_skills ranked by market importance
# - priority recommendations

# STEP 1 — Normalize user skills
# - lowercase everything
# - strip whitespace
# - convert to set for fast lookup

# STEP 2 — Normalize market skills
# - lowercase skill_name column
# - keep demand_count and weight

# STEP 3 — Compute overlap
# - intersection(user_skills, market_skills)

# STEP 4 — Compute coverage score
# - coverage = (# matched skills) / (total top market skills)

# STEP 5 — Identify gaps
# - skills in market not in user_skills

# STEP 6 — Rank missing skills
# - sort missing skills by demand_count descending
# - optionally include weight for importance score

# STEP 7 — Categorize gaps (optional advanced)
# - group into:
#   • Programming
#   • Data
#   • Cloud
#   • ML
#   • Tools

# STEP 8 — Return structured output
# - coverage_score
# - top 10 missing high-value skills
# - formatted for dashboard use

import pandas as pd
from typing import List, Dict

def compute_skill_gap(user_skills: List[str], market_df: pd.DataFrame) -> Dict:
    # STEP 1 — Normalize user skills
    normalized_user = set([s.lower().strip() for s in user_skills])

    # STEP 2 — Normalize market skills
    market_df['skill_name'] = market_df['skill_name'].str.lower().str.strip()
    market_skills = set(market_df['skill_name'])

    # STEP 3 — Compute overlap
    matched = normalized_user.intersection(market_skills)

    # STEP 4 — Coverage score
    coverage = len(matched) / len(market_skills) if len(market_skills) > 0 else 0

    # STEP 5 — Missing skills
    missing = market_skills - normalized_user

    # STEP 6 — Rank missing by demand
    missing_df = market_df[market_df['skill_name'].isin(missing)] \
        .sort_values(by='demand_count', ascending=False)

    top_missing = missing_df[['skill_name', 'demand_count', 'market_weight']] \
        .head(10) \
        .to_dict(orient='records')

    # STEP 7 — Structured output
    return {
        "coverage_score": round(coverage * 100, 2),
        "matched_skills": sorted(list(matched)),
        "missing_top10": top_missing
    }


