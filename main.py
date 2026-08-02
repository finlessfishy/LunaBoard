version = "0.1.0"


from pylibs import utilities as util

total = 11
util.clear()
print("Loading...")
print(util.progress_bar(1, total, clear=True))
import os

print("Loading...")
print(util.progress_bar(2, total, clear=True))
import sys

print("Loading...")
print(util.progress_bar(3, total, clear=True))
import numpy as np

print("Loading...")
print(util.progress_bar(4, total, clear=True))
import sounddevice as sd

print("Loading...")
print(util.progress_bar(5, total, clear=True))
from lupa import LuaRuntime

print("Loading...")
print(util.progress_bar(6, total, clear=True))
from pynput import keyboard

print("Loading...")
print(util.progress_bar(7, total, clear=True))
import atexit

print("Loading...")
print(util.progress_bar(8, total, clear=True))
from pylibs import inputlib

print("Loading...")
print(util.progress_bar(9, total, clear=True))
import random

print("Loading...")
print(util.progress_bar(10, total, clear=True))
from pylibs import colors

print("Loading...")
print(util.progress_bar(11, total, clear=True))

util.clear()

# --- TERMINAL ECHO SUPPRESSION & CLEANUP ---
if os.name == 'posix' and sys.stdin.isatty():
    import termios
    import tty

    old_settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setcbreak(sys.stdin.fileno())
    except Exception:
        pass


def cleanup_terminal():
    if os.name == 'posix' and sys.stdin.isatty():
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


atexit.register(cleanup_terminal)
# -------------------------------------------

# Initialize Lua runtime
lua = LuaRuntime(unpack_returned_tuples=True)

with open('lunaboard.lua', 'r') as f:
    lua.execute(f.read())

get_sample_fn = lua.eval('get_sample')

# Track state
active_note_keys = set()
active_octave_keys = set()
VALID_OCTAVES = {'2', '3', '4', '5'}


def on_press(key):
    try:
        if hasattr(key, 'char') and key.char:
            char = key.char.lower()
            if char in VALID_OCTAVES:
                active_octave_keys.add(char)
            else:
                active_note_keys.add(char)
    except AttributeError:
        pass


def on_release(key):
    try:
        if hasattr(key, 'char') and key.char:
            char = key.char.lower()
            if char in VALID_OCTAVES:
                active_octave_keys.discard(char)
            else:
                active_note_keys.discard(char)
    except AttributeError:
        pass


# Start non-blocking keyboard listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Audio stream parameters
sample_rate = 44100
t = 0


def audio_callback(outdata, frames, time_info, status):
    global t
    buffer = np.zeros(frames, dtype=np.float32)

    # Convert active key set to a Lua table for polyphonic mixing
    note_keys_list = list(active_note_keys) if active_note_keys else None
    lua_keys_table = lua.table_from(note_keys_list) if note_keys_list else None

    current_octave = (
        int(list(active_octave_keys)[-1]) if active_octave_keys else 4
    )

    for i in range(frames):
        # Pass Lua table of active keys into Lua
        buffer[i] = get_sample_fn(
            t / sample_rate, lua_keys_table, current_octave
        )
        t += 1

    outdata[:] = buffer.reshape(-1, 1)


# Run audio stream
print(f'LunaBoard {version}')

keylist = [
    '[A]',
    '[S]',
    '[D]',
    '[F]',
    '[G]',
    '[H]',
    '[J]',
    '[K]',
    '[L]',
]

print('Keys for notes: ', end='')
for i in keylist:
    print(
        f"{random.choice(list(colors.colors_nr.values()))}{i}{colors.colors['R']} ",
        end='',
        flush=True,
    )
print('\nHold [1], [2], [3], [4], or [5] to select Octave (Defaults to 4).')
print('Press Ctrl+C to exit.\n')

try:
    with sd.OutputStream(
        channels=1, callback=audio_callback, samplerate=sample_rate
    ):
        while True:
            sd.sleep(1000)
except KeyboardInterrupt:
    print('\nClosing...')