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
        X.append(points.get(d).get('x'))
        Y.append(points.get(d).get('y'))
    fig, ax = plt.subplots()
    ax.plot(X, Y)

    # drawing FLs (need a function)
    for line in fl:
        X_fl = []
        Y_fl = []
        X_fl.append(points.get(line.get('id1')).get('x'))
        Y_fl.append(points.get(line.get('id1')).get('y'))
        X_fl.append(points.get(line.get('id2')).get('x'))
        Y_fl.append(points.get(line.get('id2')).get('y'))
        ax.plot(X_fl, Y_fl, color='r')

    # drawing IDs (need a function)
    for i in range(1, len(sequence)):
        plt.text(X[i], Y[i], str(sequence[i]))

    # saving picture (need function and need another paths of output)
    output_filename = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + 'track.png'
    fig.savefig(output_filename, dpi=300)
    logging.info(f"Updating track.png")
