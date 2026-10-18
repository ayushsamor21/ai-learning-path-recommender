import re

from src.catalog import CAREER_SKILLS

SKILL_KEYWORDS = {
    "Python": ["python"],
    "SQL": ["sql", "database", "databases"],
    "Statistics": ["statistics", "statistical", "probability"],
    "Machine Learning": ["machine learning", " ml", "ml ", "scikit"],
    "Deep Learning": ["deep learning", "neural network", "neural nets", "pytorch", "tensorflow"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Git": ["git", "github"],
    "Data Visualization": ["visualization", "tableau", "power bi", "matplotlib", "seaborn"],
    "Algorithms": ["algorithm", "dsa", "data structures"],
    "Software Design": ["software design", "system design", "oop", "object oriented"],
}

CAREER_KEYWORDS = {
    "Machine Learning Engineer": ["machine learning engineer", "ml engineer", "mle"],
    "Data Scientist": ["data scientist", "data science"],
    "Software Engineer": ["software engineer", "software developer", "backend", "full stack"],
    "Data Analyst": ["data analyst", "analytics", "business intelligence", "bi analyst"],
}


def analyze_user_goal(text: str) -> dict:
    text_lower = f" {text.lower()} "

    detected_skills = []
    for skill, keywords in SKILL_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_skills.append(skill)

    detected_career = None
    for career, keywords in CAREER_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_career = career
            break

    if detected_career is None:
        for career in CAREER_SKILLS:
            if career.lower() in text_lower:
                detected_career = career
                break

    timeline = "Not specified"
    match = re.search(r"(\d+)\s*(month|months|week|weeks|year|years)", text_lower)
    if match:
        timeline = f"{match.group(1)} {match.group(2)}"

    objective = "Skill development"
    if any(word in text_lower for word in ["job", "career", "employment", "placement", "interview"]):
        objective = "Career / job preparation"
    elif any(word in text_lower for word in ["project", "build", "application", "portfolio"]):
        objective = "Project development"

    weak_skills = []
    weak_match = re.search(r"(weak in|struggle with|poor at|need to learn)\s+([a-zA-Z0-9 /,+]+)", text_lower)
    if weak_match:
        blob = weak_match.group(2)
        for skill, keywords in SKILL_KEYWORDS.items():
            if any(keyword.strip() in blob for keyword in keywords):
                weak_skills.append(skill)

    return {
        "skills": detected_skills,
        "weak_skills": weak_skills,
        "career": detected_career,
        "timeline": timeline,
        "objective": objective,
    }
