import unittest

from analyzer import analyze_skills, normalize_skills, recommend_roles


class SkillAnalyzerTests(unittest.TestCase):
    def test_aliases_and_duplicate_removal(self):
        self.assertEqual(normalize_skills([" PY ", "py", "JS", "reactjs"]), ["python", "javascript", "react"])

    def test_multiword_skill_normalization(self):
        self.assertEqual(normalize_skills(["Machine   Learning", "machine learning"]), ["machine learning"])

    def test_coverage_and_deterministic_outputs(self):
        matched, missing, extra, score = analyze_skills(
            ["python", "SQL", "extra"], ["sql", "python", "pandas"]
        )
        self.assertEqual(matched, ["python", "sql"])
        self.assertEqual(missing, ["pandas"])
        self.assertEqual(extra, ["extra"])
        self.assertAlmostEqual(score, 200 / 3)

    def test_empty_required_skills_is_safe(self):
        self.assertEqual(analyze_skills(["python"], []), ([], [], ["python"], 0.0))

    def test_role_recommendations_rank_by_coverage(self):
        roles = {
            "small_role": ["python", "sql"],
            "big_role": ["python", "sql", "pandas", "numpy"],
            "other": ["java"],
        }
        self.assertEqual(recommend_roles(["python", "sql"], roles)[:2],
                         [("small_role", 2), ("big_role", 2)])


if __name__ == "__main__":
    unittest.main()
