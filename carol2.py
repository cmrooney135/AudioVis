import librosa
import numpy as np
import pandas as pd


filename = 'lib/fuzz.wav'

shape_data = []

def STFT(filename):
    print("STFT")
    audio_samples, sample_rate = librosa.load(filename, sr=None)

    n_fft = 1024
    hop_length = n_fft // 4
    frame_duration = n_fft / sample_rate
    overlap = frame_duration - hop_length
    #perform stft
    stft = librosa.stft(audio_samples, n_fft=n_fft, hop_length=hop_length)
    # 3634 columns in stft
    frequencies = librosa.fft_frequencies(sr=sample_rate, n_fft=n_fft)

    #noise extraction
    flatness = librosa.feature.spectral_flatness(y=audio_samples, hop_length=hop_length, n_fft=n_fft)

    #number of columns in the stft
    n_col = stft.shape[1]

    shape_data = []
    #i is the current time frame number
    for i in range (n_col):
        #draw circles with emilys code
        magnitude = np.abs(stft[:, i])
        phase = np.angle(stft[:, i])
        time_of_sample = i * hop_length / sample_rate
        flatness_value = flatness[0, i]
        data = pd.DataFrame({'magnitude': magnitude, 'phase': phase, 'frequency': frequencies, 'time':time_of_sample, 'noise':flatness_value})
        data = data[data['frequency'] != 0]
        data = data[data['magnitude'] != 0]
        data.sort_values(by='magnitude', ascending=False, inplace=True)
        dominant = data.head(4).copy()
        dominant['frequency'] = dominant.index * sample_rate / n_fft
        magnitudes = dominant['magnitude'].values
        phases = dominant['phase'].values
        times = dominant['time'].values
        noises = dominant['noise'].values
        shape_data.append(dominant)
        frequencies_list = dominant['frequency'].tolist()
        #print(shape_data)
    return (shape_data, frequencies_list, overlap)

