#imports
import cv2 as cv
import PIL.ImageGrab as ImageGrab
import numpy as np
import csv, queue, time
from thread_custom import Thread
#variables
global bbox, currentImg, ghosts
bbox=(672,261,1267,912)
currentImg = None
detectBuffer = queue.Queue()
show_buffer = queue.Queue()

baseDisplayImg =  np.ascontiguousarray(ImageGrab.grab(bbox))
baseDisplayImg = cv.cvtColor(baseDisplayImg, cv.COLOR_BGR2RGB)

#bounds
red_bound_lower = np.asarray([255,0,0])
red_bound_upper = np.asarray([255,2,2])

pink_bound_lower = np.asarray([255,184,255])
pink_bound_upper = np.asarray([255,187,255])

orange_bound_lower = np.array([255,184,81])
orange_bound_upper = np.array([255,187,84])

blue_bound_lower = np.asarray([0,255,255])
blue_bound_upper = np.asarray([1,255,255])
#record screen
def record(event):
    while True and not event.is_set():
        img = np.ascontiguousarray(ImageGrab.grab(bbox))
        haystack = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        detectBuffer.put(haystack)
        

#do calculations to find the ghosts and player
def detectGhost(event, threshold = 0.5):
    

    

    while True and not event.is_set():
        haystack = detectBuffer.get()
        
        red_mask = cv.inRange(haystack, red_bound_lower, red_bound_upper)
        haystack[red_mask>200]=(0,255,0)
        red = cv.bitwise_and(haystack, haystack, mask=red_mask)

        pink_mask = cv.inRange(haystack, pink_bound_lower, pink_bound_upper)
        haystack[pink_mask>200]=(255,0,0)
        pink = cv.bitwise_and(haystack, haystack, mask=pink_mask)

        orange_mask = cv.inRange(haystack, orange_bound_lower, orange_bound_upper)
        haystack[orange_mask>200]=(255,0,0)
        org = cv.bitwise_and(haystack, haystack, mask=orange_mask)

        
        low = np.array([0, 42, 0])
        high = np.array([254, 255, 255])
        mask = cv.inRange(haystack, low, high)
        result = cv.bitwise_and(haystack, haystack, mask=mask)
        result= cv.bitwise_and(haystack, haystack, mask=mask)

        #
        
        blue_mask = cv.inRange(haystack, blue_bound_lower, blue_bound_upper)
        haystack[blue_mask>200]=(100,100,255)
        blue = cv.bitwise_and(haystack, haystack, mask=blue_mask)

        show_buffer.put(result)

#display each image and ask user what way to go
##
def Show(event):
    while True and not event.is_set():
        img = show_buffer.get()
        if img is None:
            img = baseDisplayImg
            print("No Image Avaliable for display using base image")
            
        cv.imshow("hello", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            print("Hello There I am about to stop all threads try me bitch")
            cv.destroyAllWindows()
            detectionThread.stop()
            print("THREAD 1")
            ShowThread.stop()
            print("THREAD 2")
            recordThread.stop()
            print("THREAD 3")
            print(f"stopping: all threads")
#]
#print that to a file


if __name__ == "__main__":

    detectionThread = Thread(detectGhost)
    detectionThread.args = (detectionThread.event,0.6)
    

    ShowThread = Thread(Show)
    ShowThread.args = (ShowThread.event,)
    

    recordThread = Thread(record)
    recordThread.args = (recordThread.event,)

    recordThread.start_()
    detectionThread.start_()
    ShowThread.start_()

    try:
        while True:
            pass
                
    except KeyboardInterrupt:
        print("Hello There I am about to stop all threads try me bitch")
        cv.destroyAllWindows()
        detectionThread.stop()
        print("THREAD 1")
        ShowThread.stop()
        print("THREAD 2")
        recordThread.stop()
        print("THREAD 3")
        print(f"stopping: all threads")
        
        
    