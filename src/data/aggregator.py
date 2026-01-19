# PURPOSE:
# Aggregate and rank the most in-demand skills across real job postings
# using job_skills.csv + skills.csv.

# GOAL:
# Build a market skill frequency table to compare against user resume skills.

# REQUIRED INPUT FILES:
# - job_skills.csv  (job_id → skill_id)
# - skills.csv      (skill_id → skill_name)

# OUTPUT:
# Dictionary / DataFrame:
# skill_name → frequency across all jobs

# STEP 1 — Load datasets
# - Read job_skills.csv
# - Read skills.csv
# - Ensure skill_id column exists in both

# STEP 2 — Join skills to job_skills
# - Merge job_skills with skills on skill_id
# - This converts numeric IDs into readable skill names

# STEP 3 — Count skill demand
# - Count how many times each skill_name appears
# - This represents how frequently companies request that skill

# STEP 4 — Rank skills
# - Sort skills by frequency descending
# - Select top N skills as “market trending skills”

# STEP 5 — Return structured output
# - skill_name
# - demand_count
# - optional normalized weight (percentage)

# NOTE:
# This becomes the MARKET baseline used later by:
# skill_gap.py to compare against user resume skills.

import pandas as pd

def load_and_aggregate_skills(
    job_skills_path="job_skills.csv",
    skills_path="skills.csv",
    top_n=50
):
    # STEP 1 — Load datasets
    job_skills = pd.read_csv("job_skills.csv")
    skills = pd.read_csv("skills.csv")

    # STEP 2 — Merge job_skills with skills to decode skill names
    merged = job_skills.merge(skills, on="skill_id", how="left")

    # STEP 3 — Count frequency of each skill
    skill_counts = (
        merged["skill_name"]
        .dropna()
        .value_counts()
        .reset_index()
    )
    skill_counts.columns = ["skill_name", "demand_count"]

    # STEP 4 — Normalize weights (percentage demand)
    total = skill_counts["demand_count"].sum()
    skill_counts["market_weight"] = skill_counts["demand_count"] / total

    # STEP 5 — Return top trending skills
    return skill_counts.head(top_n)
