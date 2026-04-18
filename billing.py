# billing.py
from datetime import datetime
from database import get_connection

def create_bill(
    patient_id,
    consultation_fee,
    medicine_cost,
    lab_cost,
    payment_method
):
    total = (
        consultation_fee +
        medicine_cost +
        lab_cost
    )

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO billing
        (patient_id, date,
         consultation_fee,
         medicine_cost, lab_cost,
         total_amount, paid_amount,
         payment_status, payment_method)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        patient_id,
        datetime.now().strftime("%Y-%m-%d"),
        consultation_fee,
        medicine_cost,
        lab_cost,
        total,
        total,
        "Paid",
        payment_method
    ))

    bill_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return bill_id, total

def get_patient_bills(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM billing
        WHERE patient_id = ?
        ORDER BY date DESC
    """, (patient_id,))
    bills = cursor.fetchall()
    conn.close()
    return [dict(b) for b in bills]

def get_daily_revenue():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(total_amount)
        FROM billing WHERE date = ?
    """, (today,))
    total = cursor.fetchone()[0]
    conn.close()
    return total or 0

def get_monthly_revenue():
    month = datetime.now().strftime("%Y-%m")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(total_amount)
        FROM billing WHERE date LIKE ?
    """, (f"{month}%",))
    total = cursor.fetchone()[0]
    conn.close()
    return total or 0