import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the radii and rotation frequencies of the circles
radii = [3, 2, 1]  # Radii of the circles
frequencies = [100, 500, 200]  # Rotation frequencies (in rad/s) for each circle
angles = [0, 0, 0]  # Angle of the vector in each circle


# Calculate the positions of the circle centers
def calculate_positions(angles):
    positions = [(0, 0)]  # Start with the center of the first (largest) circle at (0, 0)
    total_angle = 0
    for i in range(1, len(radii)):  # Iterate through circles
        prev_radius = radii[i - 1]
        x, y = positions[i - 1]
        total_angle += angles[i - 1]
        # Calculate the new center position
        new_x = x + prev_radius * np.cos(total_angle)
        new_y = y + prev_radius * np.sin(total_angle)
        positions.append((new_x, new_y))
    return positions


# Initialize the plot
fig, ax = plt.subplots()
ax.set_aspect('equal')

# Initialize the circles and vectors
circles = []
vectors = []

for radius in radii:
    # Add a circle
    circle = plt.Circle((0, 0), radius, fill=False, edgecolor='black')
    circles.append(circle)
    ax.add_artist(circle)

    # Add a vector (line) from the center to the edge of the circle
    vector, = ax.plot([], [], 'r-', lw=2)
    vectors.append(vector)

# Set up the drawing trace for the "pencil tip"
drawing_x = []
drawing_y = []
drawing_line, = ax.plot([], [], 'b-')

# The pencil tip will be represented as a blue dot at the tip of the smallest circle's vector
pencil_tip, = ax.plot([], [], 'bo')

# Set the axis limits based on the largest radius
ax.set_xlim(-sum(radii), sum(radii))
ax.set_ylim(-sum(radii), sum(radii))


# Animation update function
def update(frame):
    # Update the angles based on the rotation frequencies and elapsed time
    dt = 0.0001  # Time elapsed for this frame
    angles[:] = [freq * dt + angle for angle, freq in zip(angles, frequencies)]  # (wt + theta)

    # Calculate the positions of the circle centers
    positions = calculate_positions(angles)  # all circle centers based on angles above

    # Update the circles and vectors
    for i in range(len(radii)):  # Iterate through circles
        # Update the position of the circle
        circle = circles[i]
        circle.set_center(positions[i])

        # Calculate the end point of the vector in the current circle
        x, y = positions[i]
        end_x = x + radii[i] * np.cos(angles[i])
        end_y = y + radii[i] * np.sin(angles[i])

        # Update the vector line data
        vectors[i].set_data([x, end_x], [y, end_y])

        # If this is the last (smallest) circle, update the pencil tip
        if i == len(radii) - 1:
            pencil_tip.set_data(end_x, end_y)

            # Append the pencil tip's position to the drawing list
            drawing_x.append(end_x)
            drawing_y.append(end_y)

    # Update the drawing line data
    drawing_line.set_data(drawing_x, drawing_y)

    return circles + vectors + [pencil_tip, drawing_line]


# Create the animation
# https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html
ani = FuncAnimation(fig, update, frames=range(500), interval=20, blit=True)

# Show the animation
plt.show()

# TO DO: figure out how to just get the shape that is drawn by the frequencies, save, and plot


