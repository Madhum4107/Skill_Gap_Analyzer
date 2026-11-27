"""Streamlit UI for the Skill Gap Analyzer."""

import json
import re

import pandas as pd
import streamlit as st

from analyzer import analyze_skills, find_related_skills, normalize_skills, recommend_roles
from skills_db import skills_db

st.set_page_config(
    page_title="Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🎯 Skill Gap Analyzer")
st.write("Explore how your current skills overlap with a target role—and discover what to learn next.")
st.caption("A transparent, rule-based learning tool. Coverage is not an employability or hiring prediction.")

with st.sidebar:
    st.header("Role profile")
    role = st.selectbox(
        "Choose a target role",
        list(skills_db),
        format_func=lambda name: name.replace("_", " ").title(),
    )
    st.divider()
    st.markdown("### Try an example")
    st.caption("Example skill sets")
    examples = {
        "Data Science starter": "Python, SQL, pandas, statistics, data visualization",
        "Data Analyst starter": "Excel, SQL, Power BI, Python, reporting",
        "Web developer starter": "HTML, CSS, JavaScript, React, Git",
    }
    selected_example = st.selectbox("Load sample skills", ["—"] + list(examples))
    st.markdown("### About this score")
    st.caption("Coverage = matched reference skills ÷ total reference skills. It does not measure skill depth, portfolio evidence, or real job requirements.")

with st.form("skill_analysis_form"):
    skill_input = st.text_area(
        "Skills you currently know",
        value=examples.get(selected_example, ""),
        placeholder="Python, SQL, machine learning, pandas…",
        help="Enter skills separated by commas, semicolons, or new lines.",
        height=110,
    )
    submitted = st.form_submit_button("Analyze my skills", type="primary", use_container_width=True)

if submitted:
    parsed = normalize_skills(re.split(r"[,;\n]+", skill_input))
    if not parsed:
        st.session_state.pop("analysis_result", None)
        st.warning("Please enter at least one skill.")
    else:
        matched, missing, extra, coverage = analyze_skills(parsed, skills_db[role])
        recommended = recommend_roles(parsed, skills_db)
        st.session_state.analysis_result = {
            "target_role": role,
            "user_skills": parsed,
            "matched": matched,
            "missing": missing,
            "extra": extra,
            "coverage": coverage,
            "recommendations": recommended,
        }

result = st.session_state.get("analysis_result")

if result:
    st.divider()
    st.subheader(f"Analysis · {result['target_role'].replace('_', ' ').title()}")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Skill coverage", f"{result['coverage']:.0f}%")
    k2.metric("Matched", len(result["matched"]))
    k3.metric("Gaps", len(result["missing"]))
    k4.metric("Extra skills", len(result["extra"]))
    st.progress(min(max(int(round(result["coverage"])), 0), 100))

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("### ✅ Skills matched")
        if result["matched"]:
            st.success(" · ".join(result["matched"]))
        else:
            st.info("No required skills matched yet.")
        st.markdown("### ➕ Skills outside this profile")
        if result["extra"]:
            st.info(" · ".join(result["extra"]))
        else:
            st.caption("No additional skills detected.")
    with right:
        st.markdown("### 📌 Skills to explore")
        if result["missing"]:
            st.warning(" · ".join(result["missing"]))
        else:
            st.success("You matched every skill in this reference list.")

    st.markdown("### Role overlap")
    role_rows = []
    for recommended_role, overlap in result["recommendations"]:
        total = len(skills_db[recommended_role])
        role_rows.append({
            "Role": recommended_role.replace("_", " ").title(),
            "Matched reference skills": overlap,
            "Reference skills": total,
            "Coverage (%)": round(overlap / total * 100, 1) if total else 0.0,
        })
    if role_rows:
        role_df = pd.DataFrame(role_rows)
        st.dataframe(
            role_df,
            hide_index=True,
            use_container_width=True,
            column_config={"Coverage (%)": st.column_config.ProgressColumn(
                "Coverage (%)", min_value=0, max_value=100, format="%.1f%%"
            )},
        )

    related = find_related_skills(result["extra"])
    if related:
        with st.expander("Explore related role mappings"):
            for skill, related_roles in related.items():
                st.write(f"**{skill.title()}** → " + ", ".join(
                    role.replace("_", " ").title() for role in related_roles
                ))

    report = json.dumps(result, indent=2, ensure_ascii=False)
    st.download_button(
        "Download analysis (JSON)",
        data=report,
        file_name="skill_gap_analysis.json",
        mime="application/json",
    )
    st.caption("This result is calculated from the curated role reference lists. Use it as a learning checklist, and verify skills against current job descriptions.")

else:
    st.info("Choose a role, enter your skills, and select **Analyze my skills** to see your results.")
    with st.expander("Browse the reference skill profiles"):
        for profile_name, required_skills in skills_db.items():
            st.markdown(f"**{profile_name.replace('_', ' ').title()}**")
            st.write(" · ".join(required_skills))

st.divider()
st.caption("Built by Madhumitha M · Python · Streamlit · Rule-based skill matching")
