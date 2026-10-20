import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent
for path in (ROOT, APP_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import pandas as pd
import streamlit as st

from theme import THEME_CSS
from src.catalog import CAREER_SKILLS, DEFAULT_SKILLS
from src.config import MONGODB_URI, mongo_uri_from_secrets
from src.db import connect_store
from src.nlp import analyze_user_goal
from src.recommender import (
    build_path,
    calculate_skill_gaps,
    progress_stats,
    recommend,
    weekly_plan,
)

st.set_page_config(
    page_title="LearnPath AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(THEME_CSS, unsafe_allow_html=True)

DEMO_USER = {"email": "demo@learnpath.ai", "name": "Demo Learner"}


@st.cache_resource
def get_store():
    uri = MONGODB_URI
    if not uri:
        try:
            uri = mongo_uri_from_secrets(st.secrets)
        except Exception:
            uri = ""
    return connect_store(uri)


def init_state():
    if "user" not in st.session_state or not st.session_state.user:
        st.session_state.user = dict(DEMO_USER)
    if "skills" not in st.session_state:
        st.session_state.skills = dict(DEFAULT_SKILLS)
    if "completed_ids" not in st.session_state:
        st.session_state.completed_ids = []
    if "generated" not in st.session_state:
        st.session_state.generated = False
    if "analysis" not in st.session_state:
        st.session_state.analysis = None
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = None
    if "goal_text" not in st.session_state:
        st.session_state.goal_text = ""


def account_key() -> str:
    return st.session_state.user["email"]


def persist(store, extra: dict | None = None):
    user = st.session_state.user
    if not user:
        return
    recs = st.session_state.recommendations
    payload = {
        "email": user["email"],
        "name": user["name"],
        "goal": st.session_state.get("career_goal", list(CAREER_SKILLS.keys())[0]),
        "experience": st.session_state.get("experience_level", "Beginner"),
        "interests": st.session_state.get("interests_text", ""),
        "hours": st.session_state.get("hours_week", 10),
        "goal_text": st.session_state.get("goal_text", ""),
        "skills": dict(st.session_state.skills),
        "completed_ids": list(st.session_state.completed_ids),
        "generated": bool(st.session_state.generated),
        "analysis": st.session_state.analysis,
        "recommendations": recs.to_dict(orient="records") if isinstance(recs, pd.DataFrame) else recs,
    }
    if extra:
        payload.update(extra)
    store.upsert_learner(payload)


def apply_learner(saved: dict | None):
    if not saved:
        return
    skills = saved.get("skills") or {}
    st.session_state.skills.update(skills)
    for skill, value in skills.items():
        st.session_state[f"skill-{skill}"] = int(value)
    st.session_state.completed_ids = list(saved.get("completed_ids") or [])
    for resource_id in st.session_state.completed_ids:
        st.session_state[f"path-{resource_id}"] = True
    if saved.get("goal"):
        st.session_state["career_goal"] = saved["goal"]
    if saved.get("experience"):
        st.session_state["experience_level"] = saved["experience"]
    if saved.get("interests"):
        st.session_state["interests_text"] = saved["interests"]
    if saved.get("hours"):
        st.session_state["hours_week"] = int(saved["hours"])
    if saved.get("name"):
        st.session_state["display_name"] = saved["name"]
    if saved.get("goal_text"):
        st.session_state.goal_text = saved["goal_text"]
        st.session_state["goal_area"] = saved["goal_text"]
    st.session_state.analysis = saved.get("analysis")
    recs = saved.get("recommendations")
    if recs:
        st.session_state.recommendations = pd.DataFrame(recs)
        st.session_state.generated = True
    elif saved.get("generated"):
        st.session_state.generated = True


def sync_complete(store, resource_id: str, widget_key: str):
    completed = set(st.session_state.completed_ids)
    if st.session_state.get(widget_key):
        completed.add(resource_id)
    else:
        completed.discard(resource_id)
    st.session_state.completed_ids = list(completed)
    persist(store)


def render_course(resource: dict, why: str | None = None, complete_key: str | None = None, store=None):
    skills = resource.get("skills") or []
    skill_label = skills if isinstance(skills, str) else " · ".join(skills)
    title = html.escape(str(resource.get("title") or ""))
    description = html.escape(str(resource.get("description") or ""))
    provider = html.escape(str(resource.get("provider") or "Catalog"))
    prerequisites = html.escape(str(resource.get("prerequisites") or "None"))

    st.markdown(
        f"""
        <div class="course">
            <div class="course-meta">{provider} · {html.escape(str(resource.get("type")))} · {html.escape(str(resource.get("level")))} · {html.escape(str(resource.get("duration")))}</div>
            <h3>{title}</h3>
            <p>{description}</p>
            <p><b>Skills:</b> {html.escape(str(skill_label))} &nbsp;·&nbsp; <b>Prerequisites:</b> {prerequisites}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns([1, 1, 3])
    with cols[0]:
        url = resource.get("url")
        if url:
            st.link_button("Open resource", url, use_container_width=True)
    if complete_key:
        with cols[1]:
            resource_id = resource["id"]
            widget_key = f"{complete_key}-{resource_id}"
            if widget_key not in st.session_state:
                st.session_state[widget_key] = resource_id in st.session_state.completed_ids
            st.checkbox(
                "Completed",
                key=widget_key,
                on_change=sync_complete,
                args=(store, resource_id, widget_key),
            )
    if why:
        st.markdown(f'<p class="why">{html.escape(str(why))}</p>', unsafe_allow_html=True)


def load_demo_learner(store):
    if st.session_state.get("_demo_loaded"):
        return
    saved = store.get_learner(DEMO_USER["email"])
    if saved:
        apply_learner(saved)
        if saved.get("name"):
            st.session_state.user["name"] = saved["name"]
    st.session_state._demo_loaded = True


def render_app(store, resources):
    user = st.session_state.user
    st.markdown(
        f"""
        <div class="topbar">
          <div class="brand">LearnPath <span class="violet">AI</span></div>
          <div class="user-pill">{html.escape(user["name"])} · {html.escape(user["email"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### Learner")
        name = st.text_input("Name", value=user["name"], key="display_name")
        goal = st.selectbox("Career goal", list(CAREER_SKILLS.keys()), key="career_goal")
        experience = st.selectbox(
            "Experience",
            ["Beginner", "Intermediate", "Advanced"],
            key="experience_level",
        )
        interests = st.text_input("Interests", value="Python, data, real projects", key="interests_text")
        hours = st.slider("Hours / week", 2, 30, 10, key="hours_week")

        st.divider()
        st.caption("Self-assess the skills this career needs.")
        for skill in CAREER_SKILLS[goal]:
            skill_key = f"skill-{skill}"
            if skill_key not in st.session_state:
                st.session_state[skill_key] = int(
                    st.session_state.skills.get(skill, DEFAULT_SKILLS.get(skill, 0))
                )
            st.slider(skill, min_value=0, max_value=100, step=5, key=skill_key)
            st.session_state.skills[skill] = int(st.session_state[skill_key])

        st.divider()
        if st.button("Save to backend", use_container_width=True):
            persist(store, extra={"name": name, "goal": goal, "experience": experience, "interests": interests, "hours": hours})
            st.success(f"Saved to {store.backend}.")
        if st.button("Reset demo session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.caption(f"Source: {store.backend}")

    st.session_state.user["name"] = name

    gaps = calculate_skill_gaps(goal, st.session_state.skills)
    path = build_path(goal)
    stats = progress_stats(path, st.session_state.completed_ids)

    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Personalized learning intelligence</div>
            <h1 class="hero-title">Turn a career goal into a sequenced, explainable path.</h1>
            <p class="hero-copy">
                LearnPath AI reads your goal, finds skill gaps, then ranks real courses and projects
                with TF-IDF, cosine similarity, and prerequisites. Your account keeps the plan.
            </p>
            <div class="chip-row">
                <div class="chip hot">TF-IDF ranking</div>
                <div class="chip">Skill-gap aware</div>
                <div class="chip">Prerequisite roadmap</div>
                <div class="chip">Saved with login</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Plan", "Skill gaps", "Roadmap", "Catalog", "Progress"]
    )

    with tab1:
        st.subheader("Describe where you want to go")
        if "goal_area" not in st.session_state:
            st.session_state.goal_area = st.session_state.goal_text or (
                f"I know some Python. I want to become a {goal} and get job-ready in 6 months."
            )
        user_goal = st.text_area(
            "Your goal",
            height=110,
            label_visibility="collapsed",
            key="goal_area",
        )
        st.session_state.goal_text = user_goal

        if st.button("Generate personalized plan", type="primary"):
            analysis = analyze_user_goal(user_goal)
            recs = recommend(
                goal=goal,
                experience=experience,
                interests=interests,
                user_goal=user_goal,
                resources=resources,
                gaps=gaps,
            )
            st.session_state.analysis = analysis
            st.session_state.recommendations = recs
            st.session_state.generated = True
            persist(store)

        if st.session_state.generated and st.session_state.analysis is not None:
            analysis = st.session_state.analysis
            recs = st.session_state.recommendations
            if isinstance(recs, list):
                recs = pd.DataFrame(recs)
            top_gap = gaps[0] if gaps else {"skill": "foundations", "gap": 0}

            c1, c2, c3, c4 = st.columns(4)
            cards = [
                ("Detected skills", ", ".join(analysis.get("skills") or []) or "None stated"),
                ("Objective", analysis.get("objective", "")),
                ("Timeline", analysis.get("timeline", "")),
                ("Largest gap", f"{top_gap['skill']} · {top_gap['gap']}%"),
            ]
            for col, (label, value) in zip([c1, c2, c3, c4], cards):
                with col:
                    st.markdown(
                        f'<div class="stat"><b>{html.escape(str(value))}</b><span>{html.escape(label)}</span></div>',
                        unsafe_allow_html=True,
                    )

            st.info(
                f"{name}, the plan targets **{goal}** at a **{experience.lower()}** level. "
                f"{top_gap['skill']} is the widest gap, so early resources lean that direction."
            )

            st.markdown("#### Recommended next resources")
            for _, row in recs.iterrows():
                render_course(row.to_dict(), why=row.get("why"), store=store)
        else:
            st.write("Write a short goal, then generate a plan. Completions and the path save to your account.")

    with tab2:
        st.subheader(f"What {goal}s typically need")
        st.write("White is where you are. Coral marks the remaining gap.")
        for item in gaps:
            st.markdown('<div class="gap-row">', unsafe_allow_html=True)
            left, right = st.columns([3, 1])
            with left:
                st.write(f"**{item['skill']}** — {item['current']}% of {item['required']}%")
                st.progress(min(item["current"] / 100, 1.0))
            with right:
                st.metric("Gap", f"{item['gap']}%")
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("#### Start here")
        for item in gaps[:3]:
            if item["gap"] > 0:
                st.warning(f"**{item['skill']}** still needs about {item['gap']} points.")

    with tab3:
        st.subheader("Prerequisite-aware sequence")
        st.write(weekly_plan(hours, path))
        for index, step in enumerate(path, start=1):
            done = "Done" if step["id"] in st.session_state.completed_ids else "Up next"
            st.markdown(
                f"""
                <div class="phase">
                    <div class="phase-index">{index:02d}</div>
                    <div class="phase-copy"><small>{html.escape(str(step['phase']))} · {html.escape(str(step['focus']))} · {done}</small></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            render_course(step, complete_key="path", store=store)

    with tab4:
        st.subheader("Full learning catalog")
        st.write("Curated courses and projects with direct links. Filter, then open the ones that fit.")
        types = st.multiselect("Type", sorted({item["type"] for item in resources}), default=["Course", "Project"])
        levels = st.multiselect(
            "Level",
            ["Beginner", "Intermediate", "Advanced"],
            default=["Beginner", "Intermediate", "Advanced"],
        )
        query = st.text_input("Search title, provider, or skill")
        filtered = []
        for item in resources:
            if item["type"] not in types or item["level"] not in levels:
                continue
            blob = " ".join(
                [
                    item["title"],
                    item["provider"],
                    item["description"],
                    " ".join(item.get("skills") or []),
                ]
            ).lower()
            if query and query.lower() not in blob:
                continue
            filtered.append(item)
        st.caption(f"{len(filtered)} resources")
        for item in filtered:
            render_course(item, store=store)

    with tab5:
        st.subheader("Progress")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Roadmap progress", f"{stats['overall']}%")
        m2.metric("Courses", f"{stats['courses_done']}/{stats['courses_total']}")
        m3.metric("Projects", f"{stats['projects_done']}/{stats['projects_total']}")
        m4.metric("Hours / week", hours)
        st.progress(stats["overall"] / 100)

        remaining = stats["remaining"]
        if remaining:
            nxt = remaining[0]
            st.success(f"Next step: **{nxt['title']}** — {nxt['focus'].lower()}.")
            st.link_button("Open next resource", nxt["url"])
        else:
            st.success("Roadmap complete. Add a harder catalog item or a new career target.")

        if st.button("Save progress"):
            persist(store)
            store.save_progress(account_key(), list(st.session_state.completed_ids), dict(st.session_state.skills))
            st.toast(f"Progress saved to {store.backend}.")

        st.divider()
        st.subheader("Was this path useful?")
        feedback = st.radio(
            "Feedback",
            ["Very useful", "Useful", "Too difficult", "Too easy", "Not useful"],
            horizontal=True,
            label_visibility="collapsed",
        )
        if st.button("Submit feedback"):
            persist(store)
            store.add_feedback(account_key(), feedback)
            adaptations = {
                "Too difficult": "Next recommendations will stay closer to beginner and prerequisite resources.",
                "Too easy": "Next recommendations will lean intermediate and advanced work.",
                "Not useful": "We will de-emphasize similar titles and surface alternatives from the catalog.",
            }
            st.info(adaptations.get(feedback, "We’ll keep the current sequencing strategy."))

    st.markdown(
        f'<p class="footer-note">LearnPath AI · Pathwise-inspired dark UI · accounts persist in {html.escape(store.backend)}</p>',
        unsafe_allow_html=True,
    )


init_state()
store = get_store()
resources = store.list_resources()
load_demo_learner(store)
render_app(store, resources)
