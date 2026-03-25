# health_helper.py
# This file contains all the AI functions
# Think of it as the BRAIN of our app

import requests  # used to talk to Ollama

# This is the address where Ollama runs on your computer
OLLAMA_URL = "http://localhost:11434/api/generate"

# This is the AI model we are using
MODEL = "llama3"

def ask_ollama(prompt):
    """
    This function sends a question to Ollama
    and returns the answer
    
    Think of it like:
    - You write a letter (prompt)
    - Put it in mailbox (requests.post)
    - Get reply back (response)
    """
    try:
        # Send the question to Ollama
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,      # which AI to use
                "prompt": prompt,    # the question
                "stream": False      # wait for full answer
            },
            timeout=60  # wait max 60 seconds
        )
        
        # Get the answer from response
        return response.json()["response"]
    
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"


def analyze_symptoms(symptoms):
    """
    Takes symptoms and returns health advice
    
    Example:
    Input:  "headache and fever"
    Output: "Here is advice for headache and fever..."
    """
    
    # This is the instruction we give to AI
    # The more detailed instruction = better answer
    prompt = f"""
    You are a helpful health assistant. 
    A patient has these symptoms: {symptoms}
    
    Please provide:
    1. What might be causing these symptoms
    2. Home remedies they can try
    3. medicines to take 
    4. Warning signs to watch for
    5. When they should see a doctor
    
    Important: Always remind them to 
    consult a real doctor for serious issues.
    Keep response simple and easy to understand.
    """
    
    return ask_ollama(prompt)


def get_diet_advice(condition):
    """
    Give diet advice for a health condition
    
    Example:
    Input:  "diabetes"
    Output: "For diabetes, eat these foods..."
    """
    prompt = f"""
    You are a nutrition expert.
    Give simple diet advice for: {condition}
    
    Include:
    1. Foods to eat
    2. Foods to avoid
    3. Sample meal plan for one day
    4. Important vitamins needed
    
    Keep it simple and practical.
    """
    
    return ask_ollama(prompt)


def get_exercise_advice(condition):
    """
    Give exercise advice for a health condition
    """
    prompt = f"""
    You are a fitness expert.
    Suggest safe exercises for someone with: {condition}
    
    Include:
    1. Best exercises for this condition
    2. Exercises to avoid
    3. How many minutes per day
    4. Safety precautions
    
    Keep advice safe and practical.
    """
    
    return ask_ollama(prompt)


def check_medicine_info(medicine_name):
    """
    Get basic information about a medicine
    """
    prompt = f"""
    Give basic information about medicine: {medicine_name}
    
    Include:
    1. What it is used for
    2. Common dosage
    3. Common side effects
    4. Important warnings
    
    Always remind to consult doctor before taking.
    """
    
    return ask_ollama(prompt)


def emergency_check(symptoms):
    """
    Check if symptoms need emergency care
    """
    prompt = f"""
    As a medical expert, check if these symptoms 
    need EMERGENCY care: {symptoms}
    
    Answer with:
    - EMERGENCY or NOT EMERGENCY
    - Reason why
    - What to do immediately
    
    Be very clear and direct.
    """
    
    return ask_ollama(prompt)


# hospital_features.py
# Professional features for hospitals

import streamlit as st
import sqlite3
import hashlib

def create_user_db():
    """Multi user login system"""
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            hospital TEXT
        )
    """)
    
    # Patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            blood_group TEXT,
            allergies TEXT,
            history TEXT,
            doctor_id INTEGER
        )
    """)
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Encrypt password for safety"""
    return hashlib.sha256(
        password.encode()
    ).hexdigest()

def login(username, password):
    """Check if login is correct"""
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    
    hashed = hash_password(password)
    
    cursor.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
    """, (username, hashed))
    
    user = cursor.fetchone()
    conn.close()
    return user

def hospital_dashboard():
    """Main hospital dashboard"""
    st.title("🏥 Hospital Health Assistant")
    
    # Login check
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.header("🔐 Login")
        username = st.text_input("Username:")
        password = st.text_input(
            "Password:", type="password"
        )
        
        if st.button("Login"):
            user = login(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Wrong credentials!")
    else:
        st.success(
            f"Welcome Dr. "
            f"{st.session_state.user[1]}!"
        )
        
        # Show hospital features
        tab1, tab2, tab3 = st.tabs([
            "👥 Patients",
            "📊 Reports",
            "🤖 AI Analysis"
        ])
        
        with tab1:
            st.header("Patient Management")
            
        with tab2:
            st.header("Hospital Reports")
            
        with tab3:
            st.header("AI Health Analysis")