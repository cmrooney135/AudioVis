import librosa
import numpy as np

filename = 'lib/fuzz.wav'
audio_samples, sample_rate = librosa.load(filename, sr=None)

n_fft = 2048
hop_length = 512
#perform stft
stft = librosa.stft(audio_samples, n_fft=n_fft, hop_length=hop_length)

#noise extraction
flatness = librosa.feature.spectral_flatness(y=audio_samples, hop_length=hop_length, n_fft=n_fft)


stft_real = np.real(stft)
stft_imag = np.imag(stft)

#number of columns in the stft
n_col = stft.shape[1]

#i is the current time frame number
for i in range (n_col):

    #draw circles with emilys code

    magnitude = np.abs(stft[:, i])
    magnitude.sort()


    dom1 = magnitude[1]
    dom2 = magnitude[2]
    dom3 = magnitude[3]

    #extract most dominant frequencies from the magnitudes  ( 2 or 3 ) and perhaps their phases
    #draw circles based on 2 or 3 most dominant frequencies


    #determine the pitch of each sample and relate it to color
    # librosa.pyin(audio_samples, 0, 2093, sample_rate, )

    # determine the amount of noise present in each sample
    # flatness value closer to 1 means it is more noise like
    #more noise  more white,
    # less noise purer colors.
    time_of_sample = i * hop_length / sample_rate
    flatness_value = flatness[0, i]
    #print(f"Spectral Flatness at time {time_of_sample}: {flatness_value}")




    real_part = np.real(stft[:, i])
    imag_part = np.imag(stft[:, i])