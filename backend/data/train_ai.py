import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# 1. Create the models folder if it doesn't exist
if not os.path.exists("backend/models"):
    os.makedirs("backend/models")

print("Generating synthetic student data...")

# 2. Generate Dummy Data (Since we don't have the CSV)
# We create 1000 random students with realistic attendance patterns
np.random.seed(42)
n_samples = 1000

total_classes = np.random.randint(50, 200, n_samples)
classes_attended = []
attendance_percentage = []
risk_labels = []

for total in total_classes:
    # Randomly decide if student is "Good" or "Bad"
    if np.random.random() > 0.3: 
        # Good student (High attendance)
        attended = np.random.randint(int(total * 0.75), total)
    else:
        # At-risk student (Low attendance)
        attended = np.random.randint(0, int(total * 0.70))
    
    classes_attended.append(attended)
    pct = (attended / total) * 100
    attendance_percentage.append(pct)
    
    # Label: 1 if attendance < 75%, else 0
    risk_labels.append(1 if pct < 75 else 0)

# Create DataFrame
df = pd.DataFrame({
    "total_classes": total_classes,
    "classes_attended": classes_attended,
    "attendance_percentage": attendance_percentage,
    "consecutive_absences": np.random.randint(0, 10, n_samples),
    "avg_attendance_last_4_weeks": np.random.uniform(50, 100, n_samples),
    "attendance_risk": risk_labels
})

# 3. Prepare for Training
features = [
    "total_classes", "classes_attended", "attendance_percentage", 
    "consecutive_absences", "avg_attendance_last_4_weeks"
]
X = df[features]
y = df["attendance_risk"]

# Split & Scale
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# 4. Train the Model
print("Training the AI model...")
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# 5. Save the Brains
joblib.dump(model, "backend/models/attendance_model.pkl")
joblib.dump(scaler, "backend/models/scaler.pkl")

print("✅ Success! Model trained and saved to 'backend/models/'")