# PURPOSE:
# Extract user skills from raw resume text and normalize them to match Kaggle skill names.

import pandas as pd
import re

# STEP 1 — Load master skill list and build canonical mapping
# lowercase_skill → original_skill
skills_df = pd.read_csv("data/skills.csv")
skill_lookup = {
    skill.lower(): skill
    for skill in skills_df["skill_name"].dropna().tolist()
}

skill_keys = set(skill_lookup.keys())

# STEP 2 — Clean resume text
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# STEP 3 — Token scanning with n-grams
def extract_skills(resume_text: str):
    cleaned = clean_text(resume_text)
    words = cleaned.split()
    found = set()

    for n in range(1, 4):  # unigram → trigram
        for i in range(len(words) - n + 1):
            token = " ".join(words[i:i+n])
            if token in skill_keys:
                found.add(skill_lookup[token])  # return canonical name

    return list(found)

# STEP 4 — Wrapper for external use
def skill_extractor(resume_text: str):
    return extract_skills(resume_text)
