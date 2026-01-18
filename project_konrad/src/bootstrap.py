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
import pandas as pd
import random
matplotlib.use('Qt5Agg')
df_thresh =pd.read_csv("./project_konrad/data/boot_data_3.csv")


def bootstrap(x,y):
    rng = np.random.default_rng()

    p = y         
    p = p / p.sum()                         
    m=int(y.sum())
    idx = rng.choice(len(p), size=m, p=p)
    samples = x[idx]
    binned_counts = np.bincount(idx, minlength=len(x))
    return binned_counts


def plot(x,y,mean,std, filename):
    plt.figure(figsize=(12, 12))
    fsize= 25
    plt.bar(x, y, edgecolor='black', width=60)
    plt.xlabel(r"$Q_\text{thresh}\;/\; e^-$",fontsize= fsize )
    plt.ylabel("Events"+r"$\;/\; 10^{3}$", fontsize= fsize )
    plt.tick_params(axis="both", labelsize=20)
    

    plt.text(
        0.05, 0.95,
        f"mean = {mean:.2f}\nstd = {std:.2f}",
        transform=plt.gca().transAxes,
        va="top",
        bbox=dict(boxstyle="round", alpha=0.8),
        fontsize= fsize 

    )

    
    plt.savefig(f"./project_konrad/figures/"+filename, dpi=100)
    #plt.show()
n=100
mean=[]
sigma=[]
x= df_thresh["PulserDAC"][:70]
y= df_thresh["Counts"][:70]
for i in range(n): 
    surr= bootstrap(x,y)
    m = np.average(x, weights=surr)
    mean.append(m)
    s= np.sqrt(np.average((x - m)**2, weights= surr))
    sigma.append(s)
    if i < 8:
        plot(x,surr,m,s,f"surr_{i}.png")




print(f"mean= {np.average(mean)} pm {np.std(mean,ddof=1)}")
print(f"sigma= {np.average(sigma)} pm {np.std(sigma,ddof=1)}")
m_org=3675.647
s_org=345.4000
x_org= df_thresh["PulserDAC"][:70]
y_org= df_thresh["Counts"][:70]
plot(x_org,y_org,m_org,s_org,"org.png")