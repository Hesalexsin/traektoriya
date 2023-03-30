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


def reduction(mat: np.array):
    summ_min = line_reduction(mat)
    summ_min += column_reduction(mat)
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
def arr_index(mat: np.array, edge_id: list) -> list[int]:
    return [np.where(mat[:, 0] == edge_id[0])[0], np.where(mat[0, :] == edge_id[1])[0]]


# Branching: exclusion and inclusion of an edge
def exclude_edge(plan: Plan, i: int, j: int):
    plan.mat[i, j] = np.inf
    lower_limit = reduction(plan.mat)
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
    avoid_cycle(plan)
    lower_limit = reduction(plan.mat)
    plan.inc_limit(lower_limit)


def include_edge_limit(plan: Plan, i: int, j: int):
    include_edge(plan, i, j)
    return plan.lower_limit


# The function, which helps to avoid infinity cycles in track
def avoid_cycle(plan: Plan):
    for id1 in plan.lst_edges.keys():
        key = plan.lst_edges[id1]
        while key in plan.lst_edges.keys() and plan.lst_edges[key] != id1:
            id2 = plan.lst_edges[key]
            index1 = arr_index(plan.mat, [id2, id1])[0]
            index2 = arr_index(plan.mat, [id2, id1])[1]
            plan.mat[index1, index2] = np.inf
            if not(id2 in plan.lst_edges.keys()):
                break
            key = plan.lst_edges[id2]


# Comparing current and ragged branches to choosing one with min lower limit
# ???????????????????????????????????????????????????????????????????????????
def ragged_branches_compare(ragged_branches: list, current: Plan) -> Plan:
    if len(ragged_branches) > 0:
        min_i = np.argmin(ragged_branches)  # index_min_plan(ragged_branches)
        if ragged_branches[min_i] < current:
            ragged_branches[min_i], current = current, ragged_branches[min_i]
    return current


# The functions, which find the remaining edges in matrix 2x2
def neighbour(i: int):
    if i == 1:
        return 2
    if i == 2:
        return 1


def find_remaining_edges(current: Plan) -> Plan:
    for i in [1, 2]:
        for j in [1, 2]:
            if current.mat[i, j] == np.inf:
                current.app(PairPoints(current.mat[i, 0], current.mat[0, neighbour(j)], True))
                current.app(PairPoints(current.mat[neighbour(i), 0], current.mat[0, j], True))
    return current


# The functions, which does the Little's algorythm
def do_new_plan(current: Plan, i: int, j: int, is_include: bool):
    branch = current.__copy__()
    branch.app(PairPoints(branch.mat[i, 0], branch.mat[0, j], is_include))
    if is_include:
        include_edge(branch, i, j)
    else:
        exclude_edge(branch, i, j)

    logging.info('The plan is made')
    return branch


def travel_salesman_problem(dist_matrix: np.array):
    """
    The main function, which realizes the Little's method
    :param dist_matrix: the two-dimensional array (matrix), whose first line and first column consist of IDs of points
                        (the left top is not ID)
                        and whose other part is the matrix of distances
                        between points with ID in appropriate lines and columns;
                        the distances between the same points are infinity;
                        the first point in the first line and the first column (after left top) is the starting point
    :return: the array with the ordered sequence of points of the shortest path from the first to the first point
             through all points
    """
    ragged_branches = []
    id_first = dist_matrix[0, 1]
    limit = reduction(dist_matrix)
    current_plan = Plan(dist_matrix, limit)
    while len(current_plan.mat) > 3:
        edge_index = find_degrees_of_zeros(current_plan.mat)
        i, j = arr_index(current_plan.mat, edge_index)[0][0], arr_index(current_plan.mat, edge_index)[1][0]

        plan_exclude = do_new_plan(current_plan.__copy__(), i, j, is_include=False)
        plan_include = do_new_plan(current_plan, i, j, is_include=True)

        if plan_include <= plan_exclude:
            current_plan, ragged_branch = plan_include, plan_exclude
        else:
            current_plan, ragged_branch = plan_exclude, plan_include

        ragged_branches.append(ragged_branch)
        current_plan = ragged_branches_compare(ragged_branches, current_plan)
        #dist_matrix = current_plan.mat.copy()

    logging.info('The iteration of the main algorithm is finished')

    current_plan = find_remaining_edges(current_plan)
    track = current_plan.do_array_ids(id_first)
    return track
