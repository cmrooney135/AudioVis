# AudioVis

The widespread availability of digital music has revolutionized the way we access, consume, and appreciate sound. Platforms like Spotify, Apple Music, and YouTube provide access to an
extensive and diverse range of music, offering listeners the opportunity to discover new artists, genres, and styles of music. This project, an audio visualizer based on the mathematical 
representation of audio signals, aims to enhance the listening experience by synchronizing music with dynamic visual effects based on the real composition of the sound.

To generate a dynamic and colorful representation of the audio, the visualizer analyzes an input
audio file and extracts frequency and magnitude data using a Short-time discrete Fourier Transform. 
It then uses the data to specify the color, shape, and width of the visualizer drawing. 
We chose this project because of our interest in music and its interesting connections to digital signal processing.
Additionally, the project allows for substantial creative freedom in the design process; audio visualization is a popular area in signal processing, 
so there are many references and libraries available for Python and therefore many opportunities to tune different aspects of the visualizer after processing the signal.

In this project we will deconstruct STFT samples from an audio file and use the top 4 dominant frequencies to create a fourier circle drawing, as a collection of points. 
Once the collection of shapes is created it will display alongside the music with a morphing animation between shapes. 
The morphing will use linear interpolation for movement of the shape, and the color. 


The animation will NOT play in real time with the audio, but when the output is sped up (for us, using imovie), 
the samples will sync. 

There are many things you can edit to affect the visualizer, try changing the n_fft, hop_size, sample_rate in STFT, 
or mess around with the colors. 
The result is below, FLASH WARNING of a song! 

<p align="center">
  <img width="460" height="300" src="[https://picsum.photos/460/300](https://github.com/cmrooney135/AudioVis/blob/main/audioVisualizer%20.gif)">
</p>

