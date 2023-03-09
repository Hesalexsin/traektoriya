import json


# preparation of input data for processing by the program
def make_json_data(json_filename):
    with open(json_filename, "r") as read_file:
        data = json.load(read_file)
    return data


# making point array to drawing
def make_points(data, n):
    points = {}
    for i in range(1, n):
        points[data[i].get('id')] = {'x': data[i].get('x'), 'y': data[i].get('y')}
    return points
