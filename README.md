# Skill Gap Analyzer

A small career-exploration tool that compares a user's skill list with a curated role profile and highlights areas to learn next.

> **What it is:** a transparent, rule-based skill matching application—not an AI hiring model or a validated employability score.

## Preview

![App preview](output.png.png)

🎬 Demo video: [View the demo](demo.mp4)

## Features

- Explore curated profiles for data, software, DevOps, cybersecurity, business, and marketing roles
- Normalize common skill aliases (for example, `py` → `python`, `ml` → `machine learning`)
- Identify matched, missing, and additional skills
- Show a skill-coverage percentage for the selected profile
- Recommend related roles based on skill overlap
- Discover related career paths from additional skills

## How the score works

```
Coverage = (Matched required skills / Total required skills) × 100
```

This score is a checklist-style coverage indicator. It does not measure proficiency, project quality, experience, interview performance, or hiring probability.

## Tech stack

- Python
- Streamlit

## Run locally

```bash
git clone https://github.com/Madhum4107/Skill_Gap_Analyzer.git
cd Skill_Gap_Analyzer
python -m venv .venv
```

Activate the environment:

**Windows**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install and launch:

```bash
python -m pip install -r requirements.txt
streamlit run main.py
```

## Repository structure

```
├── main.py          # Streamlit interface
├── analyzer.py      # Skill normalization, matching, and role ranking
├── skills_db.py     # Curated role-to-skill reference profiles
├── test_analyzer.py # Unit tests for core analysis
├── requirements.txt # Runtime dependencies
├── output.png.png   # Screenshot
└── demo.mp4        # Walkthrough
```

## Tests

```bash
python -m unittest test_analyzer.py
```

## Current limitations

- Skill lists are manually curated and may not match every job description.
- Matching is based on keywords and aliases, not skill proficiency or evidence.
- Role recommendations use overlap with the reference list.
- Coverage percentages are not validated against employment outcomes.

## Roadmap

- Resume parsing with user-controlled file handling
- Job-description comparison
- Proficiency and project-evidence tracking
- Explainable weighted skill matching
- Improved test coverage and deployment

## Author

**Madhumitha M** · AI & ML student

[GitHub](https://github.com/Madhum4107) · [LinkedIn](https://www.linkedin.com/in/madhumitha4107/)
