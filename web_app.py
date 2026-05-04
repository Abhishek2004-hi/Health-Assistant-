# web_app.py - Complete Version with All Features

import streamlit as st
from health_helper import (
    analyze_symptoms,
    get_diet_advice,
    get_exercise_advice,
    check_medicine_info,
    emergency_check
)
from history_manager import (
    create_database,
    save_history,
    get_all_history,
    delete_history
)
from appointment import (
    create_appointment_db,
    book_appointment,
    get_appointments,
    DOCTORS
)
from translator import (
    LANGUAGES,
    analyze_in_language
)

# Initialize databases
create_database()
create_appointment_db()

# Page config
st.set_page_config(
    page_title="Health Assistant",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS styling
st.markdown("""
<style>
    .main {
        background-color: #f0f8ff;
    }
    .stButton > button {
        background-color: #0066cc;
        color: white;
        border-radius: 10px;
        width: 100%;
        height: 50px;
        font-size: 16px;
    }
    .stButton > button:hover {
        background-color: #0052a3;
    }
    h1 {
        color: #0066cc;
        text-align: center;
    }
    h2 {
        color: #0052a3;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🏥 Personal Health Assistant")
st.warning(
    "⚠️ This is NOT a replacement for real doctors!"
)
st.divider()

# Sidebar
st.sidebar.title("📋 Main Menu")
st.sidebar.image(
    "https://img.icons8.com/color/96/hospital.png",
    width=100
)

option = st.sidebar.selectbox(
    "Choose Feature:",
    [
        "🏠 Home",
        "🔍 Symptom Analyzer",
        "🥗 Diet Advisor",
        "🏃 Exercise Advisor",
        "💊 Medicine Info",
        "🚨 Emergency Check",
        "📋 Patient History",
        "📅 Book Appointment",
        "🌍 Language Support"
    ]
)

# HOME PAGE
if option == "🏠 Home":
    st.header("Welcome to Health Assistant! 👋")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("""
        ### 🔍 Symptom Checker
        Describe symptoms and get
        instant AI health advice
        """)

    with col2:
        st.success("""
        ### 📅 Book Appointment
        Book doctor appointments
        quickly and easily
        """)

    with col3:
        st.warning("""
        ### 📋 Health History
        Save and track your
        health records
        """)

    st.divider()
    st.subheader("🚀 Quick Actions")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Check Symptoms Now"):
            st.session_state.page = "symptoms"
    with col2:
        if st.button("🚨 Emergency Check"):
            st.session_state.page = "emergency"

# SYMPTOM ANALYZER
elif option == "🔍 Symptom Analyzer":
    st.header("🔍 Symptom Analyzer")

    language = st.selectbox(
        "Choose Response Language:",
        list(LANGUAGES.keys())
    )

    symptoms = st.text_area(
        "Describe your symptoms in detail:",
        placeholder="Example: I have headache, fever 102°F and body pain since 2 days",
        height=150
    )

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Your Age:", 1, 100, 25)
    with col2:
        gender = st.selectbox(
            "Gender:", ["Male", "Female", "Other"]
        )

    if st.button("🔍 Analyze Symptoms"):
        if symptoms:
            with st.spinner("🤖 AI is analyzing..."):
                full_symptoms = f"""
                Patient Age: {age}
                Gender: {gender}
                Symptoms: {symptoms}
                """
                result = analyze_in_language(
                    full_symptoms, language
                )

            # Save to history
            save_history(
                "Symptom Analysis",
                symptoms,
                result
            )

            st.success("✅ Analysis Complete!")

            # Show result in nice box
            st.markdown("""
            <div style='background:#e8f4f8;
                padding:20px; border-radius:10px;
                border-left:5px solid #0066cc'>
            """, unsafe_allow_html=True)
            st.write(result)
            st.markdown("</div>",
                unsafe_allow_html=True)
        else:
            st.error("❌ Please enter your symptoms!")

# DIET ADVISOR
elif option == "🥗 Diet Advisor":
    st.header("🥗 Personalized Diet Advisor")

    col1, col2 = st.columns(2)
    with col1:
        condition = st.text_input(
            "Health Condition:",
            placeholder="diabetes, blood pressure"
        )
    with col2:
        language = st.selectbox(
            "Language:", list(LANGUAGES.keys())
        )

    if st.button("🥗 Get Diet Plan"):
        if condition:
            with st.spinner("Creating diet plan..."):
                result = get_diet_advice(condition)
            st.success("✅ Diet Plan Ready!")
            st.write(result)
        else:
            st.error("Please enter condition!")

# EXERCISE ADVISOR
elif option == "🏃 Exercise Advisor":
    st.header("🏃 Exercise Advisor")

    condition = st.text_input(
        "Your health condition:",
        placeholder="knee pain, back pain, diabetes"
    )

    fitness_level = st.selectbox(
        "Your fitness level:",
        ["Beginner", "Intermediate", "Advanced"]
    )

    if st.button("🏃 Get Exercise Plan"):
        if condition:
            with st.spinner("Creating exercise plan..."):
                full_condition = f"""
                Condition: {condition}
                Fitness Level: {fitness_level}
                """
                result = get_exercise_advice(
                    full_condition
                )
            st.success("✅ Exercise Plan Ready!")
            st.write(result)
        else:
            st.error("Please enter condition!")

# MEDICINE INFO
elif option == "💊 Medicine Info":
    st.header("💊 Medicine Information")
    st.info("Always consult doctor before taking medicine!")

    medicine = st.text_input(
        "Enter medicine name:",
        placeholder="Paracetamol, Ibuprofen, Aspirin"
    )

    if st.button("💊 Get Medicine Info"):
        if medicine:
            with st.spinner("Getting information..."):
                result = check_medicine_info(medicine)
            st.success("✅ Information Ready!")
            st.write(result)
        else:
            st.error("Please enter medicine name!")

# EMERGENCY CHECK
elif option == "🚨 Emergency Check":
    st.header("🚨 Emergency Checker")
    st.error("For life threatening emergencies call 112!")

    symptoms = st.text_area(
        "Describe symptoms:",
        placeholder="chest pain, difficulty breathing",
        height=150
    )

    if st.button("🚨 Check Emergency Level"):
        if symptoms:
            with st.spinner("Checking..."):
                result = emergency_check(symptoms)

            if "EMERGENCY" in result.upper():
                st.error(f"🚨 {result}")
                st.error("CALL 112 IMMEDIATELY!")
            else:
                st.success(result)
        else:
            st.error("Please enter symptoms!")

# PATIENT HISTORY
elif option == "📋 Patient History":
    st.header("📋 Patient History")

    records = get_all_history()

    if records:
        st.success(f"Found {len(records)} records")

        for record in records:
            with st.expander(
                f"📅 {record[1]} - {record[2]}"
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Your Input:**")
                    st.info(record[3])
                with col2:
                    st.write("**AI Response:**")
                    st.success(record[4])

        if st.button("🗑️ Clear All History"):
            delete_history()
            st.success("History cleared!")
            st.rerun()
    else:
        st.info("No history found!")

# BOOK APPOINTMENT
elif option == "📅 Book Appointment":
    st.header("📅 Book Doctor Appointment")

    tab1, tab2 = st.tabs([
        "📅 New Appointment",
        "📋 My Appointments"
    ])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            patient_name = st.text_input(
                "Your Full Name:"
            )
            specialty = st.selectbox(
                "Specialty:",
                list(DOCTORS.keys())
            )
            doctor = st.selectbox(
                "Doctor:",
                DOCTORS[specialty]
            )

        with col2:
            date = st.date_input("Appointment Date:")
            time = st.selectbox(
                "Time Slot:",
                [
                    "9:00 AM", "10:00 AM",
                    "11:00 AM", "2:00 PM",
                    "3:00 PM", "4:00 PM"
                ]
            )
            phone = st.text_input("Phone Number:")

        symptoms = st.text_area(
            "Describe your problem:"
        )

        if st.button("📅 Book Appointment"):
            if patient_name and symptoms and phone:
                result = book_appointment(
                    patient_name, doctor,
                    specialty, str(date),
                    time, symptoms
                )
                st.success(f"✅ {result}")
                st.balloons()

                st.info(f"""
                **Booking Confirmation:**
                - 👤 Patient: {patient_name}
                - 👨‍⚕️ Doctor: {doctor}
                - 🏥 Specialty: {specialty}
                - 📅 Date: {date}
                - ⏰ Time: {time}
                - 📞 Phone: {phone}
                """)
            else:
                st.error("Please fill all fields!")

    with tab2:
        search_name = st.text_input(
            "Enter your name to search:"
        )
        if st.button("🔍 Find Appointments"):
            if search_name:
                appointments = get_appointments(
                    search_name
                )
                if appointments:
                    for apt in appointments:
                        st.success(f"""
                        **Appointment #{apt[0]}**
                        - Doctor: {apt[2]}
                        - Date: {apt[4]}
                        - Time: {apt[5]}
                        - Status: {apt[7]}
                        """)
                else:
                    st.info("No appointments found!")

# LANGUAGE SUPPORT
elif option == "🌍 Language Support":
    st.header("🌍 Multi-Language Health Assistant")

    language = st.selectbox(
        "Choose Your Language:",
        list(LANGUAGES.keys())
    )

    symptoms = st.text_area(
        "Enter symptoms (in any language):"
    )

    if st.button("🌍 Get Advice in Your Language"):
        if symptoms:
            with st.spinner("Translating..."):
                result = analyze_in_language(symptoms, language)
            st.success("✅ Response Ready!")
            st.write(result)
        else:
            st.error("Please enter symptoms!")