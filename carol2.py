import librosa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import gcd
from math import ceil
from matplotlib.animation import FuncAnimation
import time
import sys

filename = 'lib/fuzz.wav'

shape_data = []

def STFT(filename):
    print("STFT")
    audio_samples, sample_rate = librosa.load(filename, sr=None)

    n_fft = 1024
    hop_length = n_fft // 4
    overlap = n_fft-hop_length
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
        #print(shape_data)
    return (shape_data)



def draw_shapes(shape_data):
    print("draw_shapes initiated")
    shape_array = []
    for df in shape_data:
        print("DF in shape_data entered")
        magnitudes = df['magnitude'].values
        print(len(magnitudes))
        phases = df['phase'].values
        frequencies = df['frequency'].values
        times = df['time'].values
        noises = df['noise'].values
        new = calculate_drawn_shape(magnitudes, phases, frequencies,times)
        shape_array.append(new)
        #print(shape_array)
    print(len(shape_array))
    return shape_array
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



def calculate_drawn_shape(magnitudes,phases, frequencies,times):

    radii = magnitudes
    angles = phases
    # Define a function to calculate the least common multiple (LCM)
    #print(radii)

    def lcm(a, b):
        a = ceil(a)
        b = ceil(b)
        return abs(a * b) // gcd(a, b)

    # Calculate the overall LCM of frequencies
    overall_lcm = frequencies[0]
    for freq in frequencies[1:]:
        freq = ceil(freq)
        overall_lcm = lcm(overall_lcm, freq)
    #print(f'overall_lcm: {overall_lcm}')

    overall_gcd = frequencies[0]
    for freq in frequencies[1:]:
        freq = ceil(freq)
        overall_gcd = gcd(ceil(overall_gcd), freq)
    #print(f'overall_gcd: {overall_gcd}')

    # Calculate the duration for one full iteration based on the slowest frequency
    sorted_freqs = sorted(frequencies)
    duration = 2 * np.pi / overall_gcd  # Full rotation period for the slowest frequency

    # Calculate the positions of the circle centers
    #this is never being entered
    def calculate_positions(angles):
        #this is being entered like a million times
        #print("calculate positions initiated")
        positions = [(0, 0)]  # Initial position at the center of the first (largest) circle
        total_angle = 0
        #print(f'radii len: {len(radii)}')
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
    #print(overall_lcm)
    dt = 0.00001
    print("dt = ", dt)
    # A small time step for accuracy
    #print(duration)

    # Simulate the rotation for one full iteration of the slowest frequency
    time = 0
    while (time < duration):
        #print("Time:", time)
        #print("(time < duration):", (time < duration))

        # Update the angles based on the rotation frequencies and time
        angles = [(freq * time) for freq in frequencies]



        # Calculate the positions of the circle centers
        positions = calculate_positions(angles)
        #print(positions)

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




data = STFT(filename)
print(data)
magnitudes_data = [item['magnitude'] for item in data]
frequencies_data = [item['frequency'] for item in data]
phases_data = [item['phase'] for item in data]
times_data = [item['time'] for item in data]
noises_data = [item['noise'] for item in data]


shapes = draw_shapes(data)

circle_sets = []
print("length of shape_data : ", len(shapes))
#print(shapes)
# Define sets of circles (radii, frequencies, angles) as a list of dictionaries
#this is never being entered
for shape_data in shapes:
    radii = [shape[0] for shape in shape_data]
    angles = [shape[1] for shape in shape_data]
    frequencies = [shape[2] for shape in shape_data]
    circle_set = {"radii": radii, "frequencies": frequencies, "angles": angles}
    circle_sets.append(circle_set)

for circle_set in circle_sets:
    print("Radii:", circle_set.get("radii"))

    # Calculate the drawings for each set of circles
    drawings = [calculate_drawn_shape(circle_set) for circle_set in circle_sets]

    # Create the figure for animation
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # Initialize the plot line for the animation
    line, = ax.plot([], [], 'b-')

    radii_lists = [circle_set["radii"] for circle_set in circle_sets if circle_set.get("radii")]

    # Calculate the maximum radius if there are non-empty radii lists
    if radii_lists:
        max_radius = max(max(radii) for radii in radii_lists)
    else:
        # Provide a default maximum radius if all radii lists are empty
        max_radius = 10

# Frame update function for the animation
def update(frame):
    # Clear the line data
    line.set_data([], [])

    # Get the current drawing based on the frame index
    current_drawing = drawings[frame % len(drawings)]

    # Extract the x and y coordinates from the current drawing
    x_coords, y_coords = zip(*current_drawing)

    # Update the line data with the current drawing
    line.set_data(x_coords, y_coords)

    return line,


# Create the animation with frames cycling through the different drawings
ani = FuncAnimation(fig, update, frames=len(drawings), interval=100, blit=True)

# Show the animation
plt.show()