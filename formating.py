import json
import logging
import sys


# preparation of input data for processing by the program
def make_json_data(json_filename: str):
    try:
        with open(json_filename, "r") as read_file:
            data = json.load(read_file)
        return data
    except OSError:
        logging.error(f"File doesn't exist")
        sys.exit(-1)


# making point array to drawing
def make_points(data: object):
    points = {}
    for p in data:
        points[p['id']] = {'x': p['x'], 'y': p['y']}
    return points
