import numpy as np
from travelling_salesman_problem import line_reduction, column_reduction, \
    find_degrees_of_zeros, exclude_edge, include_edge
from travelling_salesman_problem import travel_salesman_problem
from edges import make_array, update_edges_with_fl, update_with_fz
from formating import make_points, make_json_data
from draw_track import draw_track
import logging
import logging.config
import sys

# main function
if __name__ == '__main__':
    logging.config.fileConfig('logconfig.ini')
    logging.getLogger().level = logging.INFO
    filename = 'input.json'
    data = make_json_data(filename)

    try:
        data_points = data['data_points']
    except KeyError:
        logging.error(f"No data or data in invalid format")
        sys.exit(-1)
    try:
        data_forbidden_lines = data['forbidden_lines']
    except KeyError:
        logging.info(f"No forbidden lines")
        data_forbidden_lines = []

    try:
        data_forbidden_zones = data['data_forbidden_zone']
    except KeyError:
        logging.info(f"No forbidden zones")
        data_forbidden_zones = []

    logging.debug(f"Read data: "
                  f" data points "
                  f" {data_points} "
                  f" forbidden_lines "
                  f" {data_forbidden_lines} "
                  f" forbidden_zones "
                  f" {data_forbidden_zones} \n")

    points = make_points(data_points)
    a = make_array(points)
    resp, flag = update_edges_with_fl(a, len(points), points, data_forbidden_lines)
    if flag != 'invalid data':
        a = resp
    else:
        logging.error(f"Invalid data in forbidden lines module")
        sys.exit(-1)
    logging.debug(f"Made array: \n {a} \n")

    resp, flag = update_with_fz(a, len(points), points, data_forbidden_zones)
    if flag != 'invalid data':
        a = resp
    else:
        logging.error(f"Invalid data in forbidden zone module")
        sys.exit(-1)
    logging.debug(f"Made array: \n {a} \n")
    sequence = travel_salesman_problem(a)

    logging.debug(f"Formed sequence: \n {sequence} \n")
    draw_track(points, sequence, data_forbidden_lines, data_forbidden_zones)
