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

load_r1=sio.loadmat('C:/Users/yyb/Desktop/2_man_demo/track/radar1_1.mat')
r1=load_r1['radar1']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/2_man_demo/track/radar3_1.mat')
r2=load_r2['radar3']

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
prexiao2=2.8
preda2=2.0
prexiao1=2.9
preda1=3.5
km22=Kalman(2.0,0)
km33=Kalman(2.5,0)
km2=Kalman(1,0)
km3=Kalman(3,0)

xl = np.arange(0, 4.5, 0.5)
yl = np.arange(-4.5, 0, 0.5)
for ijj in range(100):


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
    # plt.scatter(ijj, xiao1, color='y')
    # plt.scatter(ijj, da1, color='y')
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





    # plt.scatter(ijj, xiao2, color='r')
    # plt.scatter(ijj, da2, color='b')



    xlab2, ylab2 = liangyuan.ly(xiao1, da2)
    xlab3, ylab3 = liangyuan.ly(da1, xiao2)

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