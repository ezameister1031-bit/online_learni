from pynput import keyboard
import time

class ActivityMonitor:
    def __init__(self):
        self.last_time = time.time()
        self.idle_limit = 10  # 秒（本番は300など）

    def on_press(self, key):
        self.last_time = time.time()

    def start(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.daemon = True
        listener.start()

    def is_idle(self):
        return time.time() - self.last_time > self.idle_limit
