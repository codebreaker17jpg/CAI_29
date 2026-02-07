# 🎓 Smart Curriculum & Attendance System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-orange)

## 📌 Project Overview
The **Smart Curriculum Activity and Attendance App** is an AI-powered system designed to modernize educational tracking. It replaces manual roll calls with **Face Recognition** and uses **Machine Learning** to predict student detention risks before they happen.

This project was built as a Capstone Project to solve the inefficiency of manual attendance and provide actionable insights to faculty.

## ✨ Key Features

### 1. 📸 Smart Attendance (Face ID)
- **Zero-Touch Logging:** Students simply look at the camera to mark attendance.
- **Anti-Spoofing:** Built with `face_recognition` and OpenCV to detect live faces.
- **Instant Database Entry:** Automatically logs the student ID, date, and time into SQLite.

### 2. 🔮 AI Risk Predictor
- **Early Warning System:** Uses Logistic Regression to analyze attendance history.
- **Simulator Mode:** Teachers can adjust variables (e.g., "What if this student misses 3 more days?") to see if a student falls into the "At Risk" category.

### 3. 📊 Admin Dashboard & Reports
- **Live Logs:** View real-time attendance records.
- **Excel Export:** One-click download of attendance reports (`.csv`) for official record-keeping.
- **Data Visualization:** Clean tables showing "Safe" vs. "At Risk" status.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | Streamlit (Python) |
| **Backend** | FastAPI |
| **Database** | SQLite3 |
| **Computer Vision** | OpenCV, face_recognition, dlib |
| **Machine Learning** | Scikit-Learn, Pandas, NumPy |

---