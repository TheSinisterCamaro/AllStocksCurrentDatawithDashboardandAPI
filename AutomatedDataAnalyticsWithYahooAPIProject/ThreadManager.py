import threading

class ThreadManager:
    def __init__(self):
        self.stop_flag = threading.Event()

    def get_stop_flag(self):
        return self.stop_flag
