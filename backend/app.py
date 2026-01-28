from fastapi import FastAPI
import joblib
import numpy as np
from backend.database import create_table, get_connection

app = FastAPI(title="Punjab Smart Attendance API")

# Load model and scaler
model = joblib.load("backend/models/attendance_model.pkl")
scaler = joblib.load("backend/models/scaler.pkl")

# Create DB table on startup
create_table()

@app.get("/")
def home():
    return {"message": "Punjab Smart Attendance API is running"}

@app.post("/predict")
def predict_attendance_risk(
    total_classes: int,
    classes_attended: int,
    attendance_percentage: float,
    consecutive_absences: int,
    avg_attendance_last_4_weeks: float
):
    # Prepare input
    data = np.array([[
        total_classes,
        classes_attended,
        attendance_percentage,
        consecutive_absences,
        avg_attendance_last_4_weeks
    ]])

    # Scale + predict
    data_scaled = scaler.transform(data)
    prediction = model.predict(data_scaled)[0]

    # Store in DB
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attendance_predictions (
            total_classes,
            classes_attended,
            attendance_percentage,
            consecutive_absences,
            avg_attendance_last_4_weeks,
            prediction
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        total_classes,
        classes_attended,
        attendance_percentage,
        consecutive_absences,
        avg_attendance_last_4_weeks,
        int(prediction)
    ))

    conn.commit()
    conn.close()

    return {
        "attendance_risk": int(prediction),
        "status": "At Risk" if prediction == 1 else "Safe"
    }

@app.get("/records")
def get_all_records(limit: int = 50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            id,
            total_classes,
            classes_attended,
            attendance_percentage,
            consecutive_absences,
            avg_attendance_last_4_weeks,
            prediction,
            created_at
        FROM attendance_predictions
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows
