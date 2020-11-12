import numpy as np
from numpy import fft

from stream_sim import *


def main():

    make_stream()

    signal = np.genfromtxt(FILE_NAME, delimiter=',')

    fourier = fft.rfft(signal)

    print(fourier)

    n = fourier.size
    time_step = 1
    freq = fft.rfftfreq(n, time_step)

    print(freq, freq.size)


if __name__ == '__main__':
    main()
