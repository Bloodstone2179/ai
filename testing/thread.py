import  datacollector
import cv2 as cv
from thread_custom import Thread
ThreadsStarted = []

record_thread = Thread(datacollector.record)
record_thread.args = (record_thread.event,)


#display_thread = Thread(datacollector.show)
#display_thread.args = (display_thread.event,)


writer_thread = Thread(datacollector.dataWriter)
writer_thread.args = (writer_thread.event,)

Red_detection_thread = Thread(datacollector.getRedGhostPosition)
Red_detection_thread.args = (Red_detection_thread.event,0.75)
Blue_detection_thread = Thread(datacollector.getBlueGhostPosition)
Blue_detection_thread.args = (Blue_detection_thread.event,0.75)
Pink_detection_thread = Thread(datacollector.getpinkGhostPosition)
Pink_detection_thread.args = (Pink_detection_thread.event,0.75)
Orange_detection_thread = Thread(datacollector.getOrangeGhostPosition)
Orange_detection_thread.args = (Orange_detection_thread.event,0.75)



record_thread.start_()
#display_thread.start_()
Red_detection_thread.start_()
Blue_detection_thread.start_()
Pink_detection_thread.start_()
Orange_detection_thread.start_()
writer_thread.start_()
ThreadsStarted.append(record_thread)
#ThreadsStarted.append(display_thread)
ThreadsStarted.append(Red_detection_thread)
ThreadsStarted.append(Blue_detection_thread)
ThreadsStarted.append(Pink_detection_thread)
ThreadsStarted.append(Orange_detection_thread)
ThreadsStarted.append(writer_thread)

try:
    while True:
        pass
            
except KeyboardInterrupt:
    print(f"IMAGES PROCSSED: {str(datacollector.imagesProcessed)}")
    for threads in ThreadsStarted:
        threads.stop()
    print("stoping")
    
    cv.destroyAllWindows()
    
'''
time.sleep(2)
record_thread.stop()
'''