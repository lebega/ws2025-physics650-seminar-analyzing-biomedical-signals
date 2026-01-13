from os import path

import matplotlib.pyplot as plt

from config import get_plot_dir
import tisean.functions as ts

plt.rcParams.update(
    {
        # Figure
        "figure.figsize": (6, 3),  # fits Beamer nicely
        "figure.dpi": 150,
        "savefig.dpi": 300,
        # Lines & markers
        "lines.linewidth": 1.0,
        "lines.markersize": 4,
        # Fonts (match LaTeX look)
        "font.size": 10,
        "axes.labelsize": 9,
        "axes.titlesize": 9,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        # LaTeX rendering (optional but recommended)
        "text.usetex": True,
        "font.family": "serif",
        # Clean look
        "axes.linewidth": 0.8,
    }
)


def plot_henon_vs_noisy_attractor(steps):
    # create henon timeseries
    henon = ts.henon(steps)
    y = henon[:, 0]
    # reconstruct henon attractor
    Y = ts.delay(y)
    # add noise and reconstruct noisy attractor
    x = ts.addnoise(y)
    X = ts.delay(x)

    # plot
    fig, ax = plt.subplots(1, 2)

    ax[0].scatter(Y[:, 0], Y[:, 1], s=5)
    ax[0].set_xlabel(r"$y_n$")
    ax[0].set_ylabel(r"$y_{n+1}$")
    ax[1].scatter(X[:, 0], X[:, 1], s=5)
    ax[1].set_xlabel(r"$x_n$")
    ax[1].set_ylabel(r"$x_{n+1}$")

    plt.tight_layout()
    plt.savefig(path.join(get_plot_dir(), "02_phasespace_henon-noise-attr.pdf"))
    plt.close()


def run():
    plot_henon_vs_noisy_attractor(10000)


if __name__ == "__main__":
    run()
