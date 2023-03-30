import matplotlib.pyplot as plt
import logging
from datetime import datetime
from formating import make_points, make_json_data


# drawing track - shortpath between points and save picture with forbidden lines
def draw_track(points: dict, sequence: list, fl: list):
    X = []
    Y = []
    # drawinng track (need a function)
    for d in sequence:
        point = points[d]
        X.append(point['x'])
        Y.append(point['y'])
    fig, ax = plt.subplots()
    ax.plot(X, Y)

    # drawing FLs (need a function)
    for line in fl:
        id1 = line['id1']
        id2 = line['id2']
        X_fl = [points[id1]['x'], points[id2]['x']]
        Y_fl = [points[id1]['y'], points[id2]['y']]
        ax.plot(X_fl, Y_fl, color='r')

    # drawing IDs (need a function)
    for i in range(1, len(sequence)):
        plt.text(X[i], Y[i], str(sequence[i]))

    # saving picture (need function and need another paths of output)
    output_filename = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + 'track.png'
    fig.savefig(output_filename, dpi=300)
    logging.info(f"Updating track.png")
