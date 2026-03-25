# appointment.py
# Manages doctor appointments

import sqlite3
from datetime import datetime

def create_appointment_db():
    """Create appointments database"""
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY,
            patient_name TEXT,
            doctor_name TEXT,
            specialty TEXT,
            date TEXT,
            time TEXT,
            symptoms TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def book_appointment(
    patient_name,
    doctor_name,
    specialty,
    date,
    time,
    symptoms
):
    """Book a new appointment"""
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO appointments 
        (patient_name, doctor_name, specialty,
         date, time, symptoms, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        patient_name,
        doctor_name,
        specialty,
        date,
        time,
        symptoms,
        "Confirmed"
    ))
    
    conn.commit()
    conn.close()
    return "Appointment booked successfully!"

def get_appointments(patient_name):
    """Get all appointments for a patient"""
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM appointments
        WHERE patient_name = ?
        ORDER BY date DESC
    """, (patient_name,))
    
    records = cursor.fetchall()
    conn.close()
    return records

# List of available doctors
DOCTORS = {
    "General Physician": [
        "Dr. Sharma", "Dr. Patel", "Dr. Kumar"
    ],
    "Cardiologist": [
        "Dr. Singh", "Dr. Mehta"
    ],
    "Dermatologist": [
        "Dr. Gupta", "Dr. Joshi"
    ],
    "Neurologist": [
        "Dr. Verma", "Dr. Rao"
    ],
    "Orthopedic": [
        "Dr. Nair", "Dr. Reddy"
    ]
}