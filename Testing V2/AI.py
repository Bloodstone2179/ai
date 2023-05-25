#imports
import cv2 as cv
import PIL.ImageGrab as ImageGrab
import numpy as np
import csv, queue
from thread_custom import Thread
#variables
global bbox, currentImg, ghostImg
bbox=(672,261,1267,912)
currentImg = None
detectBuffer = queue.Queue()
ghostImg = cv.imread("color-0.png", cv.IMREAD_GRAYSCALE)



#record screen
def record():
    while True:
        img = np.ascontiguousarray(ImageGrab.grab(bbox))
        haystack = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        detectBuffer.put(haystack)
        cv.imshow("hello", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            detectionThread.event.set()
            cv.destroyAllWindows()
            break



#do calculations to find the ghosts and player
def detectGhost(event, threshold = 0.5):
    while True and not event.is_set():
        haystack = detectBuffer.get()
        result = cv.matchTemplate(haystack, ghostImg, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val >= threshold:
            print(f"ghost found  Max Threshold:{str(round(max_val, 4))}  Max loc {str(max_loc)}" )

#display each image and ask user what way to go


#print that to a file


if __name__ == "__main__":
    for i in range(4):
        img = cv.imread(f"color-{i}.png", cv.IMREAD_GRAYSCALE)
        cv.imwrite(f"grayscale-{i}.png", img)
    detectionThread = Thread(detectGhost)
    detectionThread.args = (detectionThread.event,0.6)
    detectionThread.start_()
    record()
    