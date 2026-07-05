# IoT and Computer Vision-Based Smart Stick for the Visually Impaired Person

# 1. cv2 (OpenCV)
#        -> Used to capture and process video frames from ESP32-CAM stream
#        -> Reads MJPEG stream are other from ESP32-CAM
#        -> Displays video
#        -> Draws bounding boxes after detection

# 2. requests
# A. Used to send HTTP commands to ESP32
# B. Sends detection result (e.g., "person detected")
# C. ESP32 uses this signal to trigger DFPlayer Mini

#3.  numpy
# i. Used for handling image data as arrays
# ii. Converts raw stream bytes into image format
# iii. Required for OpenCV processing

#4.  time
#  a) Used for timing control
#  b) Adds delay between detections
#  c) Prevents sending too many requests to ESP32

# 5. YOLO (Ultralytics)
# AI model used for object detection
# Detects objects (person, bottle, car, etc.)
# Returns bounding boxes, labels, confidence scores

"""......................................
......................................."""

# PROJECT WORKFLOW

# 1. ESP32-CAM streams live video over WiFi
# 2. Python (cv2) reads the stream frame-by-frame
# 3. YOLO model processes each frame and detects objects
# 4. If target object is detected:
#       -> Python sends HTTP request using requests
# 5. ESP32 receives signal
# 6. ESP32 triggers DFPlayer Mini
# 7. DFPlayer plays corresponding voice/audio

##################################################
##################################################

# MAIN PURPOSE

#  Build a real-time vision-based alert system
#  Detect object using AI
#  Send signal to hardware
#  Play voice feedback via DFPlayer Mini


###################################################
###################################################


import cv2
import requests
import numpy as np
import time
from ultralytics import YOLO

# Here we put our ESP32 IP and ESP32-CAM URL
# Before this I use the ip of both devices but this work smootly

CAM_URL = "http://192.168.170.105/"  

#  use Port 80 here. Mean HTTP 

ESP32_IP = "192.168.170.166"


# In frist way to test the YOLOV8n becuse this is light model
# If further need to use other microcontrol we test the YOLO11
# YOLO mean-> You Only Look Once, it's a real-time object detection system that can identify and locate multiple objects in an image or video stream with high accuracy and speed. The "v8n" version is a lightweight model designed for efficient inference on edge devices, making it ideal for applications like our smart stick project where resources are limited.
model = YOLO("yolov8n.pt") 

print("Starting AI System with Advanced Stream Decoder...")
last_voice_time = 0
VOICE_COOLDOWN = 4  

while True:
    try:
        print(f" Connecting to {CAM_URL}...")
        
        # stream=True tells Python to intercept the raw MJPEG bytes over WiFi
        res = requests.get(CAM_URL, stream=True, timeout=5)
        
        if res.status_code != 200:
            print(" Cannot connect to camera. Retrying...")
            time.sleep(2)
            continue

        byte_buffer = b''
        print(" Stream connected! Processing AI...")

        for chunk in res.iter_content(chunk_size=1024):
            byte_buffer += chunk
            
            # Search the byte stream for the start and end of a JPEG frame
            a = byte_buffer.find(b'\xff\xd8')
            b = byte_buffer.find(b'\xff\xd9')
            
            # If we find a full image frame, extract it!
            if a != -1 and b != -1:
                jpg = byte_buffer[a:b+2]
                byte_buffer = byte_buffer[b+2:] # Clear buffer for the next frame
                
                # Convert the raw bytes into a frame OpenCV can read
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                
                if frame is None:
                    continue
                    
                # --- AI PROCESSING ---
                display_frame = frame.copy()
                
                # High speed, low RAM inference
                results = model.predict(frame, imgsz=256, conf=0.5, verbose=False)
                detected_something = False

                for r in results:
                    boxes = r.boxes
                    if len(boxes) > 0:
                        detected_something = True
                        
                        best_box = boxes[0] 
                        cls = int(best_box.cls[0])
                        conf = float(best_box.conf[0])
                        label = model.names[cls]
                        
                        x1, y1, x2, y2 = map(int, best_box.xyxy[0])
                        cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(display_frame, f"{label} {conf:.2f}", (x1, y1 - 10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                        track_id = cls + 3 

                        if time.time() - last_voice_time > VOICE_COOLDOWN:
                            try:
                                payload = {"id": track_id, "name": label}
                                requests.get(f"http://{ESP32_IP}/play", params=payload, timeout=0.2)
                                print(f" Sent -> ID: {track_id} | Name: {label}")
                                last_voice_time = time.time()
                            except:
                                print(" ESP32 Audio Offline...")
                        break 

                # Play "Confused" (83.mp3) if confidence is too low
                if not detected_something:
                    low_conf = model.predict(frame, imgsz=256, conf=0.2, verbose=False)
                    if len(low_conf[0].boxes) > 0:
                        if time.time() - last_voice_time > VOICE_COOLDOWN:
                            try:
                                requests.get(f"http://{ESP32_IP}/play", params={"id": 83, "name": "Unknown"}, timeout=0.2)
                                print("❓ Sent -> ID: 83 | Name: Unknown")
                                last_voice_time = time.time()
                            except:
                                pass

                # --- RESIZE WINDOW FOR DISPLAY ---
                # This scales the final output window down to 50% without affecting AI accuracy
                small_display = cv2.resize(display_frame, (0, 0), fx=0.5, fy=0.5)

                # Show the smaller feed
                cv2.imshow("Smart Stick AI Monitor", small_display)
                
                # ESC key to exit safely
                if cv2.waitKey(1) & 0xFF == 27:
                    res.close()
                    cv2.destroyAllWindows()
                    exit()

    except Exception as e:
        print(f" Network error: {e}. Retrying in 2 seconds...")
        time.sleep(2)