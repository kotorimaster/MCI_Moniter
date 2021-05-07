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
load_r1=sio.loadmat('C:/Users/yyb/Desktop/brs/g11.mat')
r1=load_r1['radar1']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/brs/g22.mat')
r2=load_r2['radar2']
load_r3=sio.loadmat('C:/Users/yyb/Desktop/brs/g33.mat')
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
PD1=PureData1[110,:]

PD2=PureData2[250,:]

PD3=PureData3[110,:]
PD1=np.reshape(PD1,[-1])
PD2 = np.reshape(PD2, [ -1])
PD3 = np.reshape(PD3, [ -1])
PD3=PD3.tolist()
PD2=PD2.tolist()
PD1=PD1.tolist()
print(PD3)
plt.plot(PD2)









#
# for zzz in range(len(yuce_xx)):
#     plt.scatter(zzz, yuce_xx[zzz], color='g')
# for zzzz in range(len(yuce_xxx)):
#     plt.scatter(zzzz, yuce_xxx[zzzz], color='b')
# file=open('C:/Users/yyb/Desktop/brs/radar_lw_1.txt','w')
# for fp in result:
# 	file.write(str(fp))
# 	file.write('\n')
# file.close()

# for zzz in range(len(yuce_x)):
#     plt.scatter(zzz, yuce_x[zzz], color='b')
# for zzzz in range(len(yuce_y)):
#     plt.scatter(zzzz, yuce_y[zzzz], color='b')

plt.show()