import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



    # Red color
    low_red = np.array([140, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    frame[red_mask>200]=(0,255,0)
    red = cv2.bitwise_and(frame, frame, mask=red_mask)



    # Green color
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    frame[green_mask>200]=(255,0,0)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)

    # Every color except white
    low = np.array([0, 42, 0])
    high = np.array([179, 255, 255])
    mask = cv2.inRange(hsv_frame, low, high)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    result= cv2.bitwise_and(frame, frame, mask=mask)

    # Blue color
    low_blue=np.array([43,80,125])
    high_blue=np.array([102,255,255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    frame[blue_mask>200]=(100,100,255)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    

    cv2.imshow("Frame", frame)
    cv2.imshow("hsv_frame", hsv_frame)
    #cv2.imshow("Red", red)
   # cv2.imshow("Blue", blue)
    #cv2.imshow("Green", green)
    cv2.imshow("Result", result)

    key = cv2.waitKey(1)
    if key == 27:
        break
