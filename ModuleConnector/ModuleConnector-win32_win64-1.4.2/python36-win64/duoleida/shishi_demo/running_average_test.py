#-*-coding:utf-8 -*-
import scipy.io as sio
from kalman import *
import location_multi
import pca_filter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from sympy import*
import rangr_multi
import lse
import newnew_multi
from gmphd_single import *
import time
from scipy.signal.wavelets import cwt, ricker
load_r1=sio.loadmat('C:/Users/yyb/Desktop/brs/gg1.mat')
r1=load_r1['radar1']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/brs/gg2.mat')
r2=load_r2['radar2']
load_r3=sio.loadmat('C:/Users/yyb/Desktop/brs/gg3.mat')
r3=load_r3['radar3']
M=10
L=100
RawData1=r1[:,0:750]
RawData2=r2[:,0:750]
RawData3=r3[:,0:750]
###后截250
PureData1=pca_filter.p_f(RawData1,M,L)
PureData2=pca_filter.p_f(RawData2,M,L)
PureData3=pca_filter.p_f(RawData3,M,L)
####################################################################




for zzz in range(len(yuce_x)):
    plt.scatter(zzz, yuce_x[zzz], color='b')
for zzzz in range(len(yuce_y)):
    plt.scatter(zzzz, yuce_y[zzzz], color='b')

plt.show()