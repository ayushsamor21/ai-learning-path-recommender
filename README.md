# LearnPath AI

## AI-Powered Personalized Learning Path Recommender

LearnPath AI is an AI-powered personalized learning assistant that transforms a learner's career goal into a structured, explainable and prerequisite-aware learning roadmap.

The system analyzes learner goals, skills, experience level, interests and learning objectives to identify skill gaps and recommend relevant courses, projects and learning resources.

---

## Live Application

https://ai-learning-path-recommender-uuyrf2ejxzxg7zs3dkbfzz.streamlit.app/

## GitHub Repository

https://github.com/ayushsamor21/ai-learning-path-recommender

---

## Problem Statement

Online learning platforms provide thousands of courses and learning resources. However, learners often struggle to determine what they should learn first, which prerequisites they need, which skills they are missing, and how to build a structured roadmap toward a career.

LearnPath AI addresses this problem by generating a personalized learning roadmap based on the learner's career objective, current skills, experience and learning needs.

---

## Proposed Solution

LearnPath AI converts a learner's natural-language career goal into a structured learning path.

Workflow:

Learner Goal
    |
Learner Profile
    |
Goal Analysis
    |
Skill Gap Analysis
    |
Recommendation Engine
    |
Prerequisite-Aware Learning Path
    |
Progress Tracking
    |
Learner Feedback
    |
Adaptive Recommendations

---

## Key Features

- Conversational learning assistant
- Learner profiling
- Natural-language goal analysis
- Career-specific skill-gap analysis
- AI/ML-based resource recommendation
- TF-IDF vectorization
- Cosine similarity
- Experience-level matching
- Prerequisite-aware learning path
- Course recommendations
- Project recommendations
- Explainable recommendations
- Progress dashboard
- Feedback-based adaptation

---

## AI/ML Methodology

### TF-IDF Vectorization

TF-IDF converts learner goals and learning-resource descriptions into numerical feature vectors.

### Cosine Similarity

Cosine similarity measures the similarity between the learner's goal and available learning resources.

### Experience-Level Matching

Resources are categorized as Beginner, Intermediate or Advanced and are matched with the learner's experience level.

### Skill-Gap Analysis

The system compares the learner's current skills with skills required for the target career and identifies areas requiring improvement.

### Recommendation Ranking

Recommendations consider goal similarity, learner experience, skill gaps, resource relevance and prerequisites.

---

## Personalization

LearnPath AI creates a learner profile containing:

- Name
- Career goal
- Experience level
- Interests
- Existing skills
- Learning objective
- Learning timeline
- Weekly learning availability

---

## Example

Example learner input:

"I know basic Python and SQL. I am weak in statistics. I want to become a data scientist and get a job in 6 months."

The system identifies:

Target Career: Data Scientist

Existing Skills:
- Python
- SQL

Skill Gaps:
- Statistics
- Machine Learning

Learning Objective:
Career / Job Preparation

Timeline:
6 months

Example learning path:

Python Fundamentals
    |
SQL for Data Science
    |
NumPy for Data Science
    |
Pandas for Data Analysis
    |
Statistics for Machine Learning
    |
Machine Learning Fundamentals
    |
Data Science Project

---

## Explainable Recommendations

LearnPath AI explains why each resource was recommended.

Example:

Resource:
Statistics for Machine Learning

Why recommended:

- Statistics is important for the Data Scientist career path.
- Statistics is an identified skill gap.
- The resource matches the learner's target.
- The resource fits the learner's learning level.
- It provides a foundation for Machine Learning.

---

## System Architecture

Learner
   |
Streamlit Interface
   |
Learner Profile
   |
Natural Language Analysis
   |
Goal Analysis + Skill Gap Analysis
   |
Recommendation Engine
   |
TF-IDF + Cosine Similarity + Experience Matching
   |
Resource Dataset
   |
Recommendation Ranking
   |
Prerequisite-Aware Roadmap
   |
Progress Dashboard
   |
User Feedback

---

## User Interface

### AI Assistant

Learners describe their career goal and learning requirements using natural language.

### Skill Gap

The system identifies skills requiring improvement for the selected career.

### Learning Path

The system presents a structured sequence of learning resources.

### Progress

The dashboard provides an overview of learning progress and recommended next actions.

---

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Web Framework | Streamlit |
| Data Processing | Pandas |
| Machine Learning | Scikit-learn |
| NLP / Recommendation | TF-IDF |
| Similarity | Cosine Similarity |
| Database | MongoDB (with local JSON fallback) |
| Version Control | Git |
| Repository | GitHub |
| Deployment | Streamlit Community Cloud |

---

## Project Structure

ai-learning-path-recommender/
|
+-- app/
|   +-- app.py
|
+-- src/
|   +-- catalog.py
|   +-- db.py
|   +-- nlp.py
|   +-- recommender.py
|
+-- app.py
+-- requirements.txt
+-- .env.example
+-- README.md
+-- .gitignore

---

## Local Setup

### Prerequisites

- Python 3.10 or later
- Git
- Internet connection

### Clone Repository

git clone https://github.com/ayushsamor21/ai-learning-path-recommender.git

### Navigate to Project

cd ai-learning-path-recommender

### Create Virtual Environment

macOS / Linux:

python3 -m venv venv
source venv/bin/activate

Windows:

python -m venv venv
venv\Scripts\activate

### Install Dependencies

pip install -r requirements.txt

### Configure MongoDB (optional)

Copy `.env.example` to `.env` and set `MONGODB_URI`.

If MongoDB is unavailable, the app stores profiles, progress and feedback in a local JSON file.

On Streamlit Community Cloud, add `MONGODB_URI` under App settings → Secrets.

### Run Application

streamlit run app/app.py

### Open Browser

http://localhost:8501

---

## Deployment

Live Application:

https://ai-learning-path-recommender-uuyrf2ejxzxg7zs3dkbfzz.streamlit.app/

GitHub Repository:

https://github.com/ayushsamor21/ai-learning-path-recommender

---

## Innovation

Traditional recommendation systems mainly provide related courses.

LearnPath AI focuses on the complete learner journey:

Career Goal
    |
Current Skills
    |
Skill Gap
    |
Recommended Resources
    |
Prerequisites
    |
Learning Sequence
    |
Projects
    |
Progress

This makes the system more than a simple course search engine.

---

## Challenges

- Converting free-form learner goals into structured information
- Identifying relevant skills
- Matching learner objectives with resource descriptions
- Maintaining prerequisite relationships
- Balancing resource relevance with learner difficulty
- Providing recommendation explanations
- Creating a simple interface for a complex recommendation workflow

---

## Current Limitations

- The learning-resource catalog is curated (with real course/project links) rather than fetched from a live course API.
- Skill levels are based on learner self-assessment.
- Natural-language analysis uses structured/rule-based extraction.
- Recommendations are content-based.
- The current prototype does not use an external generative AI API.

---

## Future Scope

- LLM-powered conversational tutoring
- Advanced natural-language understanding
- Real-time learner performance analysis
- Automated assessments
- Knowledge graphs for prerequisites
- Online learning platform integration
- Resume analysis
- Job-description analysis
- Automatic career skill-gap analysis
- Advanced adaptive recommendation models
- Personalized project generation
- Learning analytics

---

## Expected Impact

LearnPath AI helps learners answer five important questions:

1. What should I learn?
2. Why should I learn it?
3. What prerequisite do I need?
4. What skill gap does it address?
5. What should I learn next?

---

## Conclusion

LearnPath AI transforms an individual's career objective into a personalized, explainable and structured learning journey.

By combining learner profiling, natural-language goal analysis, skill-gap analysis, TF-IDF, cosine similarity, experience-level matching and prerequisite-aware learning paths, the system demonstrates a practical approach to personalized learning intelligence.

### From Career Goal to Personalized Learning Path

---

## Team

National Institute of Technology Nagaland

- Guguloth Ajay
- Dondapati Harshavardhini
- Maroju Adi Lakshmi Renuka
- Kondari Venkata Teja
