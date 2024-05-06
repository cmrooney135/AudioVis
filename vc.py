import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from pytweening import easeOutQuad
from pydub import AudioSegment
import colorsys
import pygame
from IPython import display



from pytweening import easeOutQuad
from threading import Timer

def animate(points, dataframes, overlap_duration):
    animations = []
    #print("Points(0): ", points[0])
    #print("data (0)", dataframes[0])
    for i in range(len(points) - 1):
        frames, shape1, shape1_color, shape2, shape2_color, duration = animate_pair(points[i:i+2], dataframes[i:i+2], overlap_duration)
        animations.append((frames, shape1, shape1_color, shape2, shape2_color, duration))
    #print("len animations: ", len(animations))
    return animations
def animate_pair(points_pair, dataframes_pair, duration):
    def pick_color(frequency, noise):
        freq_normal = normalize(frequency, 0.1, 1)
        R = freq_normal[0]
        G = freq_normal[1]
        B = freq_normal[2]
        color1 = colorsys.rgb_to_hsv(R, G, B)
        hue = color1[0]
        noise = np.mean(noise)
        saturation = 1 - noise
        if saturation < 0.25:
            saturation = 0.25
        value = 0.99999
        color_rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        color_rgb = np.array(color_rgb)
        return color_rgb

    num_frames = 7
    frames = []

    for index in range(len(points_pair) - 1):
        shape1 = points_pair[index]
        #print("shape1: ", shape1)
        shape2 = points_pair[index + 1]
        dataframe1 = dataframes_pair[index]
        dataframe2 = dataframes_pair[index + 1]
        shape1_noise = dataframe1['noise'].values.tolist()
        shape2_noise = dataframe2['noise'].values.tolist()
        shape1_time = dataframe1['time'].values[0]
        shape2_time = dataframe2['time'].values[0]
        shape1_frequency = dataframe1['frequency'].values.tolist()
        shape2_frequency = dataframe2['frequency'].values.tolist()
        shape1_color = pick_color(shape1_frequency, shape1_noise)
        shape2_color = pick_color(shape2_frequency, shape2_noise)
        if len(shape1) != len(shape2):
            if np.abs(len(shape1) - len(shape2)) > 0:
                if len(shape1) > len(shape2):
                    n_points = len(shape1)
                    shape2 = interpolate_points(shape2, n_points)
                elif len(shape2) > len(shape1):
                    n_points = len(shape2)
                    shape1 = interpolate_points(shape1, n_points)
            # else:
            #     shape2 = [(0.5 * x, 0.5 * y) for x, y in shape1]

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

    return frames, shape1, shape1_color, shape2, shape2_color, duration

def animate2(animations, filename, overlap_duration, audio_duration):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    plt.figure(figsize=(10, 8))

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')
    ax.set_axis_off()
    ax.set_facecolor('black')

    num_shapes_drawn = 0
    def update(frame):
        shape, color = frame
        ax.clear()
        ax.plot(np.array(shape)[:, 0], np.array(shape)[:, 1], color=color)
        return ax,

    plt.pause(10)  # Wait for 2 seconds before starting animation

    for frames, shape1, shape1_color, shape2, shape2_color, overlap_duration in animations:
        print("Entered animation for loop")
        num_frames = 4
        audio = audio_duration
        print("overlap duration: ", overlap_duration)
        overlap = overlap_duration
        static = overlap_duration * 0.25
        interval = overlap / num_frames
        #x1, y1 = zip(*shape1)
        #ax.plot(x1, y1, color=shape1_color, label='Shape 1')
        num_shapes_drawn += 1
        #plt.pause(static)
        ax.clear()
        # delay between frames is interval  not the total amount of time it will take
        ani = animation.FuncAnimation(fig, update, frames=frames, blit=True, interval=interval, repeat=False)

        # Wait for animation to finish
        animation_finished = False
        while not animation_finished:
            if not plt.fignum_exists(fig.number):  # Check if figure is closed
                break
            animation_finished = ani.event_source is None or ani.event_source.callbacks is None or len(ani.event_source.callbacks) == 0
            plt.pause(0.1)

        # Clear the figure for the next animation
        plt.clf()
    # Save the animation as an MP4 with background music
    writervideo = animation.FFMpegWriter(fps=60)
    ani.save('output.mp4', writer=writervideo)
    plt.close()
    plt.close()
    pygame.mixer.music.stop()
    print("Number of shapes drawn:", num_shapes_drawn)


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