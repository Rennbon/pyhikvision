import face_recognition
import cv2
import numpy as np

url = "rtsp://admin:Aa123456@192.168.254.6:554/11"

cap = cv2.VideoCapture(url)
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
