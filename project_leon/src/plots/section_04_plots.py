from os import path

import numpy as np
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


# plot henon
def plot_noisyhenon_vs_reducedhenon_attractor(steps):
    # create henon timeseries
    henon = ts.henon(steps)
    y = henon[:, 0]
    # add noise and reconstruct noisy attractor
    x = ts.addnoise(y)
    X = ts.delay(x)
    # reduce noise and reconstruct attractor
    x_red = ts.ghkss(
        x,
    )
    X_red = ts.delay(x_red)

    fig, ax = plt.subplots(1, 2)

    ax[0].scatter(X[:, 0], X[:, 1], s=5)
    ax[0].set_xlabel(r"$x_n$")
    ax[0].set_ylabel(r"$x_{n+1}$")
    ax[1].scatter(X_red[:, 0], X_red[:, 1], s=5)
    ax[1].set_xlabel(r"$x_n^\mathrm{corr}$")
    ax[1].set_ylabel(r"$x_{n+1}^\mathrm{corr}$")

    plt.tight_layout()
    plt.savefig(path.join(get_plot_dir(), "04_results_noisy-reduced-attr.pdf"))
    plt.close()


# plot henon
def plot_noisyhenon_vs_reducedhenon_attractor_zoomed(steps):
    henon = ts.henon(steps)
    y = henon[:, 0]
    Y = ts.delay(y)
    x = ts.addnoise(y)
    x_red = ts.ghkss(
        x,
    )
    X_red = ts.delay(x_red)

    fig, ax = plt.subplots(1, 2)

    ax[0].scatter(Y[:, 0], Y[:, 1], s=5)
    ax[0].set_xlabel(r"$y_n$")
    ax[0].set_ylabel(r"$y_{n+1}$")
    ax[0].set_xlim(0.3, 0.7)
    ax[0].set_ylim(0.3, 0.7)
    ax[1].scatter(X_red[:, 0], X_red[:, 1], s=5)
    ax[1].set_xlabel(r"$x_n^\mathrm{corr}$")
    ax[1].set_ylabel(r"$x_{n+1}^\mathrm{corr}$")
    ax[1].set_xlim(0.3, 0.7)
    ax[1].set_ylim(0.3, 0.7)

    plt.tight_layout()
    plt.savefig(path.join(get_plot_dir(), "04_results_noisy-reduced-attr_zoomed.pdf"))
    plt.close()


# plot henon
def plot_noisyhenon_vs_reducedhenon_attractor_zero(steps):
    henon = ts.henon(steps)
    y = henon[:, 0]
    x = ts.addnoise(y)
    X = ts.delay(x)
    x_red = ts.lazy(x, iterations=2)[:, 0]
    X_red = ts.delay(x_red)

    fig, ax = plt.subplots(1, 2)

    ax[0].scatter(X[:, 0], X[:, 1], s=5)
    ax[0].set_xlabel(r"$x_n$")
    ax[0].set_ylabel(r"$x_{n+1}$")
    ax[1].scatter(X_red[:, 0], X_red[:, 1], s=5)
    ax[1].set_xlabel(r"$x_n^\mathrm{corr}$")
    ax[1].set_ylabel(r"$x_{n+1}^\mathrm{corr}$")

    plt.tight_layout()
    plt.savefig(path.join(get_plot_dir(), "04_results_noisy-reduced-attr_zero.pdf"))
    plt.close()


# plot henon
def plot_noisyhenon_vs_reducedhenon_attractor_zoomed_zero(steps):
    henon = ts.henon(steps)
    y = henon[:, 0]
    Y = ts.delay(y)
    x = ts.addnoise(y)
    x_red = ts.lazy(x, iterations=2)[:, 0]
    X_red = ts.delay(x_red)

    fig, ax = plt.subplots(1, 2)

    ax[0].scatter(Y[:, 0], Y[:, 1], s=5)
    ax[0].set_xlabel(r"$y_n$")
    ax[0].set_ylabel(r"$y_{n+1}$")
    ax[0].set_xlim(0.3, 0.7)
    ax[0].set_ylim(0.3, 0.7)
    ax[1].scatter(X_red[:, 0], X_red[:, 1], s=5)
    ax[1].set_xlabel(r"$x_n^\mathrm{corr}$")
    ax[1].set_ylabel(r"$x_{n+1}^\mathrm{corr}$")
    ax[1].set_xlim(0.3, 0.7)
    ax[1].set_ylim(0.3, 0.7)

    plt.tight_layout()
    plt.savefig(
        path.join(get_plot_dir(), "04_results_noisy-reduced-attr_zoomed_zero.pdf")
    )
    plt.close()


# plot henon
def plot_noisered_per_iteration(steps):
    # get data
    henon = ts.henon(steps)
    y = henon[:, 0]
    x = ts.addnoise(y)

    it = np.arange(0, 11)

    rms = [np.sqrt(np.mean((x - y) ** 2))]
    x_red = [ts.ghkss(x, iterations=1)]
    for i in range(1, 10):
        rms.append(np.sqrt(np.mean((x_red[-1] - y) ** 2)))
        x_red.append(ts.ghkss(x_red[-1], iterations=1))
    rms.append(np.sqrt(np.mean((x_red[-1] - y) ** 2)))

    # plot
    plt.plot(it, rms)
    plt.xlabel("Iteration")
    plt.ylabel(r"RMS difference from $y_n$")
    plt.tight_layout()
    plt.savefig(path.join(get_plot_dir(), "04_results_rms-diff-true.pdf"))
    plt.close()


# plot henon
def plot_noisered_per_iteration_zero(steps):
    # get data
    henon = ts.henon(steps)
    y = henon[:, 0]
    x = ts.addnoise(y)

    it = np.arange(0, 11)

    rms = [np.sqrt(np.mean((x - y) ** 2))]
    x_red = [ts.lazy(x, iterations=1, eps=0.1)[:, 0]]
    for i in range(1, 10):
        rms.append(np.sqrt(np.mean((x_red[-1] - y) ** 2)))
        x_red.append(ts.lazy(x_red[-1], iterations=1, eps=rms[-1])[:, 0])
    rms.append(np.sqrt(np.mean((x_red[-1] - y) ** 2)))

    # plot
    plt.plot(it, rms)
    plt.xlabel("Iteration")
    plt.ylabel(r"RMS difference from $y_n$")
    plt.tight_layout()
    plt.savefig(path.join(get_plot_dir(), "04_results_rms-diff-true_zero.pdf"))
    plt.close()


def run():
    plot_noisyhenon_vs_reducedhenon_attractor(10000)
    plot_noisyhenon_vs_reducedhenon_attractor_zoomed(10000)
    plot_noisyhenon_vs_reducedhenon_attractor_zero(10000)
    plot_noisyhenon_vs_reducedhenon_attractor_zoomed_zero(10000)
    plot_noisered_per_iteration(10000)
    plot_noisered_per_iteration_zero(10000)


if __name__ == "__main__":
    run()
