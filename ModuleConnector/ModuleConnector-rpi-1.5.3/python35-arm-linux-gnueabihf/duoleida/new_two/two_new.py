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
load_r1=sio.loadmat('C:/Users/yyb/Desktop/data/fenbianlv/r1.mat')
r1=load_r1['radar1']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/data/fenbianlv/r11.mat')
r2=load_r2['radar1']
load_r3=sio.loadmat('C:/Users/yyb/Desktop/data/fenbianlv/r111.mat')
r3=load_r3['radar1']
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
h=50
km1 = Kalman(1.0, 0)

lcs1=2.76
lcs2=3.66
rang1=0
rang2=0
####################################################################
km2=Kalman(2.76,0)
km3=Kalman(3.66,0)
renshu=2
result=[]
area=np.pi*3.8
font = {
    'weight': 'normal',
    'size': 20

}
for i in range(430):


    ttmm=[]
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
    a2,a1,a3=newnew_multi.l_m(PD1,PD2,PD3,M,L)
    a3=np.array(a3)
    a3=a3/156.0
    quan.append(a3)


    a3=np.reshape(a3,[a3.shape[0],1])


    a3_list=a3.tolist()
    for jjjj in range(len(a3_list)):
        plt.scatter(i,a3_list[jjjj], color='r',s=area)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.xticks([0,20,40,60,80,100,120],[0,2,4,6,8,10,12])
    sstart = time.clock()
    if(len(a3_list)==1):
        print(a3_list[0][0])
        print("111111111111111111111111111111111111111111111111111")
        wc1=abs(a3_list[0][0]-lcs1)
        wc2 = abs(a3_list[0][0] - lcs2)
        if(wc1>=wc2):
            if(wc2<0.4):
                rang2=a3_list[0][0]
                rang1=lcs1
        else:
            rang2=lcs2
            rang1=a3_list[0][0]
        lcs1=rang1
        lcs2=rang2
        print("////////////////////////////////////////")
        print(rang1)
        print(rang2)
    if (len(a3_list) == 2):
        print("2222222222222222222222222222222222222222")
        wc1 = abs(a3_list[0][0] - lcs1)
        wc2 = abs(a3_list[0][0] - lcs2)
        wc11 = abs(a3_list[1][0] - lcs1)
        wc22 = abs(a3_list[1][0] - lcs2)
        print(lcs1)
        print(lcs2)
        print(a3_list[0][0])
        minmin=min(wc1,wc2,wc11,wc22)
        if(wc1==minmin):
            if(minmin<0.4):
                rang1 = a3_list[0][0]
                if(wc22<0.4):
                    rang2=a3_list[1][0]
                else:
                    rang2=lcs2
            else:
                rang1=lcs1
                rang2=lcs2
        elif(wc2==minmin):
            if (minmin < 0.4):
                rang2 = a3_list[0][0]
                if(wc11<0.4):
                    rang1=a3_list[1][0]
                else:
                    rang1=lcs1
            else:
                rang1 = lcs1
                rang2 = lcs2
        elif (wc11 == minmin):
            if (minmin < 0.4):
                rang1 = a3_list[1][0]
                if(wc2<0.4):
                    rang2=a3_list[0][0]
                else:
                    rang2=lcs2
            else:
                rang1 = lcs1
                rang2 = lcs2
        else:

            if (minmin < 0.4):
                rang2 = a3_list[1][0]
                if(wc1<0.4):
                    rang1=a3_list[0][0]
                else:
                    rang1=lcs1
            else:
                rang1 = lcs1
                rang2 = lcs2


        # if (wc1 <=wc11):
        #     if(wc11<0.4):
        #         rang1 = a3_list[1][0]
        # elif(wc1< wc2):
        #     if (wc1 < 0.4):
        #         rang1 = a3_list[0][0]
        # else:
        #     rang1 = lcs1
        # if (wc2 >= wc22):
        #     if(wc22<0.4):
        #         rang2 = a3_list[1][0]
        # elif(wc2< wc22):
        #     if (wc2 < 0.4):
        #         rang1 = a3_list[0][0]
        # else:
        #     rang2 = lcs2
        lcs1 = rang1
        lcs2 = rang2
        print("////////////////////////////////////////")
        print(lcs1)
        print(lcs2)

    if (len(a3_list) >2):
        print("333333333333333333333333333333333333333")
        print(lcs1)
        print(lcs2)

        for iii in range(len(a3_list)):
            mmii1.append(abs(a3_list[iii][0]-lcs1))
            mmii2.append(abs(a3_list[iii][0] - lcs2))
            mmii1_na.append(a3_list[iii][0] - lcs1)
            mmii2_na.append(a3_list[iii][0] - lcs2)
        th = min(mmii1)
        TT=mmii1.index(th)
        print("------------------------")
        print(TT)

        th2=min(mmii2)
        print(th)
        print(th2)
        for itt in range(1+int((len(a3_list)-2)//1.5)):
            print(mmii1_na)
            print(mmii2_na)
            index1 = mmii1.index(min(mmii1))
            index2 = mmii2.index(min(mmii2))

            if(min(mmii1)<=th*3):

                wg1.append(mmii1_na[index1]+lcs1)

            if (min(mmii2) <= th2*3):

                wg2.append(mmii2_na[index2]+lcs2)
            mmii1.remove(min(mmii1))
            mmii2.remove(min(mmii2))
            mmii1_na.pop(index1)
            mmii2_na.pop(index2)
        junzhi1=0
        junzhi2 = 0
        if(len(wg1)!=0 and len(wg2)!=0):
            print(len(wg2))
            for iiii in range(len(wg1)):
                junzhi1=junzhi1+wg1[iiii]
            for iiiii in range(len(wg2)):
                junzhi2 = junzhi2 + wg2[iiiii]
            if(abs(junzhi1/len(wg1)-lcs1)<0.4):
                rang1=junzhi1/len(wg1)
            else:
                rang1=lcs1
            if (abs(junzhi2 / len(wg2) - lcs2) < 0.4):
                rang2 = junzhi2 / len(wg2)
            else:
                rang2=lcs2
            lcs1 = rang1
            lcs2 = rang2
        else:
            rang1 = lcs1
            rang2 = lcs2
            lcs1 = rang1
            lcs2 = rang2
    print("00000000000000000000000")
    print(rang1)
    print(rang2)
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(lcs1)
    print(lcs2)
    yuce_xx.append(rang2)
    yuce_xxx.append(rang1)

    km2.z = np.array([rang1])
    km2.kf_update()
    km3.z = np.array([rang2])
    km3.kf_update()
    yuce_x.append(km2.x[0,0])
    yuce_y.append(km3.x[0, 0])
    ttmm.append(km2.x[0,0])
    ttmm.append(km3.x[0, 0])
    ttmm=np.array(ttmm)
    result.append(ttmm)
    sstop = time.clock()
    print("_+_+_+_+_+_+_+_+_+_+_+_+_++_+__+__+_+_+")
    print(sstop-sstart)
    print("_-----------------------------------------")


    # plt.scatter(i, km2.x[0,0], color='g')
    # print("&&&&&&&&&&&&&&")
    # print( km2.x[0,0])
    # plt.scatter(i, km3.x[0, 0], color='b')












#
# for zzz in range(len(yuce_xx)):
#     plt.scatter(zzz, yuce_xx[zzz], color='g')
# for zzzz in range(len(yuce_xxx)):
#     plt.scatter(zzzz, yuce_xxx[zzzz], color='b')
# file=open('C:/Users/yyb/Desktop/brss/x11111.txt','w')
# for fp in result:
# 	file.write(str(fp))
# 	file.write('\n')
# file.close()
#
# for zzz in range(len(yuce_x)):
#     plt.scatter(zzz, yuce_x[zzz], color='b')
#     plt.xticks(fontsize=20)
#     plt.yticks(fontsize=20)
#     plt.xticks([0, 20, 40, 60, 80, 100, 120], [0, 2, 4, 6, 8, 10, 12])
# for zzzz in range(len(yuce_y)):
#     plt.scatter(zzzz, yuce_y[zzzz], color='b')
#     plt.xticks(fontsize=20)
#     plt.yticks(fontsize=20)
#     plt.xticks([0, 20, 40, 60, 80, 100, 120], [0, 2, 4, 6, 8, 10, 12])

plt.show()