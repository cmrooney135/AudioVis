import numpy as np
from pytweening import easeOutQuad
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from pydub import AudioSegment


import colorsys
def animate(points, dataframes, overlap_time, frame_duration):
    animations = []
    for i in range(len(points) - 1):
        frames, shape1, shape1_color, shape2, shape2_color, time_difference = animate_pair(points[i:i+2], dataframes[i:i+2], overlap_time, frame_duration)
        animations.append((frames, shape1, shape1_color, shape2, shape2_color, time_difference))
    return animations

def animate_pair(points_pair, dataframes_pair, overlap, frame_duration):
    def pick_color(frequency, noise):
        freq_normal = normalize(frequency, 0.1, 1)
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
        return color_rgb

    num_frames = 7
    frame_rate = int(np.ceil(num_frames / overlap))

    frames = []
    colors = []
    for index in range(len(points_pair) - 1):
        shape1 = points_pair[index]
        shape2 = points_pair[index + 1]
        dataframe1 = dataframes_pair[index]
        dataframe2 = dataframes_pair[index + 1]
        shape1_noise = dataframe1['noise'].values.tolist()
        shape2_noise = dataframe2['noise'].values.tolist()
        shape1_time = dataframe1['time'].values.tolist()
        shape2_time = dataframe2['time'].values.tolist()
        time_difference = shape2_time[0]-shape1_time[0]
        shape1_frequency = dataframe1['frequency'].values.tolist()
        shape2_frequency = dataframe2['frequency'].values.tolist()
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
            t = easeOutQuad(i / num_frames)
            intermediate_shape = [
                (shape1_point[0] * (1 - t) + shape2_point[0] * t,
                 shape1_point[1] * (1 - t) + shape2_point[1] * t)
                for shape1_point, shape2_point in zip(shape1, shape2)
            ]
            intermediate_color = (
                shape1_color[0] * (1 - t) + shape2_color[0] * t,
                shape1_color[1] * (1 - t) + shape2_color[1] * t,
                shape1_color[2] * (1 - t) + shape2_color[2] * t
            )

            frames.append((intermediate_shape, intermediate_color))

    return frames, shape1, shape1_color, shape2, shape2_color, time_difference

    # Plot the initial shapes
    plt.figure(figsize=(8, 4))

    # Define update function for animation
    fig = plt.figure()
    fig.patch.set_facecolor('black')
    plt.axis('off')
    line, = plt.plot([], [], color='red', label='Morphing')
    x1, y1 = zip(*shape1)
    print("len shape1: ", len(x1))
    x2, y2 = zip(*shape2)
    plt.plot(x1, y1, color=shape1_color, label='Shape 1')
    plt.pause(frame_duration)
    plt.clf()
    animate2(frames, shape1, shape1_color, shape2, shape2_color, time_difference)
    plt.clf()
    # plt.plot(x2, y2, color=shape2_color, label='Shape 2')
    # plt.pause(frame_duration)
    plt.clf()

    #plt.show()

    # Define update function for animation


def animate2(animations, filename):
    background_music = AudioSegment.from_wav(filename)
    background_music.export('Fuzz.mp3', format='mp3')
    print("export as mp3 successful")

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')
    ax.set_axis_off()
    ax.set_facecolor('black')

    def update(frame):
        shape, color = frame
        ax.clear()
        ax.plot(np.array(shape)[:, 0], np.array(shape)[:, 1], color=color)
        return ax,

    for frames, frame_rate, overlap, shape1, shape1_color, shape2, shape2_color, frame_duration, time_difference in animations:
        print("entered animation for loop ")
        x1, y1 = zip(*shape1)
        ax.plot(x1, y1, color=shape1_color, label='Shape 1')
        plt.pause(frame_duration*1000)
        ax.clear()

        interval = time_difference * 1000
        print("interval : ", interval)
        ani = animation.FuncAnimation(fig, update, frames=frames, blit=True, interval=interval, repeat=False)

        animation_finished = False
        while not animation_finished:
            if not plt.fignum_exists(fig.number):  # Check if figure is closed
                break
            animation_finished = ani.event_source is None or ani.event_source.callbacks is None or len(ani.event_source.callbacks) == 0
            plt.pause(0.01)

        plt.clf()

    plt.close()

    ani.save('animation_recording.mp4', writer='ffmpeg', fps=30)


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

