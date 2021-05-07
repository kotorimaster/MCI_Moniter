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

import numpy as np
import threading

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore


def try_xep1():
    log_level = 3
    with create_mc('com5') as mc2:
        # x4m300 = mc.get_x4m300()
        print('1 start')
        # we have to go to manual mode
        ##x4m300.set_sensor_mode(XTS_SM_STOP, 0)
        # x4m300.set_sensor_mode(XTS_SM_MANUAL, 0);

        xep1 = mc2.get_xep()

        # inti x4driver
        xep1.x4driver_init()

        # Set enable pin
        xep1.x4driver_set_enable(1);

        # Set iterations
        xep1.x4driver_set_iterations(16);
        # Set pulses per step
        xep1.x4driver_set_pulses_per_step(256);
        # Set dac step
        xep1.x4driver_set_dac_step(1);
        # Set dac min
        xep1.x4driver_set_dac_min(949);
        # Set dac max
        xep1.x4driver_set_dac_max(1100);
        # Set TX power
        xep1.x4driver_set_tx_power(2);

        # Enable downconversion
        xep1.x4driver_set_downconversion(0);

        # Set frame area offset
        xep1.x4driver_set_frame_area_offset(0.18)
        offset = xep1.x4driver_get_frame_area_offset()
        print('x4driver_get_frame_area_offset returned: ', offset)

        # Set frame area
        xep1.x4driver_set_frame_area(2, 6)
        frame_area = xep1.x4driver_get_frame_area()
        print('x4driver_get_frame_area returned: [', frame_area.start, ', ', frame_area.end, ']');

        # Set TX center freq
        xep1.x4driver_set_tx_center_frequency(3);

        # Set PRFdiv
        xep1.x4driver_set_prf_div(16)
        prf_div = xep1.x4driver_get_prf_div()
        print('x4driver_get_prf_div returned: ', prf_div)

        # Start streaming
        xep1.x4driver_set_fps(0.1)
        fps = xep1.x4driver_get_fps()
        print('xep_x4driver_get_fps returned: ', fps)

        # Wait 5 sec.
        time.sleep(1)

        def read_frame2():
            """Gets frame data from module"""
            d = xep1.read_message_data_float()
            frame = np.array(d.data)
            # Convert the resulting frame to a complex array if downconversion is enabled

            return frame
        # Stop streaming
        xep1.x4driver_set_fps(20);
        global frame1
        while (1):
            frame1 = read_frame2()
            # Read data float if available.
            # print(frame1[1])
            # Reset module
        xep1.module_reset()

def try_xep2():
    log_level = 3
    with create_mc('com6') as mc:
        # x4m300 = mc.get_x4m300()
        print('2 start')
        # we have to go to manual mode
        ##x4m300.set_sensor_mode(XTS_SM_STOP, 0)
        # x4m300.set_sensor_mode(XTS_SM_MANUAL, 0);

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
        xep.x4driver_set_frame_area(2, 6)
        frame_area = xep.x4driver_get_frame_area()
        print('x4driver_get_frame_area returned: [', frame_area.start, ', ', frame_area.end, ']');

        # Set TX center freq
        xep.x4driver_set_tx_center_frequency(3);

        # Set PRFdiv
        xep.x4driver_set_prf_div(16)
        prf_div = xep.x4driver_get_prf_div()
        print('x4driver_get_prf_div returned: ', prf_div)

        # Start streaming
        xep.x4driver_set_fps(20)
        fps = xep.x4driver_get_fps()
        print('xep_x4driver_get_fps returned: ', fps)

        # Wait 5 sec.
        time.sleep(1)

        def read_frame():
            """Gets frame data from module"""
            d = xep.read_message_data_float()
            frame = np.array(d.data)
            # Convert the resulting frame to a complex array if downconversion is enabled

            return frame
        # Stop streaming
        xep.x4driver_set_fps(20);
        global frame2
        while (1):
            frame2 = read_frame()
            # Read data float if available.
            # print(frame2[1])
        xep.module_reset()

def main():
    t1 = threading.Thread(target=try_xep1)
    t2 = threading.Thread(target=try_xep2)
    t1.start()
    print('*****')
    t2.start()
    # t1.join()
    print('*****')
    # t2.join()
    print('main is over')

if __name__ == "__main__":
    frame1 = np.ones([751])
    frame2 = np.ones([751])
    main()

    import sys
    win = pg.GraphicsWindow(title="Basic plotting examples")
    win.resize(1000, 600)
    win.setWindowTitle('pyqtgraph example: Plotting')

    p1 = win.addPlot(title="Receiving from Radar-1")
    curve = p1.plot(pen='r')
    data = np.random.normal(size=(10, 1000))*10

    win.nextRow()

    p2 = win.addPlot(title="Receiving from Radar-2")
    curve2 = p2.plot(pen='g')
    data2 = np.random.normal(size=(10, 1000))*10
    ptr = 0

    def update():
        global curve, data, ptr, p2, p1
        # curve.setData(data[ptr % 10]*10)
        # curve2.setData(data2[ptr % 10]*10)
        # print(data.shape)
        # print(frame1.shape)
        if (frame1[1]!=1):
            curve.setData((frame1[:-2]+np.max(frame1[:-2]))*10000)
        else:
            curve.setData(frame1)
        if (frame2[1]!=1):
            curve2.setData((frame2[:-2]+np.max(frame2[:-2]))*10000)
        else:
            curve2.setData(frame2)
        print(frame2[1]+1)
        print(frame1[1]+2)
        if ptr == 0:
            p2.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
            p1.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
        ptr += 1
       # print('update is carried out')

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(50)
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        print('graph is closed')
