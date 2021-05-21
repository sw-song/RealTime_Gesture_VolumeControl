# How it works? (only Mac)

1. run `main.py` in terminal
```
python main.py
```
2. When you place your palm on the cam, the red box recognizes your hand.

3. And Now, When you clench your fist at this time, a sky blue ring is formed on the index finger and thumb. 

4. You can adjust the volume by spreading your index finger and thumb while holding your fist with the other three fingers.

<img width="60%" src='https://github.com/sw-song/AI_Lab/blob/main/07.hand_pose_blue.gif'> 

---
---

# Step By Step Tutorial

## 1. Basic Hand Pose Estimation
<img width="40%" src='https://github.com/sw-song/AI_Lab/blob/main/01.hand_pose.gif'>

```
Step 1. Import Libraries
Step 2. Load Modules
Step 3. Image Detection Function
Step 4. Control Web Cam
```

## 2. Advanced Hand Pose Estimation
Added features
- Detect Left and Right Hand
```
Step 1. Import Libraries
Step 2. Load Modules
Step 3. Function Definition
     3-a. Get Each Hand Label
     3-b. Image Detection
Step 4. Control Web Cam
```

## 3. Hand Tracking Basic
<img width="40%" src='https://github.com/sw-song/AI_Lab/blob/main/03.hand_pose.gif'>

- Resolved No Response issues
- Display fps(frame per seconds)
- Display Circle on Image(Frame) based on image size

## 4. Hand Tracking using Module
- Same Result(Video Display) with `3. Hand Tracking Basic`
- But Used Module that implemented as classes

## 5. Volume Control with Hand Tracking (FPS < 3)
<img width="40%" src='https://github.com/sw-song/AI_Lab/blob/main/05.hand_pose.gif'>

- Volume Control using `osascript`(on Mac)


## 5. Volume Control with Hand Tracking (FPS > 10)
<img width="40%" src='https://github.com/sw-song/AI_Lab/blob/main/05.hand_pose_fps15.gif'>
<img width="40%" src='https://github.com/sw-song/AI_Lab/blob/main/05.Compare_Loop_Speed.gif'>

- Volume Control using `NSAppleScript `(on Mac)

## 6. Volume Control with Hand Tracking

- New Design (Color, Shape, Circle Size)

## 7. Volume Control with Hand Tracking - version 2
<img width="60%" src='https://github.com/sw-song/AI_Lab/blob/main/07.hand_pose.gif'> 

- Apply screen(Display Design) change when clenching and opening a fist

## 7. Volume Control with Hand Tracking - version 2, blue color
<img width="60%" src='https://github.com/sw-song/AI_Lab/blob/main/07.hand_pose_blue.gif'> 

- apply blue color
