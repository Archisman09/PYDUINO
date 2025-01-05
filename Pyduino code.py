import serial 
import mediapipe as mp
import numpy as np
import cv2 as cv 
import time
import math

def findHands(results, draw=True):
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: 
            if draw:
                mpDraw.draw_landmarks(frame, handLms, mpHand.HAND_CONNECTIONS) 
    return frame

def findPosition(frame, results, handNo=0, draw=True):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            height, width, _ = frame.shape 
            cx, cy = int(lm.x * width), int(lm.y * height) 
            lmList.append([id, cx, cy])
            if draw:
                cv.circle(frame, (cx, cy), 10, (0, 0, 255), cv.FILLED)  
    return lmList

def countFinger(lmList: list[list], tipIds: dict, ser, led=False) -> int:

    if len(lmList) != 0:
        fingers = []
        
        if lmList[list(tipIds.keys())[0]][1] < lmList[list(tipIds.keys())[0] - 1][1]: 
            fingers.append(1) 
            if led:
                connectArduinoLight(tipIds, list(tipIds.keys())[0], ser, mode=True)
        else:
            fingers.append(0) 
            if led:
                connectArduinoLight(tipIds, list(tipIds.keys())[0], ser)
        
        for key, val in tipIds.items(): 
            if key > 4:
                if lmList[key][2] < lmList[key - 2][2]:
                    fingers.append(1) #if finger open then append 1
                    if led:
                        connectArduinoLight(tipIds, key, ser, mode=True)
                else:
                    fingers.append(0) 
                    if led:
                        connectArduinoLight(tipIds, key, ser)
        return fingers.count(1)

def fingerLength(lmList, frame, servo=False):
    
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2] 
        x2, y2 = lmList[8][1], lmList[8][2] 
        x3, y3 = (x1 + x2) // 2, (y1 + y2) // 2 
        if servo:
            cv.circle(frame, (x1, y1), 7, (0, 0, 255), cv.FILLED) 
            cv.circle(frame, (x2, y2), 7, (0, 0, 255), cv.FILLED) 
            cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
            cv.circle(frame, (x3, y3), 7, (0, 0, 255), cv.FILLED) 
            length = math.hypot(x2 - x1, y2 - y1) 
            servorange = int(np.interp(length, [50, 320], [0, 9])) 
            servoBar = int(np.interp(length, [50, 320], [400, 150])) 
            servoDeg = int(np.interp(length, [50, 320], [0, 180])) 
            cv.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), thickness=2) 
            cv.rectangle(frame, (50, servoBar), (85, 400), (0, 255, 0), cv.FILLED)
            cv.putText(frame, "DEG " + str(servoDeg), (50, 135), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),thickness=2) 
            if length < 50:
                cv.circle(frame, (x3, y3), 7, (0, 255, 0), cv.FILLED) 
            

def connectArduinoLight(tipIds, id, ser, mode=False):
    
    if id == 4: #signal for LED respective to thumb
        if mode:
            ser.write(tipIds[id]) 
        else:
            ser.write(b'f')
    if id == 8: 
        if mode:
            ser.write(tipIds[id]) 
        else:
            ser.write(b'g')
    if id == 12: 
        if mode:
            ser.write(tipIds[id]) 
        else:
            ser.write(b'h')
    if id == 16: 
        if mode:
            ser.write(tipIds[id]) 
        else:
            ser.write(b'i')
    if id == 20: 
        if mode:
            ser.write(tipIds[id]) 
        else:
            ser.write(b'j')

def connectArduinoServo(servo):
    ser.write(f'{servo}'.encode()) 


# widthCam, heightCam = 1000, 500
tipIds = {4: b'a', 8: b'b', 12: b'c', 16: b'd', 20: b'e'} 
pTime = cTime = 0 
video = cv.VideoCapture(0)
# video.set(3, widthCam)
# video.set(4, heightCam)
mpHand = mp.solutions.hands 
hands = mpHand.Hands(max_num_hands=1)  
mpDraw = mp.solutions.drawing_utils 
#ser = serial.Serial("COM3", 9600, timeout=1) #specify the serial post, baudrate, and retry interval
ser=1
if __name__ == '__main__':
    """main function"""

    while True: #infinite loop for video 
        _, frame = video.read() # turn on the camera ('_' allocates less memory)
        frame=cv.flip(frame,1) #flip the frame horizonotally
        frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  #translate the colorspace from BGR to RGB, hands object only uses RGB
        results = hands.process(frameRGB) # Processes an RGB image and returns the hand landmarks of each detected hand
        frame = findHands(results) #draw lines on hand if hand is found
        lmList = findPosition(frame, results, draw=False) #return the position of each landmark
        count = countFinger(lmList, tipIds, ser, led=False) #count the number of fingers
        #fingerLength(lmList, frame, servo=False) #calculate the degree from distance between thumb and index finger
        cTime = time.time() #fetch the current system time
        fps = 1 // (cTime - pTime) #calculate fps
        pTime = cTime

        if count==None: #if no hand if present in screen then it returns None, we change it to 0 as per our preference
            count=0

        cv.putText(frame, "Fps"+str(fps), (0, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), thickness=2) #print the fps
        cv.putText(frame, "FINGER " + str(count), (35, 460), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), thickness=2) #print the count of fingers
        cv.rectangle(frame, (30, 425), (190, 470), (0, 0, 255), thickness=2) #draw the rectangle around finger count
        cv.imshow("LIVE", frame) #display the camera feed on screen
        if cv.waitKey(20) & 0xFF == ord('q'): #check if letter q is pressed for atleast 20 miliseconds then close the camera window 
            break #break out of while loop

    video.release() #release the camera
    cv.destroyAllWindows() #destroy all windows created previously
