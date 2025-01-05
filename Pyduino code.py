import serial #install module pyserial (not serial)
import mediapipe as mp
import numpy as np
import cv2 as cv #openCV - open computer vision
import time
import math

def findHands(results, draw=True):
    """find and draw the landmarks on the hand (21 points for 1 hand)"""
    if results.multi_hand_landmarks:#if hand is present in the frame then it returns true
        for handLms in results.multi_hand_landmarks: #cycles through all 21 landmarks
            if draw:
                mpDraw.draw_landmarks(frame, handLms, mpHand.HAND_CONNECTIONS) #draw the connection between landmark
    return frame

def findPosition(frame, results, handNo=0, draw=True):
    """return the x and y coordinates of landmarks on the hand 
    in the format [landmark_id,x_coordinate,y_coordinate]"""
    lmList = []
    if results.multi_hand_landmarks:#if hand is present in the frame then it returns true
        myHand = results.multi_hand_landmarks[handNo]#select hand no zero(from parameter)
        for id, lm in enumerate(myHand.landmark):
            height, width, _ = frame.shape #fetch the height and width of the camera frame
            cx, cy = int(lm.x * width), int(lm.y * height) #find the x and y coordinate with respect to the camera window
            lmList.append([id, cx, cy])
            if draw:
                cv.circle(frame, (cx, cy), 10, (0, 0, 255), cv.FILLED)  # draw big circles on the landmark
    return lmList

def countFinger(lmList: list[list], tipIds: dict, ser, led=False) -> int:
    """
    counts the number of opened fingers
    """
    if len(lmList) != 0:
        fingers = []
        # only for thumb
        if lmList[list(tipIds.keys())[0]][1] < lmList[list(tipIds.keys())[0] - 1][1]: #if tipIds 4 is left of 3 then open
            fingers.append(1) #if finger open then append 1
            if led:
                connectArduinoLight(tipIds, list(tipIds.keys())[0], ser, mode=True)
        else:
            fingers.append(0) #if finger closed then append 0
            if led:
                connectArduinoLight(tipIds, list(tipIds.keys())[0], ser)
        # for other four fingers
        for key, val in tipIds.items(): #if tipIds of rest 4 fingers if above the tipIds of that finger nimus 2 then open
            if key > 4:
                if lmList[key][2] < lmList[key - 2][2]:
                    fingers.append(1) #if finger open then append 1
                    if led:
                        connectArduinoLight(tipIds, key, ser, mode=True)
                else:
                    fingers.append(0) #if finger open then append 0
                    if led:
                        connectArduinoLight(tipIds, key, ser)
        return fingers.count(1)

def fingerLength(lmList, frame, servo=False):
    """calculate the length between index finger and thumb and translate it into degrees"""
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2] #fetch and store the x and y coordinate of thumb
        x2, y2 = lmList[8][1], lmList[8][2] #fetch and store the x and y coordinate of index finger
        x3, y3 = (x1 + x2) // 2, (y1 + y2) // 2 #find the center point between index finger and thumb
        if servo:
            cv.circle(frame, (x1, y1), 7, (0, 0, 255), cv.FILLED) #draw a circle at thumb
            cv.circle(frame, (x2, y2), 7, (0, 0, 255), cv.FILLED) #draw a circle at index finger
            cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
            cv.circle(frame, (x3, y3), 7, (0, 0, 255), cv.FILLED) #draw a circle at the midle point between thumb and index
            length = math.hypot(x2 - x1, y2 - y1) #find the distance betwwn two points
            servorange = int(np.interp(length, [50, 320], [0, 9])) #map the range (50,320) to (0, 9) to send byte data to the arduino
            servoBar = int(np.interp(length, [50, 320], [400, 150])) #convert the calculated distance to rectangular bar
            servoDeg = int(np.interp(length, [50, 320], [0, 180])) ##map the range (50,320) to (0, 180) to show the degree on screen
            cv.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), thickness=2) #draw the outer rectangle of degree bar
            cv.rectangle(frame, (50, servoBar), (85, 400), (0, 255, 0), cv.FILLED) #draw the inner rectangle that varies based on degree
            cv.putText(frame, "DEG " + str(servoDeg), (50, 135), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),thickness=2) #print the calculated degree on screen
            if length < 50:
                cv.circle(frame, (x3, y3), 7, (0, 255, 0), cv.FILLED) #if the distance between thumb and index is less than 50 change the color of circle to green
            # connectArduinoServo(servorange) #send the signal to Arduino

def connectArduinoLight(tipIds, id, ser, mode=False):
    """send the signal to arduino for turning LED on or off"""
    if id == 4: #signal for LED respective to thumb
        if mode:
            ser.write(tipIds[id]) #send the value for thumb which is fetched from the tipIds dictionary
        else:
            ser.write(b'f')
    if id == 8: #signal for LED respective to index finger
        if mode:
            ser.write(tipIds[id]) #send the value for index finger which is fetched from the tipIds dictionary
        else:
            ser.write(b'g')
    if id == 12: #signal for LED respective to middle finger
        if mode:
            ser.write(tipIds[id]) #send the value for middle finger which is fetched from the tipIds dictionary
        else:
            ser.write(b'h')
    if id == 16: #signal for LED respective to ring finger
        if mode:
            ser.write(tipIds[id]) #send the value for ring finger which is fetched from the tipIds dictionary
        else:
            ser.write(b'i')
    if id == 20: #signal for LED respective to pinky finger
        if mode:
            ser.write(tipIds[id]) #send the value for pinky finger which is fetched from the tipIds dictionary
        else:
            ser.write(b'j')

def connectArduinoServo(servo):
    ser.write(f'{servo}'.encode()) #encode the recieved number into byte string and send to arduino


# widthCam, heightCam = 1000, 500
tipIds = {4: b'a', 8: b'b', 12: b'c', 16: b'd', 20: b'e'} # key(tipId) value(turn on signal) pair for each finger tip ids
pTime = cTime = 0 #to calculate fps
video = cv.VideoCapture(0) #capture the camera and store it in a variable
# video.set(3, widthCam)
# video.set(4, heightCam)
mpHand = mp.solutions.hands #create a hand object from mediapipe
hands = mpHand.Hands(max_num_hands=1)  # specify no of hands
mpDraw = mp.solutions.drawing_utils #specify that we want to draw the the connections on hand
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