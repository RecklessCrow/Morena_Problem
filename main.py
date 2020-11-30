import itertools
import os

import numpy as np
from suffix_trees import STree



# Questions to ask
# * Is the pattern constant or a random pattern for each stream
# * Are we looking for perfect periodicity
# * How to detect when periodicity starts and chaos ends
# matthew.morena@cnu.edu

NONPERIODIC = os.path.join('data', 'binary_sequence_nonperiodic.txt')
PERIODIC = os.path.join('data', 'binary_sequence_nonperiodic_to_periodic.txt')


def perfect_periodicity(positions):

    for i in range(len(positions) - 3):
        #  todo: check if the positions of the pattern are periodic and in what range
        pass


def main():
    signal = np.genfromtxt(PERIODIC, delimiter='\n').astype(int)
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

            if len(periods) > 1:
                period_str = f'Pattern:             {pattern}\n' \
                             f'Number patterns:     {len(periods)}\n'
                # f'Period Start:        {}\n' \
                # f'Period End:          {}\n' \
                # f'Period Increment:    {}\n' \
                # f'Period:              {len(pattern)}\n' \
                print(period_str)


if __name__ == '__main__':
    main()
