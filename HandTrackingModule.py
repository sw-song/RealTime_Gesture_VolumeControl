import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.8, trackCon=0.7):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
    
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)   
                
        return img
    
    def findPosition(self, img, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            for myHand in self.results.multi_hand_landmarks:
                for id, lm in enumerate(myHand.landmark):
                            h, w, c = img.shape
                            cx, cy = int(lm.x*w), int(lm.y*h)
                            # print(id, cx, cy)
                            lmList.append([id, cx, cy])
                            if draw:
                                if id == 0:
                                    cv2.circle(img, (cx,cy), 25, (255,0,255), cv2.FILLED)
        return lmList

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
                    (255,0,255), 
                    3)
        if success == True:
            cv2.imshow('Image', img)
            cv2.waitKey(1)


if __name__ == '__main__':
    main()