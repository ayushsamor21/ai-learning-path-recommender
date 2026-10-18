import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.catalog import CAREER_SKILLS, DEFAULT_SKILLS, RESOURCES, path_for_career


def resources_frame(resources: list[dict] | None = None) -> pd.DataFrame:
    rows = []
    for item in resources or RESOURCES:
        rows.append(
            {
                **item,
                "skill_text": " ".join(item.get("skills", [])),
            }
        )
    return pd.DataFrame(rows)


def calculate_skill_gaps(goal: str, current_skills: dict[str, int] | None = None) -> list[dict]:
    required = CAREER_SKILLS[goal]
    current = current_skills or DEFAULT_SKILLS
    gaps = []
    for skill, required_level in required.items():
        current_level = int(current.get(skill, 0))
        gap = max(required_level - current_level, 0)
        gaps.append(
            {
                "skill": skill,
                "current": current_level,
                "required": required_level,
                "gap": gap,
            }
        )
    return sorted(gaps, key=lambda item: item["gap"], reverse=True)


def explain_resource(resource: dict, goal: str, gaps: list[dict], experience: str) -> str:
    gap_skills = {item["skill"] for item in gaps[:3] if item["gap"] > 0}
    overlap = [skill for skill in resource.get("skills", []) if skill in gap_skills]
    reasons = [f"Aligned with the {goal} path."]
    if overlap:
        reasons.append(f"Addresses a priority skill gap: {', '.join(overlap)}.")
    if resource.get("level") == experience:
        reasons.append(f"Matches your {experience.lower()} level.")
    elif resource.get("type") == "Project":
        reasons.append("Turns theory into a portfolio artifact.")
    if resource.get("prerequisites") and resource["prerequisites"] != "None":
        reasons.append(f"Comes after: {resource['prerequisites']}.")
    return " ".join(reasons)


def recommend(
    goal: str,
    experience: str,
    interests: str,
    user_goal: str,
    resources: list[dict] | None = None,
    gaps: list[dict] | None = None,
) -> pd.DataFrame:
    frame = resources_frame(resources)
    query = " ".join([goal, experience, interests, user_goal])
    documents = (
        frame["skill_text"]
        + " "
        + frame["title"]
        + " "
        + frame["description"]
        + " "
        + frame["provider"]
    ).tolist()

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(documents + [query])
    similarity = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    result = frame.copy()
    result["similarity"] = similarity

    difficulty = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
    user_level = difficulty[experience]
    result["difficulty_score"] = result["level"].map(difficulty)
    result["level_fit"] = 1 / (1 + (result["difficulty_score"] - user_level).abs())

    gap_skills = {item["skill"] for item in (gaps or [])[:4] if item["gap"] > 0}

    def gap_boost(skills) -> float:
        return 0.15 * len([skill for skill in skills if skill in gap_skills])

    result["gap_boost"] = result["skills"].apply(gap_boost)
    if experience == "Beginner":
        result["type_fit"] = result["type"].map({"Course": 0.12, "Project": 0.0}).fillna(0)
    else:
        result["type_fit"] = result["type"].map({"Course": 0.04, "Project": 0.1}).fillna(0)

    result["score"] = (
        result["similarity"] * 0.55
        + result["level_fit"] * 0.25
        + result["gap_boost"]
        + result["type_fit"]
    )

    if experience == "Beginner":
        result = result[result["level"] != "Advanced"]

    ranked = result.sort_values("score", ascending=False).head(8)
    ranked["why"] = ranked.apply(
        lambda row: explain_resource(row.to_dict(), goal, gaps or [], experience),
        axis=1,
    )
    return ranked


def weekly_plan(hours: int, path: list[dict]) -> str:
    if hours <= 5:
        pace = "one focused module per week"
    elif hours <= 12:
        pace = "a course module plus one practice set each week"
    else:
        pace = "a course block and a small project checkpoint each week"
    return (
        f"With {hours} hours/week, work through {pace}. "
        f"The {len(path)}-step roadmap stays prerequisite-aware: foundations first, then applied work."
    )


def progress_stats(path: list[dict], completed_ids: list[str]) -> dict:
    ids = [step["id"] for step in path]
    done = [item for item in ids if item in completed_ids]
    total = len(ids) or 1
    courses = [step for step in path if step["type"] == "Course"]
    projects = [step for step in path if step["type"] == "Project"]
    return {
        "overall": round(100 * len(done) / total),
        "courses_done": sum(1 for item in courses if item["id"] in completed_ids),
        "courses_total": len(courses),
        "projects_done": sum(1 for item in projects if item["id"] in completed_ids),
        "projects_total": len(projects),
        "remaining": [step for step in path if step["id"] not in completed_ids],
    }


def build_path(goal: str) -> list[dict]:
    return path_for_career(goal)
