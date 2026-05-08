import os
import cv2
import django
import numpy as np
from ultralytics import YOLO
import easyocr
from datetime import datetime

# 1. Setup Django so this script can talk to your Database
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_core.settings')
django.setup()
from monitor.models import Violation

# 2. Initialize the AI Models
# 'yolo11n.pt' is fast and perfect for real-time portfolio projects
model = YOLO('yolo11n.pt') 
reader = easyocr.Reader(['en'])

def run_traffic_system(video_path):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

    
    # COORDINATES: Update these based on your specific video
    STOP_LINE_Y = 400 
    
    print("AI Engine Started... Press 'q' to stop.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLOv11 Detection (classes 2,3,5,7 = car, motorcycle, bus, truck)
        results = model(frame, classes=[2, 3, 5, 7], verbose=False)

        for result in results:
            for box in result.boxes:
                # Get coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = model.names[int(box.cls[0])]
                
                # Center-bottom point of the vehicle
                cx, cy = (x1 + x2) // 2, y2

                # VIOLATION LOGIC: If vehicle passes the stop line
                if cy > STOP_LINE_Y:
                    # Draw a Red box for violation
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    
                    # Capture the plate area and run OCR
                    plate_area = frame[y1:y2, x1:x2]
                    ocr_result = reader.readtext(plate_area)
                    plate_text = ocr_result[0][1] if ocr_result else "UNKNOWN"

                    # SAVE TO DJANGO DATABASE
                    # We check if it's already recorded (basic debouncing)
                    if not Violation.objects.filter(plate_number=plate_text, vehicle_type=label).exists():
                        Violation.objects.create(
                            plate_number=plate_text.upper(),
                            vehicle_type=label.capitalize(),
                            fine_amount=500
                        )
                        print(f"DATABASE UPDATED: {label} - {plate_text}")
                else:
                    # Draw a Green box for normal movement
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw the Stop Line on the screen
        cv2.line(frame, (0, STOP_LINE_Y), (frame.shape[1], STOP_LINE_Y), (255, 255, 255), 2)
        cv2.putText(frame, "STOP LINE", (10, STOP_LINE_Y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow("Smart Traffic System - AI Feed", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("\n---Traffic System Source Menu ---")
    print("1. Ues Local Video File")
    print("2. Use Wireless Phone Camera")
    
    choice = input("Select Video Source (1 or 2): ")

    if choice == '1':
        source = "traffic_video.mp4"
    else:
        source = "http://10.135.21.212:8080/video"

    print(f"Connecting to: {source}.... ")
    run_traffic_system(source)