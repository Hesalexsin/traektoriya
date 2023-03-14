import json


# preparation of input data for processing by the program
def make_json_data(json_filename: str):
    with open(json_filename, "r") as read_file:
        data = json.load(read_file)
    return data


# making point array to drawing
def make_points(data: object):
    points = {}
    for p in data:
        points[p.get('id')] = {'x': p.get('x'), 'y': p.get('y')}
    return points
