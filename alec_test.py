import scipy
import pydub
import librosa
import numpy as np
import matplotlib.pyplot as plt
import wave
import pandas

test = wave.Wave_read('lib/acoustic.wav')

num_chanel = test.getnchannels()
frames = test.getnframes()

all_frames = test.readframes(frames)


