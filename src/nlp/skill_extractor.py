# PURPOSE:
# Extract user skills from raw resume text and normalize them to match Kaggle skill names.

# HIGH LEVEL FLOW:
# Resume text → clean → tokenize → match against master skills list → normalize → return list

import pandas as pd
import re

# STEP 1 — Load master skill list
# - Load skills.csv from dataset
# - Extract skill names column
# - Uppercase all skill names
# - Store as lookup set for fast matching

df = pd.read_csv('data/skills.csv')
skills = set(df['skill_name'].str.upper().tolist())

# STEP 2 — Clean resume text
# - Convert to lowercase
# - Remove punctuation
# - Remove extra spaces
# - Normalize separators (/, -, commas)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)      # Remove extra spaces
    return text.strip()

# STEP 3 — Token scanning
# - Split text into words and n-grams (1,2,3 word combos)
# - Compare tokens against skill list
# - Match exact occurrences of skill names
def extract_skills(resume_text):
    cleaned_text = clean_text(resume_text)
    words = cleaned_text.split()
    found_skills = set()

    # Check unigrams, bigrams, trigrams
    for n in range(1, 4):
        for i in range(len(words) - n + 1):
            token = ' '.join(words[i:i+n])
            if token in skills:
                found_skills.add(token)
    return list(found_skills)

# STEP 4 — Normalize extracted skills
# - Remove duplicates
# - Strip whitespace
# - Keep canonical names exactly as in skills.csv

# STEP 5 — Return structured output
# - List of normalized skills detected in resume
def skill_extractor(resume_text):
    extracted_skills = extract_skills(resume_text)
    normalized_skills = [skill.strip() for skill in extracted_skills]
    return list(set(normalized_skills))

