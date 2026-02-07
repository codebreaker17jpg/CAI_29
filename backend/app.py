from fastapi import FastAPI, File, UploadFile
import joblib
import numpy as np
from backend.database import (
    create_table,
    create_students_table,
    create_attendance_logs_table,
    get_connection
)
from backend.face_utils import recognize_face
from datetime import datetime

app = FastAPI(title="Punjab Smart Attendance API")

# Load model and scaler
# Ensure these files exist in backend/models/ or comment these 2 lines out if testing locally without them
try:
    model = joblib.load("backend/models/attendance_model.pkl")
    scaler = joblib.load("backend/models/scaler.pkl")
except:
    print("Warning: ML Models not found. Risk prediction will fail, but Face ID will work.")
    model = None
    scaler = None

# Create DB tables on startup
create_table()
create_students_table()
create_attendance_logs_table()

@app.get("/")
def home():
    return {"message": "Punjab Smart Attendance API is running."}

# --- THE NEW SMART FACE RECOGNITION ENDPOINT ---
@app.post("/scan_face")
async def scan_face(file: UploadFile = File(...)):
    # 1. Read the uploaded image
    image_bytes = await file.read()
    
    # 2. Use our helper to recognize the face
    name = recognize_face(image_bytes)
    
    if name and name != "Unknown" and name != "No Students Registered":
        # 3. Mark attendance in DB
        today = datetime.now().strftime("%Y-%m-%d")
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if already marked today
        cursor.execute("SELECT * FROM attendance_logs WHERE student_id = ? AND date = ?", (name, today))
        if cursor.fetchone():
            conn.close()
            return {"status": "Already Marked", "student": name}
            
        # Insert new record
        cursor.execute("INSERT INTO attendance_logs (student_id, date, status) VALUES (?, ?, ?)", (name, today, "Present"))
        conn.commit()
        conn.close()
        
        return {"status": "Success", "student": name}
    
    return {"status": "Failed", "student": name}

# --- EXISTING RISK PREDICTION ENDPOINTS ---
@app.post("/predict")
def predict_attendance_risk(
    total_classes: int,
    classes_attended: int,
    attendance_percentage: float,
    consecutive_absences: int,
    avg_attendance_last_4_weeks: float
):
    if not model:
        return {"error": "Model not loaded"}

    data = np.array([[
        total_classes,
        classes_attended,
        attendance_percentage,
        consecutive_absences,
        avg_attendance_last_4_weeks
    ]])

    data_scaled = scaler.transform(data)
    prediction = model.predict(data_scaled)[0]
    
    return {
        "attendance_risk": int(prediction),
        "status": "At Risk" if prediction == 1 else "Safe"
    }

@app.get("/records")
def get_all_records(limit: int = 50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance_predictions ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows