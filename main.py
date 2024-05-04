# DSP Final Project
# Emily Ninestein, Carol Rooney, Alec Benedict
import STFT
import draw_circles
import animation_attempt

filename = 'lib/fuzz.wav'

# How many frames to animate -- we can get rid of this once it's fast enough
num_shapes = 4

# Calculate the STFTs of the audio file, return dataframes
dataframes = STFT.STFT(filename)

# Pass dataframes to draw circles, return coordinate points of drawings
circles = draw_circles.DrawCircles(dataframes[0:num_shapes])
drawing_coords = circles.drawings

# Pass drawing coords and dataframes to animation function
animation_attempt.animate(dataframes[0:num_shapes], drawing_coords)