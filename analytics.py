# analytics.py
# Hospital statistics and reports
# Like hospital management reports

import sqlite3
import pandas as pd
from datetime import datetime
from database import get_connection

def get_total_stats():
    """Get overall hospital statistics"""
    conn = get_connection()
    cursor = conn.cursor()

    stats = {}

    # Total patients
    cursor.execute(
        "SELECT COUNT(*) FROM patients"
    )
    stats["total_patients"] = (
        cursor.fetchone()[0]
    )

    # Today's appointments
    today = datetime.now().strftime(
        "%Y-%m-%d"
    )
    cursor.execute("""
        SELECT COUNT(*) FROM appointments
        WHERE date = ?
    """, (today,))
    stats["today_appointments"] = (
        cursor.fetchone()[0]
    )

    # Total doctors
    cursor.execute("""
        SELECT COUNT(*) FROM users
        WHERE role = 'doctor'
    """)
    stats["total_doctors"] = (
        cursor.fetchone()[0]
    )

    # Today's revenue
    cursor.execute("""
        SELECT SUM(total_amount)
        FROM billing WHERE date = ?
    """, (today,))
    revenue = cursor.fetchone()[0]
    stats["today_revenue"] = revenue or 0

    conn.close()
    return stats

def get_patient_gender_data():
    """Get patient gender distribution"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT gender, COUNT(*) as count
        FROM patients
        GROUP BY gender
    """)
    data = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in data}

def get_monthly_patients():
    """Get monthly patient registration"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            strftime('%Y-%m', registered_at)
            as month,
            COUNT(*) as count
        FROM patients
        GROUP BY month
        ORDER BY month DESC
        LIMIT 6
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def get_appointment_stats():
    """Get appointment statistics"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM appointments
        GROUP BY status
    """)
    data = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in data}