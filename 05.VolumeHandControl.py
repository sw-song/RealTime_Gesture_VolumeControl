import cv2
import time
import numpy as np
import HandTrackingModule as HTM 
import math
import subprocess

# call(["osascript -e 'set volume output volume 100'"], shell=True)
# same code below
# import osascript 
# import applescript
#import os
#os.system('say "your program has finished"')
##### parameter
pTime = 0

#### Video Controler
cap = cv2.VideoCapture(0)

#### Object Detection Module
detector = HTM.handDetector()


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    cv2.rectangle(img, (50,100), (85,300), (0,255,0), 3)
    if len(lmList) > 21:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx12, cy12 = (x1 + x2) // 2, (y1 + y2) // 2

        x3, y3 = lmList[25][1], lmList[25][2]
        x4, y4 = lmList[29][1], lmList[29][2]
        cx34, cy34 = (x3 + x4) // 2, (y3 + y4) // 2

        cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx12,cy12), 10, (255,0,255), cv2.FILLED)

        cv2.circle(img, (x3,y3), 15, (255,255,255), cv2.FILLED)
        cv2.circle(img, (x4,y4), 15, (255,255,255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        #if length <= 30:
        #    length = 30
        #elif length >= 230:
        #    length = 230
        range100 = lambda x : 30 if x <= 30 else 230 if x >= 230 else x
        length = range100(length)
        print('length : ',length)
        #osascript.run('set volume output volume {}'.format(int(length-30)/2)),
        subprocess.call("osascript -e 'set volume output volume {}'".format((length-30)/2), shell=True)
        out= subprocess.check_output(["osascript -e 'output volume of (get volume settings)'"], shell=True)
        #code, out, err = osascript.run("output volume of (get volume settings)")
        print('out : ', out)
        print(100+length)
        cv2.rectangle(img, (50, (300-int(length-30))), (85,300), (255,0,0), cv2.FILLED)

    elif len(lmList) != 0:
        print(lmList[4], lmList[8])
        print('---')
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx12, cy12 = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx12,cy12), 10, (255,0,255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        #if length <= 30:
        #    length = 30
        #elif length >= 230:
        #    length = 230
        range100 = lambda x : 30 if x <= 30 else 230 if x >= 230 else x
        length = range100(length)
        print('length : ',length)
        # osascript.run('set volume output volume {}'.format(int(length-30)/2)),
        subprocess.call("osascript -e 'set volume output volume {}'".format((length-30)/2), shell=True)
        out= subprocess.check_output(["osascript -e 'output volume of (get volume settings)'"], shell=True)
        # code, out, err = osascript.run("output volume of (get volume settings)")
        print('out : ', out)
        print(100+length)
        cv2.rectangle(img, (50, (300-int(length-30))), (85,300), (255,0,0), cv2.FILLED)
        cv2.putText(img, 'Volume: {} %'.format(int(length-30)/2), (40, 400),
                cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    else:
        print('Hands up!')
        
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, 'FPS: {}'.format(int(fps)), (40, 50),
                cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)