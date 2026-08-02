-- synth_config.lua

-- Map note names to standard musical frequencies (Hz)
local frequencies = {
  -- Octave 2
  C2 = 65.41,   CS2 = 69.30,  D2 = 73.42,   DS2 = 77.78,
  E2 = 82.41,   F2 = 87.31,   FS2 = 92.50,  G2 = 98.00,
  GS2 = 103.83, A2 = 110.00,  AS2 = 116.54, B2 = 123.47,

  -- Octave 3
  C3 = 130.81,  CS3 = 138.59, D3 = 146.83,  DS3 = 155.56,
  E3 = 164.81,  F3 = 174.61,  FS3 = 185.00, G3 = 196.00,
  GS3 = 207.65, A3 = 220.00,  AS3 = 233.08, B3 = 246.94,

  -- Octave 4 (Standard Middle Octave)
  C4 = 261.63,  CS4 = 277.18, D4 = 440.00 * (2^(-7/12)), -- 293.66
  DS4 = 311.13, E4 = 329.63,  F4 = 349.23,  FS4 = 369.99,
  G4 = 392.00,  GS4 = 415.30, A4 = 440.00,  AS4 = 466.16,
  B4 = 493.88,

  -- Octave 5
  C5 = 523.25,  CS5 = 554.37, D5 = 587.33,  DS5 = 622.25,
  E5 = 659.25,  F5 = 698.46,  FS5 = 739.99, G5 = 783.99,
  GS5 = 830.61, A5 = 880.00,  AS5 = 932.33, B5 = 987.77
}


-- Waveform synthesis
function sine_wave(freq, time)
    return math.sin(2 * math.pi * freq * time)
end

function square_wave(freq, time)
    return sine_wave(freq, time) >= 0 and 0.3 or -0.3
end

-- Python calls this for every audio frame
-- key_char: active key (e.g., 'a', 'g') or nil
function get_sample(time, key_char)
    if not key_char then
        return 0.0 -- Silence when no key is held
    end

    local upper_key = string.upper(key_char)
    local freq = frequencies[upper_key]

    if not freq then
        return 0.0 -- Unmapped key
    end

    -- Blend sine and square wave for a crisp synth tone
    local tone = (sine_wave(freq, time) * 0.6) + (square_wave(freq, time) * 0.4)
    return tone * 0.5 -- Master volume scaling
end