import streamlit as st
import matplotlib.pyplot as plt
from database import get_user_stats, calculate_user_rank


def show_public_profile(username):

    st.title("👤 Public Profile")

    # Get user data ONCE
    user_data = get_user_stats(username)

    if not user_data:
        st.error("User not found.")
        return

    # Safe access with defaults
    avg_quiz = user_data.get("avg_quiz", 0)
    avg_interview = user_data.get("avg_interview", 0)
    job_readiness = user_data.get("job_readiness", 0)
    career_score = user_data.get("career_score", 0)
    target_role = user_data.get("target_role", "Not Selected")
    resume = user_data.get("resume", None)
    profile_pic = user_data.get("profile_pic", None)

    # ==========================
    # ACHIEVEMENTS
    # ==========================

    st.markdown("### 🏆 Achievements")

    badges = []

    if avg_quiz > 80:
        badges.append("🧠 Quiz Master")

    if avg_interview > 80:
        badges.append("🎤 Interview Pro")

    if job_readiness > 85:
        badges.append("🚀 Job Ready Elite")

    if career_score > 90:
        badges.append("🔥 Top Performer")

    if badges:
        for badge in badges:
            st.success(badge)
    else:
        st.info("No achievements unlocked yet.")

    # ==========================
    # PERFORMANCE GRAPH
    # ==========================

    st.markdown("### 📈 Performance Overview")

    scores = [avg_quiz, avg_interview, job_readiness]
    labels = ["Quiz", "Interview", "Job Readiness"]

    fig = plt.figure()
    plt.plot(labels, scores)
    plt.ylim(0, 100)
    plt.xlabel("Category")
    plt.ylabel("Score")
    plt.title("Performance Overview")

    st.pyplot(fig)

    # ==========================
    # HEADER SECTION
    # ==========================

    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(
            profile_pic or
            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            width=140
        )

    with col2:
        st.markdown(f"## {username}")
        st.write(target_role)

        st.markdown(
            f"### 💯 Career Score: {career_score} / 100"
        )

        rank = calculate_user_rank(career_score)
        st.markdown(f"### 🏅 Rank: {rank}")

    # ==========================
    # QUIZ PERFORMANCE
    # ==========================

    st.markdown("### 📊 Quiz Performance")
    st.progress(avg_quiz / 100)
    st.write(f"Average Quiz Score: {round(avg_quiz, 2)}%")

    # ==========================
    # INTERVIEW PERFORMANCE
    # ==========================

    st.markdown("### 🎤 Interview Performance")
    st.progress(avg_interview / 100)
    st.write(f"Average Interview Score: {round(avg_interview, 2)}%")

    # ==========================
    # JOB READINESS
    # ==========================

    st.markdown("### 🚀 Job Readiness")
    st.progress(job_readiness / 100)
    st.write(f"Job Readiness Score: {round(job_readiness, 2)}%")

    # ==========================
    # RESUME SECTION
    # ==========================

    if resume:
        st.markdown("### 📄 Resume")
        st.download_button(
            "Download Resume",
            resume,
            file_name=f"{username}_resume.txt"
        )

    # ==========================
    # PUBLIC SHAREABLE LINK
    # ==========================

    st.markdown("### 🔗 Public Profile Link")
    public_url = f"http://localhost:8501/?profile={username}"
    st.code(public_url)