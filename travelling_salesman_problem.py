import numpy as np
from plan_pair import PairPoints, Plan

import logging
import logging.config

# Constructing loggers:
'''logging.config.fileConfig('logconfig_algorithm.ini')'''

logging.basicConfig(
    filename='algorithm.log',
    level=logging.INFO,
    format='%(levelname)s:%(funcName)s:%(name)s:%(message)s'
)


# These functions find minimal values in lines/columns and subtract them from the lines/columns
def line_reduction(mat: np.array):
    summ_min = mat[1:, 1:].min(axis=1).sum()
    mat[1:, 1:] -= mat[1:, 1:].min(axis=1)[:, np.newaxis]
    return summ_min


def column_reduction(mat: np.array):
    summ_min = mat[1:, 1:].min(axis=0).sum()
    mat[1:, 1:] -= mat[1:, 1:].min(axis=0)
    return summ_min


'''def line_reduction(plan: Plan):
    summ_min = plan.mat[1:, 1:].min(axis=1).sum()
    plan.mat[1:, 1:] -= plan.mat[1:, 1:].min(axis=1)[:, np.newaxis]
    plan.inc_limit(summ_min)


def column_reduction(plan: Plan):
    summ_min = plan.mat[1:, 1:].min(axis=0).sum()
    plan.mat[1:, 1:] -= plan.mat[1:, 1:].min(axis=0)
    plan.inc_limit(summ_min)'''


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
def arr_index(mat: np.array, edge_id: list) -> list[int]:
    return [np.where(mat[:, 0] == edge_id[0])[0], np.where(mat[0, :] == edge_id[1])[0]]


# Branching: exclusion and inclusion of an edge
def exclude_edge(plan: Plan, i: int, j: int):
    plan.mat[i, j] = np.inf
    lower_limit = line_reduction(plan.mat)
    lower_limit += column_reduction(plan.mat)
    plan.inc_limit(lower_limit)


def exclude_edge_limit(plan: Plan, i: int, j: int):
    exclude_edge(plan, i, j)
    return plan.lower_limit


def include_edge(plan: Plan, i: int, j: int):
    i_index = arr_index(plan.mat, [plan.mat[0, j], plan.mat[i, 0]])[0]
    j_index = arr_index(plan.mat, [plan.mat[0, j], plan.mat[i, 0]])[1]
    plan.mat[i_index, j_index] = np.inf
    plan.mat = np.delete(plan.mat, i, 0)
    plan.mat = np.delete(plan.mat, j, 1)
    lower_limit = line_reduction(plan.mat)
    lower_limit += column_reduction(plan.mat)
    plan.inc_limit(lower_limit)


def include_edge_limit(plan: Plan, i: int, j: int):
    include_edge(plan, i, j)
    return plan.lower_limit


# The function, which helps to avoid infinity cycles in track
def avoid_cycle(plan: Plan):
    for k in range(len(plan.track) - 1, -1, -1):
        for i in range(k - 2, -1, -1):
            plan.mat[arr_index(plan.mat, [plan.track[k], plan.track[i]])[0],
            arr_index(plan.mat, [plan.track[k], plan.track[i]])[1]] = np.inf


# Comparing current and ragged branches to choosing one with min lower limit
# ???????????????????????????????????????????????????????????????????????????
def ragged_branches_compare(ragged_branches: list, current: Plan) -> Plan:
    if len(ragged_branches) > 0:
        min_i = np.argmin(ragged_branches)  # index_min_plan(ragged_branches)
        if ragged_branches[min_i] < current:
            ragged_branches[min_i], current = current, ragged_branches[min_i]
    return current


# The function, which find the remaining edges in matrix 2x2
# ????????????????????????????????????????????????????????????
def neighbour(i: int):
    if i == 1:
        return 2
    if i == 2:
        return 1


def find_remaining_edges(mat: np.array, current: Plan) -> Plan:
    for i in [1, 2]:
        for j in [1, 2]:
            if mat[i, j] == np.inf:
                current.app(PairPoints(mat[i, 0], mat[0, neighbour(j)], True))
                current.app(PairPoints(mat[neighbour(i), 0], mat[0, j], True))
    return current


# The function, which makes right list of track points
def make_list_points(current: Plan, first_id: int):
    current.do_array_ids()
    current.make_right_order(first_id)


# The functions, which does the Little's algorythm
def do_new_plan(current: Plan, i: int, j: int, is_less_inc: bool):
    branch = current.__copy__()
    branch.app(PairPoints(branch.mat[i, 0], branch.mat[0, j], is_less_inc))
    branch.do_array_ids()
    if is_less_inc:
        include_edge(branch, i, j)
        avoid_cycle(branch)
    else:
        exclude_edge(branch, i, j)
    '''line_reduction(branch.mat)
    column_reduction(branch.mat)'''

    logging.info('The plan is made')
    return branch


def travel_salesman_problem(dist_matrix: np.array):
    ragged_branches = []
    id_first = dist_matrix[0, 1]
    line_lim = line_reduction(dist_matrix)
    col_lim = column_reduction(dist_matrix)
    current_plan = Plan(dist_matrix, line_lim + col_lim)
    while len(dist_matrix) > 3:
        edge_index = find_degrees_of_zeros(dist_matrix)
        i, j = arr_index(dist_matrix, edge_index)[0][0], arr_index(dist_matrix, edge_index)[1][0]
        exc_lim = exclude_edge_limit(current_plan.__copy__(), i, j)
        inc_lim = include_edge_limit(current_plan.__copy__(), i, j)

        ragged_branch = do_new_plan(current_plan.__copy__(), i, j, inc_lim > exc_lim)
        current_plan = do_new_plan(current_plan, i, j, inc_lim <= exc_lim)

        ragged_branches.append(ragged_branch)
        current_plan = ragged_branches_compare(ragged_branches, current_plan)
        dist_matrix = current_plan.mat.copy()

        logging.info('The iteration of the main algorithm is finished')

    current_plan = find_remaining_edges(dist_matrix, current_plan)
    make_list_points(current_plan, id_first)
    return current_plan.track
