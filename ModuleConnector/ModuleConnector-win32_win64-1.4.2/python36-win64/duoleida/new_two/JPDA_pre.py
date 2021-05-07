#-*-coding:utf-8 -*-
import scipy.io as sio
import pca_filter
import numpy as np
import matplotlib.pyplot as plt
from sympy import*
import newnew_multi
load_r1=sio.loadmat('C:/Users/yyb/Desktop/track/radar1_1.mat')
r1=load_r1['radar1']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/track/radar2_1.mat')
r2=load_r2['radar2']
load_r3=sio.loadmat('C:/Users/yyb/Desktop/track/radar3_1.mat')
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

quan=[]
fig=plt.figure()
h=1

for i in range(100):
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
    a1,a2,a3=newnew_multi.l_m(PD1,PD2,PD3,M,L)
    a3=np.array(a3)
    a3=a3/156.0
    quan.append(a3)


    a3=np.reshape(a3,[a3.shape[0],1])

    a3_list=a3.tolist()
    for jjjj in range(len(a3_list)):
        plt.scatter(i,a3_list[jjjj], color='r')



plt.show()