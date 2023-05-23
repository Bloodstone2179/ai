.event,0.75)
Orange_detection_thread = Thread(datacollector.getOrangeGhostPosition)
Orange_detection_thread.args = (Orange_detection_thread.event,0.75)



record_thread.start_()
display_thread.start_()
Red_detection_thread.start_()