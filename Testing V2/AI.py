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
red = cv.cvtColor(cv.imread("color-2.png", cv.IMREAD_UNCHANGED), cv.COLOR_BGR2HSV)
blue = cv.cvtColor(cv.imread("color-3.png", cv.IMREAD_UNCHANGED), cv.COLOR_BGR2HSV)
pink = cv.cvtColor(cv.imread("color-1.png", cv.IMREAD_UNCHANGED), cv.COLOR_BGR2HSV)
orange = cv.cvtColor(cv.imread("color-0.png", cv.IMREAD_UNCHANGED), cv.COLOR_BGR2HSV)

baseDisplayImg =  np.ascontiguousarray(ImageGrab.grab(bbox))
baseDisplayImg = cv.cvtColor(baseDisplayImg, cv.COLOR_BGR2HSV)

ghosts = [red, blue, pink, orange]
#record screen
def record(event):
    while True and not event.is_set():
        img = np.ascontiguousarray(ImageGrab.grab(bbox))
        haystack = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        detectBuffer.put(haystack)
        '''
        cv.imshow("HSV", haystack)
        if cv.waitKey(1) & 0xFF == ord('q'):
            detectionThread.event.set()
            ShowThread.event.set()
            recordThread.event.set()
            cv.destroyAllWindows()
            break
            '''

#do calculations to find the ghosts and player
def detectGhost(event, threshold = 0.5):
    while True and not event.is_set():
        haystack = detectBuffer.get()
        for ghost in ghosts:
            result = cv.matchTemplate(haystack, ghost, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if max_val >= threshold:
                needle_w = ghost.shape[1]
                needle_h = ghost.shape[0]
                print(f"ghost found  Max Threshold:{str(round(max_val, 4))}  Max loc {str(max_loc)}" )
                cv.rectangle(img=haystack, pt1=max_loc, pt2=(needle_w + max_loc[0], needle_h + max_loc[1]), color=(255,45,255), lineType=cv.LINE_4,thickness=3)
        show_buffer.put(haystack)

#display each image and ask user what way to go
def Show(event):
    while True and not event.is_set():
        img = show_buffer.get()
        if img is None:
            img = baseDisplayImg
            print("No Image Avaliable for display using base image")
        cv.imshow("hello", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            print("Wagwan general")
            detectionThread.event.set()
            ShowThread.event.set()
            recordThread.event.set()
            cv.destroyAllWindows()

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
        
        
    