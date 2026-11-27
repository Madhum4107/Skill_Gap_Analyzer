import re

import streamlit as st
from skills_db import skills_db
from analyzer import analyze_skills, recommend_roles, find_related_skills, normalize_skills

st.set_page_config(page_title="Skill Gap Analyzer", page_icon="🎯", layout="centered")

st.title("🎯 Skill Gap Analyzer")
st.write("Compare your skills with a target role, discover gaps, and explore adjacent career paths.")

with st.sidebar:
    st.header("About")
    st.write("A rule-based skill matching demo using a curated role-to-skill reference database.")
    st.caption("The readiness score is a skill-coverage indicator, not a job guarantee.")

role = st.selectbox("Target role", list(skills_db.keys()), format_func=lambda x: x.replace("_", " ").title())
user_input = st.text_area(
    "Your skills",
    placeholder="Python, SQL, machine learning, pandas",
    help="Separate skills with commas, semicolons, or new lines. Multi-word skills are supported.",
    height=100,
)

if st.button("Analyze skills", type="primary", use_container_width=True):
    user_skills = normalize_skills(re.split(r"[,;\n]+", user_input))

    if not user_skills:
        st.warning("Enter at least one skill to analyze.")
    else:
        matched, missing, extra, score = analyze_skills(user_skills, skills_db[role])
        st.divider()
        st.subheader("Your analysis")

        c1, c2, c3 = st.columns(3)
        c1.metric("Readiness coverage", f"{score:.1f}%")
        c2.metric("Matched", len(matched))
        c3.metric("Missing", len(missing))
        st.progress(int(round(score)))

        with st.expander("Matched skills", expanded=True):
            st.success(", ".join(matched) if matched else "No required skills matched yet.")
        with st.expander("Skills to focus on", expanded=True):
            st.warning(", ".join(missing) if missing else "You matched every skill in this role's reference list!")
        with st.expander("Additional skills"):
            st.info(", ".join(extra) if extra else "No additional skills detected.")

        st.caption(f"Coverage is calculated from {len(skills_db[role])} skills in the role reference list.")

        st.subheader("Related career paths")
        related = find_related_skills(extra)
        if related:
            for skill, roles in related.items():
                st.write(f"**{skill.title()}** → {', '.join(r.replace('_', ' ').title() for r in roles)}")
        else:
            st.write("No related-role mapping found for your additional skills.")

        st.subheader("Roles with the strongest skill overlap")
        recommendations = recommend_roles(user_skills, skills_db)
        for recommended_role, count in recommendations:
            total = len(skills_db[recommended_role])
            coverage = (count / total * 100) if total else 0
            st.write(f"**{recommended_role.replace('_', ' ').title()}** — {count}/{total} skills ({coverage:.1f}% coverage)")

st.divider()
st.caption("Built by Madhumitha M · Python · Streamlit · Rule-based matching")
