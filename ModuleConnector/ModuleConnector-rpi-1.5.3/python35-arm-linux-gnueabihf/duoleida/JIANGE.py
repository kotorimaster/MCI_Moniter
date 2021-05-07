from multiprocessing import Pool
import os, time, random
import multiprocessing

import time
from pymoduleconnector import create_mc
import numpy as np
import scipy.io as sio



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
        xep.x4driver_set_fps(20);
        save2 = np.ones((1000, 751))
        print(i+" wait")
        #e.wait()

        for jj in range(1000):
            frame2 = read_frame()
            save2[jj, 0:750] = frame2
            ll2=time.clock()-start
            save2[jj, -1] = ll2

        # Reset module
        sio.savemat('C:/Users/yyb/Desktop/ceshi/radar'+i+'SING.mat', {'radar'+i: save2})
        xep.module_reset()


def try_xep2(start,i,com):
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
        xep.x4driver_set_fps(20);
        save2 = np.ones((1000, 751))
        print(i+" wait")
        #e.wait()

        for jj in range(1000):
            frame2 = read_frame()
            save2[jj, 0:750] = frame2
            ll2=time.clock()-start
            save2[jj, -1] = ll2
            #time.sleep(0.01)

        # Reset module
        sio.savemat('C:/Users/yyb/Desktop/ceshi/radar'+i+'_SING.mat', {'radar'+i: save2})
        xep.module_reset()

if __name__=='__main__':

    p = Pool()
    #e = multiprocessing.Event()
    aaa = time.clock()

    #p.apply_async(try_xep, args=(aaa,"1","com5"))
    p.apply_async(try_xep2, args=(aaa, "2", "com8"))
    # p.apply_async(try_xep, args=(aaa, "3", "com7"))
    # p.apply_async(try_xep, args=(aaa, "4", "com8"))

    time.sleep(3)
    print("KAISHI")
   # e.set()

    p.close()
    p.join()
    print 'All subprocesses done.'