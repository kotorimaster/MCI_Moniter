#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import threading
import numpy as np
from numpy import *
from  Tkinter import *
import pymoduleconnector
from pymoduleconnector import ModuleConnector
from pymoduleconnector.ids import *
from optparse import OptionParser
import sys
import youhua
import liangyuan
import max_two
import time
from pymoduleconnector import create_mc
import matplotlib.pyplot as plt
import threading
import scipy.io as sio
import pca_filter
import random
from Tkinter import *
import single_new_multi
from kalman import *
import cmath
from gmphd import *
plt.ion()
flag1=0
flag2=0
flag3=1
tmp1=[]
tmp2=[]
tmp3=[]
tmp1=np.array(tmp1)
tmp2=np.array(tmp2)
tmp3=np.array(tmp3)

M = 0
L = 100
def x1(con,start,i,com):

    global flag1
    global flag2
    global flag3
    global tmp1
    global tmp2
    global tmp3
    M = 0
    L = 100
    with create_mc(com) as mc:
        print(i+' start')
        xep = mc.get_xep()

        # inti x4driver
        xep.x4driver_init()

        # Set enable pin
        xep.x4driver_set_enable(1);

        # Set iterations
        xep.x4driver_set_iterations(16);
        # Set pulses per step
        xep.x4driver_set_pulses_per_step(256);
        # Set dac step
        xep.x4driver_set_dac_step(1);
        # Set dac min
        xep.x4driver_set_dac_min(949);
        # Set dac max
        xep.x4driver_set_dac_max(1100);
        # Set TX power
        xep.x4driver_set_tx_power(2);

        # Enable downconversion
        xep.x4driver_set_downconversion(0);

        # Set frame area offset
        xep.x4driver_set_frame_area_offset(0.18)
        offset = xep.x4driver_get_frame_area_offset()


        # Set frame area
        xep.x4driver_set_frame_area(0.2, 5)
        frame_area = xep.x4driver_get_frame_area()

        # Set TX center freq
        xep.x4driver_set_tx_center_frequency(3);

        # Set PRFdiv
        xep.x4driver_set_prf_div(16)
        prf_div = xep.x4driver_get_prf_div()


        # Start streaming
        xep.x4driver_set_fps(0.1)
        fps = xep.x4driver_get_fps()



        def read_frame():
            """Gets frame data from module"""
            d = xep.read_message_data_float()
            frame = np.array(d.data)
            # Convert the resulting frame to a complex array if downconversion is enabled
            return frame

        # Stop streaming
        xep.x4driver_set_fps(5)
        print(i + " wait")
        while (True):
            flag1 = 0
            con.acquire()
            save1 = np.ones((1, 751))

            for jj in range(1):

                frame2 = read_frame()

                save1[jj, 0:750] = frame2
                ll2=time.clock()-start
                save1[jj, -1] = ll2


            RawData1 = save1[:, 0:750]
            PureData1 = pca_filter.p_f(RawData1, M, L)
            tmp1=PureData1
            con.wait()
            con.release()
        xep.module_reset()


def x2(con,start,i,com):
    global flag1
    global flag2
    global flag3
    global tmp1
    global tmp2
    global tmp3
    M = 0
    L = 100
    with create_mc(com) as mc:
        print(i + ' start')
        xep = mc.get_xep()

        # inti x4driver
        xep.x4driver_init()

        # Set enable pin
        xep.x4driver_set_enable(1);

        # Set iterations
        xep.x4driver_set_iterations(16);
        # Set pulses per step
        xep.x4driver_set_pulses_per_step(256);
        # Set dac step
        xep.x4driver_set_dac_step(1);
        # Set dac min
        xep.x4driver_set_dac_min(949);
        # Set dac max
        xep.x4driver_set_dac_max(1100);
        # Set TX power
        xep.x4driver_set_tx_power(2);

        # Enable downconversion
        xep.x4driver_set_downconversion(0);

        # Set frame area offset
        xep.x4driver_set_frame_area_offset(0.18)
        offset = xep.x4driver_get_frame_area_offset()


        # Set frame area
        xep.x4driver_set_frame_area(0.2, 5)
        frame_area = xep.x4driver_get_frame_area()


        # Set TX center freq
        xep.x4driver_set_tx_center_frequency(3);

        # Set PRFdiv
        xep.x4driver_set_prf_div(16)
        prf_div = xep.x4driver_get_prf_div()


        # Start streaming
        xep.x4driver_set_fps(0.1)
        fps = xep.x4driver_get_fps()


        def read_frame():
            """Gets frame data from module"""
            d = xep.read_message_data_float()
            frame = np.array(d.data)
            # Convert the resulting frame to a complex array if downconversion is enabled
            return frame

        # Stop streaming
        xep.x4driver_set_fps(5)
        print(i + " wait")
        while (True):
            flag1 = 0
            con.acquire()
            save2 = np.ones((1, 751))

            for jj in range(1):
                frame2 = read_frame()

                save2[jj, 0:750] = frame2
                ll2 = time.clock() - start
                save2[jj, -1] = ll2


            RawData2 = save2[:, 0:750]
            PureData2 = pca_filter.p_f(RawData2, M, L)
            tmp2 = PureData2

            con.wait()
            con.release()
        xep.module_reset()


con = threading.Condition()
t1 = threading.Thread(name="1", target=x1,args=(con,1,"1","com6"))
t2 = threading.Thread(name="2", target=x2,args=(con,1,"2","com4"))


t1.start()

t2.start()



########################################################################


ycl=0
leji1=np.zeros((1,600))
leji2=np.zeros((1,600))

x_p = 0
y_p = 0
xl = np.arange(0, 4.5, 0.5)
yl = np.arange(-4.5, 0, 0.5)

weihu1=np.zeros(15)
weihu2=np.zeros(15)
weihu11=np.zeros(15)
weihu22=np.zeros(15)

jingjie1 = np.zeros(15)
jingjie2 = np.zeros(15)
jingjie11 = np.zeros(15)
jingjie22 = np.zeros(15)
jingjiecount1=0
jingjiecount2=0
zf1=-1
zf2=-1
pnum = float(156)
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
ijj=0
prexiao1=2.5
preda1=3.3
prexiao2=2.3
preda2=3.8
area=np.pi*20
while (True):

    con.acquire()
    ########################################################################
    if(tmp1!=[] and tmp2!=[] and ycl<100 ):
        print(tmp1.shape)

        tmp1=np.reshape(tmp1,[1,600])
        tmp2 = np.reshape(tmp2, [1, 600])

        leji1 = np.vstack((leji1, tmp1))
        leji2 = np.vstack((leji2, tmp2))

        # print(ycl)

        ycl=ycl+1
        print(ycl)
        tmp1=[]
        tmp2 = []

        con.notifyAll()
    if (tmp1 != [] and tmp2 != []  and ycl == 100):
        print('innit')
        ycl = ycl + 1
        tmp1 = np.reshape(tmp1, [1, 600])
        tmp2 = np.reshape(tmp2, [1, 600])


        print('￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥')

        leji1 = np.vstack((leji1, tmp1))
        leji2 = np.vstack((leji2, tmp2))


        leji1 = leji1[1:101, :]
        leji2 = leji2[1:101, :]


        PureData1 = pca_filter.p_f(leji1, M, L)
        PureData2 = pca_filter.p_f(leji2, M, L)

        print(PureData1.shape)
        p1 = PureData1[99, :]
        p2 = PureData2[99, :]

        PD1 = np.reshape(p1, [1, -1])
        PD2 = np.reshape(p2, [1, -1])

        xiao1, da1 = max_two.mt(PD1)
        xiao2, da2 = max_two.mt(PD2)
        xiao1, da1, prexiao1, preda1 = youhua.yh(xiao1, da1, prexiao1, preda1)
        xiao2, da2, prexiao2, preda2 = youhua.yh(xiao2, da2, prexiao2, preda2)
        km2 = Kalman(2.5, 0)
        km3 = Kalman(3.3, 0)
        km22 = Kalman(2.3, 0)
        km33 = Kalman(3.8, 0)


        print(leji1.shape)
        print(leji2.shape)

        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(PureData1.shape)
        print(PureData2.shape)


        tmp1 = []
        tmp2 = []



        con.notifyAll()

    if(tmp1!=[] and tmp2!=[] and ycl>100 ):
        start=time.time()
        ijj=ijj+1
        ycl = ycl + 1
        tmp1 = np.reshape(tmp1, [1, 600])
        tmp2 = np.reshape(tmp2, [1, 600])

        leji1 = np.vstack((leji1, tmp1))
        leji2 = np.vstack((leji2, tmp2))


        leji1=leji1[1:101,:]
        leji2 = leji2[1:101, :]

        PureData1 = pca_filter.p_f(leji1, M, L)
        PureData2 = pca_filter.p_f(leji2, M, L)


        p1=PureData1[99,:]
        p2 = PureData2[99, :]

        PD1 = np.reshape(p1, [1, -1])
        PD2 = np.reshape(p2, [1, -1])

        xiao1, da1 = max_two.mt(PD1)
        xiao2, da2 = max_two.mt(PD2)
        xiao1, da1, prexiao1, preda1 = youhua.yh(xiao1, da1, prexiao1, preda1)
        xiao2, da2, prexiao2, preda2 = youhua.yh(xiao2, da2, prexiao2, preda2)

        end2=time.time()
        #########################################################################################

        km2.z = np.array([xiao1])
        km2.kf_update()
        km3.z = np.array([da1])
        km3.kf_update()
        km22.z = np.array([xiao2])
        km22.kf_update()
        km33.z = np.array([da2])
        km33.kf_update()

        if (ijj < 10):
            weihu1[ijj] = km2.x[0, 0]
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

        if (abs(km2.x[0, 0] - km3.x[0, 0]) < 0.1 and precha1 < 0.1):

            if (jingjiecount1 == 0):
                prek1 = (weihu1[14] - weihu1[0])
                prek2 = (weihu2[14] - weihu2[0])
                chaflag1 = 1
            jingjiecount1 = jingjiecount1 + 1

            precha1 = (km2.x[0, 0] - km3.x[0, 0])

        if (abs(km22.x[0, 0] - km33.x[0, 0]) < 0.1 and precha2 < 0.1):
            if (jingjiecount2 == 0):
                prek11 = (weihu11[14] - weihu11[0])
                prek22 = (weihu22[14] - weihu22[0])
                chaflag2 = 1
            jingjiecount2 = jingjiecount2 + 1

            precha2 = (km22.x[0, 0] - km33.x[0, 0])


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
                if ((jingjiek1 * prek2 > 0 and jingjiek1 * prek1 < 0) or (
                        jingjiek2 * prek1 > 0 and jingjiek2 * prek2 < 0)):
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
                if ((jingjiek11 * prek22 > 0 and jingjiek11 * prek11 < 0) or (
                        jingjiek22 * prek11 > 0 and jingjiek22 * prek22 < 0)):
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
        if (zf1 == 1):
            ra1 = km2.x[0, 0]
            ra2 = km3.x[0, 0]
        else:
            ra1 = km2.x[0, 0]
            ra2 = km3.x[0, 0]

        if (zf2 == 1):
            rb1 = km22.x[0, 0]
            rb2 = km33.x[0, 0]
        else:
            rb1 = km22.x[0, 0]
            rb2 = km33.x[0, 0]


        print(rb1)
        print(ijj)
        xlab2, ylab2 = liangyuan.ly(ra1, rb2)
        xlab3, ylab3 = liangyuan.ly(ra2, rb1)
        print(xlab2)
        print(ylab2)
        print(xlab3)
        print(ylab3)

        ####################################################


        # plt.clf()

        # plt.scatter(xlab2, ylab2, color='r',s=area)
        # plt.scatter(xlab3, ylab3, color='b',s=area)
        # for ii in range(8):
        #     for iii in range(8):
        #         plt.text(iii*0.5-1.77,4-0.25-ii*0.5,str(ii*8+iii+1),fontdict={'size':15})
        # plt.scatter(ijj, ra1, color='r')
        # plt.scatter(ijj, ra2, color='b')
        plt.scatter(xlab2, ylab2, color='r')
        plt.scatter(xlab3, ylab3, color='b')

        plt.xticks(xl)
        plt.yticks(yl)
        plt.grid(True)


        plt.pause(0.0005)
        plt.show()



        tmp1 = []
        tmp2 = []



        con.notifyAll()
        end = time.time()
        print("+++++++++++++++++++++++++++++++++")
        print(end-start)
        print("+++++++++++++++++++++++++++++++++")


    con.release()




