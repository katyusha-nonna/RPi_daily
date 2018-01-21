import cv2
import os

haarcascade_path=os.getcwd()+"/haarcascade_frontalface_default.xml"
face_det=cv2.CascadeClassifier(haarcascade_path)
camera=cv2.VideoCapture(0)
while camera.isOpened():
    ret, frame=camera.read()
    gray_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=face_det.detectMultiScale(gray_frame)
    if len(faces)>0:
        for single_face in faces:
            (x, y, w, h)=faces[0]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("camera", frame)
    if cv2.waitKey(1)==ord("q"):
        break
camera.release()
cv2.destroyAllWindows()
