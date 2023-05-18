import numpy as np
from actions_with_matrixes import matrix_transformation, find_degrees_of_zeros, arr_index
from plan_pair import PairPoints, Plan

import logging
import logging.config

# Constructing loggers:
logging.basicConfig(
    filename='algorithm.log',
    level=logging.INFO,
    format='%(levelname)s:%(funcName)s:%(name)s:%(message)s',
    filemode='w'
)


# Branching: exclusion and inclusion of an edge
def exclude_edge(plan: Plan, i: int, j: int):
    plan.mat[i, j] = np.inf
    matrix_transformation(plan)


def include_edge(plan: Plan, i: int, j: int):
    i_index, j_index = arr_index(plan.mat, [plan.mat[0, j], plan.mat[i, 0]])
    plan.mat[i_index, j_index] = np.inf
    plan.mat = np.delete(plan.mat, i, 0)
    plan.mat = np.delete(plan.mat, j, 1)
    if len(plan.mat) > 2:
        avoid_cycle(plan)
    matrix_transformation(plan)


# The function, which helps to avoid infinity cycles in track
def avoid_cycle(plan: Plan):
    for id1 in plan.lst_edges.keys():
        key = plan.lst_edges[id1]
        while key in plan.lst_edges.keys() and plan.lst_edges[key] != id1:
            id2 = plan.lst_edges[key]
            index1, index2 = arr_index(plan.mat, [id2, id1])
            plan.mat[index1, index2] = np.inf
            if not (id2 in plan.lst_edges.keys()):
                break
            key = plan.lst_edges[id2]


# Comparing current and ragged branches to choosing one with min lower limit
def ragged_branches_compare(ragged_branches: list, current: Plan) -> Plan:
    if len(ragged_branches) > 0:
        min_i = np.argmin(ragged_branches)
        if ragged_branches[min_i] < current and ragged_branches[min_i].lower_limit is not np.nan:
            ragged_branches[min_i], current = current, ragged_branches[min_i]
    return current


# The functions, which does the Little's algorythm
def do_new_plan(current: Plan, i: int, j: int, is_include: bool):
    branch = current.__copy__()
    branch.app(PairPoints(branch.mat[i, 0], branch.mat[0, j], is_include))
    include_edge(branch, i, j) if is_include else exclude_edge(branch, i, j)
    logging.info('The plan is made')
    return branch


def travel_salesman_problem(dist_matrix: np.array, id_airport: int):
    """
    The main function, which realizes the Little's method
    :param dist_matrix: the two-dimensional array (matrix), whose first line and first column consist of IDs of points
                        (the left top is not ID), other part - matrix of distances;
                        the distances between the same points are infinity;
    :param id_airport: the ORIGIN ID of the first point/base airport
    :return: the array with the ordered sequence of points of the shortest path from the first to the first point
             through all points
    """
    ragged_branches = []
    current_plan = Plan(dist_matrix, 0)
    matrix_transformation(current_plan)
    while len(current_plan.mat) > 2:
        edge_index = find_degrees_of_zeros(current_plan.mat)
        i, j = arr_index(current_plan.mat, edge_index)[0][0], arr_index(current_plan.mat, edge_index)[1][0]

        plan_exclude = do_new_plan(current_plan, i, j, is_include=False)  # it can NOT copy matrix
        plan_include = do_new_plan(current_plan, i, j, is_include=True)
        if plan_include <= plan_exclude:
            current_plan, ragged_branch = plan_include, plan_exclude
        else:
            current_plan, ragged_branch = plan_exclude, plan_include

        logging.debug("chosen edge: " + str(edge_index))
        logging.debug("\ncurrent_plan matrix: \n" + str( current_plan.mat))
        logging.debug("\nragged_branch matrix: \n" + str(ragged_branch.mat))

        ragged_branches.append(ragged_branch)
        current_plan = ragged_branches_compare(ragged_branches, current_plan)

        logging.debug("\nnew current_plan matrix: \n" + str(current_plan.mat))
        logging.info('The iteration of the main algorithm is finished')

    current_plan.app(PairPoints(current_plan.mat[1, 0], current_plan.mat[0, 1], True))
    return current_plan.do_array_ids(id_airport)
