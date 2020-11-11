import numpy as np
from numpy import fft

signal = np.genfromtxt('stream.csv', delimiter=',')

fourier = fft.rfft(signal)

print(fourier)

n = fourier.size
time_step = 1
freq = fft.rfftfreq(n, time_step)

print(freq, freq.size)
