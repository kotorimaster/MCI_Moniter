#-*-coding:utf-8 -*-
import scipy.io as sio
import single_one
import pca_filter

from sympy import*

import newnew_multi
from gmphd_single import *


load_r2=sio.loadmat('C:/Users/yyb/Desktop/two_radar/r2.mat')
r2=load_r2['radar2']
load_r3=sio.loadmat('C:/Users/yyb/Desktop/two_radar/r3.mat')
r3=load_r3['radar3']
M=10
L=100

RawData2=r2[:,0:750]
RawData3=r3[:,0:750]
###后截250

PureData2=pca_filter.p_f(RawData2,M,L)
PureData3=pca_filter.p_f(RawData3,M,L)
####################################################################

fig=plt.figure()
h=10

for i in range(40):


    ttmm=[]
    print("==========="+str(i)+"===========")
    mmii1 = []
    mmii2 = []
    mmii1_na = []
    mmii2_na = []
    wg1=[]
    wg2=[]

    PD2=PureData2[i+h,:]

    PD3=PureData3[i+h,:]

    PD2 = np.reshape(PD2, [1, -1])
    PD3 = np.reshape(PD3, [1, -1])
    a2,a3=single_one.l_m(PD2,PD3,M,L)
    plt.scatter(i,a2,color='r')
    plt.scatter(i, a3, color='b')

plt.show()