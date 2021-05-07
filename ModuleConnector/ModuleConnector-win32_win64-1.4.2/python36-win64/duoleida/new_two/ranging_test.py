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
from scipy import signal
import liangyuan
import jihuo
load_r1=sio.loadmat('C:/Users/yyb/Desktop/2_man_demo/track/radar3_1.mat')
r1=load_r1['radar3']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/2_man_demo/track/radar3_1.mat')
r2=load_r2['radar3']
load_r3=sio.loadmat('C:/Users/yyb/Desktop/2_man_demo/track/radar3_1.mat')
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
h=1
km1 = Kalman(1.0, 0)
####################################################################
prexiao=3.3
preda=4
km2=Kalman(3.3,0)
km3=Kalman(4,0)
renshu=2
result=[]
area=np.pi*3.8
font = {
    'weight': 'normal',
    'size': 20

}
tmp_dist3 = []
tmp_num3 = []
pnum = float(156)

weihu1=np.zeros(15)
weihu2=np.zeros(15)
jingjie1 = np.zeros(15)
jingjie2 = np.zeros(15)

flagjj=0
jingjiecount=0
prek1=0
prek2=0
zf=1
precha=0
chaflag=0
chixu=0
for ijj in range(140):
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
    PD3 = np.reshape(PD3, [1, -1])
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

        # plt.plot(PD3[0, :].tolist())
        # for iii in range(len(peaked)):
        #     plt.scatter(peaked[iii], PD3[0, peaked[iii]])

        max1=max1+ L + 0.2 * pnum
        max2 = max2 + L + 0.2 * pnum
        max1 = max1 / 156.0
        max2 = max2 / 156.0


    xiao=min(max1,max2)
    da=max(max1,max2)
    # print("()()(()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()(")
    # print(xiao)
    # print(da)
    # print(prexiao-xiao)
    # print(preda-da)
    # print("()()(()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()(")
    plt.scatter(ijj, xiao, color='y')
    plt.scatter(ijj, da, color='y')
    if(abs(prexiao-xiao)>=1):
        if (xiao - prexiao >= 0):
            xiao = prexiao + 0.2*jihuo.jh(xiao - prexiao)
        else:
            xiao = prexiao - 0.2*jihuo.jh(abs(xiao - prexiao))
    if(abs(prexiao-xiao)>0.2 and abs(prexiao-xiao)<1):
        if(xiao-prexiao>=0):
            xiao=prexiao+0.8*jihuo.jh(xiao-prexiao)
        else:
            xiao = prexiao - 0.8*jihuo.jh(abs(xiao - prexiao))

    if (abs(preda - da) >= 1):
        if (da - preda >= 0):
            da = preda + 0.15 * jihuo.jh(da - preda)
        else:
            da = preda - 0.15 * jihuo.jh(abs(da - preda))
    if (abs(preda - da) >= 0.5 and abs(preda-da)<1):
        if (da - preda >= 0):
            da = preda + 0.2*jihuo.jh(da - preda)
        else:
            da = preda - 0.2*jihuo.jh(abs(da - preda))
    if (abs(preda - da) > 0.2 and abs(preda-da)<1):
        if (da - preda >= 0):
            da = preda + 0.7*jihuo.jh(da - preda)
        else:
            da = preda - 0.7*jihuo.jh(abs(da - preda))
    prexiao=xiao
    preda=da
    # plt.scatter(ijj, xiao, color='y')
    # plt.scatter(ijj, da, color='y')
#################################################################################################################
    # xlab1,ylab1=liangyuan.ly(xiao,da)
    # xlab2, ylab2 = liangyuan.ly(da, xiao)
    # xlab3, ylab3 = liangyuan.ly(da, da)
    # xlab4, ylab4 = liangyuan.ly(xiao, xiao)
    # print("()()(()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()(")
    # print (str(xlab1)+"()()()()()()()()()()()"+str(ylab1))
    # print (str(xlab2) + "()()()()()()()()()()()" + str(ylab2))
    # print (str(xlab3) + "()()()()()()()()()()()" + str(ylab3))
    # print (str(xlab4) + "()()()()()()()()()()()" + str(ylab4))
    # print("()()(()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()(")
    # plt.scatter(xlab1,ylab1,color='g')
    # plt.scatter(xlab2, ylab2, color='r')
    # plt.scatter(xlab3, ylab3, color='b')
    # plt.scatter(xlab4, ylab4, color='y')
#################################################################################################################
    # if(abs(xiao-prexiao)>0.4):
    #     xiao=0.9*prexiao+0.1*xiao
    #     prexiao=xiao
    # else:
    #     prexiao=xiao
    # if (abs(da - preda) > 0.3):
    #     da =  preda
    #     preda = da
    # else:
    #     preda=da
    # # plt.scatter(ijj, xiao, color='r')
    # # plt.scatter(ijj, da, color='g')
    km2.z = np.array([xiao])
    km2.kf_update()
    km3.z = np.array([da])
    km3.kf_update()

    if (ijj < 15):
        weihu1[ijj]=km2.x[0, 0]
        weihu2[ijj] = km3.x[0, 0]
    else:
        weihu1[0] = weihu1[1]
        weihu1[1] = weihu1[2]
        weihu1[2] = weihu1[3]
        weihu1[3] = weihu1[4]
        weihu1[4] = weihu1[5]
        weihu1[5] = weihu1[6]
        weihu1[6] = weihu1[7]
        weihu1[7] = weihu1[8]
        weihu1[8] = weihu1[9]
        weihu1[9] = weihu1[10]
        weihu1[10] = weihu1[11]
        weihu1[11] = weihu1[12]
        weihu1[12] = weihu1[13]
        weihu1[13] = weihu1[14]
        weihu1[14] = km2.x[0, 0]
        weihu2[0] = weihu2[1]
        weihu2[1] = weihu2[2]
        weihu2[2] = weihu2[3]
        weihu2[3] = weihu2[4]
        weihu2[4] = weihu2[5]
        weihu2[5] = weihu2[6]
        weihu2[6] = weihu2[7]
        weihu2[7] = weihu2[8]
        weihu2[8] = weihu2[9]
        weihu2[9] = weihu2[10]
        weihu2[10] = weihu2[11]
        weihu2[11] = weihu2[12]
        weihu2[12] = weihu2[13]
        weihu2[13] = weihu2[14]
        weihu2[14] = km3.x[0, 0]

    print(abs(km2.x[0, 0] - km3.x[0, 0]))
    print(precha)
    if(abs(km2.x[0, 0]-km3.x[0, 0])<0.1 and precha<0.1):

        if(jingjiecount==0):
            prek1=(weihu1[14]-weihu1[0])
            prek2=(weihu2[14]-weihu2[0])
            chaflag = 1
        jingjiecount = jingjiecount + 1

        precha=(km2.x[0, 0]-km3.x[0, 0])

    if(abs(km2.x[0, 0]-km3.x[0, 0])>0.1 and precha<0.1 and chaflag==1):
        jingjie1[chixu]=km2.x[0, 0]
        jingjie2[chixu] = km3.x[0, 0]
        chixu=chixu+1
        print("(*&)(^%*%&)(%(^$^&$(*&)(")
        print(chixu)
        if(chixu==15):
            print("(*&)(^%*%&)(%(^$^&$(*&)(")
            print(jingjie1)
            print(jingjie2)

            print("(*&)(^%*%&)(%(^$^&$(*&)(")
            chixu=0
            chaflag=0
            precha=0
            jingjiecount=0
            jingjiek1=jingjie1[14]-jingjie1[0]
            jingjiek2 = jingjie2[14] - jingjie2[0]
            if((jingjiek1*prek2>0 and jingjiek1*prek1<0) or (jingjiek2*prek1>0 and jingjiek2*prek2<0 ) ):
                zf=zf*-1
            prek1=0
            prek2=0
            jingjie1[0]=0
            jingjie1[1] = 0
            jingjie1[2] = 0
            jingjie1[3] = 0
            jingjie1[4] = 0
            jingjie1[5] = 0
            jingjie1[6] = 0
            jingjie1[7] = 0
            jingjie1[8] = 0
            jingjie1[9] = 0
            jingjie1[10] = 0
            jingjie1[11] = 0
            jingjie1[12] = 0
            jingjie1[13] = 0
            jingjie1[14] = 0

            jingjie2[0] = 0
            jingjie2[1] = 0
            jingjie2[2] = 0
            jingjie2[3] = 0
            jingjie2[4] = 0
            jingjie2[5] = 0
            jingjie2[6] = 0
            jingjie2[7] = 0
            jingjie2[8] = 0
            jingjie2[9] = 0
            jingjie2[10] = 0
            jingjie2[11] = 0
            jingjie2[12] = 0
            jingjie2[13] = 0
            jingjie2[14] = 0


    # if(zf==1):
    #     plt.scatter(ijj, km2.x[0, 0], color='r')
    #     plt.scatter(ijj, km3.x[0, 0], color='b')
    # if (zf == -1):
    #     plt.scatter(ijj, km2.x[0, 0], color='b')
    #     plt.scatter(ijj, km3.x[0, 0], color='r')


#
#
#
# plt.plot(a3_list)
# print(len(a3_list))

plt.show()