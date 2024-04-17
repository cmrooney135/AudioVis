# DSP Final Project
# Emily Ninestein, Carol Rooney, Alec Benedict

# Because we can decompose signals into component sine waves,
# and convert sine waves into circles, we can convert every component sine wave
# of a signal into circles, and represent the signal as a sum of circles, where the y axis
# is the original signal, and the x axis is the signal with every component sine wave phase shifted
# by 90˚.
#
# This results in a visualization of the signal that is one part real
# and one part imaginary, but also perceptually meaningful:
# -Loud sounds have large shapes, and quiet sounds have small shapes.
#     Near silence is a dot in the middle, and pure silence is a plain black screen.
# -A pure sine wave is just a circle, where the radius corresponds to amplitude.
#     Purer sounds are very round because they’re made of very few sine waves.
# -Brighter sounds end up looking spiky because they have many frequency components and
#     also digital sound has limited resolution/is “pixelated”.
# -Percussive/transient sounds flash on the screen because these signals are very short.
# -Sustained tones create sustained shapes because tones are periodic signals that have
#     repeating parts that have the same shape, and these shapes keep getting traced out over and
#     over again.
# -Multiple tones in perfect harmony also have sustained shapes because perfect harmony means
#     the frequencies are integer ratios of each other. In other words, the combination of these periodic signals is also a periodic signal.
# -Multiple tones in imperfect harmony have shifting/vibrating shapes because something to do
#     with interference and beating and it’s just not periodic so the same shape doesn’t get
#     repeated ok also most music uses imperfect harmony so every time there are multiple tones
#     it’s probably gonna look messy sorry this deserves a dedicated post
#
# Thickness: inversely proportional to speed.
# Hue: instantaneous pitch, derived from angular velocity.
# Saturation: inversely proportional to amount of noise
# The thickness decreases as the beam moves faster.
# This causes high-frequency sounds or loud sounds to appear thinner.
# The color is a lot more complicated. Using the HSV color space:
# -Hue relates to pitch (more technically, pitch class). Pitch is circular,
#     and hue is circular, so this is a natural mapping to make.
# -Saturation corresponds to amount of noise, where:
#         more noise → more white, less noise → purer colors.
# -Value is maxed out because I want only the brightest colors