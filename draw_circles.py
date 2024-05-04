import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import gcd
import pandas as pd

# Needs to pass all of the dataframes and get all of the coordinates out

class DrawCircles:
    def __init__(self, dataframes):
        # Initialize with a list of pandas dataframes
        self.dataframes = dataframes
        self.drawings = [self.calculate_drawn_shape(df) for df in dataframes]

        # Create the figure for animation
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')

        # Initialize the plot line for the animation
        self.line, = self.ax.plot([], [], 'b-')

        # Set the axis limits
        max_radius = max(max(df['magnitude']) for df in dataframes)
        self.ax.set_xlim(-20, 20)
        self.ax.set_ylim(-20, 20)

    def normalize(self, arr, t_min, t_max):
        """Normalize an array of values"""
        norm_arr = []
        diff = t_max - t_min
        diff_arr = max(arr) - min(arr)
        for i in arr:
            temp = (((i - min(arr)) * diff) / diff_arr) + t_min
            norm_arr.append(temp)
        return norm_arr

    def lcm(self, a, b):
        """Calculate the least common multiple (LCM) of two values"""
        return abs(a * b) // gcd(a, b)

    def calculate_drawn_shape(self, df):
        """Calculate the drawn shape from a dataframe"""
        # Extract columns from the dataframe
        magnitudes = df['magnitude'].tolist()
        phases = df['phase'].tolist()
        frequencies = df['frequency'].tolist()

        # Normalize radii and phases as needed
        radii = self.normalize(magnitudes, 1, 10)  # Normalize magnitudes
        angles = phases  # Use phases directly

        # Calculate the overall LCM of frequencies
        overall_lcm = round(frequencies[0])
        for freq in frequencies[1:]:
            overall_lcm = self.lcm(overall_lcm, round(freq))

        # Calculate the overall GCD of frequencies
        overall_gcd = round(frequencies[0])
        for freq in frequencies[1:]:
            overall_gcd = gcd(overall_gcd, round(freq))

        # Calculate the duration for one full iteration based on the slowest frequency
        duration = 2 * np.pi / overall_gcd  # Full rotation period for the slowest frequency

        # Calculate the positions of the circle centers
        def calculate_positions(angles, radii):
            """Calculate the positions of the circle centers"""
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

    # def update(self, frame):
    #     """Frame update function for the animation"""
    #     # Clear the line data
    #     self.line.set_data([], [])
    #
    #     # Get the current drawing based on the frame index
    #     current_drawing = self.drawings[frame % len(self.drawings)]
    #
    #     # Extract the x and y coordinates from the current drawing
    #     x_coords, y_coords = zip(*current_drawing)
    #
    #     # Update the line data with the current drawing
    #     self.line.set_data(x_coords, y_coords)
    #
    #     return self.line,
    #
    # def start_animation(self):
    #     """Create the animation with frames cycling through the different drawings"""
    #     ani = FuncAnimation(self.fig, self.update, frames=len(self.drawings), interval=100, blit=True)
    #
    #     # Show the animation
    #     plt.show()


# # Assuming `dataframes` is a list of pandas dataframes
# dataframes = [
#     pd.DataFrame({
#         'magnitude': [0.005907, 0.003294, 0.001658, 0.001316],
#         'phase': [-0.987585, 1.372912, -1.965995, 1.075551],
#         'frequency': [43.066406, 86.132812, 129.199219, 172.265625],
#         'time': [0.0, 0.0, 0.0, 0.0],
#         'noise': [0.004468, 0.004468, 0.004468, 0.004468],
#     }, ),
#     pd.DataFrame({
#         'magnitude': [0.005907, 0.003294, 0.001658, 0.001316],
#         'phase': [-0.987585, 1.372912, -1.965995, 1.075551],
#         'frequency': [43.066406, 86.132812, 129.199219, 172.265625],
#         'time': [0.0, 0.0, 0.0, 0.0],
#         'noise': [0.004468, 0.004468, 0.004468, 0.004468],
#     }),
# ]

# # Create an instance of DrawCircles and start the animation
# circles = DrawCircles(dataframes)
# circles.start_animation()
