from os import path

import numpy as np
import matplotlib.pyplot as plt

from config import get_plot_dir
import tisean.functions as ts

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


# plot henon vs noisy henon
def plot_henon_vs_noise(steps):
    # create henon timeseries
    henon = ts.henon(steps)
    x1 = henon[:, 0]
    # create noise timeseries of same mean and std
    mu = np.mean(x1)
    sigma = np.std(x1)
    x2 = np.random.normal(mu, sigma, steps)
    n = np.arange(steps)

    # plot
    fig, ax = plt.subplots(2, 1)

    ax[0].plot(n, x1)
    ax[0].set_xlabel(r"$n$")
    ax[0].set_ylabel(r"$x_n$")
    ax[1].plot(n, x2)
    ax[1].set_xlabel(r"$n$")
    ax[1].set_ylabel(r"$\eta_n$")

    plt.tight_layout()
    plt.savefig(path.join(get_plot_dir(), "01_motivation_henon-noise-ts.pdf"))
    plt.close()


def plot_henon_vs_noisy(steps):
    # create henon timeseries
    henon = ts.henon(steps)
    x1 = henon[:, 0]
    # create noise timeseries of same mean and std
    mu = np.mean(x1)
    sigma = np.std(x1)
    x2 = np.random.normal(mu, sigma, steps)
    n = np.arange(steps)

    # plot
    fig, ax = plt.subplots(2, 1)

    ax[0].plot(n, x1)
    ax[0].set_xlabel(r"$n$")
    ax[0].set_ylabel(r"$x_n$")
    ax[1].plot(n, x1 + 0.05 * x2)
    ax[1].set_xlabel(r"$n$")
    ax[1].set_ylabel(r"$x_n + 0.05\cdot\eta_n$")

    plt.tight_layout()
    plt.savefig(path.join(get_plot_dir(), "01_motivation_henon-noisy-ts.pdf"))
    plt.close()


def plot_henon_vs_noise_power(steps):
    # create henon timeseries
    henon = ts.henon(steps)
    x1 = henon[:, 0]
    # create noise timeseries of same mean and std
    mu = np.mean(x1)
    sigma = np.std(x1)
    x2 = np.random.normal(mu, sigma, steps)
    N = steps

    # calculate power spectrum
    X1 = np.fft.rfft(x1)
    X2 = np.fft.rfft(x2)
    freqs = np.fft.rfftfreq(N)
    y1 = (np.abs(X1) ** 2) / N
    y2 = (np.abs(X2) ** 2) / N
    half_N = N // 2

    # plot
    fig, ax = plt.subplots(2, 1)

    ax[0].semilogy(freqs[:half_N], y1[:half_N])
    ax[0].set_xlabel(r"Frequency (cycles per sample)")
    ax[0].set_ylabel(r"Power")
    ax[1].semilogy(freqs[:half_N], y2[:half_N])
    ax[1].set_xlabel(r"Frequency (cycles per sample)")
    ax[1].set_ylabel(r"Power")

    plt.tight_layout()
    plt.savefig(path.join(get_plot_dir(), "01_motivation_henon-noise-power.pdf"))
    plt.close()


def run():
    plot_henon_vs_noise(200)
    plot_henon_vs_noisy(200)
    plot_henon_vs_noise_power(2000)


if __name__ == "__main__":
    run()
