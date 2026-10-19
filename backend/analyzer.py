import re

# Skill peru -> aa skill ki vere peru lu (aliases).
# Example: resume lo "mysql" ani unte, adi "sql" skill ga count avthundi.
SKILLS = {
    "python": ["python"],
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "react": ["react", "reactjs", "react.js"],
    "fastapi": ["fastapi"],
    "docker": ["docker"],
    "aws": ["aws", "amazon web services"],
    "git": ["git", "github"],
    "javascript": ["javascript", "js"],
    "java": ["java"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
}


def contains_word(text, word):
    """Text lo `word` poorthi padam ga unte matrame True.
    Example: "sql" ni "nosql" lo match cheyyadu, "react" ni "reactive" lo match cheyyadu."""
    pattern = r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])"
    return re.search(pattern, text) is not None


def has_skill(text, aliases):
    """Aa skill ki sambandhinchina e peru unna text lo undo check chestundi."""
    return any(contains_word(text, alias) for alias in aliases)


def analyze_resume(resume_text, jd_text):
    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    matched_skills = []
    missing_skills = []
    suggestions = []

    for skill, aliases in SKILLS.items():
        # JD lo ee skill adagakapothe, danini matched leda missing ani count cheyyam
        if not has_skill(jd_text, aliases):
            continue

        if has_skill(resume_text, aliases):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
            suggestions.append(
                f"Try learning {skill} for this profile, add {skill} to your resume"
            )

    # Score = JD adigina skills lo, resume lo unnavi entha percent
    required_count = len(matched_skills) + len(missing_skills)
    if required_count == 0:
        matched_score = 0.0
    else:
        matched_score = round(len(matched_skills) / required_count * 100, 2)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "matched_score": matched_score,
    }