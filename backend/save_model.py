import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("backend/data/Attendance_risk.csv")


features = [
    "total_classes",
    "classes_attended",
    "attendance_percentage",
    "consecutive_absences",
    "avg_attendance_last_4_weeks"
]

X = df[features]
y = df["attendance_risk"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# Save model and scaler
joblib.dump(model, "backend/models/attendance_model.pkl")
joblib.dump(scaler, "backend/models/scaler.pkl")

print("Model and scaler saved successfully.")
