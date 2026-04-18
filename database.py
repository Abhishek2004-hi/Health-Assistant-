# database.py
# Creates ALL database tables
# Think of it as setting up
# all filing cabinets in hospital

import sqlite3
from datetime import datetime

DATABASE = "hospital.db"

def get_connection():
    """
    Get database connection
    Like picking up phone to call database
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_all_tables():
    """
    Create ALL tables needed
    Like setting up all departments
    in a new hospital
    """
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE (Doctors + Admins)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            created_at TEXT
        )
    """)

    # PATIENTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            patient_id TEXT UNIQUE,
            full_name TEXT,
            age INTEGER,
            gender TEXT,
            blood_group TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            emergency_contact TEXT,
            allergies TEXT,
            registered_at TEXT
        )
    """)

    # APPOINTMENTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY,
            patient_id TEXT,
            doctor_id INTEGER,
            date TEXT,
            time TEXT,
            reason TEXT,
            status TEXT,
            notes TEXT,
            created_at TEXT
        )
    """)

    # MEDICAL RECORDS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY,
            patient_id TEXT,
            doctor_id INTEGER,
            date TEXT,
            diagnosis TEXT,
            symptoms TEXT,
            treatment TEXT,
            prescription TEXT,
            notes TEXT,
            follow_up TEXT
        )
    """)

    # LAB REPORTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lab_reports (
            id INTEGER PRIMARY KEY,
            patient_id TEXT,
            test_name TEXT,
            result TEXT,
            normal_range TEXT,
            status TEXT,
            date TEXT,
            notes TEXT
        )
    """)

    # BILLING TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS billing (
            id INTEGER PRIMARY KEY,
            patient_id TEXT,
            date TEXT,
            consultation_fee REAL,
            medicine_cost REAL,
            lab_cost REAL,
            total_amount REAL,
            paid_amount REAL,
            payment_status TEXT,
            payment_method TEXT
        )
    """)

    # MEDICINES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            price REAL,
            stock INTEGER,
            expiry TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("All tables created! ✅")
    