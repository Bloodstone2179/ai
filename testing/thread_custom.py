import threading
import queue
class Thread:
    funcName = None
    args = ()
    threadCreated = None
    event = None
    def __init__(self, funcName = None, args = None):
        self.funcName = funcName
        self.args = args
        self.event = threading.Event()
    def start_(self):
        self.threadCreated = threading.Thread(target=self.funcName, args=self.args)
        self.threadCreated.start()
    def ReturnTest(self):
        print(f"func Name {self.funcName}, args = {self.args}, thread = {self.threadCreated}")
    def stop(self):
        self.event.set()
        self.join()
    def join(self):
        self.threadCreated.join()