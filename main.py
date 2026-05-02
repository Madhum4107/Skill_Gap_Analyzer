import streamlit as st
from skills_db import skills_db
from analyzer import analyze_skills, recommend_roles, find_related_skills

# 🔥 PAGE SETTINGS
st.set_page_config(page_title="AI Skill Gap Analyzer", layout="centered")

# 🔥 TITLE + DESCRIPTION
st.title("🚀 AI Skill Gap Analyzer")
st.write("Analyze your skills, find missing skills, and get career recommendations instantly!")

# 🔥 SIDEBAR
st.sidebar.title("📌 About Project")
st.sidebar.write("This tool helps you identify skill gaps and become job-ready.")

# 🔥 ROLE SELECT
role = st.selectbox("🎯 Select Target Role", list(skills_db.keys()))

# 🔥 USER INPUT
user_input = st.text_input("🧠 Enter your skills (comma or space separated)")

# 🔥 ANALYZE BUTTON
if st.button("Analyze"):

    # INPUT HANDLING
    if "," in user_input:
        user_skills = [s.strip().lower() for s in user_input.split(",") if s.strip()]
    else:
        user_skills = [s.strip().lower() for s in user_input.split() if s.strip()]

    # 🔥 ANALYSIS
    matched, missing, extra, score = analyze_skills(user_skills, skills_db[role])

    # 🔥 SECTION DIVIDER
    st.markdown("---")
    st.subheader("📊 Analysis Result")

    # ✅ MATCHED
    st.subheader("✅ Matched Skills")
    st.success(", ".join(matched) if matched else "None")

    # ❌ MISSING
    st.subheader("❌ Missing Skills")
    st.error(", ".join(missing) if missing else "None")

    # ⚠️ EXTRA
    st.subheader("⚠️ Other Skills")
    st.info(", ".join(extra) if extra else "None")

    # 📊 SCORE
    st.subheader("📊 Readiness Score")
    st.progress(int(score))
    st.success(f"{score:.2f}% ready for {role}")

    # 🔥 TOTAL SKILLS COUNT
    st.write(f"🧾 Total Skills Required: {len(skills_db[role])}")

    # 💡 RELATED ROLES
    st.markdown("---")
    st.subheader("💡 Your Skills Are Useful In")

    related = find_related_skills(extra)

    if related:
        for skill, roles in related.items():
            st.write(f"👉 {skill} → {', '.join(roles)}")
    else:
        st.write("No mapped roles")

    # 🎯 ROLE RECOMMENDATION
    st.markdown("---")
    st.subheader("🎯 Recommended Roles")

    for r, sc in recommend_roles(user_skills, skills_db):
        st.write(f"👉 {r} (match: {sc} skills)")

# 🔥 FOOTER
st.markdown("---")
st.caption("🚀 Built by Madhu | AI & Data Science Enthusiast")