import random
import pytisean.pytisean as pt
from pytisean import tiseano
import numpy as np
import copy

"""Wrapper for Pytisean"""
def iid(): 
    pass 

def fourier(x,n): 
    SEED= random.randint(0,10000)
    data, msg = pt.tiseanio(
    "surrogates",
    "-n", str(n),
    "-i", "0",
    "-S",
    "-I", str(SEED),
    #"-o", dir,
    data=np.asarray(x) 
    )
    return data, msg


def AAFT(x,n): 
    SEED= random.randint(0,10000)
    data, msg = pt.tiseanio(
    "surrogates",
    "-n", str(n),
    "-I", str(SEED),
    #"-o", dir,
    data=np.asarray(x) 
    )
    return data, msg

def IAAFT(x,n): 
    SEED= random.randint(0,10000)
    data, msg = pt.tiseanio(
    "surrogates",
    "-n", str(n),
    "-i", "0",
    "-S",
    "-I", str(SEED),
    #"-o", dir,
    data=np.asarray(x) 
    )
    return data, msg

def get_henon(x_0,y_0,n, a= 1.4,b=0.3):
    x = 0 
    y = 0
    x_values = []
    y_values = []  
    for i in range(n):
        x_values.append(x)
        y_values.append(y)
        x_new= 1-a*x**2+y
        y= b*x
        x= x_new
    return x_values, y_values 
def reconstruct_phase_space(x,m,t):  
    s_length = len(x)-m*t
    x= np.array(x)
    s=np.empty((s_length,m))
    for i in range (s_length): 
        index = np.array([i+j*t for j in range(0,m)])
        s[i]=x[index]
        
    return s
def time_reversal(x): 
    n= len(x)
    a= copy.copy(x)[1:n]
    b= copy.copy(x)[0:n-1]
    c= np.pow(a-b,3)
    d= np.pow(np.average(np.pow(a-b,2)),3/2)
    print(f"{a=}")
    print(f"{b=}")
    print(f"{c=}")
    return np.average(c)/d

