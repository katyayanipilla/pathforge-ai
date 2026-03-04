import streamlit as st
from ai_engine import *
from datetime import datetime
from database import init_db, save_quiz_attempt, save_interview_result, save_skill_gap, save_resume
from public_profile import show_public_profile
from database import register_user, login_user
from database import init_db

st.markdown("""
<style>

/* MAIN TEXT COLOR FIX */
html, body, [class*="css"]  {
    color: white !important;
}

/* Headers brighter */
h1, h2, h3, h4 {
    color: #ffffff !important;
}

/* Labels */
label {
    color: #f1f5f9 !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #1e293b);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

init_db()
# ==========================================
# AUTO LOAD PROFILE FROM SHAREABLE LINK
# ==========================================

query_params = st.query_params

if "profile" in query_params:
    from public_profile import show_public_profile
    show_public_profile(query_params["profile"])
    st.stop()

st.set_page_config(page_title="AI CAREER ROADMAP GENERATOR", layout="wide")

st.markdown("""
<style>

/* ===== App Background ===== */
.stApp {
    background: linear-gradient(135deg, #0f172a, #0b1120);
    color: #ffffff !important;
}

/* ===== Fix Grey Text ===== */
html, body, [class*="css"]  {
    color: #ffffff !important;
}

/* ===== Headings ===== */
h1 {
    font-size: 42px !important;
    font-weight: 800 !important;
    text-align: center;
    color: #ffffff !important;
}

h2, h3 {
    color: #38bdf8 !important;
    font-weight: 700 !important;
}

/* ===== Sidebar Styling ===== */
[data-testid="stSidebar"] {
    background-color: #0b1120;
}

/* Highlight Selected Sidebar */
div[role="radiogroup"] > label {
    background-color: #1e293b;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 6px;
    color: white !important;
}

div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
    display: none;
}

div[role="radiogroup"] > label:hover {
    background-color: #2563eb;
    transform: scale(1.02);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #2563eb, #38bdf8);
    color: white;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #1d4ed8, #0ea5e9);
    transform: scale(1.03);
}

/* Cards */
.card {
    background-color: #1e293b;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

/* Inputs */
input, textarea {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)
# =====================================================
# SESSION STATE INIT
# =====================================================
if "interview_scores" not in st.session_state:
    st.session_state.interview_scores = []

if "job_readiness_score" not in st.session_state:
    st.session_state.job_readiness_score = 0
    
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "mastery" not in st.session_state:
    st.session_state.mastery = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "interview_question" not in st.session_state:
    st.session_state.interview_question = None
    
    
# ===============================
# AUTH SYSTEM
# ===============================

# ===============================
# MODERN CENTERED AUTH UI
# ===============================

# ===============================
# PERFECT CENTERED LOGIN UI
# ===============================

# ===============================
# SIMPLE CLEAN CENTERED LOGIN
# ===============================

import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    # Remove Streamlit top space
    st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        max-width: 500px;
    }

    .stApp {
        background: linear-gradient(135deg, #020617, #0f172a);
    }

    .title {
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        color: white;
        margin-bottom: 30px;
    }

    .stTextInput > div > div > input {
        height: 45px;
        border-radius: 8px;
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
    }

    .stButton > button {
        width: 100%;
        height: 45px;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 10px;
        background: linear-gradient(90deg,#7c3aed,#38bdf8);
        border: none;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # CENTER TITLE
    st.markdown("<div class='title'>🚀 AI CAREER ROADMAP GENERATOR</div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    from database import register_user, login_user

    # LOGIN BUTTON (below password)
    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    # REGISTER BUTTON (below login)
    if st.button("Register"):
        if username and password:
            if register_user(username, password):
                st.success("Account Created! Please Login.")
            else:
                st.error("Username already exists.")
        else:
            st.warning("Please fill all fields.")

    st.stop()
# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

st.markdown("<h1 style='text-align:center;'>🚀 AI CAREER ROADMAP GENERATOR</h1>", unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", [
    "🏠Dashboard",
    "📚Roadmap",
    "🧠Daily Quiz",
    "📊Skill Gap",
    "🎤Interview",
    "👩‍🏫Mentor Chat",
    "📄Resume Builder",
    "🎓Career Predictor",
    "👤Public Profile"
])

# =====================================================
# DASHBOARD
# =====================================================

if page == "🏠Dashboard":

    st.markdown("<h3 style='text-align:center; color:#94a3b8;'>AI Career Intelligence Dashboard</h3>", unsafe_allow_html=True)

    quiz_scores = list(st.session_state.mastery.values())

    avg_quiz = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0

    avg_interview = (
        sum(st.session_state.interview_scores) / len(st.session_state.interview_scores)
        if st.session_state.interview_scores else 0
    )

    job_ready = st.session_state.job_readiness_score

    career_score = (avg_quiz * 0.4) + (avg_interview * 0.3) + (job_ready * 0.3)

    st.markdown("## 🧠 Career Intelligence Score")
    st.progress(career_score / 100)
    st.markdown(f"<h2 style='color:#38bdf8;'>{round(career_score,2)} / 100</h2>", unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Quiz Performance")
        st.write(round(avg_quiz,2))

        st.subheader("🎤 Interview Performance")
        st.write(round(avg_interview,2))

    with col2:
        st.subheader("📈 Job Readiness")
        st.write(round(job_ready,2))

    if quiz_scores:
        weakest = min(st.session_state.mastery, key=st.session_state.mastery.get)
        strongest = max(st.session_state.mastery, key=st.session_state.mastery.get)

        st.markdown("---")
        st.subheader("🎯 Weakest Topic")
        st.write(weakest)

        st.subheader("🔥 Strongest Topic")
        st.write(strongest)

    if career_score < 50:
        st.warning("Focus on fundamentals and consistency.")
    elif career_score < 75:
        st.info("You're progressing well. Improve interview depth.")
    else:
        st.success("You are nearing job-ready level. Start applying confidently.")
        
# =====================================================
# ROADMAP
# =====================================================

elif page == "📚Roadmap":

    st.title("🗺 AI Career Roadmap")

    role = st.text_input("Target Role")
    duration = st.selectbox("Duration (Months)", [3, 6, 9])
    level = st.selectbox("Your Level", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate Roadmap"):

        with st.spinner("Generating structured roadmap..."):
            roadmap = generate_roadmap(role, duration, level)

        if roadmap:
            for week in roadmap:
                st.markdown("---")
                st.markdown(f"""
                   <div class="card">
                   <h2>Week {week['week_number']} — {week['title']}</h2>
                   """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("### 📚 Concepts")
                for c in week["concepts"]:
                    st.write("-", c)

                st.markdown("### 🎓 Resources")
                for r in week["learning_resources"]:
                    st.write("-", r)

                st.markdown("### 🚀 Project")
                st.write(week["project"])

                st.markdown("### 🎯 Outcome")
                st.write(week["outcome"])

        else:
            st.error("Roadmap generation failed.")

# =====================================================
# DAILY QUIZ (25 Questions)
# =====================================================

elif page == "🧠Daily Quiz":

    st.title("🧠 Adaptive Daily Quiz")

    topic = st.text_input("Topic")
    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate 25 Question Quiz"):

        with st.spinner("Generating questions..."):
            st.session_state.quiz_data = generate_daily_quiz(topic, difficulty)
            st.session_state.quiz_submitted = False
            st.session_state.quiz_score = 0

    if st.session_state.quiz_data:

        for i, q in enumerate(st.session_state.quiz_data):

            st.markdown(f"### Q{i+1}: {q['question']}")

            selected = st.radio(
                "Choose answer",
                q["options"],
                key=f"quiz_{i}"
            )

        if st.button("Submit Quiz"):

            score = 0

            for i, q in enumerate(st.session_state.quiz_data):
                user_ans = st.session_state[f"quiz_{i}"]

                if user_ans == q["correct_answer"]:
                    score += 1

            percentage = (score / len(st.session_state.quiz_data)) * 100
            save_quiz_attempt("st.session_state.username", topic, percentage)

            st.session_state.quiz_score = percentage
            st.session_state.mastery[topic] = percentage
            st.session_state.quiz_submitted = True

        if st.session_state.quiz_submitted:

            st.success(f"Final Score: {round(st.session_state.quiz_score,2)}%")

            st.markdown("## ❌ Incorrect Answers Explanation")

            for i, q in enumerate(st.session_state.quiz_data):
                user_ans = st.session_state[f"quiz_{i}"]

                if user_ans != q["correct_answer"]:
                    st.markdown(f"**Q{i+1}: {q['question']}**")
                    st.write("Correct Answer:", q["correct_answer"])
                    st.write("Explanation:", q["explanation"])
                    st.markdown("---")

# =====================================================
# SKILL GAP
# =====================================================

elif page == "📊Skill Gap":

    st.title("📊 Job Ready Skill Gap Analyzer")

    skills = st.text_area("Your Current Skills")
    role = st.text_input("Target Role")

    if st.button("Analyze Skill Gap"):

        with st.spinner("Analyzing..."):
            result = skill_gap_analysis(skills, role)
            st.write("DEBUG RESULT:", result)

        if result and "job_readiness_score" in result:

            save_skill_gap(
                st.session_state.username,
                role,
                result["job_readiness_score"]
            )

            st.session_state.job_readiness_score = result["job_readiness_score"]

            st.subheader("Strengths")
            st.write(result.get("strengths", "N/A"))

            st.subheader("Missing Skills")
            st.write(result.get("missing_skills", "N/A"))

            st.subheader("Recommended Projects")
            st.write(result.get("recommended_projects", "N/A"))

            st.subheader("Job Readiness Score")
            st.progress(result["job_readiness_score"] / 100)

            st.write(result.get("final_advice", ""))

        else:
            st.error("Skill gap analysis failed. Please try again.")
# =====================================================
# INTERVIEW
# =====================================================

elif page == "🎤Interview":

    st.title("🎤 Realistic AI Mock Interview")

    role = st.text_input("Target Role")

    if st.button("Generate Interview Question"):
        st.session_state.interview_question = generate_interview_question(role)

    if st.session_state.interview_question:
        st.subheader("Question")
        st.write(st.session_state.interview_question)

        answer = st.text_area("Your Answer")

        if st.button("Evaluate Answer"):
            result = evaluate_interview_answer(
                role,
                st.session_state.interview_question,
                answer
            )
            avg_interview_score = (
                result["technical_score"] +
                result["communication_score"] +
                result["confidence_score"]
            ) / 3
            save_interview_result(
                "st.session_state.username",
                role,
                result["technical_score"],
                result["communication_score"],
                result["confidence_score"]
            )

            st.session_state.interview_scores.append(avg_interview_score)

            if result:
                st.write("Technical Score:", result["technical_score"])
                st.write("Communication Score:", result["communication_score"])
                st.write("Confidence Score:", result["confidence_score"])
                st.write("Feedback:", result["feedback"])
                st.write("Improvement Suggestions:", result["improvement_suggestions"])
       


# =====================================================
# MENTOR CHAT
# ==================================================
elif page == "👩‍🏫Mentor Chat":

    st.title("🧘 AI Career Mentor")

    user_msg = st.text_input("Ask your career doubt")

    if st.button("Get Guidance"):
        reply = mentor_chat(user_msg)
        st.write(reply)

# =====================================================
# RESUME BUILDER
# =====================================================

# ===================================
# RESUME BUILDER SECTION
# ===================================

if page == "📄Resume Builder":

    st.header("📄 AI Resume Builder") 

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    linkedin = st.text_input("LinkedIn URL")
    github = st.text_input("GitHub URL")

    st.subheader("Professional Summary")
    summary = st.text_area("Write a short professional summary")

    st.subheader("Skills (comma separated)")
    skills = st.text_area("Python, SQL, Machine Learning, etc")

    st.subheader("Education")
    education = st.text_area("Degree, University, Year")

    st.subheader("Work Experience")
    experience = st.text_area("Company, Role, Achievements")

    st.subheader("Projects")
    projects = st.text_area("Project Name - Description")

    if st.button("Generate Resume"):
        
        resume_content = f"""
{name}
Email: {email}
Phone: {phone}
LinkedIn: {linkedin}
GitHub: {github}

-----------------------------

PROFESSIONAL SUMMARY
{summary}

-----------------------------

SKILLS
{skills}

-----------------------------

EDUCATION
{education}

-----------------------------

EXPERIENCE
{experience}

-----------------------------

PROJECTS
{projects}
"""

        from database import save_resume
        save_resume(st.session_state.username, "General", resume_content)

        st.success("Resume Generated Successfully!")

        st.download_button(
            "Download Resume",
            resume_content,
            file_name=f"{name}_resume.txt"
        )
# =====================================================
# CAREER PREDICTOR
# =====================================================

elif page == "🎓Career Predictor":

    st.title("🔮 AI Career Predictor")

    skills = st.text_input("Your Skills")
    interests = st.text_input("Your Interests")

    if st.button("Predict Best Career Path"):

        result = career_predictor(skills, interests)

        if result:
            st.subheader("Best Career Paths")
            st.write(result["best_career_paths"])
            st.write("Growth Potential:", result["growth_potential"])
            st.write("Salary Projection:", result["salary_projection"])


# =====================================================
# PUBLIC PROFILE
# =====================================================

elif page == "👤Public Profile":

    st.title("👤 Public Profile")

    username = st.text_input("Enter Username to View Profile")

    if st.button("View Profile"):
        if username:
            show_public_profile(username)
        else:
            st.warning("Please enter a username.")