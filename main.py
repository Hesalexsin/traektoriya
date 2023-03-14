import numpy as np
from travelling_salesmans_task import line_reduction, column_reduction, \
    find_degrees_of_zeros, exclude_edge, include_edge
from travelling_salesmans_task import travel_salesmans_task
from edges import make_array
from formating import make_points, make_json_data
from draw_track import draw_track
import logging
import logging.config

# main function
if __name__ == '__main__':
    logging.config.fileConfig('logconfig.ini')
    logging.getLogger().level = logging.INFO
    filename = 'input.json'
    data = make_json_data(filename).get('data_points')
    logging.debug(f"Read data: \n {data} \n")
    points = make_points(data)
    a = make_array(points)
    logging.debug(f"Made array: \n {a} \n")
    sequence = travel_salesmans_task(a)

    logging.debug(f"Formed sequence: \n {sequence} \n")
    draw_track(points, sequence)

    # print()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

"""a = np.array([[0, 1, 2, 3, 4, 5],
                  [1, np.inf, 20, 18, 12, 8],
                  [2, 5, np.inf, 14, 7, 11],
                  [3, 12, 18, np.inf, 6, 11],
                  [4, 11, 17, 11, np.inf, 12],
                  [5, 5, 5, 5, 5, np.inf]])"""

"""    a = np.array([[0, 1, 2, 3, 4, 5, 6],
                  [1, np.inf, 41, 40, 48, 40, 42],
                  [2, 48, np.inf, 41, 49, 42, 46],
                  [3, 22, 22, np.inf, 23, 24, 19],
                  [4, 15, 17, 11, np.inf, 10, 14],
                  [5, 47, 43, 18, 42, np.inf, 52],
                  [6, 34, 39, 30, 39, 32, np.inf]])
    sequence = travel_salesmans_task(a)
    print(a, sequence)"""

"""
filename = 'data.json'
    data = make_json_data(filename)
    a = make_array(data.get('data_points'))
    print(a)
    sequence = travel_salesmans_task(a)
    points = make_points(data.get('data_points'),len(data.get('data_points')))
    print(points.get(1001))

    print(sequence)
    draw_track(points,sequence)

    #print()"""
