-- synth_config.lua

-- Waveform math written in Lua
function sine_wave(freq, time)
    return math.sin(2 * math.pi * freq * time)
end

function square_wave(freq, time)
    return sine_wave(freq, time) >= 0 and 0.5 or -0.5
end

-- Python calls this function continuously to render audio frames
function get_sample(time)
    -- Play a 440 Hz square wave note (A4)
    local note_freq = 440
    return square_wave(note_freq, time)
end
