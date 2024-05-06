# DSP Final Project
# Emily Ninestein, Carol Rooney, Alec Benedict
import STFT

import draw_circles
from vc import animate
from vc import animate2
import matplotlib.pyplot as plt


filename = 'lib/linear_chirp.wav'

num_shapes = 20


# How many frames to animate -- we can get rid of this once it's fast enough

# Calculate the STFTs of the audio file, return dataframes
shape_data, overlap_duration, frame_duration, audio_duration = STFT.STFT(filename)

#print("shape data:", shape_data)
print("non overlap time : ", frame_duration)
print("shape_data length ", len(shape_data))

time_per_animation = (frame_duration + overlap_duration)
print("time per frame : " , frame_duration)
print("time per overlap : " , overlap_duration)

print("time per animation: ", time_per_animation)

print("number of shapes not clipped = ", len(shape_data[0:num_shapes]))

# Pass dataframes to draw circles, return coordinate points of drawings
circles = draw_circles.DrawCircles(shape_data)
drawing_coords = circles.drawings

# Pass drawing coords and dataframes to animation function
animations = animate(drawing_coords, shape_data, overlap_duration)
animate2(animations, filename, overlap_duration, audio_duration)

