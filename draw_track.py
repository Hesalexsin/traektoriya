import matplotlib.pyplot as plt
from formating import make_points, make_json_data


# drawing track - shortpath between points and save picture
def draw_track(points, sequence):
    X = []
    Y = []
    for d in sequence:
        X.append(points.get(1000 + d).get('x'))
        Y.append(points.get(1000 + d).get('y'))
    fig, ax = plt.subplots()
    ax.plot(X, Y)

    for i in range(1, len(sequence)):
        plt.text(X[i], Y[i], str(sequence[i] + 1000))
    fig.savefig("track.png", dpi=300)
