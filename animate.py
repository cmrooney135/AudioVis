import numpy as np
from pytweening import easeOutQuad
import matplotlib.pyplot as plt
from matplotlib import animation
import colorsys
import matplotlib.colors as mcolors


def generate_frames(shape1, shape2, transition_frames, frame_rate):
    shape1_frames = []
    shape2_frames = []
    transition_frames = []

    # Generate frames for shape 1
    for _ in range(frame_rate):
        shape1_frames.append(shape1)

    # Generate frames for transition
    for frame in transition_frames:
        intermediate_shape = [
            ((1 - t) * x1 + t * x2, (1 - t) * y1 + t * y2)
            for (x1, y1), (x2, y2) in zip(shape1, shape2)
        ]
        transition_frames.append(intermediate_shape)

    # Generate frames for shape 2
    for _ in range(frame_rate):
        shape2_frames.append(shape2)

    return shape1_frames, transition_frames, shape2_frames

def animate(points, dataframe, overlap, frame_duration):
    def pick_color(frequency, noise):
        freq_normal = normalize(frequency, 0.1,1)
        R = freq_normal[0]
        G = freq_normal[1]
        B = freq_normal[2]
        color1 = colorsys.rgb_to_hsv(R, G, B)
        hue = color1[0]
        noise = np.mean(noise)
        saturation = 1 - noise
        if (saturation < 0.25):
            saturation = 0.25
        value = 0.99999
        color_rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        color_rgb = np.array(color_rgb)
        #print(color_rgb)
        return color_rgb

    # Calculate the frame rate needed to achieve at least 5 frames
    num_frames = int((len(points) - 1) * (frame_duration + overlap))
    frame_rate = 1 / (frame_duration + overlap)

    # Compute intermediate shapes using easeOutQuad interpolation
    frames = []

    for index in range(len(points) - 1):
        shape1 = points[index]
        shape2 = points[index + 1]

        dataframe1 = dataframe[index]
        dataframe2 = dataframe[index + 1]
        shape1_noise = dataframe1['noise'].values.tolist()
        shape2_noise = dataframe2['noise'].values.tolist()
        shape1_frequency = dataframe1['frequency'].values.tolist()
        shape2_frequency = dataframe2['frequency'].values.tolist()
        nframes_shape1 = int(frame_rate * frame_duration)
        nframes_transition = int(frame_rate * overlap)
        nframes_shape2 = int(frame_rate * frame_duration)
        shape1_color = pick_color(shape1_frequency, shape1_noise)
        shape2_color = pick_color(shape2_frequency, shape2_noise)
        if len(shape1) != len(shape2):
            if len(shape1) > len(shape2):
                n_points = len(shape1)
                shape2 = interpolate_points(shape2, n_points)
            else:
                n_points = len(shape2)
                shape1 = interpolate_points(shape1, n_points)

        for i in range(num_frames):
            t = i / num_frames  # Interpolation parameter
            intermediate_shape = [
                ((1 - t) * x1 + t * x2, (1 - t) * y1 + t * y2)
                for (x1, y1), (x2, y2) in zip(shape1, shape2)
            ]
            intermediate_color = (
                shape1_color[0] * (1 - t) + shape2_color[0] * t,
                shape1_color[1] * (1 - t) + shape2_color[1] * t,
                shape1_color[2] * (1 - t) + shape2_color[2] * t
            )
            frames.append((intermediate_shape, intermediate_color))



    # Plot the initial shapes
    #plt.figure(figsize=(8, 4))

    # Define update function for animation
    fig = plt.figure()
    fig.patch.set_facecolor('black')
    plt.axis('off')
    line, = plt.plot([], [], color='red', label='Morphing')
    #print("length of points : ", len(points))
    #print("shape1 = ", shape1)
    x1, y1 = zip(*shape1)
    #print("len shape1: ", len(x1))
    x2, y2 = zip(*shape2)
    #print("len shape2: ", len(x2))
    plt.plot(x1, y1, color=shape1_color, label='Shape 1')
    plt.plot(x2, y2, color=shape2_color, label='Shape 2')
    plt.legend()
    #plt.show()

    # Define update function for animation
    def update(frame):
        shape, color = frame
        line.set_data(np.array(shape)[:, 0], np.array(shape)[:, 1])
        line.set_color(color)
        return line,

    # Animate
    ani = animation.FuncAnimation(plt.gcf(), update, frames=frames, blit=True, interval=1000 / frame_rate, repeat=False)

    #plt.show()
    return ani

def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr)) * diff) / diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr
def interpolate_points(points, num_points):
    if len(points) < 2:
        return points
    x = np.array([point[0] for point in points])
    y = np.array([point[1] for point in points])
    t = np.linspace(0, 1, len(points))
    t_new = np.linspace(0, 1, num_points)
    x_new = np.interp(t_new, t, x)
    y_new = np.interp(t_new, t, y)
    return [(x, y) for x, y in zip(x_new, y_new)]

