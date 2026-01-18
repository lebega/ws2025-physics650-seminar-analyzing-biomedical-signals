import os
import shutil
import sys
import tempfile
from fix_temp_path import fix_tmp_for_pytisean
import pytisean.pytisean as pt
from pytisean import tiseano
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from surrogate import *
n = 50
def plot(x,y,filename, labels, xl="x",yl="amplitude"): 
    fsize= 20
    plt.tick_params(axis="both", labelsize=15)
    w= 10
    fig, ax = plt.subplots(figsize=(w, 5))
    bars=ax.bar(x, y, edgecolor="k", width=1)
    ax.set_xlabel(xl,fontsize= fsize )
    ax.set_ylabel(yl,fontsize= fsize)
    ax.bar_label(bars, labels=labels, padding=2, fontsize=8)
    plt.savefig(f"./project_konrad/figures/{filename}", dpi= 300)
matplotlib.use('Qt5Agg')

n_gauss= 100_000
mu, sigma = 0.0, 1.0
x = np.random.normal(mu, sigma, size=n_gauss)

bins = n
hist, edges = np.histogram(x, bins=bins, density=True)

centers = range(n)
widths  = 10




hist_sort=np.sort(hist)

x_h, y_h = get_henon(0,0,n)
x_h_sort= np.sort(x_h)


idx_h = np.argsort(x_h)
idx = np.argsort(hist)
plot(centers,hist,"Gauss_01.png",range(n), xl="time")
plot(centers,hist_sort,"Gauss_02.png",idx,xl="rank")
plot(centers,x_h,"Gauss_03.png",range(n), xl="time")
plot(centers,x_h_sort,"Gauss_04.png",idx_h,xl="rank")
plot(centers,hist_sort, "Gauss_05.png",idx_h,xl="rank")
plot(centers, hist[idx_h], "Gauss_06.png",range(n), xl="time")


