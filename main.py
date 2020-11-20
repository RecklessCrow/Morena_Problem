import numpy as np
from suffix_trees import STree
from stream_sim import *

make_stream()

signal = np.genfromtxt(FILE_NAME, delimiter=',')
n = len(signal)

signal_string = ''.join(signal.astype(str))
del signal

st = STree.STree(signal_string)
del signal_string

vectors = []


def perfect_periodicity(period, start_pos, pattern):
    # count number of pattern occurrences in T from start given period
    return 1


def main():
    period_list = []

    for occur_vec in vectors:
        k = len(occur_vec)
        for j in range(n // 2):
            period = occur_vec[j + 1] - occur_vec[j]  # candidate period
            start_pos = occur_vec[j]
            end_pos = occur_vec[k]

            count_p = 0
            for i in range(j, k):
                if start_pos % period == occur_vec[i] % period:
                    count_p += 1

            confidence = count_p / perfect_periodicity(period, start_pos, pattern)


if __name__ == '__main__':
    main()
