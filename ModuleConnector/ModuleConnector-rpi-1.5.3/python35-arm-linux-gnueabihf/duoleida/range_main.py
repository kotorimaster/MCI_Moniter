#-*-coding:utf-8 -*-
import scipy.io as sio
import cv2
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
load_r1=sio.loadmat('C:/Users/yyb/Desktop/duoren/radar1_1.mat')
r1=load_r1['radar1']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/duoren/radar2_1.mat')
r2=load_r2['radar2']
load_r3=sio.loadmat('C:/Users/yyb/Desktop/duoren/radar3_1.mat')
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
resfac = 0.98
obsntype = 'chirp'  # 'chirp' or 'spect'
transntype = 'vibrato'  # 'fixedvel' or 'vibrato'

survivalprob = 0.98  # 0.95 # 1
clutterintensitytot = 4 # 2 #4   # typical num clutter items per frame
sampling=0.05
transntypes = {
    'fixedvel': array([[1, 1, 0], [0, 1, 0], [0, 0, 1]]),  # simple fixed-velocity state update
    'vibrato': array([[1, 0, sampling*1,0], [0, 1, 0,sampling*1], [0, 0, 1,0],[0, 0, 0,1]])  # simple harmonic motion
}

obsntypes = {
    # 1D spectrum-type - single freq value per bin
    'spect': {'obsnmatrix': array([[1, 0, 1]]),
              'noisecov': [[0.5]],
              'obstospec': array([[1]])
              },
    # 2D chirp-type [start, end]
    'chirp': {'obsnmatrix': array([[1, 0, 0,0], [0, 1, 0,0]]),#观测矩阵
              'noisecov': [[0.5], [0.5]],
              'obstospec': array([[0.5, 0.5]])
              }
}
birthgmm = [GmphdComponent(0.1, [-1.7, 0.2, 0,0], [[0.5, 0, 0,0], [0, 0.5, 0,0], [0, 0, 0.1,0],[0, 0, 0,0.1]]),
            GmphdComponent(0.1,[1.7, 3, 0,0] , [[0.5, 0, 0,0], [0, 0.5, 0,0], [0, 0, 0.1,0],[0, 0, 0,0.1]])]  # fine carpet
transnmatrix = transntypes[transntype]
obsnmatrix = obsntypes[obsntype]['obsnmatrix']
clutterintensity = clutterintensityfromtot(clutterintensitytot, obsntype)
qqq=array([[sampling*sampling*sampling*sampling*1/4, 0, sampling*sampling*sampling*1/2,0], [0,sampling*sampling*sampling*sampling*1/4, 0, sampling*sampling*sampling*1/2], [ sampling*sampling*sampling*1/2, 0, sampling*sampling,0],[0,  sampling*sampling*sampling*1/2, 0, sampling*sampling]])
g = Gmphd(birthgmm, survivalprob, 0.7, transnmatrix,qqq , obsnmatrix,
          obsntypes[obsntype]['noisecov'], clutterintensity)
yuce_x=[]
yuce_y=[]
yuce_x2=[]
yuce_y2=[]
quanbu=[0,0]
####################################################################
d=2
for i in range(4):
    PD1=PureData1[i+d,:]

    PD2=PureData2[i+d,:]

    PD3=PureData3[i+d,:]
    PD1=np.reshape(PD1,[1,-1])
    PD2 = np.reshape(PD2, [1, -1])
    PD3 = np.reshape(PD3, [1, -1])



    a=new_multi.l_m(PD1,PD2,PD3,M,L)
    quanbu = np.vstack((quanbu, a))
    a=np.reshape(a,[a.shape[0],a.shape[1]])

    a_list=a.tolist()

    g.update(a_list)  # here we go!
    g.prune(maxcomponents=50, mergethresh=0.15)
    estitems = g.extractstatesusingintegral(bias=bias)
    estitems=np.array(estitems)

    estitems=np.reshape(estitems,[estitems.shape[0],estitems.shape[1]])
    estitems = np.transpose(estitems)
    obsmatrix = np.array([[1, 0, 1,0], [0, 1, 0,1]])
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
        yuce_x2.append(jieguo[1, 0])
        yuce_y.append(jieguo[0, 1])
        yuce_y2.append(jieguo[1,1])

    # AP=[[0,0],[-1.5*156,1.5*1.732*156],[1.5*156,1.5*1.732*156]]
# AP=np.array(AP)
# rxx,ryy=lse.lse(AP,a,4)
# print(rxx/156)
# print(ryy/156)
print(quanbu[1:,0].shape)
quanbu_x=quanbu[1:,0].tolist()
quanbu_y=quanbu[1:,1].tolist()
fig=plt.figure()
plt.scatter(quanbu_x,quanbu_y,color='b')

plt.scatter(yuce_x2,yuce_y2, color='g')
plt.scatter(yuce_x,yuce_y, color='r')

plt.show()