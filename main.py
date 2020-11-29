import itertools

import numpy as np
from suffix_trees import STree
from stream_sim import *


# Questions to ask
# * Is the pattern constant or a random pattern for each stream
# * Are we looking for perfect periodicity
# * How to detect when periodicity starts and chaos ends
# matthew.morena@cnu.edu


def perfect_periodicity(positions):

    for i in range(len(positions) - 3):
        if positions[i + 1] - positions[i] != positions[i + 2] - positions[i + 1]:
            pass


def main():
    signal = np.genfromtxt(FILE_NAME, delimiter=',').astype(int)
    T = ''.join(signal.astype(str))
    n = len(T)
    limit = n // 32
    del signal
    st = STree.STree(T)

    # iterate over all potential patterns of length 3 to the limit
    for i in range(3, limit):
        for pattern in map(''.join, itertools.product('01', repeat=i)):
            periods = list(st.find_all(pattern))
            periods.sort()

            if periods is None:
                continue

            print(perfect_periodicity(periods))

            # if len(periods) > 1:
            #     period_str = f'Pattern:             {pattern}\n' \
            #                  f'Period:              {len(pattern)}\n' \
            #                  f'Period Start:        {1}\n' \
            #                  f'Period Increment:    {1}\n' \
            #                  f'Number patterns:     {len(periods)}\n'
            #     print(period_str)


if __name__ == '__main__':
    main()
