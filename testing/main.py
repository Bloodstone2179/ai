import datacollector
from thread_custom import Thread
from time import sleep
datacollector.setup()
#datacollector.record()

recordThread = Thread(datacollector.record)
recordThread.args = (recordThread.event,)

recordThread.start_()

sleep(0.1)
recordThread.stop()