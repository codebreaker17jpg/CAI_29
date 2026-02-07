import sqlite3

def get_connection():
    conn = sqlite3.connect("backend/attendance.db", check_same_thread=False)
    return conn

#attendance predictions table
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_classes INTEGER,
            classes_attended INTEGER,
            attendance_percentage REAL,
            consecutive_absences INTEGER,
            avg_attendance_last_4_weeks REAL,
            prediction INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

#students table
def create_students_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE,
            name TEXT,
            institute TEXT
        )
    """)

    conn.commit()
    conn.close()

#attendance logs table
def create_attendance_logs_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            date TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()
