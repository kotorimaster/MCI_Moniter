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
import scipy.io as sio
import datetime


def try_xep1():
    # print(datetime.datetime.now())
    log_level = 3
    with create_mc('com16') as mc2:
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
        xep1.x4driver_set_frame_area(0.2, 5)
        frame_area = xep1.x4driver_get_frame_area()
        print('x4driver_get_frame_area returned: [', frame_area.start, ', ', frame_area.end, ']')

        # Set TX center freq
        xep1.x4driver_set_tx_center_frequency(4)

        # Set PRFdiv
        xep1.x4driver_set_prf_div(16)
        prf_div = xep1.x4driver_get_prf_div()
        print('x4driver_get_prf_div returned: ', prf_div)

        # Start streaming
        xep1.x4driver_set_fps(0.1)
        fps = xep1.x4driver_get_fps()
        print('xep_x4driver_get_fps returned: ', fps)

        # Wait 5 sec.
        # time.sleep(1)

        # def readdata():
        #     if xep.peek_message_data_float() > 0:
        #
        #         data_float = xep.read_message_data_float()
        #         frame2 = np.array(data_float.data)
        #
        #     # fig=plt.plot
        #     # plt.plot(data_float)
        #     # frame = np.array(data_float.data)
        #     # fig = plt.figure()
        #     # plt.plot(frame)
        #     # plt.show()
        #     else:
        #         print('No data float messages available--------1.')
        #     return frame2

        def read_frame():
            """Gets frame data from module"""
            d = xep1.read_message_data_float()
            frame = np.array(d.data)
            # Convert the resulting frame to a complex array if downconversion is enabled

            return frame

        # Stop streaming
        xep1.x4driver_set_fps(20)
        for iii in range(20):
            save1 = np.ones((300, 751))
            for ii in range(300):
                frame = read_frame()
                # Read data float if available.
                print(frame.size)
                save1[ii, 0:750] = frame
                oldtime = datetime.datetime.now()
                strr = str(oldtime)
                l = strr.split(':')
                fen = int(l[1])
                ll = fen * 100 + float(l[-1])

                save1[ii, -1] = ll

            sio.savemat('C:/Users/yyb/Desktop/jiaozhun/n5/4/'+str(iii+80)+'.mat', {'radar2': save1})
        xep1.module_reset()




def main():
    t1 = threading.Thread(target=try_xep1)

    t1.start()



if __name__ == "__main__":
    main()