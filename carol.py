# DSP Final Project
# Emily Ninestein, Carol Rooney, Alec Benedict
import librosa
# How to take real time fft (carol)

# How to draw shapes with fft (emily)

# Design filter to get color from signal
# Design filter to get line thickness

# Filtering noise

import pydub as pd
import librosa as libr
import numpy as np
import wave as wv
import matplotlib.pyplot as plt
import scipy
from scipy.io import wavfile
from scipy.signal import find_peaks
from scipy import signal
from pydub import AudioSegment
from pydub.playback import play
filename = 'lib/fuzz.wav'

#code to play song
#wav_file = AudioSegment.from_file(filename, format = "wav")
#play(wav_file)
with wv.open(filename, 'rb') as wf:
    num_frames = wf.getnframes()
    frame_rate = wf.getframerate()
    frames = wf.readframes(num_frames)

    duration = num_frames / frame_rate

data = np.frombuffer(frames, dtype=np.int16)
sampling_rate = wf.getframerate()

window = signal.get_window('blackmanharris', 2048)
window_size = len(window)
hop_length = 512


nper = window_size // 2

# maybe do a for loop for the length of the file. perform a FFT on each sample, and extract the two
#dominant frequencies using find_peaks and assign emilys picture to each sample
#each sample has a different picture, based on its frequency
# the animation is the transition between pictures, and can be as long as the hop size duration
# Amplitude is what determines


# how will we do noise detection ?
# thickness of the line related to the speed of the dot
#


frequencies, times, stft_data = signal.stft(data, sampling_rate, window='blackmanharris', nperseg=window_size, noverlap=window_size-hop_length, nfft=window_size)

frame_duration = window_size / sampling_rate
hop_duration = hop_length / sampling_rate


plt.figure(figsize=(12, 6))
plt.pcolormesh(times, frequencies, np.abs(stft_data)**0.3, shading='gouraud', cmap='inferno')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [s]')
plt.title('Spectrogram')
plt.colorbar(label='Magnitude')
plt.ylim(0, 2000)
plt.show()