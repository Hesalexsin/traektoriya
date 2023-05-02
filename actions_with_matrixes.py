from plan_pair import Plan
import numpy as np
from math import isinf, isnan


# These functions find minimal values in lines/columns and subtract them from the lines/columns (primary transformation)
def line_reduction(mat: np.array):
    summ_min = mat[1:, 1:].min(axis=1).sum()
    if isnan(summ_min) or isinf(summ_min):
        return np.inf
    mat[1:, 1:] -= mat[1:, 1:].min(axis=1)[:, np.newaxis]
    return summ_min


def column_reduction(mat: np.array):
    summ_min = mat[1:, 1:].min(axis=0).sum()
    if isnan(summ_min) or isinf(summ_min):
        return np.inf
    mat[1:, 1:] -= mat[1:, 1:].min(axis=0)
    return summ_min


def reduction(mat: np.array):
    summ_min = line_reduction(mat)
    summ_min += column_reduction(mat)
    return summ_min


# Additional(secondary) matrix transformation
def line_transformation(plan: Plan):
    counts_zeros_in_lines = np.sum(plan.mat[1:, 1:] == 0, axis=1)
    indexes = [idx + 1 for idx, cnt in enumerate(counts_zeros_in_lines) if cnt == 1]
    numbers_columns = [list(line).index(0) for line in plan.mat[indexes]]
    for column in set(numbers_columns):
        group_idx = [idx for idx, col in zip(indexes, numbers_columns) if col == column]
        if len(group_idx) > 1:
            min_elem = np.concatenate((plan.mat[group_idx, 1:column], plan.mat[group_idx, column + 1:]), axis=1).min()
            if isnan(min_elem) or isinf(min_elem):
                plan.inc_limit(np.inf)
                break
            plan.mat[group_idx, 1:] -= min_elem
            plan.mat[1:, column] += min_elem
            plan.inc_limit(min_elem * (len(group_idx) - 1))


def column_transformation(plan: Plan):
    counts_zeros_in_columns = np.sum(plan.mat[1:, 1:] == 0, axis=0)
    indexes = [idx + 1 for idx, cnt in enumerate(counts_zeros_in_columns) if cnt == 1]
    numbers_lines = [list(column).index(0) for column in plan.mat.transpose()[indexes]]
    for line in set(numbers_lines):
        group_idx = [idx for idx, lin in zip(indexes, numbers_lines) if lin == line]
        if len(group_idx) > 1:
            min_elem = np.concatenate((plan.mat[1:line, group_idx], plan.mat[line + 1:, group_idx]), axis=0).min()
            plan.mat[1:, group_idx] -= min_elem
            plan.mat[line, 1:] += min_elem
            plan.inc_limit(min_elem * (len(group_idx) - 1))


def secondary_transformation(plan: Plan):
    line_transformation(plan)
    column_transformation(plan)


# General matrix transformation:
def matrix_transformation(plan: Plan):
    lower_limit = reduction(plan.mat)
    plan.inc_limit(lower_limit)
    secondary_transformation(plan)


# Finding of the biggest degrees of zeros and choosing of the edge
def degree_of_the_one_zero(mat: np.array, i: int, j: int):
    return (np.concatenate((mat[1:i, j], mat[i + 1:, j])).min() +
            np.concatenate((mat[i, j + 1:], mat[i, 1:j])).min())


def find_degrees_of_zeros(mat: np.array):  # ??????????????????????????
    """
    :param mat: REDUCED matrix
    :return: array of 2 INDEXES of zero with the biggest degrees
    """
    res, i, j = -1, 0, 0
    index1, index2 = np.where(mat == 0)
    for k in range(1, len(index1)):
        curr = degree_of_the_one_zero(mat, index1[k], index2[k])
        if curr > res:
            res, i, j = curr, index1[k], index2[k]
    return [mat[i, 0], mat[0, j]]


# Set accordance between indexes og matrix and id
def arr_index(mat: np.array, edge_id: list):
    index1, index2 = np.where(mat[:, 0] == edge_id[0])[0], np.where(mat[0, :] == edge_id[1])[0]
    return index1, index2
