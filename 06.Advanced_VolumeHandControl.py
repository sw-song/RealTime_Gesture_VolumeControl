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
detector = A_HTM.handDetector()
s = NSA.alloc().initWithSource_("tell app \"Finder\" to activate")
s.executeAndReturnError_(None)

while True:

    # Find Hand
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)
    cv2.rectangle(img, (50,100), (85,300), (0,0,0), 3)
    script = NSA.alloc().initWithSource_('output volume of (get volume settings)')
    result, error_info = script.executeAndReturnError_(None)
    volume = int(result.stringValue())
    print(volume)
    cv2.rectangle(img, (52, (302-(2*volume))), (83,298), (0,0,255), cv2.FILLED)
    cv2.putText(img, 'Volume: {} %'.format(volume), (40, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
    
    if len(lmList) != 0:

        # Filter based on size
        area = (bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100
        # Find Distance Between index and Thumb

        # Convert Volume 
        # Reduce Resolution to make it smoother
        # Check Fingers up
        # If pinky is down set volume
        # Drawings


        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx12, cy12 = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx12,cy12), 10, (255,0,255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)
        range30to230 = lambda x : 30 if x <= 30 else 230 if x >= 230 else x
        length100 = (range30to230(length)-30)/2
        script = NSA.alloc().initWithSource_('set volume output volume {}'.format(length100))
        script.executeAndReturnError_(None)
        #volume = int(result.stringValue())
        #cv2.rectangle(img, (50, (100+(2*volume))), (85,300), (0,0,255), cv2.FILLED)
        #cv2.putText(img, 'Volume: {} %'.format(volume), (40, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
    

    # Frame rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, 'FPS: {}'.format(int(fps)), (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)