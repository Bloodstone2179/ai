import  numpy, mss, pyscreeze, time, os,queue
import pandas as pd
import cv2 as cv
from PIL import ImageGrab
import numpy as np
from datetime import date


global i_,even, sct, frameCount_red,frameCount_blue,frameCount_pink,frameCount_orange, mon, img, grayScaleGhosts, method, img_after, imagesProcessed, today
today = str(date.today())
i_ = 0
imagesProcessed = 0
frameCount_red = 0
frameCount_blue = 0
frameCount_pink = 0
frameCount_orange = 0
mon = {"top":0,"left":0, "width":600,"height":600}
img = None
sct = mss.mss()
method = cv.TM_CCOEFF_NORMED

grayscaleGhosts = [cv.imread("color-0.png", cv.IMREAD_GRAYSCALE),
                   cv.imread("color-1.png", cv.IMREAD_GRAYSCALE),
                   cv.imread("color-2.png", cv.IMREAD_GRAYSCALE),
                   cv.imread("color-3.png", cv.IMREAD_GRAYSCALE)]

colourscaleGhosts = [cv.imread("color-0.png", cv.IMREAD_UNCHANGED),
                   cv.imread("color-1.png", cv.IMREAD_UNCHANGED),
                   cv.imread("color-2.png", cv.IMREAD_UNCHANGED),
                   cv.imread("color-3.png", cv.IMREAD_UNCHANGED)]
'''
i = 0
for each in grayscaleGhosts:
    cv.imwrite(f"Grayscale-{str(i)}.png", each)
    i += 1
ii = 0
for each in colourscaleGhosts:
    cv.imwrite(f"color-{str(ii)}.png", each)
    ii += 1
    '''
detect_out_img = queue.Queue()
detection_buffer_red = queue.Queue()
detection_buffer_blue = queue.Queue()
detection_buffer_pink = queue.Queue()
detection_buffer_orange = queue.Queue()

red = queue.Queue()
blue = queue.Queue()
pink = queue.Queue()
org = queue.Queue()

show_buffer = queue.Queue()
every_ghost_pos = []
frame_number = queue.Queue()
dataWriterQueue = queue.Queue()
playerPos = (0,0)
show_buffer.put( numpy.array(ImageGrab.grab(bbox=(672,261,1267,912))))

with open("testing.csv", "w") as w:
    w.write("numpy array, pink pos, red pos, orange pos, blue pos, playerPositions, way to go \n")

def record(event):
    global frameCount_red, frameCount_blue, frameCount_pink, frameCount_orange
    while True:
        if event.is_set():
            break
        else:

            # Get raw pixels from the screen, save it to a Numpy array
            img = numpy.array(ImageGrab.grab(bbox=(672,261,1267,912)))
            frameCount_red += 1
            frameCount_blue += 1
            frameCount_pink += 1
            frameCount_orange += 1
            haystack_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            #haystack_img = img
            detection_buffer_red.put(haystack_img, False)
            detection_buffer_blue.put(haystack_img, False)
            detection_buffer_pink.put(haystack_img, False)
            detection_buffer_orange.put(haystack_img, False)
            show_buffer.put(img, False)

def show(event):
    while True:
        if event.is_set():
            break
        else:
            
            frame = show_buffer.get()
            cv.imshow("Video", cv.cvtColor(frame,cv.COLOR_BGR2RGB))
            
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            
 
def getRedGhostPosition(event, threshold:float = 0.7):
    global frameCount_red, frameCount_blue, frameCount_pink, frameCount_orange, imagesProcessed
    while True:
        ghostPosition_buffer_ = []
        if event.is_set():
            break
        else:
            haystack_img = detection_buffer_red.get()
            
            
            result = cv.matchTemplate(haystack_img, grayscaleGhosts[2],method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if max_val >= threshold:
                needle_w = grayscaleGhosts[2].shape[1]
                needle_h = grayscaleGhosts[2].shape[0]
                # Calculate the bottom right corner of the rectangle to draw
                top_left = max_loc
                bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
                print(f'RED GHOST \n .  - found frame number {str(frameCount_red)}, \n  - POS: X: {max_loc[0]}, Y: {max_loc[1]}, to: X: {bottom_right[0]}, Y: {bottom_right[1]} \n')
                imagesProcessed += 1
                red.put((max_loc, bottom_right))

            
                #print(f'RED Ghost Not Found. frame number {str(frame_number.get())}')
        detect_out_img.put(haystack_img,False)

def getBlueGhostPosition(event, threshold:float = 0.7):
    global frameCount_red, frameCount_blue, frameCount_pink, frameCount_orange, imagesProcessed
    while True:
        ghostPosition_buffer_ = []
        if event.is_set():
            break
        else:
            haystack_img = detection_buffer_blue.get()
            
            
            result = cv.matchTemplate(haystack_img, grayscaleGhosts[3],method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if max_val >= threshold:
                needle_w = grayscaleGhosts[3].shape[1]
                needle_h = grayscaleGhosts[3].shape[0]
                # Calculate the bottom right corner of the rectangle to draw
                top_left = max_loc
                bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
                print(f'BLUE GHOST \n .  - found frame number {str(frameCount_blue)}, \n  - POS: X: {max_loc[0]}, Y: {max_loc[1]}, to: X: {bottom_right[0]}, Y: {bottom_right[1]} \n')
                imagesProcessed += 1
                # Get the size of the needle image. With OpenCV images, you can get the dimensions 
                # via the shape property. It returns a tuple of the number of rows, columns, and 
                # channels (if the image is color):
                
                blue.put((max_loc, bottom_right))

            
                #print(f'BLUE Ghost Not Found. frame number {str(frame_number.get())}')
            

def getpinkGhostPosition(event, threshold:float = 0.7):
    global frameCount_red, frameCount_blue, frameCount_pink, frameCount_orange, imagesProcessed
    while True:
        ghostPosition_buffer_ = []
        if event.is_set():
            break
        else:
            haystack_img = detection_buffer_pink.get()
            
            
            result = cv.matchTemplate(haystack_img, grayscaleGhosts[1],method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if max_val >= threshold:
                needle_w = grayscaleGhosts[1].shape[1]
                needle_h = grayscaleGhosts[1].shape[0]
                # Calculate the bottom right corner of the rectangle to draw
                top_left = max_loc
                bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
                print(f'PINK GHOST \n .  - found frame number {str(frameCount_pink)}, \n  - POS: X: {max_loc[0]}, Y: {max_loc[1]}, to: X: {bottom_right[0]}, Y: {bottom_right[1]} \n')
                imagesProcessed += 1
                pink.put((max_loc, bottom_right))

            
                #print(f'PINK Ghost Not Found. frame number {str(frame_number.get())}')
            

def getOrangeGhostPosition(event, threshold:float = 0.7):
    global frameCount_red, frameCount_blue, frameCount_pink, frameCount_orange, imagesProcessed
    while True:
        ghostPosition_buffer_ = {"NAME: " : None, "max_loc" : None, "Bottom_right": None}
        if event.is_set():
            break
        else:
            haystack_img = detection_buffer_orange.get()
            
            
            result = cv.matchTemplate(haystack_img, grayscaleGhosts[0],method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if max_val >= threshold:
                needle_w = grayscaleGhosts[0].shape[1]
                needle_h = grayscaleGhosts[0].shape[0]
                # Calculate the bottom right corner of the rectangle to draw
                top_left = max_loc
                bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
                print(f'ORANGE GHOST \n .  - found frame number {str(frameCount_orange)}, \n  - POS: X: {max_loc[0]}, Y: {max_loc[1]}, to: X: {bottom_right[0]}, Y: {bottom_right[1]} \n')
                imagesProcessed +=1
                org.put((max_loc, bottom_right))
            
                #print(f'ORANGE Ghost Not Found. frame number {str(frame_number.get())}')
            
        
            
def dataWriter(event):
    global imagesProcessed, today
    while True:
        if event.is_set():
            break
        else:
            img = show_buffer.get()
        
            p = pink.get()
            r = red.get()
            o = org.get()
            b = blue.get()
            with open("testing.csv", "a") as f:
                imgPath = "images/" + str(today) + "-_-" + str(imagesProcessed) + ".jpeg"
                print(f"{imgPath},{p},{r},{o},{b}, None, None \n")
                f.write(f"{imgPath},{p},{r},{o},{b}, None, None \n")
                
                
                cv.rectangle(img, p[0],p[1], (255,20,147), 2, cv.LINE_4) #pink
                cv.rectangle(img, r[0],r[1], (255,0,0), 2, cv.LINE_4) # red
                cv.rectangle(img, o[0],o[1], (255,140,0), 2, cv.LINE_4) # orange
                cv.rectangle(img, b[0],b[1], (0,0,255), 2, cv.LINE_4) # blue
                cv.imwrite(imgPath, img)
                    
           


'''
result = cv.matchTemplate(haystack_img, needle_img, cv.TM_SQDIFF_NORMED)
threshold = 0.17
locations = np.where(result <= threshold)
# We can zip those up into a list of (x, y) position tuples
locations = list(zip(*locations[::-1]))
print(locations)
if locations:
    print('Found needle.')

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]
    line_color = (0, 255, 0)
    line_type = cv.LINE_4

    # Loop over all the locations and draw their rectangle
    for loc in locations:
        # Determine the box positions
        top_left = loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        # Draw the box
        cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
'''
def getPlayerLocation(playerNeedle):
    #(numpyarray, ghostpostitions, playerPosition, way i went)
    #dataWriterQueue.put()
    pass
