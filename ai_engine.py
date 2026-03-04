import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

# =====================================================
# ENV SETUP
# =====================================================

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY missing in .env file")

client = Groq(api_key=api_key)
MODEL = "llama-3.1-8b-instant"

# =====================================================
# SAFE JSON PARSER
# =====================================================

def safe_json_parse(text):
    try:
        # Remove markdown code blocks
        text = re.sub(r"```json|```", "", text).strip()

        # Extract first JSON object using regex
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            json_str = match.group()
            return json.loads(json_str)

        return None

    except Exception as e:
        print("JSON Parse Error:", e)
        print("RAW TEXT:", text)
        return None


def ask_ai(system_prompt, user_prompt, temperature=0.3, max_tokens=6000):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()

# =====================================================
# ROADMAP ENGINE
# =====================================================

def generate_roadmap(role, duration_months, level):

    total_weeks = duration_months * 4

    system_prompt = """
You are a world-class curriculum architect.
Return strictly valid JSON.
No explanations.
"""

    user_prompt = f"""
Create a {total_weeks}-week structured roadmap for becoming a {role}.
User Level: {level}

Each week must include:
- week_number
- title
- concepts (list)
- learning_resources (list)
- project
- outcome

Return JSON list.
"""

    response = ask_ai(system_prompt, user_prompt, 0.2)
    return safe_json_parse(response) or []

# =====================================================
# ADAPTIVE QUIZ ENGINE (25 QUESTIONS)
# =====================================================

def generate_daily_quiz(topic, difficulty="Beginner", covered_subtopics=None):

    if covered_subtopics is None:
        covered_subtopics = []

    system_prompt = """
You are an elite technical exam creator.
Return strictly valid JSON.
"""

    user_prompt = f"""
Topic: {topic}
Difficulty: {difficulty}
Avoid subtopics already covered: {covered_subtopics}

Generate 25 MCQs.

Each must include:
- question
- options (4)
- correct_answer
- explanation
- subtopic

Return JSON list.
"""

    response = ask_ai(system_prompt, user_prompt, 0.4)
    return safe_json_parse(response) or []

# =====================================================
# INTERVIEW ENGINE
# =====================================================

def generate_interview_question(role, round_type="technical"):

    system_prompt = """
You are a senior FAANG interviewer.
Ask one realistic deep interview question.
"""

    user_prompt = f"""
Role: {role}
Round Type: {round_type}
"""

    return ask_ai(system_prompt, user_prompt)


def evaluate_interview_answer(role, question, answer):

    system_prompt = """
You are evaluating a job candidate.
Return strictly valid JSON.
"""

    user_prompt = f"""
Role: {role}
Question: {question}
Candidate Answer: {answer}

Return:
{{
  "technical_score": 0-10,
  "communication_score": 0-10,
  "confidence_score": 0-10,
  "feedback": "",
  "ideal_answer": "",
  "improvement_suggestions": ""
}}
"""

    response = ask_ai(system_prompt, user_prompt)
    return safe_json_parse(response) or {}

# =====================================================
# SKILL GAP ANALYSIS
# =====================================================

def skill_gap_analysis(current_skills, target_role):

    system_prompt = """
You are a senior hiring manager.
Return strictly valid JSON.
"""

    user_prompt = f"""
Current Skills: {current_skills}
Target Role: {target_role}

Return:
{{
  "strengths": [],
  "missing_skills": [],
  "recommended_projects": [],
  "certifications": [],
  "interview_preparation": [],
  "job_readiness_score": 0,
  "final_advice": ""
}}
"""

    response = ask_ai(system_prompt, user_prompt)
    return safe_json_parse(response) or {}

# =====================================================
# ADVANCED RESUME BUILDER
# =====================================================

def generate_advanced_resume(details, target_role):

    system_prompt = """
You are a top-tier resume strategist.
Create an ATS-optimized, executive-level resume.
Quantify achievements.
No placeholders.
Professional formatting.
"""

    user_prompt = f"""
Target Role: {target_role}
User Details:
{details}
"""

    return ask_ai(system_prompt, user_prompt, 0.4, 7000)

# =====================================================
# EMOTIONAL INTELLIGENCE MENTOR
# =====================================================

def mentor_chat(message):

    system_prompt = """
You are an emotionally intelligent career mentor.
Motivate.
Give clarity.
Remove confusion.
Provide step-by-step guidance.
Reduce anxiety.
Encourage discipline.
"""

    return ask_ai(system_prompt, message, 0.6)

# =====================================================
# CAREER PREDICTOR
# =====================================================

def career_predictor(skills, interests):

    system_prompt = """
You are an AI career strategist.
Return strictly valid JSON.
"""

    user_prompt = f"""
Skills: {skills}
Interests: {interests}

Return:
{{
  "best_career_paths": [],
  "reasoning": "",
  "growth_potential": "",
  "salary_projection": ""
}}
"""

    response = ask_ai(system_prompt, user_prompt)
    return safe_json_parse(response) or {}

# =====================================================
# SMART STUDY PLAN
# =====================================================

def generate_smart_study_plan(topic, mastery):

    if mastery < 40:
        return f"""
📘 Foundation Plan for {topic}
- Revise core fundamentals
- Solve 50 beginner problems
- Watch structured tutorials
- Build 1 small project
"""

    elif mastery < 70:
        return f"""
⚡ Intermediate Plan for {topic}
- Build 2 mini projects
- Practice medium interview questions
- Study real-world use cases
"""

    else:
        return f"""
🔥 Advanced Plan for {topic}
- Build production-level project
- Contribute to open source
- Solve hard interview questions
- Prepare system design basics
"""