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
import matplotlib.patches as patches
matplotlib.use('Qt5Agg')
n=1000
points = np.random.rand(n,2)
amount_inside = 0
for p in points: 
    amount_inside += (p[0]**2+p[1]**2) < 1
pi = 4* amount_inside / n 
print(pi)
fig, ax = plt.subplots(figsize=(10, 10))
x , y =points.transpose() 
ax.scatter(x,y,marker=".")
angles=np.linspace(0,np.pi/2, 1000)
x_circ=np.cos(angles)
y_circ=np.sin(angles)
ax.set_xlabel("x")
ax.set_xlabel("y")
ax.plot(x_circ,y_circ, color="green", linewidth=2)

rect = patches.Rectangle(
    (0, 0),      
    1,          
    1,         
    linewidth=2,
    edgecolor='red',
    facecolor='none'  
)

ax.add_patch(rect)
ax.set_xlabel("X")
ax.set_ylabel("Y")
plt.savefig("./project_konrad/figures/monte_carlo.png", dpi=300)
plt.show()