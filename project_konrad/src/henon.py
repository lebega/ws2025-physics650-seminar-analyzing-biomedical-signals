#!/usr/bin/env python3
import os
import shutil
import sys
import tempfile
from fix_temp_path import fix_tmp_for_pytisean
import pytisean.pytisean as pt
from pytisean import tiseano
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from surrogate import *

def delay_embed(x, m=2, tau=1, horizon=1):
    x = np.asarray(x, dtype=float)
    n = x.shape[0]
    t0 = (m - 1) * tau
    t_max = n - 1 - horizon
    if t_max < t0:
        raise ValueError("Time series too short for given m, tau, and horizon.")

    times = np.arange(t0, t_max + 1) 
    Y = np.column_stack([x[times - j*tau] for j in range(m)])
    y_future = x[times + horizon]
    return Y, y_future, times
    
matplotlib.use('Qt5Agg')
tmp = fix_tmp_for_pytisean()
print("Using temp dir1:", tmp)
import pytisean.pytisean as pt

n= 500
m=99
pt.DIRSTR=tmp
x_henon, y_henon = get_henon(0,0,n)


Y = reconstruct_phase_space(x_henon,2,1)
Y= Y.transpose()

surrogates = np.empty((m,n))
for i in range(m): 
    surrogates[i],_=IAAFT(x_henon,1)
def nlpe_local_constant(x, m=2, tau=1, horizon=1, k=20, theiler=0, normalize=True):
    Y, y_future, times = delay_embed(x, m=m, tau=tau, horizon=horizon)
    M = Y.shape[0]
    if k >= M:
        raise ValueError("k must be smaller than number of embedded points.")

    preds = np.empty(M, dtype=float)

    for i in range(M):
        d2 = np.sum((Y - Y[i])**2, axis=1)

        mask = np.abs(times - times[i]) <= theiler
        d2[mask] = np.inf

        nn_idx = np.argpartition(d2, kth=k)[:k]
        nn_idx = nn_idx[np.isfinite(d2[nn_idx])]
        if nn_idx.size < max(3, k//4):
            preds[i] = np.mean(y_future)
        else:
            preds[i] = np.mean(y_future[nn_idx])

    rmse = np.sqrt(np.mean((y_future - preds)**2))
    if normalize:
        scale = np.std(y_future, ddof=1)
        nlpe = rmse / scale if scale > 0 else np.nan
    else:
        nlpe = rmse

    details = {
        "rmse": rmse,
        "preds": preds,
        "y_future": y_future,
        "times": times,
        "M": M
    }
    return nlpe, details


def _rank_match(values, target_sorted):
    order = np.argsort(values)
    out = np.empty_like(values)
    out[order] = target_sorted
    return out
nlpe,_= nlpe_local_constant(x_henon)
print(nlpe)
for s in surrogates:
    a,_= nlpe_local_constant(s)
    print(a)

x_2,_= AAFT(x_henon,1)
def plot(x,y, filename):
    plt.figure(figsize=(12, 5))
    fsize= 25
    plt.plot(x, y)
    plt.xlabel("time",fontsize= fsize )
    plt.ylabel("amplitude", fontsize= fsize )
    plt.savefig(f"./project_konrad/figures/{filename}", dpi= 300)
plot(range(n),x_henon, "henon.png")
plot(range(n),x_2, "fake_henon.png")