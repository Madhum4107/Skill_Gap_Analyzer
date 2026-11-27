"""Core skill matching and role recommendation utilities."""

from collections.abc import Iterable

alias_map = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "js": "javascript",
    "node": "nodejs",
    "reactjs": "react",
    "py": "python",
    "stats": "statistics",
    "sklearn": "scikit-learn",
    "powerbi": "power bi",
}

related_map = {
    "python": ["backend_developer", "data_scientist", "python_developer"],
    "java": ["backend_developer", "java_developer"],
    "sql": ["data_analyst", "backend_developer"],
    "html": ["frontend_developer", "full_stack_developer"],
    "css": ["frontend_developer"],
    "javascript": ["frontend_developer", "full_stack_developer"],
    "seo": ["digital_marketing"],
    "marketing": ["digital_marketing"],
}


def normalize_skills(skills: Iterable[str]) -> list[str]:
    """Normalize whitespace/case/aliases and remove duplicates, preserving order."""
    normalized = []
    seen = set()
    for skill in skills:
        if skill is None:
            continue
        cleaned = " ".join(str(skill).lower().strip().split())
        if not cleaned:
            continue
        canonical = alias_map.get(cleaned, cleaned)
        if canonical not in seen:
            normalized.append(canonical)
            seen.add(canonical)
    return normalized


def analyze_skills(user_skills, required_skills):
    """Return matched, missing, extra skill lists and coverage percentage."""
    user = set(normalize_skills(user_skills))
    required = set(normalize_skills(required_skills))

    matched = sorted(user & required)
    missing = sorted(required - user)
    extra = sorted(user - required)

    score = (len(matched) / len(required) * 100) if required else 0.0
    return matched, missing, extra, score


def recommend_roles(user_skills, skills_db):
    """Rank roles by skill coverage, then overlap count, with stable tie-breaking."""
    user = set(normalize_skills(user_skills))
    scored = []
    for role, required in skills_db.items():
        required_set = set(normalize_skills(required))
        overlap = len(user & required_set)
        coverage = overlap / len(required_set) if required_set else 0.0
        scored.append((role, overlap, coverage))
    scored.sort(key=lambda item: (-item[2], -item[1], item[0]))
    return [(role, overlap) for role, overlap, _ in scored[:3]]


def find_related_skills(extra_skills):
    """Return role mappings for known additional skills."""
    return {
        skill: related_map[skill]
        for skill in sorted(set(normalize_skills(extra_skills)))
        if skill in related_map
    }
