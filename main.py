import cv2
import time
import numpy as np
import Advanced_HandTrackingModule as A_HTM 
import math
from Foundation import NSAppleScript as NSA

def main():
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
        lmList, bbox = detector.findPosition(img, Bdraw=True)
        detector.displayVolume(img, color='r')

        if len(lmList) != 0:
            fingers = detector.fingersUp()
            print(sum(fingers))
            if sum(fingers) <= 2:
                while True:
                    success, img = cap.read()
                    img = detector.findHands(img, draw=False)
                    lmList, bbox = detector.findPosition(img, Cdraw=True)
                    #cv2.circle(img, lmList[9], 20, (255,255,255))
                    
                    # Display Volume
                    detector.displayVolume(img, color='g')
                    # Hand in screen,
                    if len(lmList) != 0:
                        # Find Distance Between index and Thumb (for control volume with hand gesture)
                        length, img, lineInfo = detector.findDistance(4,8,img)
                        # print(length)

                        # Convert Volume 
                        range30to230 = lambda x : 30 if x <= 30 else 230 if x >= 230 else x
                        length100 = int((range30to230(length)-30)/2)
                        
                        script = NSA.alloc().initWithSource_('set volume output volume {}'.format(length100))
                        script.executeAndReturnError_(None)

                        fingers = detector.fingersUp()
                        print(sum(fingers))
                        if sum(fingers) >= 4:
                            break


                    # Frame rate
                    cTime = time.time()
                    fps = 1/(cTime - pTime)
                    pTime = cTime
                    cv2.putText(img, 'FPS: {}'.format(int(fps)), (40, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (86,50,19), 2)
                    cv2.imshow("Img", img)
                    cv2.waitKey(1)


        # Frame rate
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, 'FPS: {}'.format(int(fps)), (40, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255), 2)
        cv2.imshow("Img", img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()