import sys
import os

# ✅ Force Python to treat /src as module root
SRC_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, SRC_PATH)

import pandas as pd
import streamlit as st

from src.nlp.skill_extractor import skill_extractor
from src.nlp.skill_gap import compute_skill_gap


# -------------------------
# Resolve project root paths
# -------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MARKET_SKILLS_PATH = os.path.join(DATA_DIR, "market_skills.csv")


@st.cache_data
def load_market_data():
    df = pd.read_csv(MARKET_SKILLS_PATH)
    df["skill_name"] = df["skill_name"].str.lower().str.strip()
    return df


def main():
    st.set_page_config(page_title="AI Job Market Analyzer", layout="wide")
    st.title("AI Job Market Skill Gap Analyzer")

    market_df = load_market_data()

    st.header("Paste Resume Text")
    resume_text = st.text_area(
        "Resume / Skills",
        height=250,
        placeholder="Paste your resume here..."
    )

    if st.button("Analyze Skills"):
        if not resume_text.strip():
            st.warning("Please paste resume text first.")
            return

        with st.spinner("Extracting skills and analyzing gap..."):
            user_skills = skill_extractor(resume_text)
            results = compute_skill_gap(user_skills, market_df)

        st.subheader("Coverage Score")
        st.metric("Market Skill Coverage", f"{results['coverage_score']}%")

        st.subheader("Matched Skills")
        st.write(results["matched_skills"])

        st.subheader("Top Missing Skills")
        st.dataframe(pd.DataFrame(results["missing_top10"]), use_container_width=True)


if __name__ == "__main__":
    main()
