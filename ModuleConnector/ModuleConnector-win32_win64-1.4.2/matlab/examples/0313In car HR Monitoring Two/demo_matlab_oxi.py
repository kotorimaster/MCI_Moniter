#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
# sys.path.append('.\\)
# sys.path.append("/home/pi/ModuleConnector/ModuleConnector-rpi-1.5.3/python35-arm-linux-gnueabihf/duoleida")
import numpy as np
from numpy import *
import pymoduleconnector
# from pymoduleconnector import ModuleConnector
# from pymoduleconnector.ids import *
from optparse import OptionParser
import time
# from pymoduleconnector import create_mc
import scipy.io as sio
# import pca_filter
# import serial
import threading
import pandas as pd  # 导入pandas
from pandas import DataFrame
from datetime import datetime
import socket


# 加入求平均值 修改界面 解决matlab内存不足的问题 血氧仪有问题

def coll():
    print('aa')

    # print("coll start")
    # global RawData
    # global RadarStrTime
    # RawData = np.zeros((300, 437))
    # RadarStrTime = time.asctime(time.localtime(time.time()))
    # com = "com4"

    # with create_mc(com) as mc:
    #
    #     print("radar part")

    # xep = mc.get_xep()
    #
    # # inti x4driver
    # xep.x4driver_init()
    #
    # # Set enable pin
    # xep.x4driver_set_enable(1)
    #
    # # Set iterations
    # xep.x4driver_set_iterations(64)
    # # Set pulses per step
    # xep.x4driver_set_pulses_per_step(13)
    # # Set dac step
    # xep.x4driver_set_dac_step(1)
    # # Set dac min
    # xep.x4driver_set_dac_min(949)
    # # Set dac max
    # xep.x4driver_set_dac_max(1100)
    # # Set TX power
    # xep.x4driver_set_tx_power(2)
    #
    # # Enable downconversion
    # xep.x4driver_set_downconversion(0)
    #
    # # Set frame area offset
    # xep.x4driver_set_frame_area_offset(0.18)
    #
    # # Set frame area
    # xep.x4driver_set_frame_area(0.2,3)
    # frame_area = xep.x4driver_get_frame_area()
    #
    # # Set TX center freq
    # xep.x4driver_set_tx_center_frequency(3);
    #
    # # Set PRFdiv
    # xep.x4driver_set_prf_div(16)
    # prf_div = xep.x4driver_get_prf_div()
    #
    # xep.x4driver_set_fps(20)
    #
    # def read_frame():
    #     # """Gets frame data from module"""
    #     d = xep.read_message_data_float()
    #     frame = np.array(d.data)
    #     # Convert the resulting frame to a complex array if downconversion is enabled
    #     return frame
    #
    # while True:
    #     frame = read_frame()
    #     RawData = np.insert(RawData, 300, values=frame, axis=0)#参数：被插入矩阵，插入位置，插入矩阵，行/列
    #     RawData = RawData[1:, :]  # 去掉第一行
    #
    #     RadarStrTime = time.asctime(time.localtime (time.time()))
    #


def process():
    # print("process start ")
    # import matplotlib.pyplot as plt
    # from IPython.core.pylabtools import figsize
    # print('Init matlab......' + time.asctime(time.localtime (time.time())))
    # import mlab
    # from mlab.releases import latest_release as mlab
    # mlab.path(mlab.path(), r'E:\pyproject\in Car HR Monitoring Two')
    # mlab.path(mlab.path(), r'D:\pythonproject\in Car HR Monitoring Two')
    # print('matlab start......' + time.asctime(time.localtime (time.time())))
    #
    global RawData
    global RadarStrTime
    global data
    global time_oxi_1
    global time_oxi_2
    global time_oxi_3
    global time_oxi_1_seconds
    global time_oxi_2_seconds
    global time_oxi_3_seconds

    global nPR_1
    global nPR_2
    global nPR_3
    global device_1
    global device_2
    global device_3
    global size_sliding

    time_oxi_1_seconds = [0]
    time_oxi_2_seconds = [0]
    time_oxi_3_seconds = [0]
    time_oxi_1 = [0]
    time_oxi_2 = [0]
    time_oxi_3 = [0]
    nPR_1 = [0]
    nPR_2 = [0]
    nPR_3 = [0]

    device_1 = [0]
    device_2 = [0]
    device_3 = [0]

    size_sliding = 15

    Radarbox = [0, 0, 0, 0, 0, 0]

    mean1 = [0, 0, 0]

    Oxi = [1, 1, 1, 1, 1, 1]
    Oxi2 = [1, 1, 1, 1, 1, 1]
    Oxi3 = [1, 1, 1, 1, 1, 1]


    timebox = [0, 0, 0, 0, 0, 0]

    xxx = [1, 2, 3, 4, 5, 6]

    # plt.figure(figsize=(10, 6))

    while True:
        start = time.clock()
        RadarStrTime = time.asctime(time.localtime(time.time()))

        RadarTime = int(RadarStrTime[11:13]) * 10000 + int(RadarStrTime[14:16]) * 100 + int(RadarStrTime[17:19])  # time
        # print('' + str(len(RawData[0])) + ' lie ' + str(len(RawData)) + ' hang ')

        # HRRadar = mlab.demo(RawData)
        str_time=RadarStrTime[11:13]+RadarStrTime[14:16]+RadarStrTime[17:19]

        mean1.remove(mean1[0])
        mean1.append(0)

        Radarbox.remove(Radarbox[0])
        Radarbox.append(round(np.mean(mean1)))

        timebox.append(RadarTime)
        timebox.remove(timebox[0])

        date_in_second = int(RadarStrTime[11:13]) * 3600 + int(RadarStrTime[14:16]) * 60 + int(RadarStrTime[17:19])

        print("system_time")
        print(RadarStrTime)
        print(date_in_second)
        print(time_oxi_1[-1])
        int_time = date_in_second - 5

        # print(len(time_oxi_1_seconds))

        if len(time_oxi_1_seconds) >= size_sliding + 10:
            # print("entering")
            for index in range(len(time_oxi_1_seconds)):

                if time_oxi_1_seconds[index] - int_time == 0:
                    # print("perfect")
                    time_start = time_oxi_1_seconds[index] - 14
                    if time_start in time_oxi_1_seconds:
                        time_index = time_oxi_1_seconds.index(time_start)
                        value_1_instant = nPR_1[index]
                        # print('selected perfect')
                        # print(RadarStrTime)
                        # print(time_oxi_1[time_index])
                        value_nPR_1 = nPR_1[time_index:index + 1]
                        value_1 = np.mean(value_nPR_1)
                        break
                    elif time_start + 1 in time_oxi_1_seconds and time_start not in time_oxi_1_seconds:
                        time_index = time_oxi_1_seconds.index(time_start + 1)
                        value_1_instant = nPR_1[index]
                        # print('selected shift')
                        # print(RadarStrTime)
                        # print(time_oxi_1[time_index])
                        value_nPR_1 = nPR_1[time_index:index + 1]
                        value_1 = np.mean(value_nPR_1)
                        break
                elif time_oxi_1_seconds[index] - int_time == 1:

                    # print("one second shift")
                    # print(RadarStrTime)
                    time_start = int_time - 14
                    if time_start in time_oxi_1_seconds:
                        time_index = time_oxi_1_seconds.index(time_start)
                        value_1_instant = nPR_1[index - 1]
                        # print(time_oxi_1[time_index])
                        value_nPR_1 = nPR_1[time_index:index]
                        value_1 = np.mean(value_nPR_1)
                        break
                    elif time_start + 1 in time_oxi_1_seconds and time_start not in time_oxi_1_seconds:
                        time_index = time_oxi_1_seconds.index(time_start + 1)
                        value_1_instant = nPR_1[index - 1]
                        # print(time_oxi_1[time_index])
                        value_nPR_1 = nPR_1[time_index:index]
                        value_1 = np.mean(value_nPR_1)
                        break
                    else:
                        value_1 = nPR_1[-1]
                        value_1_instant = nPR_1[-1]
                else:
                    # print('No Radar Time Updated')
                    value_1 = nPR_1[-1]
                    value_1_instant = nPR_1[-1]
                    break
        elif len(time_oxi_1) <= 1:
            # print("initiating...")
            value_1 = 0
            value_1_instant = 0
        else:
            # print("sliding window preparing...")
            value_1 = nPR_1[-1]
            value_1_instant = nPR_1[-1]

        if len(time_oxi_2_seconds) >= size_sliding + 10:
            # print("entering")
            for index in range(len(time_oxi_2_seconds)):

                if time_oxi_2_seconds[index] - int_time == 0:
                    # print("perfect")
                    time_start = time_oxi_2_seconds[index] - 14
                    if time_start in time_oxi_2_seconds:
                        time_index = time_oxi_2_seconds.index(time_start)
                        value_2_instant = nPR_2[index]
                        # print('selected perfect')
                        # print(RadarStrTime)
                        # print(time_oxi_2[time_index])
                        value_nPR_2 = nPR_2[time_index:index + 1]
                        value_2 = np.mean(value_nPR_2)
                        break
                    elif time_start + 1 in time_oxi_2_seconds and time_start not in time_oxi_2_seconds:
                        time_index = time_oxi_2_seconds.index(time_start + 1)
                        value_2_instant = nPR_2[index]
                        # print('selected shift')
                        # print(RadarStrTime)
                        # print(time_oxi_2[time_index])
                        value_nPR_2 = nPR_2[time_index:index + 1]
                        value_2 = np.mean(value_nPR_2)
                        break
                elif time_oxi_2_seconds[index] - int_time == 1:

                    # print("one second shift")
                    # print(RadarStrTime)
                    time_start = int_time - 14
                    if time_start in time_oxi_2_seconds:
                        time_index = time_oxi_2_seconds.index(time_start)
                        value_2_instant = nPR_2[index - 1]
                        # print(time_oxi_2[time_index])
                        value_nPR_2 = nPR_2[time_index:index]
                        value_2 = np.mean(value_nPR_2)
                        break
                    elif time_start + 1 in time_oxi_2_seconds and time_start not in time_oxi_2_seconds:
                        time_index = time_oxi_2_seconds.index(time_start + 1)
                        value_2_instant = nPR_2[index - 1]
                        # print(time_oxi_2[time_index])
                        value_nPR_2 = nPR_2[time_index:index]
                        value_2 = np.mean(value_nPR_2)
                        break
                    else:
                        value_2 = nPR_2[-1]
                        value_2_instant = nPR_2[-1]
                        break
                else:
                    # print('No Radar Time Updated')
                    value_2 = nPR_2[-1]
                    value_2_instant = nPR_2[-1]
                    break

        elif len(time_oxi_2) <= 1:
            # print("initiating...")
            value_2 = 0
            value_2_instant = 0
        else:
            # print("sliding window preparing...")
            value_2 = nPR_2[-1]
            value_2_instant = nPR_2[-1]


        if len(time_oxi_3_seconds) >= size_sliding + 10:
            # print("entering")
            for index in range(len(time_oxi_3_seconds)):

                if time_oxi_3_seconds[index] - int_time == 0:
                    # print("perfect")
                    time_start = time_oxi_3_seconds[index] - 14
                    if time_start in time_oxi_3_seconds:
                        time_index = time_oxi_3_seconds.index(time_start)
                        value_3_instant = nPR_3[index]
                        # print('selected perfect')
                        # print(RadarStrTime)
                        # print(time_oxi_3[time_index])
                        value_nPR_3 = nPR_3[time_index:index + 1]
                        value_3 = np.mean(value_nPR_3)
                        break
                    elif time_start + 1 in time_oxi_3_seconds and time_start not in time_oxi_3_seconds:
                        time_index = time_oxi_3_seconds.index(time_start + 1)
                        value_3_instant = nPR_3[index]
                        # print('selected shift')
                        # print(RadarStrTime)
                        # print(time_oxi_3[time_index])
                        value_nPR_3 = nPR_3[time_index:index + 1]
                        value_3 = np.mean(value_nPR_3)
                        break
                elif time_oxi_3_seconds[index] - int_time == 1:

                    # print("one second shift")
                    # print(RadarStrTime)
                    time_start = int_time - 14
                    if time_start in time_oxi_3_seconds:
                        time_index = time_oxi_3_seconds.index(time_start)
                        value_3_instant = nPR_3[index - 1]
                        # print(time_oxi_3[time_index])
                        value_nPR_3 = nPR_3[time_index:index]
                        value_3 = np.mean(value_nPR_3)
                        break
                    elif time_start + 1 in time_oxi_3_seconds and time_start not in time_oxi_3_seconds:
                        time_index = time_oxi_3_seconds.index(time_start + 1)
                        value_3_instant = nPR_3[index - 1]
                        # print(time_oxi_2[time_index])
                        value_nPR_3 = nPR_3[time_index:index]
                        value_3 = np.mean(value_nPR_3)
                        break
                    else:
                        value_3 = nPR_3[-1]
                        value_3_instant = nPR_3[-1]
                        break
                else:
                    # print('No Radar Time Updated')
                    value_3 = nPR_3[-1]
                    value_3_instant = nPR_3[-1]
                    break

        elif len(time_oxi_3) <= 1:
            # print("initiating...")
            value_3 = 0
            value_3_instant = 0
        else:
            # print("sliding window preparing...")
            value_3 = nPR_3[-1]
            value_3_instant = nPR_3[-1]

        print("real time sliding value")

        print(float('%.2f' % value_1))
        print(float('%.2f' % value_2))
        print(float('%.2f' % value_3))

        f = open('oxi1_data_matlab.txt','w')
        f.write(str_time+' '+ str(round(value_1))+'\n')
        f.close()

        f = open('oxi2_data_matlab.txt', 'w')
        f.write(str_time + ' ' + str(round(value_2)) + '\n')
        f.close()


        print("real time Oximeter value")

        print(value_1_instant)
        print(value_2_instant)
        print(value_3_instant)

        Oxi.remove(Oxi[0])
        Oxi.append(float('%.2f' % value_1))
        Oxi2.remove(Oxi2[0])
        Oxi2.append(float('%.2f' % value_2))
        Oxi3.remove(Oxi3[0])
        Oxi3.append(float('%.2f' % value_3))

        # print("Oxi")
        # print(Oxi)
        # print("Oxi2")
        # print(Oxi2)

        value_1 = 0
        value_2 = 0

        if Oxi.count(0) == len(Oxi):
            # print('Oxi outage occured')
            time_oxi_1 = [0]
            time_oxi_1_seconds = [0]
            nPR_1 = [0]
            device_1 = [0]

        if Oxi2.count(0) == len(Oxi2):
            # print('Oxi2 outage occured')
            time_oxi_2 = [0]
            time_oxi_2_seconds = [0]
            nPR_2 = [0]
            device_2 = [0]
        if Oxi3.count(0) == len(Oxi3):
            # print('Oxi3 outage occured')
            time_oxi_3 = [0]
            time_oxi_3_seconds = [0]
            nPR_3 = [0]
            device_3 = [0]

        time.sleep(2)


def oximeter():
    HOST = ""
    PORT = 10001
    global data

    data = []
    global time_oxi_1
    global time_oxi_2
    global time_oxi_3
    time_oxi_1 = [0]
    time_oxi_2 = [0]
    time_oxi_3 = [0]

    global time_oxi_1_seconds
    global time_oxi_2_seconds
    global time_oxi_3_seconds
    time_oxi_1_seconds = [0]
    time_oxi_2_seconds = [0]
    time_oxi_3_seconds = [0]

    global nPR_1
    global nPR_2
    global nPR_3
    nPR_1 = [0]
    nPR_2 = [0]
    nPR_3 = [0]
    global device_1
    global device_2
    global device_3
    device_1 = [0]
    device_2 = [0]
    device_3 = [0]

    global listen_time

    listen_time = 20
    # count = 0

    global size_sliding
    size_sliding = 15

    while (1):

        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print('socket created')

        try:
            ss.bind((HOST, PORT))
        except socket.error as err:
            print('bind failed, error code:' + str(err[0]) + '.message:' + err[1])
            sys.exit()

        print('socket Bind Success!')

        ss.listen(listen_time)
        print('socket now is listening')


        while 1:
            conn, addr = ss.accept()
            # print('Connect with' + addr[0] + ':' + str(addr[1]))
            buf = conn.recv(64)

            # conn.sendto("OK",addr)

            # print(buf)
            data = buf.split()  # split string into a list
            # print(data)
            # print(len(data))

            if data == "socket connected":
                data = ""

            if len(data) == 4:

                time = data[1]
                time_in_second = int(time[0:2]) * 3600 + int(time[3:5]) * 60 + int(time[6:8])

                heartbeat = int(data[2])
                device = data[3]

                if device == 'oximeter1':
                    time_oxi_1.append(time)
                    time_oxi_1_seconds.append(time_in_second)
                    nPR_1.append(heartbeat)
                    device_1.append(device)
                    if len(time_oxi_1) >= 2 * size_sliding:
                        time_oxi_1 = time_oxi_1[-2 * size_sliding:]
                        time_oxi_1_seconds = time_oxi_1_seconds[-2 * size_sliding:]
                        nPR_1 = nPR_1[-2 * size_sliding:]
                        device_1 = device_1[-2 * size_sliding:]
                        # print(time_oxi_1)
                        # print(time_oxi_1_seconds)
                        # print(nPR_1)
                        # print(device_1)
                    else:
                        None
                elif device == 'oximeter2':
                    time_oxi_2.append(time)
                    time_oxi_2_seconds.append(time_in_second)
                    nPR_2.append(heartbeat)
                    device_2.append(device)
                    if len(time_oxi_2) >= 2 * size_sliding:
                        time_oxi_2 = time_oxi_2[-2 * size_sliding:]
                        time_oxi_2_seconds = time_oxi_2_seconds[-2 * size_sliding:]
                        nPR_2 = nPR_2[-2 * size_sliding:]
                        device_2 = device_2[-2 * size_sliding:]
                        # print(time_oxi_2)
                        # print(time_oxi_2_seconds)
                        # print(nPR_2)
                        # print(device_2)
                    else:
                        None
                elif device == 'oximeter3':
                    time_oxi_3.append(time)
                    time_oxi_3_seconds.append(time_in_second)
                    nPR_3.append(heartbeat)
                    device_3.append(device)
                    if len(time_oxi_3) >= 2 * size_sliding:
                        time_oxi_3 = time_oxi_3[-2 * size_sliding:]
                        time_oxi_3_seconds = time_oxi_3_seconds[-2 * size_sliding:]
                        nPR_3 = nPR_3[-2 * size_sliding:]
                        device_3 = device_3[-2 * size_sliding:]
                        # print(time_oxi_3)
                        # print(time_oxi_3_seconds)
                        # print(nPR_3)
                        # print(device_3)
                    else:
                        None
                else:
                    None

        ss.close


thread1 = threading.Thread(name='1', target=coll, args=[])
thread1.start()
thread2 = threading.Thread(name='2', target=process, args=[])
thread2.start()
thread3 = threading.Thread(name='3', target=oximeter, args=[])
thread3.start()
