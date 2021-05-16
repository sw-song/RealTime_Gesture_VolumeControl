import cv2
import mediapipe as mp
import time
import math 
from Foundation import NSAppleScript as NSA

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.8, trackCon=0.7):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
    
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.NSA = NSA
        

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)   
                
        return img


    def displayVolume(self, img, color='r'):
        self.script = self.NSA.alloc().initWithSource_('output volume of (get volume settings)')
        result, error_info = self.script.executeAndReturnError_(None)
        volume = int(result.stringValue())
        if color == 'r':
            cv2.rectangle(img, (50,100), (75,300), (0,0,255), 3)
            cv2.rectangle(img, (52, (302-(2*volume))), (73,298), (200,200,255), cv2.FILLED)
            cv2.putText(img, 'Volume: {} %'.format(volume), (40, 330), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255), 2)
        elif color == 'g':
            cv2.rectangle(img, (50,100), (75,300), (0,255,0), 3)
            cv2.rectangle(img, (52, (302-(2*volume))), (73,298), (200,255,200), cv2.FILLED)
            cv2.putText(img, 'Volume: {} %'.format(volume), (40, 330), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
        else:
            print('display Volume - color None')
            
    def findPosition(self, img, Bdraw=False, Cdraw=False):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            for myHand in self.results.multi_hand_landmarks:
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    
                    xList.append(cx)
                    yList.append(cy)
                    # print(id, cx, cy)
                    self.lmList.append([id, cx, cy])
                    if len(self.lmList) == 10:
                        if Cdraw:
                            cv2.circle(img, (cx,cy), 100, (165,255,165))
                            #cv2.circle(img, (cx,cy), 205, (0,255,0))
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if Bdraw:
                cv2.rectangle(img, (bbox[0]-20, bbox[1]-20), (bbox[2]+20, bbox[3]+20), (0,0,255), 2)
            if Cdraw and len(self.lmList)>=9:
                cv2.circle(img, (self.lmList[9][1], self.lmList[9][2]), (xmax-xmin), (0,255,0))
                cv2.putText(img, '{}'.format(xmax-xmin), (self.lmList[9][1], self.lmList[9][2]+10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
        return self.lmList, bbox

    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, img, draw=True):
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        length = math.hypot(x2-x1, y2-y1)
        if draw:
            if length <= 30:
                cv2.circle(img, (cx,cy), 25, (200,255,200), 3)
                cv2.putText(img, 'Mute', (cx,cy-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
            elif length >= 230:
                cv2.circle(img, (cx,cy), 25, (200,255,200), 3)
                cv2.putText(img, 'MAX Volume', (cx,cy-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
            else:
                cv2.circle(img, (x1,y1), 15, (0,255,0), 2)
                cv2.circle(img, (x2,y2), 15, (0,255,0), 2)
                cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 1)
                cv2.putText(img, '{:.2f}'.format(length), (cx,cy), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0),2)
                #cv2.circle(img, (cx,cy), 10, (0,255,0), 2)
        return length, img, [x1, y1, x2, y2, cx, cy]

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = handDetector()
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
                    (0,0,255), 
                    3)
        if success == True:
            cv2.imshow('Image', img)
            cv2.waitKey(1)


if __name__ == '__main__':
    main()