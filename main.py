import itertools
import os
from itertools import groupby
from multiprocessing import Pool, cpu_count

import numpy as np

NONPERIODIC = os.path.join('data', 'binary_sequence_nonperiodic.txt')
PERIODIC = os.path.join('data', 'binary_sequence_nonperiodic_to_periodic.txt')

threads = cpu_count()

signal = np.genfromtxt(PERIODIC, delimiter='\n').astype(int)
T = ''.join(signal.astype(str))
limit = 8


def check_periodicity(idx_list):
    def all_equal(iterable):
        """
        from https://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical
        :param iterable:
        :return:
        """
        g = groupby(iterable)
        return next(g, True) and not next(g, False)

    new_idx_list = idx_list
    while len(new_idx_list) > 2:
        pattern_distances = [new_idx_list[i + 1] - new_idx_list[i] for i in range(len(new_idx_list) - 1)]

        if all_equal(pattern_distances):
            return True, new_idx_list

        new_idx_list = new_idx_list[1:]

    return False, idx_list


# Python program for KMP Algorithm:
# from https://www.geeksforgeeks.org/python-program-for-kmp-algorithm-for-pattern-searching-2/
def kmp_search(pat, txt=T):
    # create lps[] that will hold the longest prefix suffix
    # values for pattern
    lps = [0] * len(pat)
    j = 0  # index for pat[]

    # Preprocess the pattern (calculate lps[] array)
    compute_lps_array(pat, lps)

    indexes = []
    i = 0  # index for txt[]
    while i < len(txt):
        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == len(pat):
            idx = i - j
            if len(indexes) == 0:
                indexes.append(idx)
            elif idx - indexes[-1] > len(pat):
                indexes.append(idx)
            j = lps[j - 1]

            # mismatch after j matches
        elif i < len(txt) and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return indexes


def compute_lps_array(pat, lps):
    longest_length = 0  # length of the previous longest prefix suffix
    i = 1

    # the loop calculates lps[i] for i = 1 to M-1
    while i < len(pat):
        if pat[i] == pat[longest_length]:
            longest_length += 1
            lps[i] = longest_length
            i += 1
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar
            # to search step.
            if longest_length != 0:
                longest_length = lps[longest_length - 1]

                # Also, note that we do not increment i here
            else:
                lps[i] = 0
                i += 1


def main():
    with Pool(threads // 2) as p:
        patterns = [p.map(''.join, itertools.product('01', repeat=i), chunksize=250) for i in range(1, limit + 1)]

        def temp(patterns, start_index=len(T)):
            idx_lists = []
            period_idxs = []
            for pat in patterns:
                idx_lists.append([idx_list
                                  for idx_list
                                  in p.map(kmp_search, pat, chunksize=250)])
                period_idxs.append([(pat, idx_list)
                                    for pat, (periodic, idx_list)
                                    in zip(pat, p.map(check_periodicity, idx_lists[-1], chunksize=250))
                                    if idx_list and periodic])

            for i in range(len(period_idxs) - 1, -1, -1):

                if not period_idxs[i]:
                    continue

                min_idx = float('inf')
                sample = None
                for j in range(len(period_idxs[i])):
                    # print(period_idxs[i][j])
                    if min(period_idxs[i][j][1]) < min_idx and min(period_idxs[i][j][1]) < start_index:
                        sample = period_idxs[i][j]
                return sample[0], min(sample[1])

        substring, start_index = temp(patterns)
        pattern = ''
        while substring != pattern:
            pattern = substring
            print(f'Current pattern:    {pattern}\n'
                  f'Starting index:     {start_index}')
            new_patterns = [[bit_string + pattern] for p in patterns for bit_string in p]
            try:
                s, start_index = temp(new_patterns, start_index)
                substring = s
            except TypeError:
                break

        period_idxs = kmp_search(pattern)
        period_idxs = check_periodicity(period_idxs)[1]

        pattern = T[period_idxs[0]: period_idxs[1]]

        print(f'\n'
              f'Pattern:    {pattern}\n'
              f'Indexes:    {period_idxs}')


if __name__ == '__main__':
    main()
