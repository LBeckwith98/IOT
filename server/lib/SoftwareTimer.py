import time

# This class acts as a software timer
class OneShotTimer:

    def __init__(self, duration):
        self.duration = duration
        self.begin_time = None

    def start(self):
        self.begin_time = time.time()

    def expired(self):
        return (time.time() - self.begin_time) > self.duration
