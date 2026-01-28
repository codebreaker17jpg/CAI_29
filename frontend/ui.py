import streamlit as st
import requests

st.set_page_config(page_title="Punjab Smart Attendance System")

st.title("Punjab Smart Attendance Risk Predictor")
st.write("Government Institutions – Attendance Monitoring")

st.subheader("Enter Attendance Details")

total_classes = st.number_input("Total Classes", min_value=1, value=200)
classes_attended = st.number_input("Classes Attended", min_value=0, value=150)
attendance_percentage = st.number_input("Attendance Percentage", min_value=0.0, max_value=100.0, value=75.0)
consecutive_absences = st.number_input("Consecutive Absences", min_value=0, value=1)
avg_attendance_last_4_weeks = st.number_input("Average Attendance (Last 4 Weeks)", min_value=0.0, max_value=100.0, value=80.0)

if st.button("Predict Attendance Risk"):
    payload = {
        "total_classes": total_classes,
        "classes_attended": classes_attended,
        "attendance_percentage": attendance_percentage,
        "consecutive_absences": consecutive_absences,
        "avg_attendance_last_4_weeks": avg_attendance_last_4_weeks
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", params=payload)
        result = response.json()

        st.subheader("Prediction Result")
        if result["attendance_risk"] == 1:
            st.error("⚠️ Student is AT RISK of low attendance")
        else:
            st.success("✅ Student attendance is SAFE")

    except Exception as e:
        st.error("Backend API is not running. Please start the FastAPI server.")


#Prediction Records
st.divider()
st.subheader("Admin View – Recent Predictions")

if st.button("Load Recent Records"):
    try:
        records = requests.get("http://127.0.0.1:8000/records").json()

        if len(records) == 0:
            st.info("No records found.")
        else:
            st.table([
                {
                    "ID": r[0],
                    "Total": r[1],
                    "Attended": r[2],
                    "Attendance %": r[3],
                    "Absences": r[4],
                    "Avg 4 Weeks": r[5],
                    "Risk": "At Risk" if r[6] == 1 else "Safe",
                    "Time": r[7]
                }
                for r in records
            ])
    except:
        st.error("Unable to fetch records. Is backend running?")
    
