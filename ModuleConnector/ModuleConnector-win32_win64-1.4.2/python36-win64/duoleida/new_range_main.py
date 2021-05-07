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
from scipy.signal.wavelets import cwt, ricker
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

survivalprob = 0.5  # 0.95 # 1
clutterintensitytot = 4 # 2 #4   # typical num clutter items per frame
sampling=0.05
transntypes = {

    'vibrato': array([[1.0,sampling*0.1], [0.0,0.01]])  # simple harmonic motion
}

obsntypes = {

    # 2D chirp-type [start, end]
    'chirp': {'obsnmatrix': array([1.0,1.0]),#观测矩阵
              'noisecov': [0.6]

              }
}
birthgmm = [GmphdComponent(0.1, [x/10,0.0], [[0.5, 0.0],[0.0,0.2]])
           for x in range(0, 50, 1) ]  # fine carpet

# birthgmm = [GmphdComponent(1.0, [x, 0, offset], [[10.0, 0, 0], [0, 0.1, 0], [0, 0, 3]]) \
# 	for offset in range(0, 5, 0.2) for x in range(0, 5, 0.1)]  # fine carpet
transnmatrix = transntypes[transntype]
obsnmatrix = obsntypes[obsntype]['obsnmatrix']
clutterintensity = clutterintensityfromtot(clutterintensitytot, obsntype)
qqq=array([[sampling*sampling*sampling*sampling*1/4, sampling*sampling*sampling*1/2], [sampling*sampling*sampling*1/2,sampling*sampling]])
g = Gmphd(birthgmm, survivalprob, 0.5, transnmatrix,qqq , obsnmatrix,
          obsntypes[obsntype]['noisecov'], clutterintensity)
yuce_x=[]
yuce_y=[]
quan=[]
fig=plt.figure()
h=103
km1 = Kalman(1.0, 0)

####################################################################
for i in range(300):
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

    g.update(a3_list)  # here we go!
    g.prune(maxcomponents=100, mergethresh=0.12)
    estitems = g.extractstatesusingintegral(bias=bias)

    estitems=np.array(estitems)
    print('estitems!!!!!!!!!!!!!!!!11'+str(estitems.shape))

    estitems=np.reshape(estitems,[estitems.shape[0],estitems.shape[1]])
    estitems = np.transpose(estitems)
    obsmatrix = np.array([1.0, 0.0])
    jieguo = np.dot(obsmatrix, estitems)
    jieguo=np.transpose(jieguo)
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print(jieguo)
    print(jieguo.shape)
    for iiii in range(len(a3_list)):
        plt.scatter(i,a3_list[iiii], color='r')


    # fig=plt.figure()
    # plt.scatter(jieguo[0],jieguo[1])
    # plt.show()
    jg=min(jieguo[0],jieguo[1])
    jg_max = max(jieguo[0], jieguo[1])
    km1.z = np.array([jg])
    km1.kf_update()
    jg_k = km1.x[0, 0]



    # for jj in range(2):
    #     plt.scatter(i,jieguo[0], color='g')
    #     #
    #     plt.scatter(i,jieguo[1], color='g')



    # AP=[[0,0],[-1.5*156,1.5*1.732*156],[1.5*156,1.5*1.732*156]]
# AP=np.array(AP)
# rxx,ryy=lse.lse(AP,a,4)
# print(rxx/156)
# print(ryy/156)
#




plt.show()