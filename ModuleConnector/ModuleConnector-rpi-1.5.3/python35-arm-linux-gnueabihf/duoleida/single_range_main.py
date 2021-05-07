#-*-coding:utf-8 -*-
import scipy.io as sio

import pca_filter
import numpy as np
import matplotlib.pyplot as plt

from sympy import*

import single_new_multi
from kalman import *
import cmath
from pykalman import KalmanFilter
from kalman_two import *

load_r1=sio.loadmat('C:/Users/yyb/Desktop/brs/s1.mat')
r1=load_r1['radar1']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/brs/s2.mat')
r2=load_r2['radar2']
load_r3=sio.loadmat('C:/Users/yyb/Desktop/brs/s3.mat')
r3=load_r3['radar3']
M=10
L=100
RawData1=r1[:,0:750]
RawData2=r2[:,0:750]
RawData3=r3[:,0:750]
###后截50
PureData1=pca_filter.p_f(RawData1,M,L)
PureData2=pca_filter.p_f(RawData2,M,L)
PureData3=pca_filter.p_f(RawData3,M,L)
h=10
radar1=[]
radar2=[]
radar3=[]
yuanshi1=[]
yuanshi2=[]
yuanshi3=[]
wucha=0
##############################################
i_PD1 = PureData1[0 + h, :]

i_PD2 = PureData2[0 + h, :]

i_PD3 = PureData3[0 + h, :]
i_PD1 = np.reshape(i_PD1, [1, -1])
i_PD2 = np.reshape(i_PD2, [1, -1])
i_PD3 = np.reshape(i_PD3, [1, -1])

i_v1, i_v2, i_v3 = single_new_multi.l_m(i_PD1, i_PD2, i_PD3, M, L)
km=Kalman(i_v1,0)
km2=Kalman(i_v2,0)
km3=Kalman(i_v3,0)
kmx=Kalman_two(-0.6,0)
kmy=Kalman_two(0.75,0)
def maxmax(x,y,z):
    max=x
    if y>max:
        max=y
    if z>max:
        max=z
    return max
xl = np.arange(-2.2, 2.2, 0.2)
yl = np.arange(0, 5, 0.2)
for i in range(450):
    print('jishujishujishujishujishu'+str(i))
    PD1 = PureData1[i + h, :]

    PD2 = PureData2[i + h, :]

    PD3 = PureData3[i + h, :]
    PD1 = np.reshape(PD1, [1, -1])
    PD2 = np.reshape(PD2, [1, -1])
    PD3 = np.reshape(PD3, [1, -1])

    v1, v2, v3 = single_new_multi.l_m(PD1, PD2, PD3, M, L)
    km.z=np.array([v1])
    km.kf_update()
    km2.z = np.array([v2])
    km2.kf_update()
    km3.z = np.array([v3])
    km3.kf_update()
    print(km.x[0,0])
    print(km2.x[0, 0])
    print(km3.x[0, 0])
    print('##################')
    jg=km.x[0,0]/156
    jg2 = km2.x[0, 0]/156
    jg3= km3.x[0, 0]/156


    yuanshi1.append(v1)
    yuanshi2.append(v2)
    yuanshi3.append(v3)

    radar1.append(float(jg))
    radar2.append(float(jg2))
    radar3.append(float(jg3))

# plt.plot(yuanshi1,'r-')
# plt.plot(yuanshi2,'g-')
# plt.plot(yuanshi3,'b-')
# plt.show()
#########################################################
    a=1.5
    b=-1.5
    x1 = (jg * jg - jg2 * jg2 - a * a) / (2 * a)
    if (jg2 * jg2 - x1 * x1 >= 0):
        y1 = cmath.sqrt(jg2 * jg2 - x1 * x1).real
    else:
        y1 = 0

    # #######################radar1,radar3############################
    x2 = (jg * jg - jg3 * jg3) / (4 * a)
    if (jg * jg - (x2 + a) * (x2 + a) >= 0):
        y2 = cmath.sqrt(jg * jg - (x2 + a) * (x2 + a)).real
    else:
        y2 = 0

    # #######################radar2,radar3############################
    x3 = (jg3 * jg3 - jg2 * jg2 +a*a) / (2 * a)
    if (jg2 * jg2 - x3 * x3 >= 0):
        y3 = cmath.sqrt(jg2 * jg2 - x3 * x3).real
    else:
        y3 = 0
    x = (x1 + x2 + x3) / 3

    y = (y1 + y2 + y3) / 3

    kmx.z = np.array([x])
    kmx.kf_update()
    kmy.z = np.array([y])
    kmy.kf_update()
    xx = kmx.x[0, 0]
    yy=kmy.x[0,0]
    plt.scatter(x,y,color='r')
    plt.scatter(xx, yy, color='g')


    plt.xticks(xl)
    plt.yticks(yl)
    plt.grid(True)
    wucha=(abs(y-3))+wucha
    print('!!!!!!!!!!!!!!!!!!')
    print(abs(y-3))
print('&&&&&&&&&&&&&&&&&&&&&&&&&')
print(wucha/180)
plt.plot([0,0],[1.5,4],'k-')
plt.xticks(xl)
plt.yticks(yl)
plt.show()






