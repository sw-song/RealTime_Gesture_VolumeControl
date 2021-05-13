import cv2
import mediapipe as mp 
import time
import HandTrackingModule as htm 

cap = cv2.VideoCapture(0)
pTime = 0
cTime = 0
detector = htm.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList[0])

    cTime = time.time()
    fps = 1/(cTime-pTime) # Frame Per Seconds
    pTime = cTime         # ex. fps == 1 / 0.03 == 33.33

    cv2.putText(img, 
                str(int(fps)), 
                (10,70), 
                cv2.FONT_HERSHEY_PLAIN, 
                3, 
                (255,0,255), 
                3)
    if success == True:
        cv2.imshow('Image', img)
        cv2.waitKey(1)