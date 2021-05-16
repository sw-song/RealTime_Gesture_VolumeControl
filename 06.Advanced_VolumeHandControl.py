import cv2
import time
import numpy as np
import Advanced_HandTrackingModule as A_HTM 
import math
from Foundation import NSAppleScript as NSA

##### parameter
pTime = 0
area = 0
#### Video Controler
cap = cv2.VideoCapture(0)

#### Object Detection Module
detector = A_HTM.handDetector(maxHands=1)


while True:

    # Find Hand
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmList, bbox = detector.findPosition(img, draw=True)
    #cv2.circle(img, lmList[9], 20, (255,255,255))
    
    # Display Volume
    cv2.rectangle(img, (50,100), (85,300), (0,255,0), 3)
    script = NSA.alloc().initWithSource_('output volume of (get volume settings)')
    result, error_info = script.executeAndReturnError_(None)
    volume = int(result.stringValue())
    cv2.rectangle(img, (52, (302-(2*volume))), (83,298), (200,255,200), cv2.FILLED)
    cv2.putText(img, 'Volume: {} %'.format(volume), (40, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
    print(len(lmList))
    # Hand in screen,
    if len(lmList) != 0:

        # Find Distance Between index and Thumb (for control volume with hand gesture)
        length, img, lineInfo = detector.findDistance(4,8,img)
        # print(length)

        # Convert Volume 
        range30to230 = lambda x : 30 if x <= 30 else 230 if x >= 230 else x
        length100 = int((range30to230(length)-30)/2)
        
    
        # Check Fingers up
        fingers = detector.fingersUp()
        #if not fingers[2]:
        script = NSA.alloc().initWithSource_('set volume output volume {}'.format(length100))
        script.executeAndReturnError_(None)

        # If pinky is down set volume
        # Drawings
        #cv2.rectangle(img, (52, (302-(2*length100))), (83,298), (0,0,255), cv2.FILLED)
        #cv2.putText(img, 'Volume: {} %'.format(length100), (40, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
    

        #volume = int(result.stringValue())
        #cv2.rectangle(img, (50, (100+(2*volume))), (85,300), (0,0,255), cv2.FILLED)
        #cv2.putText(img, 'Volume: {} %'.format(volume), (40, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
    

    # Frame rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, 'FPS: {}'.format(int(fps)), (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)