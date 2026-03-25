# history_manager.py
# This saves all patient conversations
# SQLite = a simple database stored as a file

import sqlite3      # database library
from datetime import datetime  # for timestamps

def create_database():
    """
    Creates a database file called health_history.db
    Think of it like creating an Excel file
    """
    conn = sqlite3.connect("health_history.db")
    cursor = conn.cursor()
    
    # Create table - like creating Excel columns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY,
            date TEXT,
            type TEXT,
            input TEXT,
            response TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_history(query_type, user_input, ai_response):
    """
    Save a conversation to database
    
    Example:
    type = "symptoms"
    input = "headache and fever"
    response = "Here is advice..."
    """
    conn = sqlite3.connect("health_history.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO history (date, type, input, response)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        query_type,
        user_input,
        ai_response
    ))
    
    conn.commit()
    conn.close()

def get_all_history():
    """
    Get all saved conversations
    Returns list of all records
    """
    conn = sqlite3.connect("health_history.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM history 
        ORDER BY date DESC
    """)
    
    records = cursor.fetchall()
    conn.close()
    return records

def delete_history():
    """Delete all history"""
    conn = sqlite3.connect("health_history.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()