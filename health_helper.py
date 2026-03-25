# health_helper.py
# Using Groq API instead of Ollama
# Works on cloud deployment!

import os
import requests
from groq import Groq

# Get API key from environment
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def ask_groq(prompt):
    """
    Send question to Groq AI
    Works online - no local install needed!
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def analyze_symptoms(symptoms):
    prompt = f"""
    You are a helpful health assistant.
    Patient symptoms: {symptoms}
    
    Please provide:
    1. Possible causes
    2. Home remedies
    3. Medicines to take
    4. Warning signs
    5. When to see a doctor
    
    Keep response simple and clear.
    """
    return ask_groq(prompt)


def get_diet_advice(condition):
    prompt = f"""
    You are a nutrition expert.
    Give diet advice for: {condition}
    
    Include:
    1. Foods to eat
    2. Foods to avoid
    3. Sample meal plan
    4. Important vitamins
    """
    return ask_groq(prompt)


def get_exercise_advice(condition):
    prompt = f"""
    You are a fitness expert.
    Suggest exercises for: {condition}
    
    Include:
    1. Best exercises
    2. Exercises to avoid
    3. Duration per day
    4. Safety tips
    """
    return ask_groq(prompt)


def check_medicine_info(medicine):
    prompt = f"""
    Give information about: {medicine}
    
    Include:
    1. What it treats
    2. Common dosage
    3. Side effects
    4. Warnings
    
    Always remind to consult doctor.
    """
    return ask_groq(prompt)


def emergency_check(symptoms):
    prompt = f"""
    Check if these symptoms need emergency care:
    {symptoms}
    
    Answer clearly:
    - EMERGENCY or NOT EMERGENCY
    - Reason
    - What to do immediately
    """
    return ask_groq(prompt)