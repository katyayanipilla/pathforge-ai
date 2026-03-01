from groq import Groq
import os
from dotenv import load_dotenv
import json
import random


load_dotenv()
client = Groq(api_key="GROQ_API_KEY")

MODEL = "llama-3.1-8b-instant"

def ask_ai(prompt):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return completion.choices[0].message.content

def generate_roadmap(goal, duration):
    return ask_ai(f"""
Create a detailed learning roadmap.

Goal: {goal}
Duration: {duration}

Include:
- Weekly plan
- Skills
- Projects
- Resources
- Interview prep
""")
    
def generate_daily_quiz(topic: str, num_questions: int = 25):

    prompt = f"""
Generate {num_questions} multiple choice questions about {topic}.

Return ONLY JSON in this format:

[
  {{
    "question": "Question text",
    "correct_answer": "Correct answer",
    "wrong_answers": [
      "Wrong answer 1",
      "Wrong answer 2",
      "Wrong answer 3"
    ]
  }}
]

Rules:
- Do NOT label A/B/C/D
- Do NOT shuffle answers
- Only JSON
"""

    response = ask_ai(prompt)
    quiz_raw = json.loads(response)

    final_quiz = []

    for q in quiz_raw:
        options = [q["correct_answer"]] + q["wrong_answers"]
        random.shuffle(options)

        correct_letter = ["A", "B", "C", "D"][options.index(q["correct_answer"])]

        final_quiz.append({
            "question": q["question"],
            "options": {
                "A": options[0],
                "B": options[1],
                "C": options[2],
                "D": options[3]
            },
            "correct": correct_letter
        })

    return final_quiz
    
def generate_resume(details):
    return ask_ai(f"""
Create an ATS optimized professional resume:
{details}
""")

def generate_interview(role):
    return ask_ai(f"""
Generate technical and behavioral interview questions with answers for {role}.
""")

def skill_gap(current_skills, target_role):
    return ask_ai(f"""
User current skills: {current_skills}
Target role: {target_role}

Analyze skill gap and suggest missing skills in priority order.
""")
def mentor_chat(message):
    return ask_ai(f"""
You are a professional career mentor.
Guide the student clearly and motivationally.

Student Question: {message}
""")
def calculate_sincerity(created_at, last_updated, update_count, progress):
    created = datetime.fromisoformat(created_at)
    last = datetime.fromisoformat(last_updated)

    days_active = (last - created).days + 1
    if days_active <= 0:
        return 0

    consistency_score = min(update_count / days_active, 1) * 40
    progress_score = (progress / 100) * 40
    recency_score = 20 if (datetime.now() - last).days <= 2 else 0

    sincerity_score = consistency_score + progress_score + recency_score
    return round(sincerity_score, 1)