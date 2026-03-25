import os
import requests
from dotenv import load_dotenv

load_dotenv()  # ← This loads your .env file

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def ask_groq(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000
        }
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_symptoms(symptoms):
    return ask_groq(f"""
    You are a health assistant.
    Symptoms: {symptoms}
    Give:
    1. Possible causes
    2. Home remedies
    3. Medicines
    4. Warning signs
    5. When to see doctor
    """)

def get_diet_advice(condition):
    return ask_groq(f"""
    Give diet advice for: {condition}
    Include foods to eat, avoid, meal plan.
    """)

def get_exercise_advice(condition):
    return ask_groq(f"""
    Give safe exercises for: {condition}
    Include best exercises, duration, safety tips.
    """)

def check_medicine_info(medicine):
    return ask_groq(f"""
    Give information about medicine: {medicine}
    Include usage, dosage, side effects, warnings.
    """)

def emergency_check(symptoms):
    return ask_groq(f"""
    Is this an emergency: {symptoms}
    Answer EMERGENCY or NOT EMERGENCY with reason.
    """)