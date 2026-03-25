import streamlit as st
from health_helper import (
    analyze_symptoms,
    get_diet_advice,
    get_exercise_advice,
    check_medicine_info,
    emergency_check
)

# Page configuration
st.set_page_config(
    page_title="Health Assistant",
    page_icon="🏥",
    layout="wide"
)

# Main title
st.title("🏥 Personal Health Assistant")
st.warning("⚠️ This is NOT a replacement for real doctors!")
st.divider()

# Sidebar menu
st.sidebar.title("📋 Menu")
option = st.sidebar.selectbox(
    "Choose a feature:",
    [
        "🔍 Symptom Analyzer",
        "🥗 Diet Advisor",
        "🏃 Exercise Advisor",
        "💊 Medicine Info",
        "🚨 Emergency Check"
    ]
)

# Feature 1: Symptom Analyzer
if option == "🔍 Symptom Analyzer":
    st.header("🔍 Symptom Analyzer")
    st.write("Describe your symptoms and get health advice")
    symptoms = st.text_area(
        "Enter your symptoms:",
        placeholder="Example: I have headache and fever since 2 days"
    )
    if st.button("Analyze Symptoms 🔍"):
        if symptoms:
            with st.spinner("Analyzing your symptoms..."):
                result = analyze_symptoms(symptoms)
            st.success("Analysis Complete!")
            st.write(result)
        else:
            st.error("Please enter your symptoms!")

# Feature 2: Diet Advisor
elif option == "🥗 Diet Advisor":
    st.header("🥗 Diet Advisor")
    st.write("Get personalized diet advice")
    condition = st.text_input(
        "Enter your health condition:",
        placeholder="Example: diabetes, high blood pressure"
    )
    if st.button("Get Diet Advice 🥗"):
        if condition:
            with st.spinner("Getting diet advice..."):
                result = get_diet_advice(condition)
            st.success("Diet Plan Ready!")
            st.write(result)
        else:
            st.error("Please enter your condition!")

# Feature 3: Exercise Advisor
elif option == "🏃 Exercise Advisor":
    st.header("🏃 Exercise Advisor")
    st.write("Get safe exercise recommendations")
    condition = st.text_input(
        "Enter your health condition:",
        placeholder="Example: knee pain, back pain"
    )
    if st.button("Get Exercise Advice 🏃"):
        if condition:
            with st.spinner("Getting exercise advice..."):
                result = get_exercise_advice(condition)
            st.success("Exercise Plan Ready!")
            st.write(result)
        else:
            st.error("Please enter your condition!")

# Feature 4: Medicine Info
elif option == "💊 Medicine Info":
    st.header("💊 Medicine Information")
    st.write("Get basic information about medicines")
    medicine = st.text_input(
        "Enter medicine name:",
        placeholder="Example: Paracetamol, Ibuprofen"
    )
    if st.button("Get Medicine Info 💊"):
        if medicine:
            with st.spinner("Getting medicine information..."):
                result = check_medicine_info(medicine)
            st.success("Medicine Info Ready!")
            st.write(result)
        else:
            st.error("Please enter medicine name!")

# Feature 5: Emergency Check
elif option == "🚨 Emergency Check":
    st.header("🚨 Emergency Checker")
    st.write("Check if your symptoms need emergency care")
    symptoms = st.text_area(
        "Describe your symptoms:",
        placeholder="Example: severe chest pain and difficulty breathing"
    )
    if st.button("Check Emergency 🚨"):
        if symptoms:
            with st.spinner("Checking emergency level..."):
                result = emergency_check(symptoms)
            st.write(result)
        else:
            st.error("Please enter your symptoms!")