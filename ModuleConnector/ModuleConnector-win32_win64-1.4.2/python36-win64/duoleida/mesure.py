#-*-coding:utf-8 -*-
import scipy.io as sio

import pca_filter
import numpy as np
import matplotlib.pyplot as plt

from sympy import*

import single_new_multi
from gmphd import *
from pykalman import KalmanFilter


load_r1=sio.loadmat('C:/Users/yyb/Desktop/duoleida_ceshi/radar2_three_1.mat')
r1=load_r1['radar2']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/duoleida_ceshi/radar3_two_5.mat')
r2=load_r2['radar3']
load_r3=sio.loadmat('C:/Users/yyb/Desktop/duoleida_ceshi/radar5_one_5.mat')
r3=load_r3['radar5']
M=10
L=100
RawData1=r1[:,0:750]
RawData2=r2[:,0:750]
RawData3=r3[:,0:750]
###后截50
PureData1=pca_filter.p_f(RawData1,M,L)
PureData2=pca_filter.p_f(RawData2,M,L)
PureData3=pca_filter.p_f(RawData3,M,L)
h=0
radar1=[]
radar2=[]
radar3=[]

kf=KalmanFilter(n_dim_obs=1,n_dim_state=1,initial_state_mean=670,initial_state_covariance=8,transition_matrices=[1],observation_matrices=[1],observation_covariance=8,transition_covariance=np.eye(1),transition_offsets=None)

for i in range(180):
    print('jishujishujishujishujishu'+str(i))
    PD1 = PureData1[i + h, :]

    PD2 = PureData2[i + h, :]

    PD3 = PureData3[i + h, :]
    PD1 = np.reshape(PD1, [1, -1])
    PD2 = np.reshape(PD2, [1, -1])
    PD3 = np.reshape(PD3, [1, -1])

    v1, v2, v3 = single_new_multi.l_m(PD1, PD2, PD3, M, L)
    radar1.append(int(v1))
    radar2.append(int(v2))
    radar3.append(int(v3))
radar1=np.array(radar1)
radar2=np.array(radar2)
radar3=np.array(radar3)
r1=int(np.median(radar1) + L + 0.22 * 156)
r2=int(np.median(radar2) + L + 0.22 * 156)
r3=int(np.median(radar3) + L + 0.22 * 156)
print (r1)
print (r2)
print (r3)











