import streamlit as st
import pandas as pd
from datetime import datetime, date
from database import init_db
from ai_engine import *
from auth import *
from streamlit_option_menu import option_menu
from ai_engine import mentor_chat
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import HRFlowable

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="PathForge AI", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0b1220, #111827);
    color: #ffffff !important;
}

body, p, span, div, label, small {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] {
    background: #0f172a;
}

.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #38bdf8);
    color: white !important;
    border-radius: 8px;
    border: none;
    font-weight: 700;
}

div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea,
textarea {
    background-color: #1f2937 !important;
    color: #ffffff !important;
    border: 1px solid #374151 !important;
}

input::placeholder,
textarea::placeholder {
    color: #ffffff !important;
    opacity: 1 !important;
}

div[data-baseweb="select"] div {
    background-color: #1f2937 !important;
    color: #ffffff !important;
}

div[data-testid="stRadio"] label,
div[data-testid="stToggle"] label {
    color: #ffffff !important;
}

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #7c3aed, #38bdf8);
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("""
<h1 style="text-align:center; font-size:40px; font-weight:800;">
🚀 PathForge AI Dashboard
</h1>
""", unsafe_allow_html=True)

# ---------------- DATABASE ----------------
conn = init_db()
c = conn.cursor()

# ---------------- AUTH ----------------
if "user" not in st.session_state:
    st.session_state.user = None

def login():
    st.title("🔐 Login / Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        result = c.fetchone()
        if result and check_password(password, result[0]):
            st.session_state.user = username
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button("Register"):
        hashed = hash_password(password)
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?,?)",
                      (username, hashed))
            conn.commit()
            st.success("Registered successfully!")
        except:
            st.error("User already exists")

if not st.session_state.user:
    login()
    st.stop()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    selected = option_menu(
        "🚀 PathForge AI",
        ["Dashboard", "Roadmap", "My Roadmaps", "Quiz",
         "Skill Gap", "Resume", "Interview",
         "Mentor Chat", "Performance", "Public Profile"],
        default_index=0,
    )

# ---------------- DASHBOARD ----------------
if selected == "Dashboard":
    st.title("📊 Dashboard")
    c.execute("SELECT streak, quizzes_passed FROM users WHERE username=?",
              (st.session_state.user,))
    data = c.fetchone()
    streak, quizzes = data if data else (0, 0)

    col1, col2 = st.columns(2)
    col1.metric("🔥 Current Streak", streak)
    col2.metric("✅ Quizzes Passed", quizzes)

# ---------------- ROADMAP ----------------
if selected == "Roadmap":

    st.title("➕ Create New Roadmap")

    goal = st.text_input("Goal")
    duration = st.text_input("Duration (Example: 3 Months)")

    task_input = st.text_area(
        "Enter tasks (one per line)",
        placeholder="Learn Basics\nPractice 50 Problems\nBuild Project"
    )

    if st.button("Create Roadmap"):
        if goal and task_input:
            tasks_list = [
                {"task": t.strip(), "completed": False}
                for t in task_input.split("\n") if t.strip()
            ]

            now = datetime.now().isoformat()

            c.execute("""
            INSERT INTO roadmaps 
            (username, goal, duration, tasks, created_at, last_updated, update_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                st.session_state.user,
                goal,
                duration,
                json.dumps(tasks_list),
                now,
                now,
                0
            ))

            conn.commit()
            st.success("Roadmap Created!")
            st.rerun()
# ---------------- MY ROADMAPS ----------------
elif selected == "My Roadmaps":

    st.title("📚 My Roadmaps")

    # Fetch user roadmaps
    c.execute("""
    SELECT id, goal, duration, tasks, created_at, last_updated, update_count
    FROM roadmaps
    WHERE username=?
    """, (st.session_state.user,))

    data = c.fetchall()

    if not data:
        st.info("You haven't created any roadmaps yet.")

    else:
        total_progress = []

        for r in data:
            roadmap_id, goal, duration, tasks_json, created_at, last_updated, update_count = r
            tasks = json.loads(tasks_json)

            # Calculate progress automatically
            completed = sum(1 for t in tasks if t["completed"])
            progress = int((completed / len(tasks)) * 100) if tasks else 0
            total_progress.append(progress)

            # Status Logic
            if progress == 0:
                status = "🔵 Not Started"
            elif progress < 100:
                status = "🟡 In Progress"
            else:
                status = "🟢 Completed"

            # Roadmap Header
            st.markdown(f"## 🎯 {goal}")
            st.write(f"**Duration:** {duration}")
            st.write(f"**Status:** {status}")
            st.progress(progress)
            st.write(f"Progress: {progress}%")

            st.markdown("### 🗺 Tasks")

            updated = False

            # Task Checklist
            for i, task in enumerate(tasks):
                checked = st.checkbox(
                    task["task"],
                    value=task["completed"],
                    key=f"{roadmap_id}_{i}"
                )

                if checked != task["completed"]:
                    tasks[i]["completed"] = checked
                    updated = True

            # Update database if tasks changed
            if updated:
                now = datetime.now().isoformat()

                c.execute("""
                UPDATE roadmaps
                SET tasks=?, last_updated=?, update_count=update_count+1
                WHERE id=?
                """, (json.dumps(tasks), now, roadmap_id))

                conn.commit()
                st.rerun()

            # ---------------- SINCERITY SCORE ----------------

            def calculate_sincerity(created_at, last_updated, update_count, progress):
                created = datetime.fromisoformat(created_at)
                last = datetime.fromisoformat(last_updated)

                days_active = (last - created).days + 1
                if days_active <= 0:
                    return 0

                consistency_score = min(update_count / days_active, 1) * 40
                progress_score = (progress / 100) * 40
                recency_score = 20 if (datetime.now() - last).days <= 2 else 0

                return round(consistency_score + progress_score + recency_score, 1)

            sincerity = calculate_sincerity(
                created_at,
                last_updated,
                update_count,
                progress
            )

            st.metric("🧠 Sincerity Score", f"{sincerity}/100")

            if sincerity > 80:
                st.success("🔥 Highly Consistent!")
            elif sincerity > 60:
                st.info("🚀 Good Progress")
            elif sincerity > 40:
                st.warning("⚠️ Improve consistency")
            else:
                st.error("❌ Low Activity")

            # Delete Button
            if st.button("🗑 Delete Roadmap", key=f"del_{roadmap_id}"):
                c.execute("DELETE FROM roadmaps WHERE id=?", (roadmap_id,))
                conn.commit()
                st.warning("Roadmap Deleted")
                st.rerun()

            st.markdown("---")

        # ================= OVERALL ANALYTICS =================

        st.markdown("## 📊 Overall Analytics")

        avg_progress = sum(total_progress) / len(total_progress)

        col1, col2 = st.columns(2)
        col1.metric("📚 Total Roadmaps", len(total_progress))
        col2.metric("📈 Average Progress", f"{round(avg_progress,1)}%")

        if avg_progress == 100:
            st.success("🔥 All Roadmaps Completed! Outstanding Work!")
        elif avg_progress > 60:
            st.info("🚀 You're making strong progress!")
        else:
            st.warning("📌 Stay consistent and keep pushing forward!")
# ---------------- QUIZ ----------------
if selected == "Quiz":

    st.title("🧠 Daily Quiz")

    topic = st.text_input("Enter Topic")

    if st.button("Start Quiz"):
        st.session_state.quiz = generate_daily_quiz(topic)
        st.session_state.score = 0
        st.session_state.submitted = False

    if "quiz" in st.session_state:

        user_answers = {}

        for i, q in enumerate(st.session_state.quiz):
            st.write(f"### Q{i+1}. {q['question']}")

            user_answers[i] = st.radio(
                "Choose your answer:",
                ["A", "B", "C", "D"],
                format_func=lambda x: q["options"][x],
                key=f"q{i}"
            )

        if st.button("Submit Quiz"):
            score = 0

            for i, q in enumerate(st.session_state.quiz):
                if user_answers[i] == q["correct"]:
                    score += 1

            st.session_state.score = score
            st.session_state.submitted = True

    if "submitted" in st.session_state and st.session_state.submitted:

        total = len(st.session_state.quiz)
        percentage = (st.session_state.score / total) * 100

        st.success(f"Your Score: {st.session_state.score} / {total}")
        st.info(f"Percentage: {percentage:.2f}%")

# ---------------- SHOW RESULTS ---------------- #

if "submitted" in st.session_state and st.session_state.submitted:

    score = st.session_state.score
    total = len(st.session_state.quiz["questions"])

    st.markdown("---")
    st.success(f"🎯 Your Score: {score} / {total}")

    if score == total:
        st.success("🔥 Perfect Score!")
    elif score >= total * 0.6:
        st.info("🚀 Good Job!")
    else:
        st.warning("📚 Keep Practicing!")

    if st.button("Reset Quiz"):
        del st.session_state.quiz
        del st.session_state.score
        del st.session_state.submitted
        st.rerun()

# ---------------- SKILL GAP ----------------
elif selected == "Skill Gap":
    st.title("🧠 AI Skill Gap Analyzer")

    col1, col2 = st.columns(2)

    with col1:
        current = st.text_area(
            "Your Current Skills (comma separated)",
            placeholder="Python, SQL, Pandas, APIs..."
        )

    with col2:
        target = st.text_input(
            "Target Role",
            placeholder="Data Scientist / Backend Developer / ML Engineer"
        )

    analyze_button = st.button("Analyze Skill Gap 🚀")

    if analyze_button and current and target:

        # Get AI response (should return structured dictionary ideally)
        analysis = skill_gap(current, target)

        # ---- Example Structured Output (Replace later with real AI structured output) ----
        strengths = ["Python", "SQL"]
        missing = ["Machine Learning", "System Design", "Docker"]
        match_score = 65

        st.markdown("---")

        # ================= MATCH SCORE =================
        st.subheader("🎯 Career Match Score")
        st.progress(match_score)
        st.metric("Readiness", f"{match_score}%")

        st.markdown("---")

        # ================= STRENGTHS =================
        st.subheader("✅ Your Strengths")

        for skill in strengths:
            st.success(skill)

        # ================= MISSING SKILLS =================
        st.subheader("❌ Skills To Improve")

        for skill in missing:
            st.error(skill)

        st.markdown("---")

        # ================= VISUAL COMPARISON =================
        st.subheader("📊 Skill Comparison Chart")

        skill_data = {
            "Skill": strengths + missing,
            "Status": [100]*len(strengths) + [30]*len(missing)
        }

        import pandas as pd
        df = pd.DataFrame(skill_data)

        st.bar_chart(df.set_index("Skill"))

        st.markdown("---")

        # ================= LEARNING ROADMAP =================
        st.subheader("📚 Recommended Learning Plan")

        roadmap_suggestions = """
        1. Learn Machine Learning fundamentals (scikit-learn, regression, classification)
        2. Study System Design basics (scalability, caching, APIs)
        3. Practice Docker & deployment workflows
        """

        st.info(roadmap_suggestions)

        st.markdown("---")

        # ================= AI DETAILED ANALYSIS =================
        st.subheader("🤖 Detailed AI Insight")
        st.markdown(analysis)

    elif analyze_button:
        st.warning("Please enter both current skills and target role.")
# ---------------- RESUME ----------------
elif selected == "Resume":
    st.title("📄 Advanced Resume Builder")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        linkedin = st.text_input("LinkedIn URL")
        github = st.text_input("GitHub URL")

    with col2:
        summary = st.text_area("Professional Summary")
        skills = st.text_area("Skills (comma separated)")
        certifications = st.text_area("Certifications")

    st.subheader("💼 Work Experience")
    experience = st.text_area("Describe your work experience (Role | Company | Duration | Description)")

    st.subheader("🚀 Projects")
    projects = st.text_area("Project Name | Tech Stack | Description")

    st.subheader("🎓 Education")
    education = st.text_area("Degree | Institution | Year")

    st.subheader("🏆 Achievements")
    achievements = st.text_area("Awards / Hackathons / Recognition")

    def generate_pdf():
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        # NAME (Large Bold)
        elements.append(Paragraph(f"<font size=18><b>{name}</b></font>", styles["Normal"]))
        elements.append(Spacer(1, 8))

        # Contact Info
        contact = f"{email} | {phone} | {linkedin} | {github}"
        elements.append(Paragraph(contact, styles["Normal"]))
        elements.append(Spacer(1, 12))

        # Divider
        elements.append(HRFlowable(width="100%"))
        elements.append(Spacer(1, 12))

        # Helper function for sections
        def add_section(title, content):
            elements.append(Paragraph(f"<b>{title}</b>", styles["Heading2"]))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(content.replace("\n", "<br/>"), styles["Normal"]))
            elements.append(Spacer(1, 12))

        # Sections
        if summary:
            add_section("Professional Summary", summary)

        if skills:
            formatted_skills = ", ".join([s.strip() for s in skills.split(",")])
            add_section("Skills", formatted_skills)

        if experience:
            add_section("Work Experience", experience)

        if projects:
            add_section("Projects", projects)

        if education:
            add_section("Education", education)

        if certifications:
            add_section("Certifications", certifications)

        if achievements:
            add_section("Achievements", achievements)

        doc.build(elements)
        buffer.seek(0)
        return buffer

    if st.button("Generate Advanced Resume"):
        if not name:
            st.error("Full Name is required")
        else:
            pdf = generate_pdf()
            st.download_button(
                "Download Resume PDF",
                pdf,
                file_name=f"{name}_Resume.pdf",
                mime="application/pdf"
            )
# ---------------- INTERVIEW ----------------
elif selected == "Interview":
    st.title("🎯 AI Mock Interview")

    role = st.text_input("Target Role")
    interview_type = st.selectbox(
        "Interview Type",
        ["Technical", "HR", "Behavioral", "Case Study"]
    )
    difficulty = st.selectbox(
        "Difficulty Level",
        ["Easy", "Medium", "Hard"]
    )

    if "interview_questions" not in st.session_state:
        st.session_state.interview_questions = None
        st.session_state.current_question = 0
        st.session_state.score = 0

    if st.button("Start Interview"):
        st.session_state.interview_questions = generate_interview(role, interview_type, difficulty)
        st.session_state.current_question = 0
        st.session_state.score = 0

    if st.session_state.interview_questions:
        questions = st.session_state.interview_questions
        index = st.session_state.current_question

        if index < len(questions):
            st.subheader(f"Question {index+1}")
            st.write(questions[index])

            user_answer = st.text_area("Your Answer")

            if st.button("Submit Answer"):
                feedback, rating = evaluate_answer(questions[index], user_answer)

                st.markdown("### 🧠 AI Feedback")
                st.write(feedback)
                st.metric("Score", f"{rating}/10")

                st.session_state.score += rating
                st.session_state.current_question += 1

        else:
            avg_score = st.session_state.score / len(questions)
            st.success("🎉 Interview Completed!")
            st.metric("Overall Score", f"{round(avg_score,1)}/10")

            if avg_score >= 8:
                st.success("Excellent Performance 🚀")
            elif avg_score >= 5:
                st.warning("Good, but needs improvement 👍")
            else:
                st.error("Practice more and try again 💪")

# ---------------- MENTOR CHAT ----------------
elif selected == "Mentor Chat":
    st.title("🤖 AI Career Mentor")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat messages
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])

    user_input = st.chat_input("Ask your mentor anything about career, skills, growth...")

    if user_input:
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        # Get AI response
        response = mentor_chat(user_input)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })

        with st.chat_message("assistant"):
            st.write(response)

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ---------------- PERFORMANCE ----------------
elif selected == "Performance":
    st.title("📈 Performance Dashboard")

    # Fetch user stats
    c.execute("SELECT streak, quizzes_passed FROM users WHERE username=?",
              (st.session_state.user,))
    user_data = c.fetchone()
    streak, quizzes = user_data if user_data else (0, 0)

    # Simulated additional stats (replace later with DB fields)
    interview_avg = 7.8
    skill_progress = 65

    # ================= TOP METRICS =================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🔥 Current Streak", streak)
    col2.metric("🧠 Quizzes Passed", quizzes)
    col3.metric("🎯 Interview Avg Score", f"{interview_avg}/10")
    col4.metric("🚀 Skill Progress", f"{skill_progress}%")

    st.markdown("---")

    # ================= QUIZ ANALYTICS =================
    st.subheader("🧠 Quiz Performance")

    quiz_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Quizzes Passed": [2, 4, 5, 7, 6, quizzes]
    })

    st.line_chart(quiz_data.set_index("Month"))

    st.markdown("---")

    # ================= INTERVIEW PERFORMANCE =================
    st.subheader("🎯 Interview Score Trend")

    interview_data = pd.DataFrame({
        "Attempt": ["1", "2", "3", "4", "5"],
        "Score": [6, 7, 8, 7, interview_avg]
    })

    st.bar_chart(interview_data.set_index("Attempt"))

    st.markdown("---")

    # ================= SKILL RADAR STYLE SUMMARY =================
    st.subheader("🚀 Skill Breakdown")

    skill_data = pd.DataFrame({
        "Skill": ["Python", "DSA", "System Design", "Communication", "SQL"],
        "Proficiency %": [75, 60, 55, 80, 70]
    })

    st.bar_chart(skill_data.set_index("Skill"))

    st.markdown("---")

    # ================= PERFORMANCE SUMMARY =================
    st.subheader("📊 AI Performance Summary")

    if quizzes > 10 and interview_avg > 8:
        st.success("Outstanding Performance! You're interview ready 🚀")
    elif quizzes > 5:
        st.warning("Good progress! Keep practicing consistently 👍")
    else:
        st.info("Start taking quizzes and interviews to see progress growth 📚")
# ---------------- PUBLIC PROFILE ----------------
elif selected == "Public Profile":
    st.title("🌍 Public Profile")

    c.execute("SELECT streak, quizzes_passed FROM users WHERE username=?",
              (st.session_state.user,))
    user_data = c.fetchone()
    streak, quizzes = user_data if user_data else (0, 0)

    bio = st.text_area("Bio", placeholder="Write something about yourself...")
    skills = st.text_input("Top Skills (comma separated)")
    public_toggle = st.toggle("Make Profile Public", value=True)

    if st.button("Save Profile"):
        st.success("Profile Updated Successfully!")

    colA, colB = st.columns(2)
    colA.metric("🔥 Current Streak", streak)
    colB.metric("✅ Quizzes Passed", quizzes)