alias_map = {
    "ml": "machine learning",
    "ai": "machine learning",
    "js": "javascript",
    "node": "nodejs",
    "reactjs": "react",
    "py": "python",
    "stats": "statistics"
}

related_map = {
    "python": ["backend_developer", "data_scientist", "python_developer"],
    "java": ["backend_developer", "java_developer"],
    "sql": ["data_analyst", "backend_developer"],
    "html": ["frontend_developer", "full_stack_developer"],
    "css": ["frontend_developer"],
    "javascript": ["frontend_developer", "full_stack_developer"],
    "seo": ["digital_marketing"],
    "marketing": ["digital_marketing"]
}


def normalize_skills(skills):
    return [alias_map.get(skill.lower().strip(), skill.lower().strip())
            for skill in skills if skill.strip()]


def analyze_skills(user_skills, required_skills):
    user_skills = set(normalize_skills(user_skills))
    required_skills = set(required_skills)

    matched = user_skills & required_skills
    missing = required_skills - user_skills
    extra = user_skills - required_skills

    score = (len(matched) / len(required_skills)) * 100

    return list(matched), list(missing), list(extra), score


def recommend_roles(user_skills, skills_db):
    user_skills = set(normalize_skills(user_skills))
    scores = {}

    for role, skills in skills_db.items():
        scores[role] = len(user_skills & set(skills))

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]


def find_related_skills(extra_skills):
    return {skill: related_map[skill] for skill in extra_skills if skill in related_map}