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
