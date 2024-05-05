import numpy as np
import librosa
import librosa.display
import pandas as pd
def compute_stft_features(audio_file, n_fft=2048, hop_length=1024, n_mels=128):
    # Load the audio file
    y, sr = librosa.load(audio_file)

    # Compute STFT
    D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)

    # Compute magnitude and phase
    magnitude = np.abs(D)
    phase = np.angle(D)

    # Compute mel spectrogram
    mel_spec = librosa.feature.melspectrogram(S=magnitude**2, sr=sr, n_mels=n_mels)

    # Compute flatness
    flatness = librosa.feature.spectral_flatness(S=magnitude)

    # Get number of samples
    num_samples = magnitude.shape[1]

    # Initialize lists to store data for DataFrame
    data = {'Magnitude': [], 'Phase': [], 'Real_Time': [], 'Flatness': []}

    for i in range(num_samples):
        # Find dominant magnitudes for the current sample
        dominant_magnitudes_indices = np.argsort(magnitude[:, i])[-4:]  # Get indices of top 4 magnitudes
        dominant_magnitudes = np.take_along_axis(magnitude[:, i], dominant_magnitudes_indices, axis=0)

        # Get corresponding phases
        phases = phase[dominant_magnitudes_indices, i]

        # Append data to the lists
        for j, magnitude_value in enumerate(dominant_magnitudes):
            data['Magnitude'].append(magnitude_value)
            data['Phase'].append(phases[j])
            data['Real_Time'].append(np.sum(np.real(D[:, i])))
            data['Flatness'].append(flatness[0, i])

    # Create DataFrame
    df = pd.DataFrame(data)

    return df

# Example usage:
audio_file = "lib/fuzz.wav"
df = compute_stft_features(audio_file)

print(df)