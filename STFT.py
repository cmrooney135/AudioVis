import librosa
import numpy as np
import pandas as pd
shape_data = []
def STFT(filename):
    #print("STFT")
    audio_samples, sample_rate = librosa.load(filename, sr=None)
    total_samples = len(audio_samples)
    audio_duration = librosa.get_duration(y=audio_samples, sr=sample_rate)
    print(len(audio_samples))
    n_fft = 2048
    n_stft = len(audio_samples)/n_fft
    hop_length = n_fft // 2
    #duration of overlap
    overlap_duration = hop_length / sample_rate
    #frame duration without overlap
    frame_duration = n_fft / sample_rate
    #audio duration
    audio_nsamples = total_samples/hop_length
    print("Frame duration:", frame_duration, "seconds")
    print("Overlap duration:", overlap_duration, "seconds")

    #perform stft
    stft = librosa.stft(audio_samples, n_fft=n_fft, hop_length=hop_length)
    # 3634 columns in stft
    frequencies = librosa.fft_frequencies(sr=sample_rate, n_fft=n_fft)

    # noise extraction
    flatness = librosa.feature.spectral_flatness(y=audio_samples, hop_length=hop_length, n_fft=n_fft)

    # number of columns in the stft
    magnitude = np.abs(stft)
    phase = np.angle(stft)
    nframes = magnitude.shape[1]
    print("magnitude size : ", nframes)

    shape_data = []
    frequencies_list = []
    # i is the current time frame number
    for i in range(nframes):
        # draw circles with emilys code
        magnitude = np.abs(stft[:, i])
        phase = np.angle(stft[:, i])
        time_of_sample = i * hop_length / sample_rate
        flatness_value = flatness[0, i]
        data = pd.DataFrame({'magnitude': magnitude, 'phase': phase, 'frequency': frequencies, 'time': time_of_sample,
                             'noise': flatness_value})
        data = data[data['frequency'] != 0]
        data = data[data['magnitude'] != 0]
        data.sort_values(by='magnitude', ascending=False, inplace=True)
        dominant = data.head(4).copy()
        # dominant['frequency'] = dominant.index * sample_rate / n_fft
        magnitudes = dominant['magnitude'].values
        phases = dominant['phase'].values
        times = dominant['time'].values
        noises = dominant['noise'].values
        shape_data.append(dominant)
        # frequencies_list = dominant['frequency'].tolist()
    # print(shape_data)
    # print(time_of_sample)
    return (shape_data, overlap_duration, frame_duration, audio_duration)