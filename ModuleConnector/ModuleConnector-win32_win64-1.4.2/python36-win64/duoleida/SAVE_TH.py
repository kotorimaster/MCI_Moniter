#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" \example xep_example.py

This is an example of how to use the XEP interface from python.
"""
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

def try_xep(start,i,com):
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
        xep.x4driver_set_downconversion(1);

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
        xep.x4driver_set_fps(20);
        save2 = np.ones((1000, 191))
        print(i+" wait")


        for jj in range(1000):
            frame2 = read_frame()
            save2[jj, 0:190] = frame2
            ll2=time.clock()-start
            save2[jj, -1] = ll2
            print(jj)

        # Reset module
        sio.savemat('C:/Users/yyb/Desktop/xintiao/4.mat', {'radar': save2})
        xep.module_reset()


def main():
    global start_time
    start_time=time.clock()
    aaa = time.clock()
    t1 = threading.Thread(name="1", target=try_xep, args=( aaa,"1","com3"))
    # t2 = threading.Thread(name="2", target=try_xep, args=(aaa,"2","com13"))
    # t3 = threading.Thread(name="3", target=try_xep, args=(aaa,"3","com7"))
    # t4 = threading.Thread(name="4", target=try_xep, args=(aaa,"4","com8"))

    t1.start()
    # print('*****')
    # t2.start()
    # t3.start()
    # t4.start()


if __name__ == "__main__":
    main()