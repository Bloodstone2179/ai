import cv2
import numpy as np

cv2.namedWindow('image')
cv2.resizeWindow('image',600,350)

def nothing(x):
    pass

cv2.createTrackbar('Hue-Upper','image',0,255,nothing)
cv2.createTrackbar('Sat-Upper','image',0,255,nothing)
cv2.createTrackbar('Val-Upper','image',0,255,nothing)

cv2.createTrackbar('Hue-Lower','image',0,255,nothing)
cv2.createTrackbar('Sat-Lower','image',0,255,nothing)
cv2.createTrackbar('Val-Lower','image',0,255,nothing)

cam= cv2.VideoCapture(0)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
text="Colour"

while True:
    r_upper = cv2.getTrackbarPos('Hue-Upper','image')
    g_upper = cv2.getTrackbarPos('Sat-Upper','image')
    b_upper = cv2.getTrackbarPos('Val-Upper','image')
    
    r_lower = cv2.getTrackbarPos('Hue-Lower','image')
    g_lower = cv2.getTrackbarPos('Sat-Lower','image')
    b_lower = cv2.getTrackbarPos('Val-Lower','image')

    lowerBound=np.array([r_lower,g_lower,b_lower])
    upperBound=np.array([r_upper,g_upper,b_upper])
    
    ret,img=cam.read()

    img=cv2.resize(img,(640,520))
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    imgHSV= cv2.cvtColor(imgRGB,cv2.COLOR_RGB2HSV)
    
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    maskFinal=maskClose
    mask = cv2.bitwise_not(mask)
    conts,h=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img,conts,-1,(255,0,0),3)
    for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
        cv2.putText(img, text,(x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), lineType=cv2.LINE_AA) 
    cv2.imshow("mask",mask)
    cv2.imshow("cam",img)
    cv2.waitKey(10)
