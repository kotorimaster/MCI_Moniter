#-*-coding:utf-8 -*-
import scipy.io as sio
from kalman import *
import location_multi
import pca_filter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from sympy import*
import youhua2
import lse
import newnew_multi
from gmphd_single import *
import time
from scipy.signal.wavelets import cwt, ricker
from scipy import signal
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
xl = np.arange(0, 13, 2)
yuce_x=[]
yuce_xx=[]
yuce_xxx=[]
yuce_y=[]
quan=[]
fig=plt.figure()
h=10
km1 = Kalman(1.0, 0)

lcs1=2.4
lcs2=3.0
rang1=0
rang2=0
####################################################################
prexiao=2.6
preda=3.0
km2=Kalman(2.46,0)
km3=Kalman(3.0,0)
renshu=2
result1=[]
result2=[]
area=np.pi*3.8
font = {
    'weight': 'normal',
    'size': 20

}
tmp_dist3 = []
tmp_num3 = []
pnum = float(156)

for ijj in range(350):


    ttmm=[]
    print("==========="+str(ijj)+"===========")
    mmii1 = []
    mmii2 = []
    mmii1_na = []
    mmii2_na = []
    wg1=[]
    wg2=[]

    PD1=PureData1[ijj+h,:]

    PD2=PureData2[ijj+h,:]

    PD3=PureData3[ijj+h,:]
    PD1=np.reshape(PD1,[1,-1])
    PD2 = np.reshape(PD2, [1, -1])
    PD3 = np.reshape(PD2, [1, -1])
    c3 = PD3.shape
    PD3[PD3 < 0] = 0

    print(c3)

    for i in range(c3[0]):
        peaked = signal.find_peaks_cwt(PD3[i, :], np.arange(5, 30))

        sh = peaked.size
        pr = 0

        for ii in range(sh):
            m = np.argmax(PD3[i, :][max(peaked[ii] - 10, 0):min(peaked[ii] + 10, 600)])
            if (peaked[ii] - 10 < 0):
                pr = 0
            else:
                pr = peaked[ii] - 10

            # print('第'+str(ii)+'次         '+str(m))
            peaked[ii] = m + pr
        print(peaked)
        peaked=peaked.tolist()
        ttmmpp3=[]
        for iii in range(len(peaked)):
            ttmmpp3.append(PD3[0,peaked[iii]])

        max1=peaked[argmax(ttmmpp3)]
        ttmmpp3.remove(ttmmpp3[argmax(ttmmpp3)])
        peaked.remove(max1)
        max2 = peaked[argmax(ttmmpp3)]
        print(max1)
        print(max2)
        # plt.plot(PD3[0, :].tolist())
        # for iii in range(len(peaked)):
        #     plt.scatter(peaked[iii], PD3[0, peaked[iii]])

        max1=max1+ L + 0.2 * pnum
        max2 = max2 + L + 0.2 * pnum
        max1 = max1 / 156.0
        max2 = max2 / 156.0


    xiao=min(max1,max2)
    da=max(max1,max2)
    plt.scatter(ijj, xiao, color='b')
    plt.scatter(ijj, da, color='b')

    ttmmp=[]
    ttmmp.append(xiao)
    ttmmp.append(da)

    xiao, da, prexiao, preda = youhua2.yh(xiao, da, prexiao, preda)
    print(preda)
    plt.scatter(ijj, xiao, color='r')
    plt.scatter(ijj, da, color='r')
    ttmmp2 = []
    ttmmp2.append(xiao)
    ttmmp2.append(da)
    result1.append(ttmmp)
    result2.append(ttmmp2)
    km2.z = np.array([xiao])
    km2.kf_update()
    km3.z = np.array([da])
    km3.kf_update()
    # plt.scatter(ijj, km2.x[0, 0], color='b')
    # plt.scatter(ijj, km3.x[0, 0], color='b')

#
#
#


file = open('C:/Users/yyb/Desktop/two_radar/11.txt', 'w')
for fp in result1:
    file.write(str(fp[0]))
    file.write(' ')
    file.write(str(fp[1]))
    file.write('\n')
file.close()

file = open('C:/Users/yyb/Desktop/two_radar/22.txt', 'w')
for fp in result2:
    file.write(str(fp[0]))
    file.write(' ')
    file.write(str(fp[1]))
    file.write('\n')
file.close()
plt.show()