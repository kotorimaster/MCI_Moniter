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
from gmphd import *
from numpy import *
import numpy.linalg
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
resfac = 0.95
survivalprob = 0.975 # 0.95 # 1
transnmatrix=array([[1-resfac,1,0], [0-resfac,1,0], [0,0,1]])
obsnmatrix=array([[1, -0.5, 1], [1, 0.5, 1]])
directlystatetospec=[[1.0,0.0,1.0]]
####################################################################
span=(0,60)
yuce_x=[]
yuce_xx=[]
yuce_xxx=[]
yuce_y=[]
quan=[]
fig=plt.figure()
h=50
km1 = Kalman(1.0, 0)

lcs1=1.1
lcs2=3.8
rang1=0
rang2=0
####################################################################
km2=Kalman(1.1,0)
km3=Kalman(3.8,0)

birthgmm = [GmphdComponent(1.0, [x, 0, offset], [[10.0, 0, 0], [0, 0.1, 0], [0, 0, 3]]) \
	for offset in range(0, 50, 2) for x in range(0, 5, 1)]  # fine carpet
g = Gmphd(birthgmm, survivalprob, 0.7, transnmatrix, 1e-9 * array([[1,0,0], [0,1,0], [0,0,1]]), obsnmatrix, [[0.5], [0.5]], 0.0167)

for i in range(1):
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
    a3=a3/15.6
    quan.append(a3)


    a3=np.reshape(a3,[a3.shape[0],1])

    a3_list=a3.tolist()
    print(a3_list)
    a3_ll=np.zeros((len(a3_list),2))
    for hang in range(len(a3_list)):

        a3_ll[hang,0]=float(a3_list[hang][0])
        a3_ll[hang, 1] = float(a3_list[hang][0])
    a3_ll=np.reshape(a3_ll,[-1,2,1])
    a3_ll=a3_ll.tolist()
    a3_ll=[[[20],[24]],[[38],[36]],[[10],[12]],[[52],[56]],[[15],[21]],[[37],[35]],[[11],[11]],[[24],[24]]]
    print("##################")
    print a3_ll
    g.update(a3_ll)
    g.prune(maxcomponents=50, mergethresh=0.15)
    estitems=g.extractstatesusingintegral(bias=2)
    # for jjjj in range(len(a3_list)):
    #     plt.scatter(i,a3_list[jjjj], color='r')
    estitems = np.array(estitems)
    estspec = [0 for _ in range(span[0], span[1])]
    for x in estitems:
        print('x***********&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        bin = int(round(dot(directlystatetospec, x)))  # project state space directly into spec
        if bin > -1 and bin < len(estspec):
            estspec[bin] += 1

    print estspec
