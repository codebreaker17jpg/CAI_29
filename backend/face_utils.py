import face_recognition
import pickle
import os
import numpy as np
import cv2 

# File to store face encodings
ENCODINGS_FILE = "backend/encodings.pkl"

def load_known_faces():
    """Loads names and face encodings from the pickle file."""
    if not os.path.exists(ENCODINGS_FILE):
        return [], []
    
    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)
    return data["encodings"], data["names"]

def save_face(name, image_path):
    """Encodes a face from an image path and saves it to the pickle file."""
    # Load existing data
    known_encodings, known_names = load_known_faces()
    
    # 1. Load image using OpenCV
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Error: Could not read image from {image_path}")
        return False

    # 2. Convert from BGR to RGB (Face Recognition requirement)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 3. CRITICAL FIX: Ensure the array is clean for dlib
    rgb_img = np.ascontiguousarray(rgb_img)
    
    # 4. Get encodings
    try:
        encodings = face_recognition.face_encodings(rgb_img)
    except Exception as e:
        print(f"Error processing face: {e}")
        return False
    
    if len(encodings) > 0:
        known_encodings.append(encodings[0])
        known_names.append(name)
        
        # Save back to file
        with open(ENCODINGS_FILE, "wb") as f:
            pickle.dump({"encodings": known_encodings, "names": known_names}, f)
        return True
    
    print("No face detected in the image.")
    return False

def recognize_face(image_bytes):
    """Takes raw image bytes, finds faces, and identifies the student."""
    known_encodings, known_names = load_known_faces()
    
    if not known_encodings:
        return "No Students Registered"

    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Convert to RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb_img = np.ascontiguousarray(rgb_img)
    
    # Find faces
    face_locations = face_recognition.face_locations(rgb_img)
    face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
    
    detected_name = "Unknown"
    
    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding)
        face_distances = face_recognition.face_distance(known_encodings, encoding)
        
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                detected_name = known_names[best_match_index]
                break 
            
    return detected_name