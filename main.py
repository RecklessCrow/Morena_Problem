import math

import numpy as np
from suffix_trees import STree
from stream_sim import *


# Questions to ask
# * Is the pattern constant or a random pattern for each stream
# * Are we looking for perfect periodicity
# * How to detect when periodicity starts and chaos ends
# matthew.morena@cnu.edu


# make_stream()


def principal_period(s):
    i = (s+s).find(s, 1, -1)
    return None if i == -1 else s[:i]


def perfect_periodicity(period, start_pos, n):
    return math.floor((n - start_pos + 1) / period)


def main():
    period_list = []

    for occur_vec in vectors:
        k = len(occur_vec)
        for j in range(n // 2):
            # todo get pattern from vec
            pattern = "0110"
            period = occur_vec[j + 1] - occur_vec[j]  # candidate period
            start_pos = occur_vec[j]
            end_pos = occur_vec[k]

            count_p = 0
            for i in range(j, k):
                if start_pos % period == occur_vec[i] % period:
                    count_p += 1

            confidence = count_p / perfect_periodicity(period, start_pos)
            
            if confidence > THRESHOLD:
                period_list.append(period)

    print(period_list)


if __name__ == '__main__':
    signal = np.genfromtxt(FILE_NAME, delimiter=',')
    signal = signal.astype(int)

    n = len(signal)

    T = ''.join(signal.astype(str))

    del signal

    pattern = '0110'  # haha jeep

    print(principal_period(T))

    st = STree.STree(T)
    periods = list(st.find_all(pattern))
    periods.sort()
    # print(periods)

    # todo make occurrence vectors

    vectors = []
    THRESHOLD = 0.5
    pass
