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
yl = np.arange(0, 5, 0.5)

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
prexiao1=2
preda1=2.5
prexiao2=1
preda2=3
area=np.pi*20
while (True):

    con.acquire()
    ########################################################################
    if(tmp1!=[] and tmp2!=[] and ycl<100 ):



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
        km2 = Kalman(2, 0)
        km3 = Kalman(2.5, 0)
        km22 = Kalman(1, 0)
        km33 = Kalman(3, 0)


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
        # xiao1, da1, prexiao1, preda1 = youhua.yh(xiao1, da1, prexiao1, preda1)
        # xiao2, da2, prexiao2, preda2 = youhua.yh(xiao2, da2, prexiao2, preda2)



        ####################################################


        # plt.clf()

        # plt.scatter(xlab2, ylab2, color='r',s=area)
        # plt.scatter(xlab3, ylab3, color='b',s=area)
        # for ii in range(8):
        #     for iii in range(8):
        #         plt.text(iii*0.5-1.77,4-0.25-ii*0.5,str(ii*8+iii+1),fontdict={'size':15})
        plt.scatter(ijj, xiao2, color='r')
        plt.scatter(ijj, da2, color='b')
        # plt.scatter(xlab2, ylab2, color='r')
        # plt.scatter(xlab3, ylab3, color='b')

        # plt.xticks(xl)
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




