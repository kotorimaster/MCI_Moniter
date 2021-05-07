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
import max_two
import liangyuan
import youhua

load_r1=sio.loadmat('C:/Users/yyb/Desktop/tiaoshi/r1.mat')
r1=load_r1['radar1']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/tiaoshi/r2.mat')
r2=load_r2['radar2']

M=10
L=100
RawData1=r1[:,0:750]
RawData2=r2[:,0:750]

###后截250
PureData1=pca_filter.p_f(RawData1,M,L)
PureData2=pca_filter.p_f(RawData2,M,L)

####################################################################
xl = np.arange(0, 13, 2)
yuce_x=[]
yuce_xx=[]
yuce_xxx=[]
yuce_y=[]
quan=[]
fig=plt.figure()
h=50


##########################################################

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

jingjiecount1=0
jingjiecount2=0
zf1=-1
zf2=-1
prexiao2=2.0
preda2=2.5
prexiao1=1
preda1=3
km22=Kalman(2.0,0)
km33=Kalman(2.5,0)
km2=Kalman(1,0)
km3=Kalman(3,0)
weihu1=np.zeros(15)
weihu2=np.zeros(15)
weihu11=np.zeros(15)
weihu22=np.zeros(15)

jingjie1 = np.zeros(15)
jingjie2 = np.zeros(15)
jingjie11 = np.zeros(15)
jingjie22 = np.zeros(15)
precha1=0
precha2=0
chaflag1=0
chaflag2=0
prek1=0
prek2=0
prek11=0
prek22=0
chixu1=0
chixu2=0
xl = np.arange(0, 4.5, 0.5)
yl = np.arange(-4.5, 0, 0.5)
for ijj in range(40):


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
    xiao1,da1=max_two.mt(PD1)
    xiao2, da2 = max_two.mt(PD2)
    xiao1,da1,prexiao1,preda1=youhua.yh(xiao1,da1,prexiao1,preda1)
    xiao2, da2,prexiao2,preda2 = youhua.yh(xiao2, da2, prexiao2, preda2)
    km2.z = np.array([xiao1])
    km2.kf_update()
    km3.z = np.array([da1])
    km3.kf_update()
    km22.z = np.array([xiao2])
    km22.kf_update()
    km33.z = np.array([da2])
    km33.kf_update()

    if (ijj < 10):
        weihu1[ijj]=km2.x[0, 0]
        weihu2[ijj] = km3.x[0, 0]
        weihu11[ijj] = km22.x[0, 0]
        weihu22[ijj] = km33.x[0, 0]
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
        weihu11[0] = weihu11[1]
        weihu11[1] = weihu11[2]
        weihu11[2] = weihu11[3]
        weihu11[3] = weihu11[4]
        weihu11[4] = weihu11[5]
        weihu11[5] = weihu11[6]
        weihu11[6] = weihu11[7]
        weihu11[7] = weihu11[8]
        weihu11[8] = weihu11[9]
        weihu11[9] = weihu11[10]
        weihu11[10] = weihu11[11]
        weihu11[11] = weihu11[12]
        weihu11[12] = weihu11[13]
        weihu11[13] = weihu11[14]
        weihu11[14] = km22.x[0, 0]
        weihu22[0] = weihu22[1]
        weihu22[1] = weihu22[2]
        weihu22[2] = weihu22[3]
        weihu22[3] = weihu22[4]
        weihu22[4] = weihu22[5]
        weihu22[5] = weihu22[6]
        weihu22[6] = weihu22[7]
        weihu22[7] = weihu22[8]
        weihu22[8] = weihu22[9]
        weihu22[9] = weihu22[10]
        weihu22[10] = weihu22[11]
        weihu22[11] = weihu22[12]
        weihu22[12] = weihu22[13]
        weihu22[13] = weihu22[14]
        weihu22[14] = km33.x[0, 0]

    if (abs(km2.x[0, 0] - km3.x[0, 0]) < 0.1 and precha1<0.1):

        if (jingjiecount1 == 0):
            prek1 = (weihu1[14] - weihu1[0])
            prek2 = (weihu2[14] - weihu2[0])
            chaflag1 = 1
        jingjiecount1 = jingjiecount1 + 1

        precha1 = (km2.x[0, 0] - km3.x[0, 0])

    if (abs(km22.x[0, 0] - km33.x[0, 0]) < 0.1 and precha2<0.1):
        if (jingjiecount2 == 0):
            prek11 = (weihu11[14] - weihu11[0])
            prek22 = (weihu22[14] - weihu22[0])
            chaflag2 = 1
        jingjiecount2 = jingjiecount2 + 1

        precha2 = (km22.x[0, 0] - km33.x[0, 0])

    # if (jingjiecount1 > 5 and (weihu2[4]-weihu2[0])*(weihu1[4]-weihu1[0])<0):
    #     print("^%$!@%^#!&#@&#)!(@&#)@(&#()!&#)(&@(")
    #     zf1 = zf1 * -1
    #     jingjiecount1 = 0
    # if (jingjiecount2 > 5 and (weihu22[4]-weihu22[0])*(weihu11[4]-weihu11[0])<0):
    #     zf2 = zf2 * -1
    #     jingjiecount2 = 0

    if (abs(km2.x[0, 0] - km3.x[0, 0]) > 0.1 and precha1 < 0.1 and chaflag1 == 1):
        jingjie1[chixu1] = km2.x[0, 0]
        jingjie2[chixu1] = km3.x[0, 0]
        chixu1 = chixu1 + 1
        print("(*&)(^%*%&)(%(^$^&$(*&)(")
        print(chixu1)
        if (chixu1 == 15):
            print("(*&)(^%*%&)(%(^$^&$(*&)(")
            print(jingjie1)
            print(jingjie2)

            print("(*&)(^%*%&)(%(^$^&$(*&)(")
            chixu1 = 0
            chaflag1 = 0
            precha1 = 0
            jingjiecount1 = 0
            jingjiek1 = jingjie1[14] - jingjie1[0]
            jingjiek2 = jingjie2[14] - jingjie2[0]
            if ((jingjiek1 * prek2 > 0 and jingjiek1 * prek1 < 0) or (jingjiek2 * prek1 > 0 and jingjiek2 * prek2 < 0)):
                zf1 = zf1 * -1
            prek1 = 0
            prek2 = 0
            jingjie1[0] = 0
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


    if (abs(km22.x[0, 0] - km33.x[0, 0]) > 0.1 and precha2 < 0.1 and chaflag2 == 1):
        jingjie11[chixu2] = km22.x[0, 0]
        jingjie22[chixu2] = km33.x[0, 0]
        chixu2 = chixu2 + 1
        print("(*&)(^%*%&)(%(^$^&$(*&)(")
        print(chixu2)
        if (chixu2 == 15):
            print("(*&)(^%*%&)(%(^$^&$(*&)(")
            print(jingjie11)
            print(jingjie22)

            print("(*&)(^%*%&)(%(^$^&$(*&)(")
            chixu2 = 0
            chaflag2 = 0
            precha2 = 0
            jingjiecount2 = 0
            jingjiek11 = jingjie11[14] - jingjie11[0]
            jingjiek22 = jingjie22[14] - jingjie22[0]
            if ((jingjiek11 * prek22 > 0 and jingjiek11 * prek11 < 0) or (jingjiek22 * prek11 > 0 and jingjiek22 * prek22 < 0)):
                zf2 = zf2 * -1
            prek11 = 0
            prek22 = 0
            jingjie11[0] = 0
            jingjie11[1] = 0
            jingjie11[2] = 0
            jingjie11[3] = 0
            jingjie11[4] = 0
            jingjie11[5] = 0
            jingjie11[6] = 0
            jingjie11[7] = 0
            jingjie11[8] = 0
            jingjie11[9] = 0
            jingjie11[10] = 0
            jingjie11[11] = 0
            jingjie11[12] = 0
            jingjie11[13] = 0
            jingjie11[14] = 0

            jingjie22[0] = 0
            jingjie22[1] = 0
            jingjie22[2] = 0
            jingjie22[3] = 0
            jingjie22[4] = 0
            jingjie22[5] = 0
            jingjie22[6] = 0
            jingjie22[7] = 0
            jingjie22[8] = 0
            jingjie22[9] = 0
            jingjie22[10] = 0
            jingjie22[11] = 0
            jingjie22[12] = 0
            jingjie22[13] = 0
            jingjie22[14] = 0
    #################################################################################################################
    if(zf1==1):
        ra1=km2.x[0, 0]
        ra2=km3.x[0, 0]
    else:
        ra1 = km2.x[0, 0]
        ra2 = km3.x[0, 0]

    if (zf2 == 1):
        rb1 = km22.x[0, 0]
        rb2 = km33.x[0, 0]
    else:
        rb1 = km22.x[0, 0]
        rb2 = km33.x[0, 0]



    # plt.scatter(ijj, rb1, color='r')
    # plt.scatter(ijj, rb2, color='b')

    # xlab1,ylab1=liangyuan.ly(xiao1,xiao2)
    # xlab4, ylab4 = liangyuan.ly(da1, da2)

    xlab2, ylab2 = liangyuan.ly(ra2, rb1)
    xlab3, ylab3 = liangyuan.ly(ra1, rb2)
    print("()()(()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()(")

    print (str(xlab2) + "()()()()()()()()()()()" + str(ylab2))
    print (str(xlab3) + "()()()()()()()()()()()" + str(ylab3))

    print("()()(()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()()(")
    #
    plt.scatter(xlab2, ylab2, color='r')
    plt.scatter(xlab3, ylab3, color='b')
    plt.xticks(xl)
    plt.yticks(yl)

#################################################################################################################


plt.show()