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
import time
from pymoduleconnector import create_mc
import matplotlib.pyplot as plt
import threading
import scipy.io as sio
import pca_filter
import random
from Tkinter import *
import rangr_multi
import lse
import new_multi
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
t1 = threading.Thread(name="1", target=x1,args=(con,1,"1","com8"))
t2 = threading.Thread(name="2", target=x2,args=(con,1,"2","com4"))
t3 = threading.Thread(name="3", target=x3,args=(con,1,"3","com5"))

t1.start()

t2.start()

t3.start()

########################################################################
tk = Tk()
length=800
canvas = Canvas(tk, width=length, height=length)
canvas.pack()
r1=canvas.create_rectangle(length/2-10, 0, length/2+10, 10,fill="red")
r2=canvas.create_rectangle(length/2-10, 0, length/2+10, 10,fill="red")
d1=canvas.create_rectangle(length/2-10, 0, length/2+10, 10,fill="blue")
d2=canvas.create_rectangle(90, 519, 100, 529,fill="blue")
d3=canvas.create_rectangle(790, 519, 800, 529,fill="blue")
canvas.create_line(0, 1, length, 1, width=2)
canvas.create_line(length/2, 0, length/2, length, width=2)
for i in range(5):
    canvas.create_line(0 + length/4 * i, 0, 0 + length/4 * i, 5, width=1)
for i in range(10):
    canvas.create_line(length/2, length/4 * i, length/2+5, length/4 * i, width=1)
x_p1 = 0
y_p1 = 0
x_p2 = 0
y_p2 = 0
####################################################################
span = (0, 60)
slopespan = (-2, 3)  # currently only used for clutter generation / inference


def clutterintensityfromtot(clutterintensitytot, obsntype):
    "from the total clutter, calculate the point-density of it"
    if obsntype == 'spect':
        clutterrange = (span[1] - span[0])
    else:
        clutterrange = (span[1] - span[0]) * (slopespan[1] - slopespan[0])
    return float(clutterintensitytot) / float(clutterrange)


####################################################################
bias = 1  # 8   # tendency to prefer false-positives over false-negatives in the filtered output
resfac = 0.95
obsntype = 'chirp'  # 'chirp' or 'spect'
transntype = 'vibrato'  # 'fixedvel' or 'vibrato'
birthprob = 0.05  # 0.05 # 0 # 0.2
survivalprob = 0.95  # 0.95 # 1
clutterintensitytot = 10  # 2 #4   # typical num clutter items per frame
transntypes = {
    'fixedvel': array([[1, 1, 0], [0, 1, 0], [0, 0, 1]]),  # simple fixed-velocity state update
    'vibrato': array([[1 - resfac, 1, 0], [0 - resfac, 1, 0], [0, 0, 1]])  # simple harmonic motion
}

obsntypes = {
    # 1D spectrum-type - single freq value per bin
    'spect': {'obsnmatrix': array([[1, 0, 1]]),
              'noisecov': [[0.5]],
              'obstospec': array([[1]])
              },
    # 2D chirp-type [start, end]
    'chirp': {'obsnmatrix': array([[1, -0.5, 1], [1, 0.5, 1]]),  # 观测矩阵
              'noisecov': [[0.5], [0.5]],
              'obstospec': array([[0.5, 0.5]])
              }
}
birthgmm = [GmphdComponent(1.0, [x, 0, offset], [[1, 0, 0], [0, 0.1, 0], [0, 0, 3]]) \
            for offset in range(5, 57, 2) for x in range(-4, 6, 2)]  # fine carpet
transnmatrix = transntypes[transntype]
obsnmatrix = obsntypes[obsntype]['obsnmatrix']
clutterintensity = clutterintensityfromtot(clutterintensitytot, obsntype)
g = Gmphd(birthgmm, survivalprob, 0.7, transnmatrix, 1e-9 * array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
          obsnmatrix,
          obsntypes[obsntype]['noisecov'], clutterintensity)
yuce_x = []
yuce_y = []
####################################################################
while (True):
    con.acquire()
    ########################################################################
    if(tmp1!=[] and tmp2!=[] and tmp3!=[]):

        t_0=tmp1[0,0]

        a = new_multi.l_m(tmp1, tmp2, tmp3, M, L)
        ############################################################################################33
        a = np.reshape(a, [a.shape[0], a.shape[1], 1])
        a_list = a.tolist()
        print(a_list[1])
        print('going to update!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1')
        g.update(a_list)  # here we go!
        g.prune(maxcomponents=20, mergethresh=0.15)
        estitems = g.extractstatesusingintegral(bias=bias)
        estitems = np.array(estitems)

        estitems = np.reshape(estitems, [estitems.shape[0], estitems.shape[1]])
        estitems = np.transpose(estitems)
        obsmatrix = np.array([[1, -0.5, 1], [1, 0.5, 1]])
        jieguo = np.dot(obsmatrix, estitems)
        jieguo = np.transpose(jieguo)

        te = canvas.create_text((10, 10), text=str(int(10000*tmp1[0, 2])), anchor=W)
        xx1=jieguo[0,0]
        yy1=jieguo[0,1]
        xx2=jieguo[1,0]
        yy2=jieguo[1,1]
        move_x1 = xx1 - x_p1
        move_y1 = yy1 - y_p1
        move_x2 = xx2 - x_p2
        move_y2 = yy2 - y_p2
        canvas.move(r1,move_x1*length/4,move_y1*length/4)
        canvas.move(r2, move_x2 * length/4, move_y2 * length/4)
        canvas.move(d1, 0, 0)
        canvas.move(d2, 0, 0)
        canvas.move(d3, 0, 0)

        tk.update()
        time.sleep(0.1)
        x_p1 = xx1
        y_p1 = yy1
        x_p2 = xx2
        y_p2 = yy2

        canvas.delete()

        print('******************************')


        tmp1=[]
        tmp2 = []
        tmp3 = []

        time.sleep(0.0001)
        con.notifyAll()
    con.release()


tk.mainloop()
