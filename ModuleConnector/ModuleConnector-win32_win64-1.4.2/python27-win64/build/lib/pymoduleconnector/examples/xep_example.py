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

def try_xep():

    log_level = 3
    with create_mc('com4') as mc:
    #x4m300 = mc.get_x4m300()

    # we have to go to manual mode
    ##x4m300.set_sensor_mode(XTS_SM_STOP, 0)
    #x4m300.set_sensor_mode(XTS_SM_MANUAL, 0);

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
		xep.x4driver_set_frame_area(2,6)
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
		print('xep_x4driver_get_fps returned: ' ,fps)

		# Wait 5 sec.
		time.sleep(5)

		# Stop streaming
		xep.x4driver_set_fps(0);

		# Read data float if available.
		if xep.peek_message_data_float() > 0:
			data_float = xep.read_message_data_float()
			#fig=plt.plot
			#plt.plot(data_float)
			frame = np.array(data_float.data)
			fig=plt.figure()
			plt.plot(frame)
			fig.savefig('E:/X4M03/ModuleConnector/ModuleConnector-win32_win64-1.4.2/python27-win64/pymoduleconnector/examples/1.png')
		else:
			print('No data float messages available.')

		# Reset module
		xep.module_reset()


def main():
   

    try_xep()

if __name__ == "__main__":
    main()
