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


def plot_noisyhenon_vs_reducedhenon_attractor(steps):
    # create henon timeseries
    henon = ts.henon(steps)
    y = henon[:, 0]
    # add noise and reconstruct noisy attractor
    x = ts.addnoise(y)
    X = ts.delay(x)
    # reduce noise and reconstruct attractor
    x_red = ts.lazy(x, iterations=2, eps=0.15)[:, 0]
    X_red = ts.delay(x_red)

    # plot
    fig, ax = plt.subplots(1, 2)

    ax[0].scatter(X[:, 0], X[:, 1], s=5)
    ax[0].set_xlabel(r"$x_n$")
    ax[0].set_ylabel(r"$x_{n+1}$")
    ax[1].scatter(X_red[:, 0], X_red[:, 1], s=5)
    ax[1].set_xlabel(r"$x_n^\mathrm{corr}$")
    ax[1].set_ylabel(r"$x_{n+1}^\mathrm{corr}$")

    plt.tight_layout()
    plt.savefig(path.join(get_plot_dir(), "03a_simple_noisy-reduced-attr.pdf"))
    plt.close()


def plot_curvature_bias():
    # SETUP PLOT
    plt.rcParams.update({"font.size": 14})
    fig, ax = plt.subplots(figsize=(8, 6))

    # CREATE DATA
    # Define the True Manifold (Parabola)
    x_true = np.linspace(-1.5, 1.5, 100)
    y_true = x_true**2
    # Define the Neighborhood
    x_neigh = np.linspace(-1.0, 1.0, 20)
    noise = np.random.normal(0, 0.05, size=x_neigh.shape)
    y_neigh = x_neigh**2 + noise
    # Calculate the Simple Average
    mean_x = np.mean(x_neigh)
    mean_y = np.mean(y_neigh)
    # The point on the manifold directly below the average
    true_y_at_mean = mean_x**2

    # PLOT
    # The Parabola
    ax.plot(x_true, y_true, "k-", lw=2, alpha=0.6, label="True Manifold $\mathcal{A}$")
    # The Neighborhood Points
    ax.scatter(
        x_neigh,
        y_neigh,
        color="gray",
        alpha=0.7,
        s=50,
        label="Neighborhood $\mathcal{U}_n$",
    )
    # The Average (Result of Simple Method)
    ax.scatter(
        mean_x,
        mean_y,
        color="red",
        s=200,
        zorder=10,
        marker="X",
        label="Average (New Point)",
    )
    # Visualize the Bias
    # Draw a line from the Manifold to the Average
    ax.vlines(mean_x, true_y_at_mean, mean_y, colors="red", linestyles="--", lw=2)
    # Annotations to explain the physics
    ax.annotate(
        "Systematic Error\n(Bias)",
        xy=(mean_x, (mean_y + true_y_at_mean) / 2),
        xytext=(mean_x + 0.5, mean_y),
        arrowprops=dict(arrowstyle="->", color="red"),
        color="red",
        fontsize=12,
        fontweight="bold",
    )
    ax.annotate(
        "Attractor shrinks\ninward",
        xy=(mean_x, mean_y),
        xytext=(-1.2, 0.8),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2", color="black"),
        fontsize=11,
    )
    # Formatting
    ax.set_xlabel("State $x_1$")
    ax.set_ylabel("State $x_2$")
    ax.legend(loc="upper center")
    ax.grid(True, linestyle=":", alpha=0.6)
    # Zoom in to relevant area
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.2, 1.5)
    # Save Plot
    plt.tight_layout()
    plt.savefig(path.join(get_plot_dir(), "03a_simple_error.pdf"))
    plt.close()


def run():
    plot_curvature_bias()
    plot_noisyhenon_vs_reducedhenon_attractor(10000)


if __name__ == "__main__":
    run()
