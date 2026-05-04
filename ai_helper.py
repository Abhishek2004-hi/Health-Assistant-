# ai_helper.py
# AI functions using Groq
# Like having an AI doctor assistant

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def ask_ai(prompt):
    """Send question to Groq AI"""
    try:
        headers = {
            "Authorization":
                f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model":
                "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000
        }
        response = requests.post(
            "https://api.groq.com/openai"
            "/v1/chat/completions",
            headers=headers,
            json=data
        )
        return response.json()[
            "choices"
        ][0]["message"]["content"]

    except Exception as e:
        return f"AI Error: {str(e)}"

def analyze_symptoms(symptoms, age, gender):
    """AI symptom analysis"""
    return ask_ai(f"""
    You are a medical AI assistant.
    Patient: {age} year old {gender}
    Symptoms: {symptoms}

    Provide:
    1. Possible diagnoses (3-5)
    2. Recommended tests
    3. Immediate care steps
    4. Red flags to watch
    5. Specialist to consult

    Be clear and professional.
    """)

def suggest_prescription(
    diagnosis, allergies
):
    """AI prescription suggestion"""
    return ask_ai(f"""
    You are a medical AI.
    Diagnosis: {diagnosis}
    Patient allergies: {allergies}

    Suggest:
    1. Medicines (generic names)
    2. Dosage for each
    3. Duration
    4. Precautions
    5. Lifestyle advice

    Note: Doctor must verify before giving.
    """)

def analyze_lab_report(
    test_name, result, normal_range
):
    """AI lab report analysis"""
    return ask_ai(f"""
    Analyze this lab report:
    Test: {test_name}
    Result: {result}
    Normal Range: {normal_range}

    Explain:
    1. Is result normal or abnormal?
    2. What does this mean?
    3. What action needed?
    4. How serious is it?

    Use simple language.
    """)

def generate_discharge_summary(
    patient_name, diagnosis,
    treatment, prescription,
    follow_up
):
    """Generate discharge summary"""
    return ask_ai(f"""
    Generate professional discharge summary:

    Patient: {patient_name}
    Diagnosis: {diagnosis}
    Treatment given: {treatment}
    Prescription: {prescription}
    Follow-up: {follow_up}

    Format as official medical document.
    Include all important instructions.
    """)