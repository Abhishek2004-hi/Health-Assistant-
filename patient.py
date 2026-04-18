# patient.py
# All patient related functions
# Like patient management department

import sqlite3
from datetime import datetime
from database import get_connection
import random
import string

def generate_patient_id():
    """
    Generate unique patient ID
    Like assigning hospital card number

    Example output: "PAT-2026-ABC12"
    """
    year = datetime.now().year
    random_part = ''.join(
        random.choices(
            string.ascii_uppercase +
            string.digits, k=5
        )
    )
    return f"PAT-{year}-{random_part}"

def register_patient(
    full_name, age, gender,
    blood_group, phone, email,
    address, emergency_contact,
    allergies
):
    """
    Register new patient
    Like receptionist adding new patient file
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        patient_id = generate_patient_id()

        cursor.execute("""
            INSERT INTO patients
            (patient_id, full_name, age,
             gender, blood_group, phone,
             email, address,
             emergency_contact,
             allergies, registered_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            patient_id, full_name, age,
            gender, blood_group, phone,
            email, address,
            emergency_contact, allergies,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )
        ))

        conn.commit()
        conn.close()
        return True, patient_id

    except Exception as e:
        return False, str(e)

def get_patient(patient_id):
    """Find patient by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM patients
        WHERE patient_id = ?
    """, (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    return dict(patient) if patient else None

def search_patients(search_term):
    """Search patients by name or phone"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM patients
        WHERE full_name LIKE ?
        OR phone LIKE ?
        OR patient_id LIKE ?
        ORDER BY registered_at DESC
    """, (
        f"%{search_term}%",
        f"%{search_term}%",
        f"%{search_term}%"
    ))
    patients = cursor.fetchall()
    conn.close()
    return [dict(p) for p in patients]

def get_all_patients():
    """Get all registered patients"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM patients
        ORDER BY registered_at DESC
    """)
    patients = cursor.fetchall()
    conn.close()
    return [dict(p) for p in patients]

def add_medical_record(
    patient_id, doctor_id,
    diagnosis, symptoms,
    treatment, prescription,
    notes, follow_up
):
    """
    Add medical record for patient
    Like doctor filling patient file
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO medical_records
        (patient_id, doctor_id, date,
         diagnosis, symptoms, treatment,
         prescription, notes, follow_up)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        patient_id, doctor_id,
        datetime.now().strftime("%Y-%m-%d"),
        diagnosis, symptoms, treatment,
        prescription, notes, follow_up
    ))
    conn.commit()
    conn.close()
    return True

def get_medical_history(patient_id):
    """Get all medical records of patient"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM medical_records
        WHERE patient_id = ?
        ORDER BY date DESC
    """, (patient_id,))
    records = cursor.fetchall()
    conn.close()
    return [dict(r) for r in records]

def add_lab_report(
    patient_id, test_name,
    result, normal_range,
    status, notes
):
    """Add lab test report"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO lab_reports
        (patient_id, test_name, result,
         normal_range, status, date, notes)
        VALUES (?,?,?,?,?,?,?)
    """, (
        patient_id, test_name, result,
        normal_range, status,
        datetime.now().strftime("%Y-%m-%d"),
        notes
    ))
    conn.commit()
    conn.close()
    return True

def get_lab_reports(patient_id):
    """Get all lab reports of patient"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM lab_reports
        WHERE patient_id = ?
        ORDER BY date DESC
    """, (patient_id,))
    reports = cursor.fetchall()
    conn.close()
    return [dict(r) for r in reports]