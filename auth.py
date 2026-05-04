# auth.py
# Handles all login and registration
# Like security guard at hospital entrance

import sqlite3
import hashlib
from datetime import datetime
from database import get_connection

def hash_password(password):
    """
    Convert password to secret code
    Like locking a safe with a key

    Example:
    "mypassword" → "a8d4f2b9c1..."
    (unreadable encrypted text)
    """
    return hashlib.sha256(
        password.encode()
    ).hexdigest()

def register_user(
    username, password,
    role, full_name,
    email, phone
):
    """
    Create new user account
    Like registering new staff member
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if username exists
        cursor.execute("""
            SELECT id FROM users
            WHERE username = ?
        """, (username,))

        if cursor.fetchone():
            conn.close()
            return False, "Username already exists!"

        # Save new user
        hashed = hash_password(password)
        cursor.execute("""
            INSERT INTO users
            (username, password, role,
             full_name, email, phone,
             created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            username, hashed, role,
            full_name, email, phone,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )
        ))

        conn.commit()
        conn.close()
        return True, "Registration successful!"

    except Exception as e:
        return False, f"Error: {str(e)}"

def login_user(username, password):
    """
    Check if login is correct
    Like security guard checking ID card
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        hashed = hash_password(password)

        cursor.execute("""
            SELECT * FROM users
            WHERE username = ?
            AND password = ?
        """, (username, hashed))

        user = cursor.fetchone()
        conn.close()

        if user:
            return True, dict(user)
        else:
            return False, "Wrong credentials!"

    except Exception as e:
        return False, f"Error: {str(e)}"

def get_all_doctors():
    """Get list of all doctors"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users
        WHERE role = 'doctor'
    """)
    doctors = cursor.fetchall()
    conn.close()
    return [dict(d) for d in doctors]
