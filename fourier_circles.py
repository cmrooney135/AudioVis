# Drawing shapes with circles using the Fourier Transform
# Emily Ninestein

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft

# Step 1: Read the .wav file
sample_rate, audio_data = wavfile.read('your_audio_file.wav')

# Convert the audio data to float type for the Fourier transform
if audio_data.dtype == np.int16:
    audio_data = audio_data.astype(np.float32) / np.iinfo(np.int16).max
elif audio_data.dtype == np.int32:
    audio_data = audio_data.astype(np.float32) / np.iinfo(np.int32).max

# Step 2: Compute the Fourier transform using FFT
fft_result = fft(audio_data)

# Step 3: Compute the frequency bins
N = len(audio_data)
frequencies = np.fft.fftfreq(N, 1/sample_rate)

# Step 4: Plot the magnitude of the Fourier transform
plt.plot(frequencies[:N//2], np.abs(fft_result)[:N//2])
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('Frequency Spectrum of Audio')
plt.show()


