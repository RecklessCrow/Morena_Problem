import itertools
import re
import os
import numpy as np

PERIODIC = os.path.join('data', 'binary_sequence_nonperiodic_to_periodic.txt')
signal = np.genfromtxt(PERIODIC, delimiter='\n').astype(int)
T = ''.join(signal.astype(str))


def find_indexes(pattern, string):
    """
    Returns Periodic indexes of a pattern given a string
    :param pattern:
    :param string:
    :return:
    """
    if pattern == '':
        return None

    idxs = [m.start() for m in re.finditer(pattern, string)]

    while len(idxs) > 2:
        pattern_distances = [idxs[i + 1] - idxs[i] for i in range(len(idxs) - 1)]

        if all(pattern_distances[0] == a_val for a_val in pattern_distances):
            return idxs

        idxs = idxs[1:]

    return None


def check_periodicity(idxs, pat_len=None):
    if pat_len is None:
        pat_len = idxs[1] - idxs[0]

    pattern_distances = [idxs[i + 1] - idxs[i] for i in range(len(idxs) - 1)]
    return all(pat_len == distance for distance in pattern_distances) and len(T) <= idxs[-1] + pat_len


def find_pattern(string, suffix='', tested=None):
    if tested is None:
        tested = []

    limit = 8
    pat_list = []

    for i in range(1, limit):
        for pat in map("".join, itertools.product('01', repeat=i)):
            pat += suffix
            idxs = find_indexes(pat, string)
            if idxs is not None and pat not in tested:
                pat_list.append((pat, idxs[0]))

    return min(pat_list, key=lambda t: t[1])[0]


if __name__ == '__main__':
    pat = find_pattern(T)
    tried = []
    start_idx = len(T)

    while find_indexes(pat, T)[0] < start_idx:
        try:
            start_idx = find_indexes(pat, T)[0]
            old_pat = pat
            pat = find_pattern(string=T, suffix=pat, tested=tried)
        except ValueError:
            pat = find_pattern(T, tested=tried)
            tried.append(pat)
            pat = find_pattern(T, tested=tried)
            start_idx = len(T)

    idxs = find_indexes(old_pat, T)
    pat = T[idxs[0]:idxs[1]]
    periodic = check_periodicity(idxs)
    print(f'Pattern = {pat}\n'
          f'Indexes = {idxs}\n')
