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
import single_new_new
from gmphd_single import *
import time
from scipy.signal.wavelets import cwt, ricker
import single_new_multi
load_r1=sio.loadmat('C:/Users/yyb/Desktop/brs/s1.mat')
r1=load_r1['radar1']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/brs/s2.mat')
r2=load_r2['radar2']
load_r3=sio.loadmat('C:/Users/yyb/Desktop/brs/s3.mat')
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

lcs1=1.2
lcs2=4
rang1=0
rang2=0
####################################################################
km2=Kalman(1.2,0)
km3=Kalman(4,0)
renshu=2
result=[]
area=np.pi*3.8
i_PD1 = PureData1[0 + h, :]

i_PD2 = PureData2[0 + h, :]

i_PD3 = PureData3[0 + h, :]
i_PD1 = np.reshape(i_PD1, [1, -1])
i_PD2 = np.reshape(i_PD2, [1, -1])
i_PD3 = np.reshape(i_PD3, [1, -1])
i_v1, i_v2, i_v3 = single_new_multi.l_m(i_PD1, i_PD2, i_PD3, M, L)
km=Kalman(i_v1,0)
km2=Kalman(i_v2,0)
km3=Kalman(i_v3,0)
for i in range(450):

    print("==========="+str(i)+"===========")


    PD1=PureData1[i+h,:]

    PD2=PureData2[i+h,:]

    PD3=PureData3[i+h,:]
    PD1=np.reshape(PD1,[1,-1])
    PD2 = np.reshape(PD2, [1, -1])
    PD3 = np.reshape(PD3, [1, -1])
    # a2,a1,a3=single_new_new.l_m(PD1,PD2,PD3,M,L)
    a11, a22, a33 = single_new_multi.l_m(PD1, PD2, PD3, M, L)
    km.z = np.array([a11])
    km.kf_update()
    km2.z = np.array([a22])
    km2.kf_update()
    km3.z = np.array([a33])
    km3.kf_update()

    a33=np.array(a33)
    a33=a33/156.0
    a33=np.reshape(a33,[a33.shape[0],1])
    a33_list=a33.tolist()
    a11 = np.array(a11)
    a11 = a11 / 156.0
    a11 = np.reshape(a11, [a11.shape[0], 1])
    a11_list = a11.tolist()
    a22 = np.array(a22)
    a22 = a22 / 156.0
    a22 = np.reshape(a22, [a22.shape[0], 1])
    a22_list = a22.tolist()



    print(km.x[0, 0])
    print(km2.x[0, 0])
    print(km3.x[0, 0])
    print('##################')
    jg = km.x[0, 0] / 156
    jg2 = km2.x[0, 0] / 156
    jg3 = km3.x[0, 0] / 156


    for jjjj in range(len(a11_list)):
        plt.scatter(i,a11_list[jjjj], color='r',s=area)

    plt.scatter(i,jg, color='b',s=area)


plt.show()