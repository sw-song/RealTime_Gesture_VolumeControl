import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                # print(img.shape)
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                if id == 0:
                    cv2.circle(img, (cx,cy), 25, (255,0,255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)   

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

#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
        

#     else:
#         break

# cap.release()
# cv2.destroyAllWindows()