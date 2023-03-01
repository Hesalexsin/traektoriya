# This is a sample Python script.
import numpy as np
from travelling_salesmans_task import line_reduction, column_reduction, \
    find_degrees_of_zeros, exclude_edge, include_edge
from travelling_salesmans_task import travel_salesmans_task

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = np.array([[0, 1, 2, 3, 4, 5],
                  [1, np.inf, 20, 18, 12, 8],
                  [2, 5, np.inf, 14, 7, 11],
                  [3, 12, 18, np.inf, 6, 11],
                  [4, 11, 17, 11, np.inf, 12],
                  [5, 5, 5, 5, 5, np.inf]])

    print(travel_salesmans_task(a))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
