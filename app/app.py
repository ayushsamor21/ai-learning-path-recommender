import re
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="LearnPath AI",
    page_icon="LP",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    padding: 28px;
    border-radius: 18px;
    border: 1px solid rgba(128,128,128,0.25);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 18px;
    opacity: 0.75;
}

.card {
    padding: 20px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.25);
    margin-bottom: 15px;
}

.phase {
    padding: 20px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.25);
    margin-bottom: 14px;
}

.small-label {
    font-size: 13px;
    opacity: 0.65;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LEARNING RESOURCES
# ============================================================

resources = pd.DataFrame([
    {
        "title": "Python Fundamentals",
        "type": "Course",
        "level": "Beginner",
        "skills": "python programming logic fundamentals",
        "prerequisites": "None",
        "duration": "2 weeks"
    },
    {
        "title": "Advanced Python",
        "type": "Course",
        "level": "Intermediate",
        "skills": "python oop functions algorithms programming",
        "prerequisites": "Python Fundamentals",
        "duration": "2 weeks"
    },
    {
        "title": "NumPy for Data Science",
        "type": "Course",
        "level": "Beginner",
        "skills": "python numpy arrays numerical computing data",
        "prerequisites": "Python Fundamentals",
        "duration": "1 week"
    },
    {
        "title": "Pandas for Data Analysis",
        "type": "Course",
        "level": "Beginner",
        "skills": "python pandas data analysis preprocessing",
        "prerequisites": "Python Fundamentals, NumPy",
        "duration": "1 week"
    },
    {
        "title": "Statistics for Machine Learning",
        "type": "Course",
        "level": "Intermediate",
        "skills": "statistics probability mathematics machine learning",
        "prerequisites": "Python Fundamentals",
        "duration": "2 weeks"
    },
    {
        "title": "Machine Learning Fundamentals",
        "type": "Course",
        "level": "Intermediate",
        "skills": "machine learning regression classification python statistics",
        "prerequisites": "Python Pandas Statistics",
        "duration": "3 weeks"
    },
    {
        "title": "Deep Learning Fundamentals",
        "type": "Course",
        "level": "Advanced",
        "skills": "deep learning neural networks tensorflow artificial intelligence",
        "prerequisites": "Machine Learning",
        "duration": "3 weeks"
    },
    {
        "title": "SQL for Data Science",
        "type": "Course",
        "level": "Beginner",
        "skills": "sql database queries data analysis",
        "prerequisites": "None",
        "duration": "1 week"
    },
    {
        "title": "Git and GitHub",
        "type": "Course",
        "level": "Beginner",
        "skills": "git github version control collaboration",
        "prerequisites": "None",
        "duration": "3 days"
    },
    {
        "title": "Data Visualization",
        "type": "Course",
        "level": "Beginner",
        "skills": "python pandas visualization charts analytics",
        "prerequisites": "Python Pandas",
        "duration": "1 week"
    },
    {
        "title": "Student Performance Predictor",
        "type": "Project",
        "level": "Intermediate",
        "skills": "python pandas machine learning regression",
        "prerequisites": "Python Pandas Machine Learning",
        "duration": "1 week"
    },
    {
        "title": "Customer Churn Prediction",
        "type": "Project",
        "level": "Intermediate",
        "skills": "python pandas classification machine learning",
        "prerequisites": "Python Pandas Machine Learning",
        "duration": "1 week"
    },
    {
        "title": "Sales Analytics Dashboard",
        "type": "Project",
        "level": "Intermediate",
        "skills": "python pandas sql visualization analytics",
        "prerequisites": "Python SQL Pandas",
        "duration": "1 week"
    },
    {
        "title": "End-to-End ML Deployment",
        "type": "Project",
        "level": "Advanced",
        "skills": "machine learning python streamlit deployment mlops",
        "prerequisites": "Machine Learning Git",
        "duration": "2 weeks"
    }
])

# ============================================================
# CAREER SKILL REQUIREMENTS
# ============================================================

career_skills = {

    "Machine Learning Engineer": {
        "Python": 80,
        "NumPy": 70,
        "Pandas": 75,
        "Statistics": 75,
        "Machine Learning": 90,
        "Deep Learning": 70,
        "Git": 60
    },

    "Data Scientist": {
        "Python": 80,
        "SQL": 75,
        "Statistics": 85,
        "NumPy": 65,
        "Pandas": 80,
        "Machine Learning": 80
    },

    "Software Engineer": {
        "Python": 80,
        "Git": 75
    },

    "Data Analyst": {
        "Python": 65,
        "SQL": 85,
        "Statistics": 70,
        "Pandas": 80,
        "Data Visualization": 80
    }
}

# ============================================================
# LEARNER SKILLS
# ============================================================

current_skills = {
    "Python": 70,
    "SQL": 40,
    "Statistics": 30,
    "NumPy": 20,
    "Pandas": 25,
    "Machine Learning": 0,
    "Deep Learning": 0,
    "Git": 30,
    "Data Visualization": 20
}

# ============================================================
# CAREER ROADMAPS
# ============================================================

learning_paths = {

    "Machine Learning Engineer": [
        ("Phase 1", "Python Fundamentals",
         "Build programming and problem-solving foundations.",
         "Foundation"),

        ("Phase 2", "NumPy and Pandas",
         "Learn numerical computing and data preprocessing.",
         "Data Processing"),

        ("Phase 3", "Statistics for Machine Learning",
         "Build probability and statistics foundations.",
         "Statistics"),

        ("Phase 4", "Machine Learning Fundamentals",
         "Learn regression, classification and evaluation.",
         "Machine Learning"),

        ("Phase 5", "Student Performance Predictor",
         "Build a real-world predictive ML project.",
         "Project"),

        ("Phase 6", "Deep Learning Fundamentals",
         "Move into neural networks and advanced AI.",
         "Advanced AI")
    ],

    "Data Scientist": [
        ("Phase 1", "Python Fundamentals",
         "Build programming foundations.",
         "Foundation"),

        ("Phase 2", "SQL for Data Science",
         "Learn database querying and analysis.",
         "Database"),

        ("Phase 3", "Pandas for Data Analysis",
         "Clean and analyze real-world datasets.",
         "Data Analysis"),

        ("Phase 4", "Statistics for Machine Learning",
         "Develop statistical reasoning.",
         "Statistics"),

        ("Phase 5", "Machine Learning Fundamentals",
         "Build predictive models.",
         "Machine Learning"),

        ("Phase 6", "Customer Churn Prediction",
         "Apply data science to a real-world problem.",
         "Project")
    ],

    "Software Engineer": [
        ("Phase 1", "Python Fundamentals",
         "Build programming foundations.",
         "Foundation"),

        ("Phase 2", "Advanced Python",
         "Learn OOP, functions and advanced programming.",
         "Programming"),

        ("Phase 3", "Git and GitHub",
         "Learn version control and collaboration.",
         "Development"),

        ("Phase 4", "Algorithms and Problem Solving",
         "Strengthen algorithmic thinking.",
         "Algorithms"),

        ("Phase 5", "Software Development Project",
         "Build a complete software application.",
         "Project")
    ],

    "Data Analyst": [
        ("Phase 1", "Python Fundamentals",
         "Learn Python for analytics.",
         "Foundation"),

        ("Phase 2", "SQL for Data Science",
         "Query and manipulate structured data.",
         "Database"),

        ("Phase 3", "Pandas for Data Analysis",
         "Clean and analyze datasets.",
         "Data Analysis"),

        ("Phase 4", "Data Visualization",
         "Create meaningful analytical dashboards.",
         "Visualization"),

        ("Phase 5", "Sales Analytics Dashboard",
         "Build a complete analytics project.",
         "Project")
    ]
}

# ============================================================
# NATURAL LANGUAGE PROFILE ANALYZER
# ============================================================

def analyze_user_goal(text):

    text_lower = text.lower()

    detected_skills = []

    skill_keywords = {
        "Python": ["python"],
        "SQL": ["sql", "database"],
        "Statistics": ["statistics", "statistical", "probability"],
        "Machine Learning": [
            "machine learning",
            "ml"
        ],
        "Deep Learning": [
            "deep learning",
            "neural network"
        ],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "Git": ["git", "github"],
        "Data Visualization": [
            "visualization",
            "tableau",
            "power bi"
        ]
    }

    for skill, keywords in skill_keywords.items():

        for keyword in keywords:

            if keyword in text_lower:

                detected_skills.append(skill)
                break

    timeline = "Not specified"

    match = re.search(
        r"(\d+)\s*(month|months|week|weeks|year|years)",
        text_lower
    )

    if match:

        timeline = (
            f"{match.group(1)} "
            f"{match.group(2)}"
        )

    objective = "Skill development"

    if any(
        word in text_lower
        for word in [
            "job",
            "career",
            "employment",
            "placement"
        ]
    ):
        objective = "Career / Job Preparation"

    elif any(
        word in text_lower
        for word in [
            "project",
            "build",
            "application"
        ]
    ):
        objective = "Project Development"

    return {
        "skills": detected_skills,
        "timeline": timeline,
        "objective": objective
    }

# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

def get_recommendations(
    goal,
    experience,
    interests,
    user_goal
):

    query = (
        goal + " " +
        experience + " " +
        interests + " " +
        user_goal
    )

    documents = (
        resources["skills"] + " " +
        resources["title"]
    ).tolist()

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(
        documents + [query]
    )

    similarity = cosine_similarity(
        matrix[-1],
        matrix[:-1]
    ).flatten()

    result = resources.copy()

    result["similarity"] = similarity

    difficulty_score = {
        "Beginner": 1,
        "Intermediate": 2,
        "Advanced": 3
    }

    user_level = difficulty_score[experience]

    result["difficulty_score"] = result[
        "level"
    ].map(difficulty_score)

    result["level_fit"] = (
        1 /
        (
            1 +
            abs(
                result["difficulty_score"]
                - user_level
            )
        )
    )

    result["score"] = (
        result["similarity"] * 0.7 +
        result["level_fit"] * 0.3
    )

    if experience == "Beginner":

        result = result[
            result["level"] != "Advanced"
        ]

    return result.sort_values(
        "score",
        ascending=False
    ).head(6)

# ============================================================
# SKILL GAP ANALYZER
# ============================================================

def calculate_skill_gaps(goal):

    required = career_skills[goal]

    gaps = []

    for skill, required_level in required.items():

        current = current_skills.get(
            skill,
            0
        )

        gap = max(
            required_level - current,
            0
        )

        gaps.append({
            "skill": skill,
            "current": current,
            "required": required_level,
            "gap": gap
        })

    return sorted(
        gaps,
        key=lambda x: x["gap"],
        reverse=True
    )

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

    <div class="hero-title">
    LearnPath AI
    </div>

    <div class="hero-subtitle">
    AI-Powered Personalized Learning Path Recommender
    </div>

    <p>
    Transform your career goal into a personalized,
    prerequisite-aware learning roadmap using
    explainable AI and skill-gap analysis.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Learner Profile")

name = st.sidebar.text_input(
    "Name",
    "Ajay"
)

goal = st.sidebar.selectbox(
    "Career Goal",
    list(career_skills.keys())
)

experience = st.sidebar.selectbox(
    "Experience Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

interests = st.sidebar.text_input(
    "Interests",
    "AI, Python, Data Science"
)

hours = st.sidebar.slider(
    "Learning Hours / Week",
    2,
    30,
    10
)

st.sidebar.divider()

st.sidebar.subheader(
    "Profile Summary"
)

st.sidebar.write(
    f"**Learner:** {name}"
)

st.sidebar.write(
    f"**Target:** {goal}"
)

st.sidebar.write(
    f"**Level:** {experience}"
)

st.sidebar.write(
    f"**Commitment:** {hours} hrs/week"
)

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "AI Assistant",
    "Skill Gap",
    "Learning Path",
    "Progress"
])

# ============================================================
# AI ASSISTANT
# ============================================================

with tab1:

    st.header("AI Learning Assistant")

    user_goal = st.text_area(
        "Describe your learning goal",
        value=(
            f"I want to become a {goal} "
            "and build real-world projects."
        ),
        height=120
    )

    if st.button(
        "Generate Personalized Plan",
        type="primary"
    ):

        profile = analyze_user_goal(
            user_goal
        )

        recommendations = get_recommendations(
            goal,
            experience,
            interests,
            user_goal
        )

        gaps = calculate_skill_gaps(
            goal
        )

        st.success(
            f"Personalized plan generated for {name}."
        )

        # ----------------------------------------------------
        # ANALYZED PROFILE
        # ----------------------------------------------------

        st.subheader(
            "AI-Analyzed Learning Profile"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.write("Detected Skills")

            if profile["skills"]:

                st.write(
                    ", ".join(
                        profile["skills"]
                    )
                )

            else:

                st.write(
                    "No explicit skills detected"
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.write("Learning Objective")

            st.write(
                profile["objective"]
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.write("Timeline")

            st.write(
                profile["timeline"]
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # EXPLANATION
        # ----------------------------------------------------

        top_gap = gaps[0]

        st.subheader(
            "Why This Learning Path?"
        )

        st.info(
            f"The system identified **{top_gap['skill']}** "
            f"as your largest skill gap at **{top_gap['gap']}%**. "
            f"Recommendations are ranked using goal similarity, "
            f"learner experience and skill-gap priorities."
        )

        # ----------------------------------------------------
        # RECOMMENDATIONS
        # ----------------------------------------------------

        st.subheader(
            "AI-Recommended Resources"
        )

        for _, resource in recommendations.iterrows():

            with st.container(border=True):

                col1, col2, col3 = st.columns(
                    [3, 1, 1]
                )

                with col1:

                    st.markdown(
                        f"### {resource['title']}"
                    )

                with col2:

                    st.write(
                        resource["type"]
                    )

                with col3:

                    st.write(
                        resource["level"]
                    )

                st.write(
                    f"Duration: "
                    f"{resource['duration']}"
                )

                st.write(
                    f"Skills: "
                    f"{resource['skills'].title()}"
                )

                st.write(
                    f"Prerequisites: "
                    f"{resource['prerequisites']}"
                )

                st.success(
                    "Recommended because it aligns "
                    "with your target career, current "
                    "level and learning objective."
                )

# ============================================================
# SKILL GAP
# ============================================================

with tab2:

    st.header(
        "Skill Gap Analysis"
    )

    st.write(
        f"Target career: **{goal}**"
    )

    gaps = calculate_skill_gaps(
        goal
    )

    for item in gaps:

        col1, col2, col3 = st.columns(
            [2, 1, 1]
        )

        with col1:

            st.write(
                f"**{item['skill']}**"
            )

        with col2:

            st.write(
                f"Current: "
                f"{item['current']}%"
            )

        with col3:

            st.write(
                f"Gap: "
                f"{item['gap']}%"
            )

        st.progress(
            min(
                item["current"] / 100,
                1
            )
        )

    st.divider()

    st.subheader(
        "Top Priority Skills"
    )

    for item in gaps[:3]:

        st.warning(
            f"**{item['skill']}** — "
            f"{item['gap']}% gap"
        )

# ============================================================
# LEARNING PATH
# ============================================================

with tab3:

    st.header(
        f"Personalized Roadmap"
    )

    st.write(
        f"Career target: **{goal}**"
    )

    st.write(
        "The roadmap follows a prerequisite-aware "
        "sequence from foundations to practical projects."
    )

    path = learning_paths[goal]

    for phase, title, description, category in path:

        st.markdown(
            f"""
            <div class="phase">

            <h3>
            {phase} — {title}
            </h3>

            <p>
            {description}
            </p>

            <small>
            Focus: {category}
            </small>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader(
        "Recommended Weekly Strategy"
    )

    st.write(
        f"Based on your availability of "
        f"**{hours} hours/week**, the system "
        f"recommends consistent weekly progression "
        f"through theory, practice and projects."
    )

# ============================================================
# PROGRESS
# ============================================================

with tab4:

    st.header(
        "Learning Progress Dashboard"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Overall Progress",
            "42%"
        )

    with col2:

        st.metric(
            "Courses Completed",
            "4"
        )

    with col3:

        st.metric(
            "Projects Completed",
            "1"
        )

    with col4:

        st.metric(
            "Skills Developing",
            "5"
        )

    st.progress(
        0.42
    )

    st.divider()

    st.subheader(
        "Skill Development"
    )

    for skill in career_skills[goal]:

        value = current_skills.get(
            skill,
            0
        )

        st.write(
            f"**{skill}: {value}%**"
        )

        st.progress(
            min(
                value / 100,
                1
            )
        )

    st.divider()

    gaps = calculate_skill_gaps(
        goal
    )

    next_skill = gaps[0]["skill"]

    st.subheader(
        "Next Recommended Action"
    )

    st.success(
        f"Focus next on **{next_skill}**. "
        f"It currently represents your largest "
        f"skill gap for the {goal} career path."
    )

    st.divider()

    st.subheader(
        "Learner Feedback"
    )

    feedback = st.radio(
        "How useful was your learning path?",
        [
            "Very useful",
            "Useful",
            "Too difficult",
            "Too easy",
            "Not useful"
        ]
    )

    if st.button(
        "Submit Feedback"
    ):

        st.success(
            f"Feedback recorded: {feedback}"
        )

        if feedback == "Too difficult":

            st.info(
                "Adaptation: prioritize prerequisite "
                "and beginner-level resources."
            )

        elif feedback == "Too easy":

            st.info(
                "Adaptation: prioritize intermediate "
                "and advanced resources."
            )

        elif feedback == "Not useful":

            st.info(
                "Adaptation: reduce similar-resource "
                "recommendations and explore alternatives."
            )

        else:

            st.info(
                "Adaptation: maintain the current "
                "learning strategy."
            )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "LearnPath AI | Explainable + Adaptive Personalized Learning"
)

