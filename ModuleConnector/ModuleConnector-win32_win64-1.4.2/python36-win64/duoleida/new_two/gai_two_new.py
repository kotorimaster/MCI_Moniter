#-*-coding:utf-8 -*-
import scipy.io as sio
from kalman import *
import data_fusion
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
import Queue
import multi_filter
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
####################################################################

yuce_x1=[]
yuce_y1=[]
yuce_x2=[]
yuce_y2=[]
yuce_x3=[]
yuce_y3=[]
yuce_xx=[]
yuce_xxx=[]

quan=[]
fig=plt.figure()
h=50
km1 = Kalman(1.0, 0)

lcs11=1.2
lcs21=4.0
rang11=0
rang21=0

lcs12=2.5
lcs22=3.1
rang12=0
rang22=0

lcs13=1.3
lcs23=3.1
rang13=0
rang23=0
####################################################################
km11=Kalman(1.2,0)
km21=Kalman(4.0,0)

km12=Kalman(2.5,0)
km22=Kalman(3.1,0)

km13=Kalman(1.3,0)
km23=Kalman(3.1,0)
renshu=2

area=np.pi*3.8
area2=np.pi*1.5
sudua=Queue.Queue()
sudub=Queue.Queue()
sudua.put(1.05)
sudub.put(3.4)
banjing=4

chushi_xa=-0.75
chushi_ya=0.73
chushi_xb=1
chushi_yb=3.18
xl = np.arange(-2.4, 2.4, 0.2)
yl = np.arange(0, 4.0, 0.2)

kmxa = Kalman(chushi_xa, 0)
kmya = Kalman(chushi_ya, 0)
kmxb = Kalman(chushi_xb, 0)
kmyb = Kalman(chushi_yb, 0)
result1=[]
result2=[]
result3=[]
for i in range(125):
    ttmm1=[]
    ttmm2 = []
    ttmm3 = []
    print("==========="+str(i)+"===========")
    mmii11 = []
    mmii21 = []
    mmii1_na1 = []
    mmii2_na1 = []
    wg11 = []
    wg21 = []

    mmii12 = []
    mmii22 = []
    mmii1_na2 = []
    mmii2_na2 = []
    wg12 = []
    wg22 = []

    mmii13 = []
    mmii23 = []
    mmii1_na3 = []
    mmii2_na3 = []
    wg13 = []
    wg23 = []

    re_la = []
    re_la_str = []
    chaa = []
    chab = []

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


    a2 = np.array(a2)
    a2 = a2 / 156.0
    quan.append(a2)
    a2 = np.reshape(a2, [a2.shape[0], 1])
    a2_list = a2.tolist()


    a1 = np.array(a1)
    a1 = a1 / 156.0
    quan.append(a1)
    a1 = np.reshape(a1, [a1.shape[0], 1])
    a1_list = a1.tolist()
    ###################################################################################
    rang13, rang23, lcs13, lcs23 = multi_filter.multi(a3_list, lcs13, lcs23, rang13, rang23, mmii13, mmii23, mmii1_na3,
                                                      mmii2_na3, wg13, wg23)
    rang11, rang21, lcs11, lcs21 = multi_filter.multi(a1_list, lcs11, lcs21, rang11, rang21, mmii11, mmii21, mmii1_na1,
                                                      mmii2_na1, wg11, wg21)
    rang12, rang22, lcs12, lcs22 = multi_filter.multi(a2_list, lcs12, lcs22, rang12, rang22, mmii12, mmii22, mmii1_na2,
                                                      mmii2_na2, wg12, wg22)


    km11.z = np.array([rang11])
    km11.kf_update()
    km21.z = np.array([rang21])
    km21.kf_update()
    ttmm1.append(km11.x[0, 0])
    ttmm1.append(km21.x[0, 0])
    ttmm1 = np.array(ttmm1)
    print "{}{}{}{}{{}{}{}{}{}{}{}{}{"
    print ttmm1
    km12.z = np.array([rang12])
    km12.kf_update()
    km22.z = np.array([rang22])
    km22.kf_update()
    ttmm2.append(km12.x[0, 0])
    ttmm2.append(km22.x[0, 0])
    ttmm2 = np.array(ttmm2)
    print "{}{}{}{}{{}{}{}{}{}{}{}{}{"
    print ttmm2
    km13.z = np.array([rang13])
    km13.kf_update()
    km23.z = np.array([rang23])
    km23.kf_update()
    ttmm3.append(km13.x[0, 0])
    ttmm3.append(km23.x[0, 0])
    ttmm3 = np.array(ttmm3)
    print "{}{}{}{}{{}{}{}{}{}{}{}{}{"
    print ttmm3
    result1.append(ttmm1)
    result2.append(ttmm2)
    result3.append(ttmm3)

    a = str(ttmm1)
    a = a[1:len(a) - 1]
    aa = a.split()
    b = str(ttmm3)
    b = b[1:len(b) - 1]
    bb = b.split()
    c = str(ttmm2)
    c = c[1:len(c) - 1]
    cc = c.split()
    end_xaa, end_yaa, end_xbb, end_ybb=data_fusion.fu(aa,bb,cc,chushi_xa,chushi_ya,chushi_xb,chushi_yb,re_la,re_la_str,chaa,chab,banjing)



    kmxa.z = np.array([end_xaa])
    kmxa.kf_update()
    kmya.z = np.array([end_yaa])
    kmya.kf_update()
    kmxb.z = np.array([end_xbb])
    kmxb.kf_update()
    kmyb.z = np.array([end_ybb])
    kmyb.kf_update()
    end_xaa = kmxa.x[0, 0]
    end_yaa = kmya.x[0, 0]
    end_xbb = kmxb.x[0, 0]
    end_ybb = kmyb.x[0, 0]

    chushi_xa = end_xaa
    chushi_ya = end_yaa
    chushi_xb = end_xbb
    chushi_yb = end_ybb

    plt.scatter(end_xaa, end_yaa, color='b', s=area)
    plt.xticks(xl)
    plt.yticks(yl)
    plt.grid(True)
    plt.scatter(end_xbb, end_ybb, color='b', s=area)
    plt.xticks(xl)
    plt.yticks(yl)
    plt.grid(True)


    # plt.scatter(i, km12.x[0,0], color='b')
    #
    # plt.scatter(i, km22.x[0, 0], color='b')



# file=open('C:/Users/yyb/Desktop/brs/radar_33333.txt','w')
# for fp in result3:
# 	file.write(str(fp))
# 	file.write('\n')
# file.close()
# file=open('C:/Users/yyb/Desktop/brs/radar_2222.txt','w')
# for fp in result2:
# 	file.write(str(fp))
# 	file.write('\n')
# file.close()
# file=open('C:/Users/yyb/Desktop/brs/radar_1111.txt','w')
# for fp in result1:
# 	file.write(str(fp))
# 	file.write('\n')
# file.close()
plt.show()