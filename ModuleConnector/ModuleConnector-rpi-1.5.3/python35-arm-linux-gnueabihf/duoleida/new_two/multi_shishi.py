#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import multi_filter
import threading
import numpy as np
from numpy import *
import data_fusion
from Tkinter import *
import pymoduleconnector
from pymoduleconnector import ModuleConnector
from pymoduleconnector.ids import *
from optparse import OptionParser
import sys
import time
from pymoduleconnector import create_mc
import matplotlib.pyplot as plt
import threading
import scipy.io as sio
import pca_filter
import random
from Tkinter import *
import newnew_multi
from kalman import *
import cmath
from gmphd import *

flag1 = 0
flag2 = 0
flag3 = 1
tmp1 = []
tmp2 = []
tmp3 = []
tmp1 = np.array(tmp1)
tmp2 = np.array(tmp2)
tmp3 = np.array(tmp3)

M = 0
L = 150
banjing=4

def x1(con, start, i, com):
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
            save1 = np.ones((1, 751))

            for jj in range(1):
                frame2 = read_frame()

                save1[jj, 0:750] = frame2
                ll2 = time.clock() - start
                save1[jj, -1] = ll2

            RawData1 = save1[:, 0:750]
            PureData1 = pca_filter.p_f(RawData1, M, L)
            tmp1 = PureData1
            con.wait()
            con.release()
        xep.module_reset()


def x2(con, start, i, com):
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


def x3(con, start, i, com):
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
            tmp3 = PureData3
            con.wait()
            con.release()
        xep.module_reset()


con = threading.Condition()
t1 = threading.Thread(name="1", target=x1, args=(con, 1, "1", "com10"))
t2 = threading.Thread(name="2", target=x2, args=(con, 1, "2", "com7"))
t3 = threading.Thread(name="3", target=x3, args=(con, 1, "3", "com8"))

t1.start()

t2.start()

t3.start()

########################################################################
tk = Tk()
length = 700
canvas = Canvas(tk, width=length, height=length)
canvas.pack()
r1 = canvas.create_rectangle(390, 680, 410, 700, fill="red")
r11 = canvas.create_rectangle(390, 680, 410, 700, fill="red")

d1 = canvas.create_rectangle(240, 670, 260, 690, fill="blue")
d2 = canvas.create_rectangle(390, 670, 410, 690, fill="blue")
d3 = canvas.create_rectangle(540, 670, 560, 690, fill="blue")

for i in range(8):
    canvas.create_line(100 * i, 0, 100 * i, 700, width=1)
for i in range(6):
    canvas.create_line(0, 100 * i, 800, 100 * i, width=1)

ycl = 0
leji1 = np.zeros((1, 550))
leji2 = np.zeros((1, 550))
leji3 = np.zeros((1, 550))
x_p = 0
y_p = 0
x_p2 = 0
y_p2 = 0
quan = []
lcs11 = 1.0
lcs21 = 3.7
rang11 = 0
rang21 = 0

lcs12 = 2.5
lcs22 = 3.1
rang12 = 0
rang22 = 0

lcs13 = 1.36
lcs23 = 3.1
rang13 = 0
rang23 = 0

km11 = Kalman(1.0, 0)
km21 = Kalman(3.7, 0)
km12 = Kalman(2.5, 0)
km22 = Kalman(3.1, 0)
km13 = Kalman(1.36, 0)
km23 = Kalman(3.1, 0)
chushi_xa=-0.75
chushi_ya=0.76
chushi_xb=1
chushi_yb=3.19
kmxa = Kalman(chushi_xa, 0)
kmya = Kalman(chushi_ya, 0)
kmxb = Kalman(chushi_xb, 0)
kmyb = Kalman(chushi_yb, 0)
while (True):
    ttmm1 = []
    ttmm2 = []
    ttmm3 = []
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
    con.acquire()
    ########################################################################
    if (tmp1 != [] and tmp2 != [] and tmp3 != [] and ycl < 100):
        print(tmp1.shape)
        print(tmp1.shape)
        print(tmp1.shape)
        tmp1 = np.reshape(tmp1, [1, 550])
        tmp2 = np.reshape(tmp2, [1, 550])
        tmp3 = np.reshape(tmp3, [1, 550])
        leji1 = np.vstack((leji1, tmp1))
        leji2 = np.vstack((leji2, tmp2))
        leji3 = np.vstack((leji3, tmp3))
        # print(ycl)

        ycl = ycl + 1
        print(ycl)
        tmp1 = []
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

        # i_v1, i_v2, i_v3 = single_new_multi.l_m(PD1, PD2, PD3, M, L)


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

    if (tmp1 != [] and tmp2 != [] and tmp3 != [] and ycl > 100):
        print('start tracking')
        ycl = ycl + 1
        tmp1 = np.reshape(tmp1, [1, 550])
        tmp2 = np.reshape(tmp2, [1, 550])
        tmp3 = np.reshape(tmp3, [1, 550])

        print('￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥')

        leji1 = np.vstack((leji1, tmp1))
        leji2 = np.vstack((leji2, tmp2))
        leji3 = np.vstack((leji3, tmp3))
        print(leji1.shape)
        print(leji2.shape)
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

        a1, a2, a3 = newnew_multi.l_m(PD1, PD2, PD3, M, L)

        a3 = np.array(a3)
        a3 = a3 / 156.0
        quan.append(a3)

        a3 = np.reshape(a3, [a3.shape[0], 1])

        a3_list = a3.tolist()

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
        rang13, rang23, lcs13, lcs23 = multi_filter.multi(a3_list, lcs13, lcs23, rang13, rang23, mmii13, mmii23,
                                                          mmii1_na3,
                                                          mmii2_na3, wg13, wg23)
        rang11, rang21, lcs11, lcs21 = multi_filter.multi(a1_list, lcs11, lcs21, rang11, rang21, mmii11, mmii21,
                                                          mmii1_na1,
                                                          mmii2_na1, wg11, wg21)
        rang12, rang22, lcs12, lcs22 = multi_filter.multi(a2_list, lcs12, lcs22, rang12, rang22, mmii12, mmii22,
                                                          mmii1_na2,
                                                          mmii2_na2, wg12, wg22)

        km11.z = np.array([rang11])
        km11.kf_update()
        km21.z = np.array([rang21])
        km21.kf_update()
        ttmm1.append(km11.x[0, 0])
        ttmm1.append(km21.x[0, 0])
        ttmm1 = np.array(ttmm1)

        km12.z = np.array([rang12])
        km12.kf_update()
        km22.z = np.array([rang22])
        km22.kf_update()
        ttmm2.append(km12.x[0, 0])
        ttmm2.append(km22.x[0, 0])
        ttmm2 = np.array(ttmm2)

        km13.z = np.array([rang13])
        km13.kf_update()
        km23.z = np.array([rang23])
        km23.kf_update()
        ttmm3.append(km13.x[0, 0])
        ttmm3.append(km23.x[0, 0])
        ttmm3 = np.array(ttmm3)

        a = str(ttmm1)
        a = a[1:len(a) - 1]
        aa = a.split()
        b = str(ttmm3)
        b = b[1:len(b) - 1]
        bb = b.split()
        c = str(ttmm2)
        c = c[1:len(c) - 1]
        cc = c.split()
        end_xaa, end_yaa, end_xbb, end_ybb = data_fusion.fu(aa, bb, cc, chushi_xa, chushi_ya, chushi_xb, chushi_yb,
                                                            re_la, re_la_str, chaa, chab, banjing)

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





        te = canvas.create_text((10, 10), text=str(int(10000 * tmp1[0, 2])), anchor=W)
        d1 = canvas.create_rectangle(240, 770, 260, 790, fill="blue")
        d2 = canvas.create_rectangle(390, 770, 410, 790, fill="blue")
        d3 = canvas.create_rectangle(540, 770, 560, 790, fill="blue")
        for i in range(8):
            canvas.create_line(100 * i, 0, 100 * i, 700, width=1)
        for i in range(7):
            canvas.create_line(0, 100 * i, 800, 100 * i, width=1)
        move_x = end_xaa - x_p
        move_y = end_yaa - y_p
        move_x = float(move_x)
        move_y = float(move_y)

        move_x2 = end_xbb - x_p2
        move_y2 = end_ybb - y_p2
        move_x2 = float(move_x2)
        move_y2 = float(move_y2)

        print(move_x * length / 4)
        print(-move_y * length / 4)

        canvas.move(r1, move_x * length / 4, -move_y * length / 4)
        canvas.move(r11, move_x2 * length / 4, -move_y2 * length / 4)

        canvas.move(d1, 0, 0)
        canvas.move(d2, 0, 0)
        canvas.move(d3, 0, 0)

        tk.update()
        time.sleep(0.1)
        x_p = end_xaa
        y_p = end_yaa
        x_p2 = end_xbb
        y_p2 = end_ybb
        canvas.delete()
        tmp1 = []
        tmp2 = []
        tmp3 = []

        con.notifyAll()

    con.release()

tk.mainloop()
