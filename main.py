from pylibs import utilities as util

total = 11
print(util.progress_bar(1, total, clear=True))
import os

print(util.progress_bar(2, total, clear=True))
import sys

print(util.progress_bar(3, total, clear=True))
import numpy as np

print(util.progress_bar(4, total, clear=True))
import sounddevice as sd

print(util.progress_bar(5, total, clear=True))
from lupa import LuaRuntime

print(util.progress_bar(6, total, clear=True))
from pynput import keyboard

print(util.progress_bar(7, total, clear=True))
import atexit

print(util.progress_bar(8, total, clear=True))
from pylibs import inputlib

print(util.progress_bar(9, total, clear=True))
import random

print(util.progress_bar(10, total, clear=True))
from pylibs import colors

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

active_keys = set()


def on_press(key):
    try:
        if hasattr(key, 'char') and key.char:
            active_keys.add(key.char.lower())
    except AttributeError:
        pass


def on_release(key):
    try:
        if hasattr(key, 'char') and key.char:
            active_keys.discard(key.char.lower())
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

    # Pick the most recently pressed key
    current_key = list(active_keys)[-1] if active_keys else None

    for i in range(frames):
        # Pass current time step and active key character into Lua
        buffer[i] = get_sample_fn(t / sample_rate, current_key)
        t += 1

    outdata[:] = buffer.reshape(-1, 1)


# Run audio stream
print('LunaBoard')

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
print('Press Ctrl+C to exit.\n')

try:
    with sd.OutputStream(
        channels=1, callback=audio_callback, samplerate=sample_rate
    ):
        while True:
            sd.sleep(1000)
except KeyboardInterrupt:
    print('\nShutting down synth...')s