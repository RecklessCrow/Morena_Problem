import itertools
import re
import os
import numpy as np

NONPERIODIC = os.path.join('data', 'binary_sequence_nonperiodic.txt')
PERIODIC = os.path.join('data', 'binary_sequence_nonperiodic_to_periodic.txt')
signal = np.genfromtxt(PERIODIC, delimiter='\n').astype(int)
T = ''.join(signal.astype(str))
del signal


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


def check_periodicity(idxs, string, pat_len=None):
    """
    Final check to see if the pattern is Truly Periodic
    :param string:
    :param idxs:
    :param pat_len:
    :return:
    """
    if len(idxs) < 3:
        return False

    if pat_len is None:
        pat_len = idxs[1] - idxs[0]

    pattern_distances = [idxs[i + 1] - idxs[i] for i in range(len(idxs) - 1)]
    pattern = string[idxs[0]:idxs[1]]
    pattern_strings = [string[idxs[i]:idxs[i + 1]] for i in range(len(idxs) - 1)]
    last_section = string[idxs[-1]:len(string)]
    return all(pat_len == distance for distance in pattern_distances) \
           and all(pat == pattern for pat in pattern_strings) \
           and pattern[:len(last_section)] == last_section \
           and len(string) <= idxs[-1] + pat_len


def find_pattern(string, limit, suffix='', tested=None):
    """
    Finds the pattern with
    :param string:
    :param limit:
    :param suffix:
    :param tested:
    :return:
    """
    if tested is None:
        tested = []

    pat_list = []

    for pat in map("".join, itertools.product('01', repeat=limit)):
        pat += suffix
        idxs = find_indexes(pat, string)
        if idxs is not None and pat not in tested:
            pat_list.append((pat, idxs[0]))

    try:
        return min(pat_list, key=lambda t: t[1])[0]
    except ValueError:
        return None


def main():

    # Todo: index is off by three, find fix

    from time import time

    start = time()
    tried = []
    i = 1
    search_limit = 10

    start_idx = len(T)
    idxs = []

    while not check_periodicity(idxs, T) and i < search_limit:
        pat = find_pattern(T, i)
        while pat is None and i < search_limit:
            i += 1
            pat = find_pattern(T, i)

        root_pat = pat
        old_pat = pat

        while pat is not None and find_indexes(pat, T)[0] < start_idx:
            start_idx = find_indexes(pat, T)[0]
            old_pat = pat
            pat = find_pattern(string=T, limit=1, suffix=pat, tested=tried)
            if pat is None:
                tried.append(root_pat)
                pat = find_pattern(T, i, tested=tried)
                root_pat = pat
                start_idx = len(T)

        idxs = find_indexes(old_pat, T)
        pat = T[idxs[0]:idxs[1]]
        i += 1

    if i < search_limit:
        print(f'Pattern = {pat}\n'
              f'Indexes = {idxs}\n'
              f'{time() - start:.2}s')
    else:
        print('Non-periodic')


if __name__ == '__main__':
    main()
