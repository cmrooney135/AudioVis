import numpy as np
from pytweening import easeOutQuad
import matplotlib.pyplot as plt
from matplotlib import animation
import colorsys


def animate(points, dataframe, overlap):
    def pick_color(frequency, noise):
        freq_normal = normalize(frequency, 0,360)
        R = freq_normal[0]
        G = freq_normal[1]
        B = freq_normal[2]
        color1 = colorsys.rgb_to_hsv(R, G, B)
        hue = color1[0]
        noise = np.mean(noise)
        saturation = noise * 255
        value = 255
        color = colorsys.hsv_to_rgb(hue, saturation, value)
        return color

    # Calculate the frame rate needed to achieve at least 5 frames
    num_frames = 10
    frame_rate = int(np.ceil(num_frames / overlap))

    # Compute intermediate shapes using easeOutQuad interpolation
    frames = []
    for index in range(len(points) - 1):
        print("entered for loop")
        shape1 = points[index]
        print(shape1)
        shape2 = points[index + 1]
        shape1_noise = dataframe[index]['noise'].values.tolist()
        shape2_noise = dataframe[index + 1]['noise'].values.tolist()
        shape1_frequency = dataframe[index]['frequency'].values.tolist()
        shape2_frequency = dataframe[index + 1]['frequency'].values.tolist()
        shape1_color = pick_color(shape1_frequency,shape1_noise)
        shape2_color = pick_color(shape2_frequency,shape2_noise)

    for i in range(num_frames):
        print("enetered for loop 2 ")
        t = easeOutQuad(i / num_frames)  # Use easeOutQuad function for faster movement
        intermediate_shape = shape1 * (1 - t) + shape2 * t
        intermediate_color = shape1_color * (1 - t) + shape2_color * t
        frames.append(intermediate_shape, intermediate_color)

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
        shape, color = frame
        line.set_data(shape[:, 0], shape[:, 1])
        line.set_color(color)
        return line,

    # Animate
    ani = animation.FuncAnimation(plt.gcf(), update, frames=frames, blit=True, interval=1000 / frame_rate, repeat=False)

    plt.show()

def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr)) * diff) / diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr










