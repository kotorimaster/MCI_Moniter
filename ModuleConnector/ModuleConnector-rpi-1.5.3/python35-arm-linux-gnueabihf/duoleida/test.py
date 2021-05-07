#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import pymoduleconnector
from pymoduleconnector import ModuleConnector
from pymoduleconnector.ids import *
from optparse import OptionParser
import sys
import time
from pymoduleconnector import create_mc
import matplotlib.pyplot as plt
import numpy as np
import threading
import scipy.io as sio
import datetime
import pca_filter
import location_multi
import juli
import random
from Tkinter import *

from matplotlib import animation


l1=0
l2=0
temp1=[]
temp2=[]
flag = 0
def try_xep(con,start,i,com):
    global l1
    global l2
    global temp1
    global temp2
    global flag
    M = 0
    L =150
    # print(datetime.datetime.now())
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
        print('x4driver_get_frame_area_offset returned: ', offset)

        # Set frame area
        xep.x4driver_set_frame_area(0.2, 5)
        frame_area = xep.x4driver_get_frame_area()
        print('x4driver_get_frame_area returned: [', frame_area.start, ', ', frame_area.end, ']');

        # Set TX center freq
        xep.x4driver_set_tx_center_frequency(3);

        # Set PRFdiv
        xep.x4driver_set_prf_div(16)
        prf_div = xep.x4driver_get_prf_div()
        print('x4driver_get_prf_div returned: ', prf_div)

        # Start streaming
        xep.x4driver_set_fps(0.1)
        fps = xep.x4driver_get_fps()
        print('xep_x4driver_get_fps returned: ', fps)


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
            save1 = np.ones((5, 751))
            con.acquire()
            flag=0
            con.wait()
            for jj in range(5):

                frame2 = read_frame()

                save1[jj, 0:750] = frame2
                ll2=time.clock()-start
                save1[jj, -1] = ll2

            print("1")
            RawData1 = save1[:, 0:750]
            PureData1 = pca_filter.p_f(RawData1, M, L)
            # print("PureData1")
            # print(PureData1)
            # print(PureData1.shape)
            temp1=PureData1
            l1=juli.l_m(PureData1,L)
            flag=1

            con.notifyAll()
            con.release()
        xep.module_reset()

def try_xep2(con,start,i,com):
    global l1
    global l2
    global temp1
    global temp2
    global flag
    M = 0
    L = 150
    # print(datetime.datetime.now())
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
        print('x4driver_get_frame_area_offset returned: ', offset)

        # Set frame area
        xep.x4driver_set_frame_area(0.2, 5)
        frame_area = xep.x4driver_get_frame_area()
        print('x4driver_get_frame_area returned: [', frame_area.start, ', ', frame_area.end, ']');

        # Set TX center freq
        xep.x4driver_set_tx_center_frequency(3);

        # Set PRFdiv
        xep.x4driver_set_prf_div(16)
        prf_div = xep.x4driver_get_prf_div()
        print('x4driver_get_prf_div returned: ', prf_div)

        # Start streaming
        xep.x4driver_set_fps(0.1)
        fps = xep.x4driver_get_fps()
        print('xep_x4driver_get_fps returned: ', fps)

        def read_frame():
            """Gets frame data from module"""
            d = xep.read_message_data_float()
            frame = np.array(d.data)
            # Convert the resulting frame to a complex array if downconversion is enabled
            return frame

        # Stop streaming
        xep.x4driver_set_fps(5)
        print(i + " wait")
        while(True):
            save2 = np.ones((5, 751))
            con.acquire()
            for jj in range(5):

                frame2 = read_frame()

                save2[jj, 0:750] = frame2
                ll2=time.clock()-start
                save2[jj, -1] = ll2
            print("2")
            RawData2 = save2[:, 0:750]
            PureData2 = pca_filter.p_f(RawData2, M, L)
            temp2=PureData2
            con.notifyAll()
            con.wait()
            con.release()
        xep.module_reset()


def main():
    global l1
    global l2
    global flag
    global temp1
    global temp2
    M = 0
    L = 150
    global start_time
    start_time=time.clock()
    aaa = time.clock()
    con = threading.Condition()

    t1 = threading.Thread(name="1", target=try_xep, args=(con, aaa,"1","com3"))
    t2 = threading.Thread(name="2", target=try_xep2, args=(con,aaa,"2","com16"))
    # t3=threading.Thread(name="draw", target=draw,args=(con,))
    t1.start()
    print('*****')
    time.sleep(0.01)
    t2.start()
    time.sleep(0.1)
    # print("t3 start***********************************")
    # t3.start()
    #########################################################################
    plt.axis([-3, 3, 0, 5])
    plt.grid(True)
    plt.ion()
    x = [-2, 2]
    y = [0, 0]
    plt.scatter(x, y, color='b')
    while(True):

        if flag==1:
            temp1=np.array(temp1)
            temp2= np.array(temp2)
            print("draw*******************")
            # plt.plot(temp2[1,:])

            r1_len, r2_len, xx, yy = location_multi.l_m(temp1, temp2, M, L)
            print("xx//////////////" + str(xx))
            print("yy//////////////" + str(yy))
            # plt.scatter(x, y, color='b')
            plt.scatter(xx, yy, color='b')
            plt.pause(0.3)

        else:
            continue





   #################################################################################

if __name__ == "__main__":
    main()