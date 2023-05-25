import cv2 as cv
from PIL import ImageGrab
import numpy as np
frame = 0
while True:
    img = np.asarray(ImageGrab.grab(bbox=(672,261,1267,912)))
    cv.imshow("Testing", img)
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    elif key == ord('f'):
        print(2)
        cv.imwrite('positive/{}.jpg'.format(frame), img)#
        frame += 1
    elif key == ord('d'):
        print(1)
        cv.imwrite('negative/{}.jpg'.format(frame), img)
        frame += 1
print("Finshed")