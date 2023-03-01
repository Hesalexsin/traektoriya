import numpy as np
from plan_pair import PairPoints, Plan, index_min_plan, is_less


# These functions find minimal values in lines/columns and subtract them from the lines/columns
def line_reduction(mat: np.array):
    summ_min = mat[1:, 1:].min(axis=1).sum()
    mat[1:, 1:] = mat[1:, 1:] - mat[1:, 1:].min(axis=1)[:, np.newaxis]
    return summ_min


def column_reduction(mat: np.array):
    summ_min = mat[1:, 1:].min(axis=0).sum()
    mat[1:, 1:] = mat[1:, 1:] - mat[1:, 1:].min(axis=0)
    return summ_min


# Finding of the biggest degrees of zeros and choosing of the edge
def degree_of_the_one_zero(mat: np.array, i: int, j: int):
    return (np.concatenate((mat[1:i, j], mat[i + 1:, j])).min() +
            np.concatenate((mat[i, j + 1:], mat[i, 1:j])).min())


def find_degrees_of_zeros(mat: np.array):
    res, i, j = -1, 0, 0
    index1, index2 = np.where(mat == 0)[0], np.where(mat == 0)[1]
    for k in range(1, len(index1)):
        curr = degree_of_the_one_zero(mat, index1[k], index2[k])
        if curr > res:
            res, i, j = curr, index1[k], index2[k]
    return [mat[i, 0], mat[0, j]]


# Set accordance between indexes og matrix and id
def arr_index(mat: np.array, edge_id: list):
    return [np.where(mat[:, 0] == edge_id[0])[0], np.where(mat[0, :] == edge_id[1])[0]]


# Branching: exclusion and inclusion of an edge
def exclude_edge(mat: np.array, i: int, j: int):
    mat[i, j] = np.inf
    return mat


def exclude_edge_limit(mat: np.array, i: int, j: int):
    mat = exclude_edge(mat, i, j)
    lower_limit = line_reduction(mat)
    lower_limit += column_reduction(mat)
    return lower_limit


def include_edge(mat: np.array, i: int, j: int):
    i_index = arr_index(mat, [mat[0, j], mat[i, 0]])[0]
    j_index = arr_index(mat, [mat[0, j], mat[i, 0]])[1]
    mat[i_index, j_index] = np.inf
    mat = np.delete(mat, i, 0)
    mat = np.delete(mat, j, 1)
    return mat


def include_edge_limit(mat: np.array, i: int, j: int):
    mat = include_edge(mat, i, j)
    lower_limit = line_reduction(mat)
    lower_limit += column_reduction(mat)
    return lower_limit


'''
def choose_branching(mat: np.array, inc_lim: int, exc_lim: int, index1: int, index2: int):
    if inc_lim < exc_lim:
        mat = include_edge(mat, index1, index2)
    else:
        mat = exclude_edge(mat, index1, index2)
    return mat'''


# Comparing current and ragged branches to choosing one with min lower limit
# ???????????????????????????????????????????????????????????????????????????
def ragged_branches_compare(ragged_branches: list, current: Plan) -> Plan:
    if len(ragged_branches) > 0:
        min_i = index_min_plan(ragged_branches)
        if is_less(ragged_branches[min_i], current):
            ragged_branches[min_i], current = current, ragged_branches[min_i]
    return current


# The function, which find the remaining edges in matrix 2x2
def find_remaining_edges(mat: np.array, current: Plan) -> Plan:
    for i in [1, 2]:
        for j in [1, 2]:
            if i != j and mat[i, j] != np.inf:
                current.app(PairPoints(mat[i, 0], mat[0, j], True))
    return current


# The function which makes array of id from array of PairPonts
def do_array_id(lst_edges: list, id1: int):
    id_first = id1
    result = [int(id1)]
    while len(lst_edges) > 0:
        for i in range(len(lst_edges)):
            if id1 == lst_edges[i].id_1():
                result.append(int(lst_edges[i].id_2()))
                id1 = lst_edges[i].id_2()
                lst_edges.pop(i)
                break
    return result


# The function, which does the Little's algorythm
def travel_salesmans_task(dist_matrix: np.array):
    ragged_branches = []
    line_lim = line_reduction(dist_matrix)
    col_lim = column_reduction(dist_matrix)
    current_plan = Plan(dist_matrix, line_lim + col_lim, [], [])
    id_first = dist_matrix[1, 0]
    while len(dist_matrix) > 3:
        edge_index = find_degrees_of_zeros(dist_matrix)
        i, j = arr_index(dist_matrix, edge_index)[0][0], arr_index(dist_matrix, edge_index)[1][0]
        exc_lim = exclude_edge_limit(dist_matrix.copy(), i, j)
        inc_lim = include_edge_limit(dist_matrix.copy(), i, j)
        '''print(exclude_edge(dist_matrix.copy(), i, j))
        print(include_edge(dist_matrix.copy(), i, j))
        print(edge_index)'''

        ragged_branch = Plan(dist_matrix.copy(), current_plan.lower_limit,
                             current_plan.lst_edges, current_plan.lst_not_edges)
        ragged_branch.app(PairPoints(dist_matrix[i, 0], dist_matrix[0, j], inc_lim >= exc_lim))
        ragged_branch.inc_limit(max(inc_lim, exc_lim))

        current_plan.app(PairPoints(dist_matrix[i, 0], dist_matrix[0, j], inc_lim < exc_lim))
        current_plan.inc_limit(min(inc_lim, exc_lim))

        if inc_lim < exc_lim:
            ragged_branch.mat = exclude_edge(dist_matrix.copy(), i, j)
            current_plan.mat = include_edge(dist_matrix, i, j)
        else:
            ragged_branch.mat = include_edge(dist_matrix.copy(), i, j)
            current_plan.mat = exclude_edge(dist_matrix, i, j)
        ragged_branches.append(ragged_branch)
        current_plan = ragged_branches_compare(ragged_branches, current_plan)
        dist_matrix = current_plan.matrix().copy()

        line_reduction(dist_matrix)
        column_reduction(dist_matrix)

    current_plan = find_remaining_edges(dist_matrix, current_plan)
    return do_array_id(current_plan.edges(), id_first)
