import logging.config
import math
import sys

import tracks as tracks

import tracks
import edges
from formating import make_json_data

logging.config.fileConfig('logconfig.ini')
logging.getLogger().level = logging.DEBUG
filename = 'one_circle_test.json'
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


path = tracks.Track(tracks.Line(tracks.Point(data_points[0]['x'],data_points[0]['y']),
                                tracks.Point(data_points[1]['x'],data_points[1]['y'])))
c = tracks.Point(data_forbidden_zones[0]['x'],data_forbidden_zones[0]['y'])
d = tracks.Point(data_forbidden_zones[0]['x'],data_forbidden_zones[0]['y'] + data_forbidden_zones[0]['r'])
alpha = d.x - c.x / data_forbidden_zones[0]['r']
print(alpha, (d.x - c.x) / data_forbidden_zones[0]['r'])
path.find_path({'fzs':[tracks.Arc(d,d, c)]})

print(path.fragments[1].length)



