version = "0.1.1"

import atexit
import os
import random
import sys
import time
from lupa import LuaRuntime
import numpy as np
from pylibs import colors, inputlib, utilities as util
from pynput import keyboard
import sounddevice as sd

# Progress loader UI
total = 11
util.clear()
print("Loading...")
for i in range(1, total + 1):
    print(util.progress_bar(i, total, clear=True))
    time.sleep(0.02)  # Short delay for visual smoothness

util.clear()

# --- TERMINAL ECHO SUPPRESSION ---
old_settings = None
if os.name == "posix" and sys.stdin.isatty():
    import termios
    import tty

    try:
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
    except Exception:
        pass


def cleanup_terminal():
    if old_settings and os.name == "posix" and sys.stdin.isatty():
        import termios

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


atexit.register(cleanup_terminal)
# ----------------------------------

# Initialize Lua engine
lua = LuaRuntime(unpack_returned_tuples=True)

# Determine path dynamically (Works for both raw Python and PyInstaller executable)
base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
lua_file_path = os.path.join(base_path, "lunaboard.lua")

with open(lua_file_path, "r") as f:
    lua.execute(f.read())

get_sample_fn = lua.eval("get_sample")

# Key tracking
active_note_keys = set()
active_octave_keys = set()
VALID_OCTAVES = {"1", "2", "3", "4", "5"}


def on_press(key):
    try:
        if hasattr(key, "char") and key.char:
            char = key.char.lower()
            if char in VALID_OCTAVES:
                active_octave_keys.add(char)
            else:
                active_note_keys.add(char)
    except AttributeError:
        pass


def on_release(key):
    try:
        if hasattr(key, "char") and key.char:
            char = key.char.lower()
            if char in VALID_OCTAVES:
                active_octave_keys.discard(char)
            else:
                active_note_keys.discard(char)
    except AttributeError:
        pass


# Start keyboard listener thread
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.daemon = True
listener.start()

# Audio callback
sample_rate = 44100
t = 0


def audio_callback(outdata, frames, time_info, status):
    global t
    buffer = np.zeros(frames, dtype=np.float32)

    note_keys_list = list(active_note_keys) if active_note_keys else None
    lua_keys_table = lua.table_from(note_keys_list) if note_keys_list else None
    current_octave = (
        int(list(active_octave_keys)[-1]) if active_octave_keys else 4
    )

    for i in range(frames):
        buffer[i] = get_sample_fn(
            t / sample_rate, lua_keys_table, current_octave
        )
        t += 1

    outdata[:] = buffer.reshape(-1, 1)


# Print UI header
print(f"LunaBoard {version}")

keylist = ["[A]", "[S]", "[D]", "[F]", "[G]", "[H]", "[J]", "[K]", "[L]"]

print("Keys for notes: ", end="")
for k in keylist:
    color_val = random.choice(list(colors.colors_nr.values()))
    print(f"{color_val}{k}{colors.colors['R']} ", end="", flush=True)

print("\nHold [1], [2], [3], [4], or [5] to select Octave (Defaults to 4).")
print("Press Ctrl+C to exit.\n")

# Main execution loop
try:
    with sd.OutputStream(
        channels=1, callback=audio_callback, samplerate=sample_rate
    ):
        while True:
            time.sleep(0.1)  # Keeps main thread alive safely across Linux platforms
except KeyboardInterrupt:
    print("\nClosing...")