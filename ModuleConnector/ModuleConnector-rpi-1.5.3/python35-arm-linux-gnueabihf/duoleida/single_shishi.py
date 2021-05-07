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
import tkFont
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
L = 150
def x1(con,start,i,com):

    global flag1
    global flag2
    global flag3
    global tmp1
    global tmp2
    global tmp3
    M = 0
    L = 150
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
    L = 150
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

def x3(con,start,i,com):
    global flag1
    global flag2
    global flag3
    global tmp1
    global tmp2
    global tmp3
    M = 0
    L = 150
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
            save3 = np.ones((1, 751))
            con.acquire()
            for jj in range(1):
                frame2 = read_frame()

                save3[jj, 0:750] = frame2
                ll2 = time.clock() - start
                save3[jj, -1] = ll2


            RawData3 = save3[:, 0:750]
            PureData3 = pca_filter.p_f(RawData3, M, L)
            tmp3= PureData3
            con.wait()
            con.release()
        xep.module_reset()

con = threading.Condition()
t1 = threading.Thread(name="1", target=x1,args=(con,1,"1","com3"))
t2 = threading.Thread(name="2", target=x2,args=(con,1,"2","com4"))
t3 = threading.Thread(name="3", target=x3,args=(con,1,"3","com5"))

t1.start()

t2.start()

t3.start()

########################################################################
tk = Tk()
length=600
canvas = Canvas(tk, width=length, height=length)
canvas.pack()
r1=canvas.create_rectangle(290, 575, 310, 595,fill="red")

d1=canvas.create_rectangle(65, 575, 85, 595,fill="blue")
d2=canvas.create_rectangle(290, 575, 310, 595,fill="blue")
d3=canvas.create_rectangle(515, 575, 535, 595,fill="blue")

for i in range(10):
    canvas.create_line(75 * i, 0, 75* i, 600, width=1)
for i in range(10):
    canvas.create_line(0, 75* i, 600, 75 * i, width=1)

ycl=0
leji1=np.zeros((1,550))
leji2=np.zeros((1,550))
leji3=np.zeros((1,550))
x_p = 0
y_p = 0

while (True):

    con.acquire()
    ########################################################################
    if(tmp1!=[] and tmp2!=[] and tmp3!=[] and ycl<100 ):
        print(tmp1.shape)
        print(tmp1.shape)
        print(tmp1.shape)
        tmp1=np.reshape(tmp1,[1,550])
        tmp2 = np.reshape(tmp2, [1, 550])
        tmp3 = np.reshape(tmp3, [1, 550])
        leji1 = np.vstack((leji1, tmp1))
        leji2 = np.vstack((leji2, tmp2))
        leji3 = np.vstack((leji3, tmp3))
        # print(ycl)

        ycl=ycl+1
        print(ycl)
        tmp1=[]
        tmp2 = []

        con.notifyAll()
    if (tmp1 != [] and tmp2 != [] and tmp3 != [] and ycl == 100):
        print('innit')
        ycl = ycl + 1
        tmp1 = np.reshape(tmp1, [1, 550])
        tmp2 = np.reshape(tmp2, [1, 550])
        tmp3 = np.reshape(tmp3, [1, 550])

        print('￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥')

        leji1 = np.vstack((leji1, tmp1))
        leji2 = np.vstack((leji2, tmp2))
        leji3 = np.vstack((leji3, tmp3))
        print(leji3.shape)
        leji1 = leji1[1:101, :]
        leji2 = leji2[1:101, :]
        leji3 = leji3[1:101, :]

        PureData1 = pca_filter.p_f(leji1, M, L)
        PureData2 = pca_filter.p_f(leji2, M, L)
        PureData3 = pca_filter.p_f(leji3, M, L)
        print(PureData1.shape)
        p1 = PureData1[99, :]
        p2 = PureData2[99, :]
        p3 = PureData3[99, :]
        PD1 = np.reshape(p1, [1, -1])
        PD2 = np.reshape(p2, [1, -1])
        PD3 = np.reshape(p3, [1, -1])

        i_v1, i_v2, i_v3 = single_new_multi.l_m(PD1, PD2, PD3, M, L)
        km = Kalman(i_v1, 0)
        km2 = Kalman(i_v2, 0)
        km3 = Kalman(i_v3, 0)


        print(leji1.shape)
        print(leji2.shape)
        print(leji3.shape)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(PureData1.shape)
        print(PureData2.shape)
        print(PureData3.shape)

        tmp1 = []
        tmp2 = []
        tmp3 = []


        con.notifyAll()

    if(tmp1!=[] and tmp2!=[] and tmp3!=[] and ycl>100 ):
        start=time.time()

        ycl = ycl + 1
        tmp1 = np.reshape(tmp1, [1, 550])
        tmp2 = np.reshape(tmp2, [1, 550])
        tmp3 = np.reshape(tmp3, [1, 550])
        leji1 = np.vstack((leji1, tmp1))
        leji2 = np.vstack((leji2, tmp2))
        leji3 = np.vstack((leji3, tmp3))

        leji1=leji1[1:101,:]
        leji2 = leji2[1:101, :]
        leji3 = leji3[1:101, :]
        PureData1 = pca_filter.p_f(leji1, M, L)
        PureData2 = pca_filter.p_f(leji2, M, L)
        PureData3 = pca_filter.p_f(leji3, M, L)

        p1=PureData1[99,:]
        p2 = PureData2[99, :]
        p3 = PureData3[99, :]
        PD1 = np.reshape(p1, [1, -1])
        PD2 = np.reshape(p2, [1, -1])
        PD3 = np.reshape(p3, [1, -1])

        v1, v2, v3 = single_new_multi.l_m(PD1, PD2, PD3, M, L)

        end2=time.time()
        #########################################################################################



        km.z = np.array([v1])
        km.kf_update()
        km2.z = np.array([v2])
        km2.kf_update()
        km3.z = np.array([v3])
        km3.kf_update()

        jg = km.x[0, 0] / 156
        jg2 = km2.x[0, 0] / 156
        jg3 = km3.x[0, 0] / 156
        ####################################################
        a = 1.5
        b = -1.5
        end3 = time.time()
        # #######################radar1,radar2############################
        x1 = (jg * jg - jg2 * jg2 - a * a) / (2 * a)
        if (jg2 * jg2 - x1 * x1 >= 0):
            y1 = cmath.sqrt(jg2 * jg2 - x1 * x1).real
        else:
            y1 = 0

        # #######################radar1,radar3############################
        x2 = (jg * jg - jg3 * jg3 - a * a + b * b) / (2 * a - 2 * b)
        if (jg * jg - (x2 + a) * (x2 + a) >= 0):
            y2 = cmath.sqrt(jg * jg - (x2 + a) * (x2 + a)).real
        else:
            y2 = 0

        # #######################radar2,radar3############################
        x3 = (jg3 * jg3 - jg2 * jg2 - b * b) / (2 * b)
        if (jg2 * jg2 - x3 * x3 >= 0):
            y3 = cmath.sqrt(jg2 * jg2 - x3 * x3).real
        else:
            y3 = 0
        x = (x1 + x2 + x3) / 3

        y = (y1 + y2 + y3) / 3+0.95
        end6= time.time()
        for ii in range(8):
            for iii in range(8):
                te = canvas.create_text(((iii)*75+33, (ii)*75+33), text=str((ii+1)*(iii+1)), anchor=W,font=('Arial',15,'bold'))

        d1 = canvas.create_rectangle(65, 575, 85, 595, fill="blue")
        d2 = canvas.create_rectangle(290, 575, 310, 595, fill="blue")
        d3 = canvas.create_rectangle(515, 575, 535, 595, fill="blue")
        for i in range(10):
            canvas.create_line(75 * i, 0, 75 * i, 600, width=1)
        for i in range(10):
            canvas.create_line(0, 75 * i, 600, 75 * i, width=1)

        canvas.create_line(150, 300, 150, 60 , width=2,fill='green')
        canvas.create_line(450, 300 , 450, 60 , width=2,fill='green')
        canvas.create_line(150, 300 , 450, 300 , width=2,fill='green')
        canvas.create_line(150, 60 , 450, 60 , width=2,fill='green')

        end7 = time.time()
        move_x = x - x_p
        move_y = y - y_p
        move_x=float(move_x)
        move_y = float(move_y)
        canvas.move(r1, move_x * 180, -move_y * 150)

        canvas.move(d1, 0, 0)
        canvas.move(d2, 0, 0)
        canvas.move(d3, 0, 0)
        end9 = time.time()
        tk.update()
        end4 = time.time()


        time.sleep(0.1)
        end5 = time.time()
        x_p = x
        y_p = y
        canvas.delete()
        tmp1 = []
        tmp2 = []
        tmp3 = []


        con.notifyAll()
        end = time.time()
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(end4 - end9)
        print(end9 - end7)

        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    con.release()



tk.mainloop()
