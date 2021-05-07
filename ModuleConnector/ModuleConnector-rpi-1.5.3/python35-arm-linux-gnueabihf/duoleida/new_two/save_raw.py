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
load_r1=sio.loadmat('C:/Users/yyb/Desktop/track/radar1_2.mat')
r1=load_r1['radar1']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/track/radar2_2.mat')
r2=load_r2['radar2']
load_r3=sio.loadmat('C:/Users/yyb/Desktop/track/radar3_2.mat')
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

yuce_x=[]
yuce_xx=[]
yuce_xxx=[]
yuce_y=[]
quan=[]
fig=plt.figure()
h=0
km1 = Kalman(1.0, 0)

lcs1=1.1
lcs2=3.8
rang1=0
rang2=0
####################################################################
km2=Kalman(1.1,0)
km3=Kalman(3.8,0)
renshu=2
result=[]
for i in range(380):
    print("==========="+str(i)+"===========")
    mmii1 = []
    mmii2 = []
    mmii1_na = []
    mmii2_na = []
    wg1=[]
    wg2=[]

    PD1=PureData1[i+h,:]

    PD2=PureData2[i+h,:]

    PD3=PureData3[i+h,:]
    PD1=np.reshape(PD1,[1,-1])
    PD2 = np.reshape(PD2, [1, -1])
    PD3 = np.reshape(PD3, [1, -1])
    a3,a2,a1=newnew_multi.l_m(PD1,PD2,PD3,M,L)
    a3=np.array(a3)
    a3=a3/156.0
    result.append(a3)
file = open('C:/Users/yyb/Desktop/brs/radar_raw1.txt', 'w')
for fp in result:
    file.write(str(fp))
    file.write('\n')
file.close()



