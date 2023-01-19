# Run this script from the repository's root.
import math
import numpy as np


def replaceMissingValues(x):
    return np.nan_to_num(x)


def countMissingValues(x, k=0):
    dim = x.ndim
    axis = k
    if isinstance(k, int):
        if (k + 1) > dim:
            raise ValueError
        else:
            if (k + dim) < 0:
                raise ValueError
            else:
                if k < 0:
                    axis = (k + dim)
    else:
        raise TypeError
    print(np.sum(np.isnan(x), axis))
    return np.sum(np.isnan(x), axis)


def exams_with_median_gt_K(x, k):
    if k < 0 or k > 100:
        raise ValueError
    val = 0
    n = replaceMissingValues(x)
    for i in n:
        i.sort()
        mid = len(i) // 2
        median = (i[mid] + i[~mid]) / 2
        if median > k:
            val += 1
        for j in i:
            if j < 0 or j > 100:
                raise ValueError
    return val


def curve_low_scoring_exams(x, k):
    if not isinstance(k, int):
        raise TypeError
    if k < 0 or k > 100:
        raise ValueError
    n = replaceMissingValues(x)
    for i in n:
        if np.mean(i) < k:
            highest = np.amax(i)
            curve = (100 - highest)
            for index, j in enumerate(i):
                if j < 0 or j > 100:
                    raise ValueError
                i[index] = round((j + curve), 1)
        else:
            for j in i:
                if j < 0 or j > 100:
                    raise ValueError
    return sorted(n, key=lambda row: sum(row))
