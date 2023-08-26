import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

face_below_center = False
start_time = None
s = True
start = time.time( )

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        roi_gray = gray[y:y+w, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
    if len(faces) > 0:
        face = faces[0]
        face_center_x = face[0] + face[2] // 2
        face_center_y = face[1] + face[3] // 2
        image_center_x, image_center_y = frame.shape[1] // 2, frame.shape[0] // 2
        displacement_x = face_center_x - image_center_x
        displacement_y = face_center_y - image_center_y
        y = displacement_y
        if (y > 0):
            t = int(time.time() - start)
            cv2.putText(frame, "{} seconds".format(t),(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(15,225,215),2)
            if t > 15:
                cv2.putText(frame, "FIX POSTURE",(50,185),cv2.FONT_HERSHEY_COMPLEX,2,(15,225,215),2)
        else:
            start = time.time( )
        cv2.rectangle(frame, (face[0], face[1]), (face[0] + face[2], face[1] + face[3]), (0, 255, 0), 2)
        cv2.line(frame, (image_center_x, image_center_y), (face_center_x, face_center_y), (255, 0, 0), 2)
    else:
        start = time.time( )
    cv2.imshow('Alert', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()