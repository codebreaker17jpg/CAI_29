import streamlit as st
import requests
import pandas as pd

# Page Config
st.set_page_config(page_title="Punjab Smart Attendance", layout="wide")
st.title("🎓 Punjab Smart Attendance System")

# Create Tabs
tab1, tab2, tab3 = st.tabs(["📸 Smart Attendance", "📊 Risk Predictor (Simulator)", "📝 Admin View"])

# --- TAB 1: FACE RECOGNITION ---
with tab1:
    st.header("Mark Attendance via Face ID")
    st.info("Look at the camera and click 'Take Photo' to mark yourself Present.")
    
    img_file_buffer = st.camera_input("Take a picture")
    
    if img_file_buffer is not None:
        with st.spinner("Processing Face..."):
            bytes_data = img_file_buffer.getvalue()
            
            try:
                # Send to backend
                files = {"file": ("filename", bytes_data, "image/jpeg")}
                response = requests.post("http://127.0.0.1:8000/scan_face", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")
                    student = data.get("student")
                    
                    if status == "Success":
                        st.success(f"✅ Attendance Marked for: **{student}**")
                        st.balloons()
                    elif status == "Already Marked":
                        st.warning(f"⚠️ Attendance already marked for today: **{student}**")
                    else:
                        st.error(f"❌ Face not recognized. (Detected: {student})")
                else:
                    st.error("Server Error.")
            except Exception as e:
                st.error(f"Could not connect to backend. {e}")

# --- TAB 2: RISK PREDICTOR (Simulator) ---
with tab2:
    st.header("🔮 Attendance Risk Simulator")
    st.markdown("""
    **Professor's Tool:** Use this simulator to check if a student is at risk of detention based on their history.
    *Try changing the values below to see the AI predict 'Safe' or 'At Risk'.*
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        total_classes = st.number_input("Total Classes Held", value=200)
        classes_attended = st.number_input("Classes Attended", value=150)
        # Auto-calculate percentage
        calc_pct = (classes_attended / total_classes) * 100 if total_classes > 0 else 0
        st.caption(f"Calculated Percentage: {calc_pct:.2f}%")
        
    with col2:
        attendance_percentage = st.slider("Current Attendance %", 0, 100, int(calc_pct))
        consecutive_absences = st.number_input("Consecutive Absences (Days)", value=1)
        avg_attendance_last_4_weeks = st.slider("Avg Attendance (Last Month)", 0, 100, 80)

    if st.button("Predict Risk Status", type="primary"):
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
            
            st.divider()
            if result["attendance_risk"] == 1:
                st.error(f"⚠️ **STATUS: AT RISK**")
                st.write("Prediction: This student is likely to fall below the mandatory attendance criteria.")
            else:
                st.success(f"✅ **STATUS: SAFE**")
                st.write("Prediction: This student has healthy attendance patterns.")
                
        except:
            st.error("Backend API is not running.")

# --- TAB 3: ADMIN RECORDS & DOWNLOAD ---
with tab3:
    st.header("📋 Daily Attendance Logs")
    
    col_a, col_b = st.columns([1, 4])
    with col_a:
        refresh = st.button("Refresh Logs")
    
    # Logic to load data
    try:
        # Fetch Data
        records = requests.get("http://127.0.0.1:8000/records").json()
        
        if len(records) > 0:
            # Convert to DataFrame
            df = pd.DataFrame(records, columns=[
                "ID", "Total Classes", "Attended", "Percentage", 
                "Consecutive Absences", "Avg (4 Weeks)", 
                "Risk Prediction", "Timestamp"
            ])
            
            # Create a "Human Readable" version for the screen
            display_df = df.copy()
            display_df["Risk Prediction"] = display_df["Risk Prediction"].apply(lambda x: "⚠️ At Risk" if x == 1 else "✅ Safe")
            
            # Show the Table
            st.dataframe(display_df, use_container_width=True)
            
            # --- THE NEW CSV DOWNLOAD BUTTON ---
            # We convert the dataframe to a CSV string
            csv = display_df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Download Report as CSV",
                data=csv,
                file_name='attendance_report.csv',
                mime='text/csv',
            )
        else:
            st.info("No records found yet.")
            
    except Exception as e:
        st.error(f"Error fetching data: {e}")