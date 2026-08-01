import sounddevice as sd
import numpy as np
from lupa import LuaRuntime

# 1. Initialize Lua engine
lua = LuaRuntime(unpack_returned_tuples=True)

# 2. Load user's Lua synth script
with open("lunaboard.lua", "r") as f:
    lua.execute(f.read())

get_sample_fn = lua.eval("get_sample") # Grab Lua function reference

# 3. Define real-time audio callback
sample_rate = 44100
t = 0

def audio_callback(outdata, frames, time, status):
    global t
    buffer = np.zeros(frames, dtype=np.float32)
    
    for i in range(frames):
        # Python queries Lua for the sample value at time 't'
        buffer[i] = get_sample_fn(t / sample_rate)
        t += 1
        
    outdata[:] = buffer.reshape(-1, 1)

# Start audio stream
with sd.OutputStream(channels=1, callback=audio_callback, samplerate=sample_rate):
    print("Soundboard running! Edit synth_config.lua to change audio logic.")
    input("Press Enter to stop...\n")