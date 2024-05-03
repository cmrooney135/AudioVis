import numpy as np
from pytweening import easeOutQuad
import matplotlib.pyplot as plt
from matplotlib import animation

# Define the number of points for the shapes
num_points = 100

# Create points for shape1 (square)
square_side = 2
half_side = square_side / 2
square_x = np.concatenate((np.linspace(-half_side, half_side, num_points),
                           np.full(num_points, half_side),
                           np.linspace(half_side, -half_side, num_points),
                           np.full(num_points, -half_side)))
square_y = np.concatenate((np.full(num_points, half_side),
                           np.linspace(half_side, -half_side, num_points),
                           np.full(num_points, -half_side),
                           np.linspace(-half_side, half_side, num_points)))
shape1 = np.column_stack((square_x, square_y))

# Create points for shape2 (circle) with the same number of points as shape1
theta_circle = np.linspace(0, 2*np.pi, 4*num_points)  # Increase the number of points
circle_x = np.cos(theta_circle)
circle_y = np.sin(theta_circle)
shape2 = np.column_stack((circle_x, circle_y))

duration = 0.0348  # Duration in seconds

# Calculate the frame rate needed to achieve at least 5 frames
num_frames = 10
frame_rate = int(np.ceil(num_frames / duration))

# Compute intermediate shapes using easeOutQuad interpolation
frames = []
for i in range(num_frames):
    t = easeOutQuad(i / num_frames)  # Use easeOutQuad function for faster movement
    intermediate_shape = shape1 * (1 - t) + shape2 * t
    frames.append(intermediate_shape)

# Plot the initial shapes
plt.figure(figsize=(8, 4))

plt.subplot(1, 2, 1)
plt.plot(shape1[:, 0], shape1[:, 1], color='blue')
plt.title('Shape 1 (Square)')
plt.axis('equal')

plt.subplot(1, 2, 2)
plt.plot(shape2[:, 0], shape2[:, 1], color='green')
plt.title('Shape 2 (Circle)')
plt.axis('equal')

plt.show()

# Plot the animation
plt.figure()
line, = plt.plot([], [], color='red', label='Morphing')
plt.plot(shape1[:, 0], shape1[:, 1], color='blue', label='Shape 1 (Square)')
plt.plot(shape2[:, 0], shape2[:, 1], color='green', label='Shape 2 (Circle)')
plt.legend()

# Define update function for animation
def update(frame):
    line.set_data(frame[:, 0], frame[:, 1])
    return line,

# Animate
ani = animation.FuncAnimation(plt.gcf(), update, frames=frames, blit=True, interval=1000 / frame_rate, repeat=False)

plt.show()
