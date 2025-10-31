import cv2
import numpy as np
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from ultralytics import YOLO
import threading

people_count = 0
model = None
cap = None
lock = threading.Lock()

def load_model():
    global model
    if model is None:
        model = YOLO('yolov8n.pt')
    return model

def home(request):
    return render(request, 'counter_app/home.html')

def detect_people(frame):
    global people_count
    
    model = load_model()
    
    results = model(frame, classes=[0], conf=0.5, verbose=False)
    
    count = 0
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = box.conf[0].cpu().numpy()
            
            cv2.rectangle(frame, 
                         (int(x1), int(y1)), 
                         (int(x2), int(y2)), 
                         (0, 255, 0), 2)
            
            label = f'Persona {conf:.2f}'
            cv2.putText(frame, label, 
                       (int(x1), int(y1) - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (0, 255, 0), 2)
            
            count += 1
    
    with lock:
        people_count = count
    
    cv2.putText(frame, f'Personas: {count}', 
               (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 
               1, (0, 255, 255), 2)
    
    return frame

def generate_frames():
    global cap
    
    if cap is None:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    while True:
        success, frame = cap.read()
        
        if not success:
            break
        
        frame = detect_people(frame)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(
        generate_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

def get_count(request):
    global people_count
    with lock:
        count = people_count
    return JsonResponse({'count': count})

