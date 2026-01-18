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
matplotlib.use('Qt5Agg')
tmp = fix_tmp_for_pytisean()
print("Using temp dir:", tmp)
pt.DIRSTR=tmp
data= np.array(pd.read_csv("./project_konrad/data/ekg.txt")["ECG_DATA"])
plt.plot(range(len(data)),data)
plt.xlabel(r"time",fontsize= 20 )
plt.ylabel("amplitude", fontsize= 20 )
plt.savefig("./project_konrad/figures/EKG.png",dpi=300)

plt.show()

print(data)

n_surrogates=199
surrogates = np.empty((n_surrogates, len(data)))
for i in range(n_surrogates):
    surrogates[i], _ = IAAFT(data, 1)

surrogate_time_reversals=np.empty(n_surrogates)
for i in range(n_surrogates): 
    surrogate_time_reversals[i]=time_reversal(surrogates[i])
print(time_reversal(data))
print(np.average(surrogate_time_reversals))
print(np.std(surrogate_time_reversals))

plt.plot(range(len(surrogates[0])),surrogates[0])

plt.show()
