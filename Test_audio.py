import librosa
import numpy as np
from scipy.io.wavfile import write

sr = 22050
duration = 60
linear_chirp = librosa.chirp(fmin=20,fmax=20000,duration=duration,sr=sr,linear=True)
linear_chirp /= np.max(np.abs(linear_chirp))
linear_chirp_int = np.int16(linear_chirp * 32767)


mono_tone = librosa.tone(frequency=440,duration=duration,sr=22050)


# Generate time array
t = np.linspace(0, duration, int(sr * duration), endpoint=False)

# Middle C
tone = np.sin(2 * np.pi * 466.164 * t)

# Increase magnitude linearly
magnitude = np.linspace(0, 1, len(t))
tone_with_increasing_magnitude = tone * magnitude

# Normalize signal to be in the range [-1, 1]
tone_with_increasing_magnitude /= np.max(np.abs(tone_with_increasing_magnitude))

# Convert signal to 16-bit integer format
tone_int = np.int16(tone_with_increasing_magnitude * 32767)


write('lib/linear_chirp.wav', sr, linear_chirp_int)
write('lib/monotone.wav', sr, mono_tone)
write('lib/tone_with_increasing_magnitude.wav', sr, tone_int)

