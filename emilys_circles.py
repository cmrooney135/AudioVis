import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import gcd
import pandas as pd

def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr)) * diff) / diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr


def lcm(a, b):
    '''Calculate the least common multiple (LCM) of two values'''
    return abs(a * b) // gcd(a, b)


def calculate_drawn_shape(df):
    ''' Calculate the drawn shape from a dataframe'''
    # Extract columns from the dataframe
    magnitudes = df['magnitude'].tolist()
    phases = df['phase'].tolist()
    frequencies = df['frequency'].tolist()
    print(f'mags: {magnitudes}')
    print(f'phases: {phases}')
    print(f'freqs: {frequencies}')

    # Normalize radii and phases as needed
    radii = normalize(magnitudes, 1, 10)  # Normalize magnitudes
    angles = phases  # Use phases directly

    print(f'radii: {radii}')

    # Calculate the overall LCM of frequencies
    overall_lcm = round(frequencies[0])
    for freq in frequencies[1:]:
        overall_lcm = lcm(overall_lcm, round(freq))

    # Calculate the overall GCD of frequencies
    overall_gcd = round(frequencies[0])
    for freq in frequencies[1:]:
        overall_gcd = gcd(overall_gcd, round(freq))

    # Calculate the duration for one full iteration based on the slowest frequency
    duration = 2 * np.pi / overall_gcd  # Full rotation period for the slowest frequency

    # Calculate the positions of the circle centers
    def calculate_positions(angles, radii):
        '''Calculate the positions of the circle centers'''
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
    dt = duration / overall_lcm

    if dt < 0.0005:
        dt = 0.0005

    time = 0

    print(dt)
    print(duration)

    while time < duration:
        # Update the angles based on the rotation frequencies and time
        angles = [(freq * time) for freq in frequencies]

        # Calculate the positions of the circle centers
        positions = calculate_positions(angles, radii)

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


# Define sets of circles using a list of pandas dataframes
# Assuming `dataframes` is a list of pandas dataframes
dataframes = [
    # Add your pandas dataframes here
    pd.DataFrame({
        'magnitude': [0.005907, 0.003294, 0.001658, 0.001316],
        'phase': [-0.987585, 1.372912, -1.965995, 1.075551],
        'frequency': [43.066406, 86.132812, 129.199219, 172.265625],
        'time': [0.0, 0.0, 0.0, 0.0],
        'noise': [0.004468, 0.004468, 0.004468, 0.004468],
    }, ),
    pd.DataFrame({
        'magnitude': [0.005907, 0.003294, 0.001658, 0.001316],
        'phase': [-0.987585, 1.372912, -1.965995, 1.075551],
        'frequency': [43.066406, 86.132812, 129.199219, 172.265625],
        'time': [0.0, 0.0, 0.0, 0.0],
        'noise': [0.004468, 0.004468, 0.004468, 0.004468],
    }, ),
    # Add more dataframes as needed
]

# Calculate the drawings for each set of circles from dataframes
drawings = [calculate_drawn_shape(df) for df in dataframes]

# Create the figure for animation
fig, ax = plt.subplots()
ax.set_aspect('equal')

# Initialize the plot line for the animation
line, = ax.plot([], [], 'b-')

# Set the axis limits based on the largest radius in the sets
ax.set_xlim(-2, 2)
ax.set_ylim(- 2, 2)


# Frame update function for the animation
def update(frame):
    # Clear the line data
    line.set_data([], [])

    # Get the current drawing based on the frame index
    current_drawing = drawings[frame % len(drawings)]
    print(len(drawings))

    # Extract the x and y coordinates from the current drawing
    x_coords, y_coords = zip(*current_drawing)

    # Update the line data with the current drawing
    line.set_data(x_coords, y_coords)

    return line,


# Create the animation with frames cycling through the different drawings
ani = FuncAnimation(fig, update, frames=len(drawings), interval=100, blit=True)

# Show the animation
plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from math import gcd

# def normalize(arr, t_min, t_max):
#     norm_arr = []
#     diff = t_max - t_min
#     diff_arr = max(arr) - min(arr)
#     for i in arr:
#         temp = (((i - min(arr)) * diff) / diff_arr) + t_min
#         norm_arr.append(temp)
#     return norm_arr

# # Function to calculate the drawn shape
# def calculate_drawn_shape(radii, frequencies, angles):
#     # Define a function to calculate the least common multiple (LCM)
#     frequencies = frequencies
#     def lcm(a, b):
#         return abs(a * b) // gcd(a, b)

#     # Calculate the overall LCM of frequencies
#     overall_lcm = round(frequencies[0])
#     for freq in frequencies[1:]:
#         overall_lcm = lcm(overall_lcm, round(freq))

#     overall_gcd = round(frequencies[0])
#     for freq in frequencies[1:]:
#         overall_gcd = gcd(overall_gcd, round(freq))

#     # Calculate the duration for one full iteration based on the slowest frequency
#     duration = 2 * np.pi / overall_gcd  # Full rotation period for the slowest frequency

#     # Calculate the positions of the circle centers
#     def calculate_positions(angles):
#         positions = [(0, 0)]  # Initial position at the center of the first (largest) circle
#         total_angle = 0
#         for i in range(1, len(radii)):
#             prev_radius = radii[i - 1]
#             x, y = positions[i - 1]
#             total_angle += angles[i - 1]
#             new_x = x + prev_radius * np.cos(total_angle)
#             new_y = y + prev_radius * np.sin(total_angle)
#             positions.append((new_x, new_y))
#         return positions

#     # Simulate the rotation and capture the path
#     drawing_x = []
#     drawing_y = []

#     # Define the time step for simulation
#     dt = duration / overall_lcm

#     # Simulate the rotation for one full iteration of the slowest frequency
#     time = 0
#     # if duration > 0.5: # to prevent long runtimes
#     #     duration = 0.5
#     if dt < 0.0005:
#         dt = 0.0005
#     print(f'duration: {duration}')
#     print(f'dt:{dt}')

#     while time < duration:
#         # Update the angles based on the rotation frequencies and time
#         angles = [(freq * time) for freq in frequencies]

#         # Calculate the positions of the circle centers
#         positions = calculate_positions(angles)

#         # Calculate the position of the smallest circle's vector tip
#         x, y = positions[-1]  # Last circle's center position
#         end_x = x + radii[-1] * np.cos(angles[-1])
#         end_y = y + radii[-1] * np.sin(angles[-1])

#         # Append the vector tip's position to the drawing lists
#         drawing_x.append(end_x)
#         drawing_y.append(end_y)

#         # Increment the time
#         time += dt

#     # Combine x and y coordinates into a list of tuples
#     coordinates = list(zip(drawing_x, drawing_y))

#     # Return the list of (x, y) coordinates
#     return coordinates


# # Define sets of circles (radii, frequencies, angles) as a list of dictionaries
# circle_sets = [
#     # {"radii": [2, 3, 1], "frequencies": [100, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [2.1, 2.9, 1], "frequencies": [100, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [2.2, 2.8, 1], "frequencies": [100, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [2.3, 2.7, 1], "frequencies": [100, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [2.5, 2.5, 1], "frequencies": [100, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [2.8, 2, 1], "frequencies": [100, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [3, 2.5, 1], "frequencies": [100, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [3.5, 3, 1], "frequencies": [100, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [4, 3.5, 1], "frequencies": [100, 500, 200], "angles": [6, 0, 0]},
#     # {"radii": [4.2, 4, 1], "frequencies": [100, 500, 200], "angles": [0, 0, 0]},
#     # Add more sets as needed
#     {"radii": normalize([0.005907, 0.003294, 0.001658, 0.001316], 1, 10), "frequencies": [43.066406, 86.132812, 129.199219, 172.265625], "angles": [-0.987585 , 1.372912 , -1.965995, 1.075551]},
#     {"radii": normalize([0.0045171, 0.0016733, 0.0010597, 0.0007124], 1, 10), "frequencies": [43.066406, 86.132812, 129.199219, 172.265625],"angles": [0.0089754, -0.0454574, -0.0039633, 0.0435943]},
#     {"radii": normalize([0.045723, 0.013932, 0.009074, 0.006153], 1, 10), "frequencies": [43.066406, 75.195312, 88.261719, 72.128906],"angles": [-0.005819, -2.523304, 0.669158, 0.338292]},
#     {"radii": normalize([0.045479, 0.010025, 0.008299, 0.003748], 1, 10),"frequencies": [43.066406, 775.195312, 818.261719, 602.929688], "angles": [0.012873, -1.321469, 1.898021, -0.890767]},
#     {"radii": normalize([0.044389, 0.005985, 0.004324, 0.003560], 1, 10),"frequencies": [43.066406, 775.195312, 818.261719, 1464.257812],"angles": [0.001410, -0.630109, -3.061796, 1.503552]},
#     {"radii": normalize([0.043826, 0.002666, 0.002584, 0.002548], 1, 10), "frequencies": [43.066406, 818.261719, 2239.453125, 2670.117188],"angles": [0.009969, -2.680762, 2.479521, 2.256769]},
#     {"radii": normalize([0.046419, 0.003846, 0.002671, 0.002591], 1, 10),"frequencies": [43.066406, 2282.519531, 2325.585938, 1076.660156],"angles": [0.009087, -0.036909, 2.884260, -2.268928]},
#     {"radii": normalize([0.005907, 0.003294, 0.001658, 0.001316], 1, 10),"frequencies": [43.066406, 86.132812, 129.199219, 172.265625],"angles": [-0.987585, 1.372912, -1.965995, 1.075551]},
#     {"radii": normalize([7.813497e-03, 9.981356e-07, 9.926085e-07, 9.850345e-07], 1, 10),"frequencies": [43.066406, 86.132812, 129.199219, 172.265625],"angles": [-0.000011, -0.179094, -0.269296, -0.360277]},
#     {"radii": normalize([0.007694, 0.000169, 0.000168, 0.000164], 1, 10),"frequencies": [43.066406, 904.394531, 1162.792969, 1119.726562],"angles": [0.015999, -1.564722, -1.005802, 2.918475]},
#     {"radii": normalize([0.007687, 0.000185, 0.000174, 0.000166], 1, 10),"frequencies": [43.066406, 86.132812, 1378.125, 1507.324219],"angles": [0.005509, -1.155179, -2.629228, -0.834599]},
#     {"radii": normalize([0.007663, 0.000210, 0.000204, 0.000203], 1, 10),"frequencies": [43.066406, 559.863281, 258.398438, 301.464844],"angles": [0.012886, -1.835954, -2.224303, 0.410187]},
#     {"radii": normalize([0.007821, 0.000065, 0.000065, 0.000065], 1, 10),"frequencies": [43.066406, 258.398438, 1076.660156, 1162.792969],"angles": [0.000271, -2.206774, -2.322529, 1.273229]},
#     {"radii": normalize([0.007792, 0.000055, 0.000055, 0.000055], 1, 10),"frequencies": [43.066406, 602.929688, 1076.660156, 1205.859375],"angles": [-0.001532, -1.780449, 1.087542, 2.721666]},
#     {"radii": normalize([0.007770, 0.000048, 0.000048, 0.000048], 1, 10),"frequencies": [43.066406, 301.464844, 602.929688, 689.0625],"angles": [0.000754, 2.035169, -2.213174, -2.574914]},
#     {"radii": normalize([0.007808, 0.000029, 0.000029, 0.000029], 1, 10),"frequencies": [43.066406, 732.128906, 1033.59375, 301.464844],"angles": [0.002164, 2.610148, 2.749921, 0.140099]},
#     {"radii": normalize([0.007750, 0.000166, 0.000164, 0.000158], 1, 10),"frequencies": [43.066406, 904.394531, 1033.59375, 129.199219],"angles": [0.008517, -2.747960, 2.957241, -0.628421] },
#     #{"radii": normalize([0.007682, 0.000257, 0.000203], 1, 10),"frequencies": [43.066406, 861.328125, 1378.125],"angles": [-0.000391, 2.250982, -1.139774]},
# ]


#     # {"radii": [2, 3, 1], "frequencies": [300, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [2, 3, 1], "frequencies": [400, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [2, 3, 1], "frequencies": [500, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [2, 3, 1], "frequencies": [600, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [2, 3, 1], "frequencies": [700, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [2, 3, 1], "frequencies": [800, 500, 200], "angles": [0, 0, 0]},
#     # {"radii": [2, 3, 1], "frequencies": [900, 500, 200], "angles": [6, 0, 0]},
#     # {"radii": [2, 3, 1], "frequencies": [1000, 500, 200], "angles": [0, 0, 0]},

# # Calculate the drawings for each set of circles
# drawings = [calculate_drawn_shape(**circle_set) for circle_set in circle_sets]

# # Create the figure for animation
# fig, ax = plt.subplots()
# ax.set_aspect('equal')

# # Initialize the plot line for the animation
# line, = ax.plot([], [], 'b-')

# # Set the axis limits based on the largest radius in the sets
# max_radius = max(max(circle_set["radii"]) for circle_set in circle_sets)
# ax.set_xlim(-max_radius * 2, max_radius * 2)
# ax.set_ylim(-max_radius * 2, max_radius * 2)

# # Frame update function for the animation
# def update(frame):
#     # Clear the line data
#     line.set_data([], [])

#     # Get the current drawing based on the frame index
#     current_drawing = drawings[frame % len(drawings)]

#     # Extract the x and y coordinates from the current drawing
#     x_coords, y_coords = zip(*current_drawing)

#     # Update the line data with the current drawing
#     line.set_data(x_coords, y_coords)

#     return line,

# # Create the animation with frames cycling through the different drawings
# ani = FuncAnimation(fig, update, frames=len(drawings), interval=100, blit=True)

# # Show the animation
# plt.show()

