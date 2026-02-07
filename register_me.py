import cv2
import os
from backend.face_utils import save_face

def capture_and_register():
    # 1. Ask for the student's name/ID first
    name = input("Enter Student Name or ID: ")
    print(f"Opening camera for {name}... Press 'SPACE' to capture, 'Q' to quit.")

    # 2. Open the Webcam
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Show the video window
        cv2.imshow("Register Student (Press Space to Capture)", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27 or k % 256 == ord('q'):
            # ESC or Q pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = f"{name}_registered.jpg"
            
            # Save the image locally first
            cv2.imwrite(img_name, frame)
            print(f"Snapshot saved: {img_name}")
            
            # 3. Send to your backend logic
            print("Processing face data...")
            success = save_face(name, img_name)
            
            if success:
                print(f"✅ Success! {name} has been registered in the database.")
            else:
                print("❌ Error: No face detected in the photo. Try again with better lighting.")
            
            # Clean up the temp file if you want, or keep it as backup
            # os.remove(img_name) 
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_register()