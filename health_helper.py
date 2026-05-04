# ai_helper.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def ask_groq(prompt):
    """Send question to Groq AI"""
    try:
        # Check if API key exists
        if not GROQ_API_KEY:
            return "❌ Error: GROQ_API_KEY not found! Please add it to .env file"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        # Debug - check response
        if response.status_code != 200:
            return f"❌ API Error {response.status_code}: {response.text}"

        result = response.json()

        # Check if choices exists
        if "choices" not in result:
            return f"❌ Unexpected response: {result}"

        return result["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "❌ Request timed out! Try again."
    except requests.exceptions.ConnectionError:
        return "❌ No internet connection!"
    except KeyError as e:
        return f"❌ Key error: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def analyze_symptoms(symptoms, age, gender):
    return ask_groq(f"""
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

def get_diet_advice(condition):
    """
    Returns diet advice based on health condition
    """
    diet_plans = {
        "diabetes": "Avoid sugar, eat high fiber foods, whole grains, vegetables.",
        "hypertension": "Reduce salt intake, eat fruits, vegetables, low-fat dairy.",
        "obesity": "Low calorie diet, avoid junk food, eat more protein and fiber.",
        "general": "Eat balanced diet with proteins, carbs, fats, vitamins and minerals."
    }
    
    condition = condition.lower()
    return diet_plans.get(condition, diet_plans["general"])

def suggest_prescription(diagnosis, allergies):
    return ask_groq(f"""
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


def analyze_lab_report(test_name, result, normal_range):
    return ask_groq(f"""
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
    treatment, prescription, follow_up
):
    return ask_groq(f"""
    Generate professional discharge summary:

    Patient: {patient_name}
    Diagnosis: {diagnosis}
    Treatment given: {treatment}
    Prescription: {prescription}
    Follow-up: {follow_up}

    Format as official medical document.
    Include all important instructions.
    """)