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
    x_red = ts.ghkss(x, iterations=5)
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
    plt.savefig(path.join(get_plot_dir(), "03b_projective_noisy-reduced-attr.pdf"))
    plt.close()


def plot_noise_reduction_comparison():
    # PLOT SETUP
    # plt.rcParams.update({'font.size': 14, 'lines.linewidth': 2})
    plt.rcParams.update(
        {
            # Figure
            "figure.figsize": (5, 3),  # fits Beamer nicely
            "figure.dpi": 150,
            "savefig.dpi": 300,
            # Lines & markers
            "lines.linewidth": 1.0,
            "lines.markersize": 4,
            # Fonts (match LaTeX look)
            "font.size": 10,
            "axes.labelsize": 11,
            "axes.titlesize": 11,
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
    fig, ax = plt.subplots(figsize=(8, 6))

    np.random.seed(42)
    n_points = 150

    # Create a highly correlated covariance matrix (representing a local line)
    # Variance in long axis = 1.0, Variance in short axis (noise) = 0.02
    angle = np.deg2rad(45)
    rotation_matrix = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    scaling_matrix = np.array([[1.0, 0], [0, 0.05]])
    cov = rotation_matrix @ scaling_matrix @ rotation_matrix.T

    # CREATE DATA
    data = np.random.multivariate_normal([0, 0], cov, n_points)
    noisy_point = np.array([0.5, 0.8])

    # simple method
    centroid = np.mean(data, axis=0)

    # projective method
    # covariance
    data_centered = data - centroid
    cov_matrix = np.cov(data_centered.T)
    # eigenvalues
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
    # identify tangent and noise
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    major_axis = eigenvectors[:, 0]
    # project noisy point to major axis
    vec_to_point = noisy_point - centroid
    projection_length = np.dot(vec_to_point, major_axis)
    projected_point = centroid + projection_length * major_axis

    # PLOT
    # plot point cloud
    ax.scatter(
        data[:, 0],
        data[:, 1],
        alpha=0.2,
        c="grey",
        label="Neighborhood $\mathcal{U}_n$",
    )
    # plot manifold line
    line_x = np.linspace(-1.5, 1.5, 10)
    line_y = centroid[1] + (line_x - centroid[0]) * (major_axis[1] / major_axis[0])
    ax.plot(
        line_x,
        line_y,
        "--",
        color="black",
        alpha=0.5,
        lw=1,
        label="Local Linear Approx.",
    )
    # The Noisy Point
    ax.scatter(
        noisy_point[0],
        noisy_point[1],
        s=150,
        c="red",
        marker="X",
        zorder=10,
        label="Noisy Observation $\mathbf{x}_n$",
    )
    # Simple Method Result
    ax.scatter(
        centroid[0],
        centroid[1],
        s=150,
        c="green",
        marker="o",
        zorder=10,
        label="Simple Method (Avg)",
    )
    # Projective Method Result
    ax.scatter(
        projected_point[0],
        projected_point[1],
        s=150,
        c="blue",
        marker="o",
        zorder=10,
        label="Projective Method",
    )
    # draw arrows
    ax.annotate(
        "",
        xy=centroid,
        xytext=noisy_point,
        arrowprops=dict(arrowstyle="->", color="green", lw=2, ls="dotted"),
    )
    ax.annotate(
        "",
        xy=projected_point,
        xytext=noisy_point,
        arrowprops=dict(arrowstyle="->", color="blue", lw=2),
    )
    # Formatting
    ax.set_aspect("equal")
    ax.set_xlabel("$x_n$")
    ax.set_ylabel("$x_{n+1}$")
    ax.legend(loc="lower right", frameon=True, fontsize=10)
    ax.grid(True, linestyle=":", alpha=0.6)
    # Limit view to relevant area
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    # Save Plot
    plt.tight_layout()
    plt.savefig(path.join(get_plot_dir(), "03b_projective_diagram-simple-prod.pdf"))
    plt.close()


def run():
    plot_noisyhenon_vs_reducedhenon_attractor(10000)
    plot_noise_reduction_comparison()


if __name__ == "__main__":
    run()
