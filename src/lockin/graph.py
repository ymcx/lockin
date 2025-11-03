import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from collections import defaultdict


def create() -> tuple[Figure, Axes, defaultdict[str, dict]]:
    plt.ion()
    figure, axes = plt.subplots()
    lines = defaultdict(dict)

    return figure, axes, lines


def update(
    iteration: int,
    scores: dict[str, float],
    figure: Figure,
    axes: Axes,
    lines: defaultdict[str, dict],
) -> None:
    for ticker, score in scores.items():
        if ticker not in lines:
            line = lines[ticker]
            line["x"] = [iteration]
            line["y"] = [score]
            line["line"] = axes.plot(line["x"], line["y"], label=ticker)[0]
        else:
            line = lines[ticker]
            line["x"].append(iteration)
            line["y"].append(score)
            line["line"].set_data(line["x"], line["y"])

    axes.relim()
    axes.autoscale_view()
    axes.legend()

    figure.canvas.draw()
    figure.canvas.flush_events()
