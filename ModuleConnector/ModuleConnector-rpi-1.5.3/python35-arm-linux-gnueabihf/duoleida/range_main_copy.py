#-*-coding:utf-8 -*-
import scipy.io as sio

import location_multi
import pca_filter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from sympy import*
import rangr_multi
import lse
import new_multi
from gmphd import *
from scipy.signal.wavelets import cwt, ricker
load_r1=sio.loadmat('C:/Users/yyb/Desktop/duoren/radar1_2.mat')
r1=load_r1['radar1']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/duoren/radar2_2.mat')
r2=load_r2['radar2']
load_r3=sio.loadmat('C:/Users/yyb/Desktop/duoren/radar3_2.mat')
r3=load_r3['radar3']
M=0
L=100
RawData1=r1[:,0:750]
RawData2=r2[:,0:750]
RawData3=r3[:,0:750]
###后截250
PureData1=pca_filter.p_f(RawData1,M,L)
PureData2=pca_filter.p_f(RawData2,M,L)
PureData3=pca_filter.p_f(RawData3,M,L)
####################################################################
span = (0, 60)
slopespan = (-2, 3)  # currently only used for clutter generation / inference
def clutterintensityfromtot(clutterintensitytot, obsntype):
    "from the total clutter, calculate the point-density of it"
    if obsntype == 'spect':
        clutterrange = (span[1] - span[0])
    else:
        clutterrange = (span[1] - span[0]) * (slopespan[1] - slopespan[0])
    return float(clutterintensitytot) / float(clutterrange)
####################################################################
bias = 1 #8   # tendency to prefer false-positives over false-negatives in the filtered output
resfac = 0.95
obsntype = 'chirp'  # 'chirp' or 'spect'
transntype = 'vibrato'  # 'fixedvel' or 'vibrato'
birthprob = 0.05  # 0.05 # 0 # 0.2
survivalprob = 0.95  # 0.95 # 1
clutterintensitytot = 5  # 2 #4   # typical num clutter items per frame
transntypes = {
    'fixedvel': array([[1, 1, 0], [0, 1, 0], [0, 0, 1]]),  # simple fixed-velocity state update
    'vibrato': array([[1 - resfac, 1, 0], [0 - resfac, 1, 0], [0, 0, 1]])  # simple harmonic motion
}

obsntypes = {
    # 1D spectrum-type - single freq value per bin
    'spect': {'obsnmatrix': array([[1, 0, 1]]),
              'noisecov': [[0.5]],
              'obstospec': array([[1]])
              },
    # 2D chirp-type [start, end]
    'chirp': {'obsnmatrix': array([[1, -0.5, 1], [1, 0.5, 1]]),#观测矩阵
              'noisecov': [[0.5], [0.5]],
              'obstospec': array([[0.5, 0.5]])
              }
}
birthgmm = [GmphdComponent(1.0, [x, 0, offset], [[2, 0, 0], [0, 0.1, 0], [0, 0, 3]]) \
            for offset in range(5, 57, 2) for x in range(-4, 6, 2)]  # fine carpet
transnmatrix = transntypes[transntype]
obsnmatrix = obsntypes[obsntype]['obsnmatrix']
clutterintensity = clutterintensityfromtot(clutterintensitytot, obsntype)
g = Gmphd(birthgmm, survivalprob, 0.7, transnmatrix, 1e-9 * array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), obsnmatrix,
          obsntypes[obsntype]['noisecov'], clutterintensity)
yuce_x=[]
yuce_y=[]
####################################################################
for i in range(300):
    PD1=PureData1[i+30,:]

    PD2=PureData2[i+30,:]

    PD3=PureData3[i+30,:]
    PD1=np.reshape(PD1,[1,-1])
    PD2 = np.reshape(PD2, [1, -1])
    PD3 = np.reshape(PD3, [1, -1])



    a=new_multi.l_m(PD1,PD2,PD3,M,L)

    a=np.reshape(a,[a.shape[0],a.shape[1],1])
    a_list=a.tolist()
    print(a_list[1])
    g.update(a_list)  # here we go!
    g.prune(maxcomponents=50, mergethresh=0.15)
    estitems = g.extractstatesusingintegral(bias=bias)
    estitems=np.array(estitems)

    estitems=np.reshape(estitems,[estitems.shape[0],estitems.shape[1]])
    estitems = np.transpose(estitems)
    obsmatrix = np.array([[1, -0.5, 1], [1, 0.5, 1]])
    jieguo = np.dot(obsmatrix, estitems)
    jieguo=np.transpose(jieguo)
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print(jieguo)
    print(jieguo.shape)


    # fig=plt.figure()
    # plt.scatter(jieguo[0],jieguo[1])
    # plt.show()
    if(jieguo[0,0]<5 and jieguo[1, 0]<5 and jieguo[0, 1]<5 and jieguo[1, 1]<5):
        yuce_x.append(jieguo[0,0])
        yuce_x.append(jieguo[1, 0])
        yuce_y.append(jieguo[1, 0])
        yuce_y.append(jieguo[1,1])

    # AP=[[0,0],[-1.5*156,1.5*1.732*156],[1.5*156,1.5*1.732*156]]
# AP=np.array(AP)
# rxx,ryy=lse.lse(AP,a,4)
# print(rxx/156)
# print(ryy/156)
fig=plt.figure()
plt.scatter(yuce_x,yuce_y)
plt.show()