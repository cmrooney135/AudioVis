import librosa
import numpy as np
import pandas as pd
import time
import sys

filename = 'lib/fuzz.wav'

shape_data = []

def STFT(filename):
    audio_samples, sample_rate = librosa.load(filename, sr=None)

    n_fft = 2048
    hop_length = 512
    #perform stft
    stft = librosa.stft(audio_samples, n_fft=n_fft, hop_length=hop_length)
    # 3634 columns in stft
    frequencies = librosa.fft_frequencies(sr=sample_rate, n_fft=n_fft)

    #noise extraction
    flatness = librosa.feature.spectral_flatness(y=audio_samples, hop_length=hop_length, n_fft=n_fft)

    #number of columns in the stft
    n_col = stft.shape[1]


    #i is the current time frame number
    for i in range (2):
        #draw circles with emilys code
        magnitude = np.abs(stft[:, i])
        phase = np.angle(stft[:, i])
        time_of_sample = i * hop_length / sample_rate
        flatness_value = flatness[0, i]

        data = pd.DataFrame({'magnitude': magnitude, 'phase': phase, 'frequency': frequencies, 'time':time_of_sample, 'noise':flatness_value})
        data = data[data['frequency'] != 0]

        data.sort_values(by='magnitude', ascending=False, inplace=True)
        dominant = data.head(4).copy()
        dominant['frequency'] = dominant.index * sample_rate / n_fft
        shape_data.append(dominant)

    return(shape_data)

def draw_shapes(shape_data):
    shape_array = []
    for df in shape_data:
        magnitudes = df['magnitude'].values
        phases = df['phase'].values
        frequencies = df['frequency'].values
        times = df['time'].values
        noises = df['noise'].values
        new = calculate_drawn_shape(magnitudes, frequencies, phases)
        shape_array.append(new)
        # construct the circles from the above values
        #figure out the color of each object
        #maybe we need a little OOP here
        # construct an array of shapes such that they can be displayed on the screen with transition time
        #that is variant on the hop size and buffer size


        # frequency is thickness
        # The thickness decreases as the beam moves faster.
        # This causes high-frequency sounds or loud sounds to appear thinner.
        # determine the amount of noise present in each sample
        # flatness value closer to 1 means it is more noise
        #more noise  more white,
        # less noise purer colors.

        #saturation is noise
        #hue is frequency
        # value is maxed out



        #real_part = np.real(stft[:, i])
        #imag_part = np.imag(stft[:, i])
    return shape_array

def calculate_drawn_shape(radii, frequencies, angles):
    # Define a function to calculate the least common multiple (LCM)
    def lcm_float(a, b):
        # Convert floating-point numbers to integers by multiplying with a large power of 10
        a_int = int(a * 10 ** 10)
        b_int = int(b * 10 ** 10)

        # Compute the LCM of the integers
        lcm_int = abs(a_int * b_int) // np.gcd(a_int, b_int)

        # Convert back to floating-point and adjust precision
        lcm_float = lcm_int / 10 ** 10

        return lcm_float

    # Calculate the overall LCM of frequencies
    overall_lcm = frequencies[0]
    for freq in frequencies[1:]:
        overall_lcm = lcm_float(overall_lcm, freq)

    # Calculate the duration for one full iteration based on the slowest frequency
    duration = 2 * np.pi / frequencies[0]  # Full rotation period for the slowest frequency

    # Calculate the positions of the circle centers
    def calculate_positions(angles):
        positions = [(0, 0)]  # Initial position at the center of the first (largest) circle
        total_angle = 0
        for i in range(1, len(radii)):
            prev_radius = radii[i - 1]
            x, y = positions[i - 1]
            total_angle += angles[i - 1]
            new_x = x + prev_radius * np.cos(total_angle)
            new_y = y + prev_radius * np.sin(total_angle)
            positions.append((new_x, new_y))
        return positions

    # Simulate the rotation and capture the path
    drawing_x = []
    drawing_y = []

    # Define the time step for simulation
    dt = duration / overall_lcm  # A small time step for accuracy

    # Simulate the rotation for one full iteration of the slowest frequency
    time = 0
    while time < duration:
        # Update the angles based on the rotation frequencies and time
        angles = [(freq * time) for freq in frequencies]

        # Calculate the positions of the circle centers
        positions = calculate_positions(angles)

        # Calculate the position of the smallest circle's vector tip
        x, y = positions[-1]  # Last circle's center position
        end_x = x + radii[-1] * np.cos(angles[-1])
        end_y = y + radii[-1] * np.sin(angles[-1])

        # Append the vector tip's position to the drawing lists
        drawing_x.append(end_x)
        drawing_y.append(end_y)

        # Increment the time
        time += dt

    # Combine x and y coordinates into a list of tuples
    coordinates = list(zip(drawing_x, drawing_y))

    # Return the list of (x, y) coordinates
    return coordinates


dat = STFT(filename)

lines = draw_shapes(dat)
print(lines)