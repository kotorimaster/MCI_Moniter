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
        xep.x4driver_set_fps(3)
        print(i + " wait")
        save1 = np.ones((100, 751))

        for jj in range(100):
            print(1)

            frame2 = read_frame()

            save1[jj, 0:750] = frame2
            ll2=time.clock()-start
            save1[jj, -1] = ll2
        print('save1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('save1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('save1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        sio.savemat('C:/Users/yyb/Desktop/ecg2/r111.mat', {'radar1': save1})



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
        xep.x4driver_set_fps(3)
        print(i + " wait")

        flag1 = 0

        save2 = np.ones((100, 751))

        for jj in range(100):
            print(2)
            frame2 = read_frame()

            save2[jj, 0:750] = frame2
            ll2 = time.clock() - start
            save2[jj, -1] = ll2
        print('save2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('save2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('save2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        sio.savemat('C:/Users/yyb/Desktop/ecg2/r222.mat', {'radar2': save2})


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

        save3 = np.ones((300, 751))

        for jj in range(300):
            print(jj)
            frame2 = read_frame()

            save3[jj, 0:750] = frame2
            ll2 = time.clock() - start
            save3[jj, -1] = ll2
        print('save3!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('save3!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('save3!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        sio.savemat('C:/Users/yyb/Desktop/brs/x33333.mat', {'radar3': save3})

        xep.module_reset()

con = threading.Condition()
aaa = time.clock()
t1 = threading.Thread(name="1", target=x1,args=(con,aaa,"1","com11"))
t2 = threading.Thread(name="2", target=x2,args=(con,aaa,"2","com8"))
# t3 = threading.Thread(name="3", target=x3,args=(con,aaa,"3","com5"))
time.sleep(2)
t1.start()
t2.start()
# # #
# t3.start()



