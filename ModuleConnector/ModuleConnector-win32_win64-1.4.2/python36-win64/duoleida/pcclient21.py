#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
# sys.path.append("F:/radar/ModuleConnector/ModuleConnector-win32_win64-1.4.2/python36-win64/duoleida")
# sys.path.append("C:/Users/zxy/Desktop")
sys.path.append("/home/pi/ModuleConnector/ModuleConnector-rpi-1.5.3/python35-arm-linux-gnueabihf/duoleida")
import threading
# import numpy as np
from numpy import *
import pymoduleconnector
from pymoduleconnector import ModuleConnector
from pymoduleconnector.ids import *
import time
from time import sleep
from pymoduleconnector import create_mc
import scipy.io as sio
# import pca_filter
# import random
from kalman import *
import serial
from socket import *
import os
from clean import *
from knn_kalman import knn_kalman

frame_gen = sio.loadmat('frame_gen.mat')['frame_gen']
con = threading.Condition()
ser = serial.Serial('/dev/device0', 9600)
com = ser.name
# 
# com='COM3'

HOST = '192.168.137.188'
PORT = 10000
BUFSIZ = 1024
ADDR = (HOST, PORT)

# path="/home/pi/workspace/timetest2/"
#######################初始化##############################
with create_mc(com) as mc:
    xep = mc.get_xep()

    # inti x4driver
    xep.x4driver_init()

    # Set enable pin
    xep.x4driver_set_enable(1)

    # Set iterations
    xep.x4driver_set_iterations(16)
    # Set pulses per step
    xep.x4driver_set_pulses_per_step(256)
    # Set dac step
    xep.x4driver_set_dac_step(1)
    # Set dac min
    xep.x4driver_set_dac_min(949)
    # Set dac max
    xep.x4driver_set_dac_max(1100)
    # Set TX power
    xep.x4driver_set_tx_power(2)

    # Enable downconversion
    xep.x4driver_set_downconversion(0)

    # Set frame area offset
    xep.x4driver_set_frame_area_offset(0.18)
    offset = xep.x4driver_get_frame_area_offset()

    # Set frame area
    xep.x4driver_set_frame_area(0.2, 5)
    frame_area = xep.x4driver_get_frame_area()

    # Set TX center freq
    xep.x4driver_set_tx_center_frequency(3)

    # Set PRFdiv
    xep.x4driver_set_prf_div(16)
    prf_div = xep.x4driver_get_prf_div()

    # Start streaming
    xep.x4driver_set_fps(0.1)
    fps = xep.x4driver_get_fps()
    # Stop streaming
    print("wait")

    # -----------------------------------读取数据与处理-------------------------------------#
    tmp = []
    tmp = np.array(tmp)
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)


    def read_frame():
        """Gets frame data from module"""
        d = xep.read_message_data_float()
        frame = np.array(d.data)
        # Convert the resulting frame to a complex array if downconversion is enabled
        return frame


    def get_data():
        save = np.ones((1, 751))

        for jj in range(1):
            frame2 = read_frame()

            save[jj, 0:750] = frame2
            # ll2=time.clock()-start
            start = 1
            ll2 = time.time() - start
            save[jj, -1] = ll2
        return save


    ################################数据处理##################################

    ycl = 0
    ijjj = 0
    leiji = np.zeros((1, 750))
    M = 0
    L = 50
    flag = 1


    def l_m(Pure, M, L):
        pnum = float(156)
        c = Pure.shape
        valueplace = zeros(c[0])
        for i in range(c[0]):
            valueplace[i] = np.argmax(Pure[i, :]) + L
        return valueplace


    while (True):
        msg = tcpCliSock.recv(1024).decode()
        if msg == "start":
            xep.x4driver_set_fps(5)
            break
        else:
            None
        sleep(0.1)

    # ----------------------------初始化一百次获得环境数据--------------------------#
    # data = sio.loadmat('./save/2019-01-15-20-35/2019-01-15-20-35rawdata3.mat')["pcradar3"]
    data = np.ones((35000, 751))
    # while 1:
    for i in range(0, 35000):
        # print(ycl)
        # initialbegin=time.time()
        save = get_data()
        data[i, :] = save
        tmp = save[:, 0:750]
        # RawData = np.reshape(data[i, 0:750],[1,750])
        # tmp=np.reshape(tmp,[1,650])
        if tmp != []:
            leiji = np.vstack((leiji, tmp))
            # print(leiji.shape)
            if ycl >= 100:
                if ycl == 100:
                    print('innit')
                    s1 = 0.9  # 目标1的当前距离
                    s2 = 4.2  # 目标2的当前距离
                    km_rg1 = Kalman(s1, 0)  # Kalman滤波后的目标1距离值
                    km_rg2 = Kalman(s2, 0)  # Kalman滤波后的目标2距离值

                    # PureData = pca_filter.p_f(leiji, M, L)
                    # p = PureData[99, :]
                    # PD = np.reshape(p, [1, -1])
                    # i_v = l_m(PD, M, L)
                    # km = Kalman(i_v, 0)
                    tcpCliSock.send("innit".encode())

                else:
                    while True:
                        msg2 = tcpCliSock.recv(1024).decode()
                        if msg2 == "detectionbegin":
                            break
                        else:
                            None
                    # 预处理--clean
                    leiji = leiji[0:100, 49:-12]
                    meandata = np.mean(leiji, axis=0)
                    dedata = leiji[0, :] - meandata
                    # dedata[0:50] = np.zeros(50)
                    signal = dedata
                    [cmap, dmap, n, ht] = clean(signal, frame_gen, 1.5e-3)
                    ss = ht[0:-25]
                    ht[0:25] = np.zeros(25)
                    ht[25:] = ss

                    # KNN + Kalman
                    km_rg1, km_rg2, s1, s2 = knn_kalman(ht, km_rg1, km_rg2, s1, s2)
                    jg1 = s1
                    jg2 = s2
                    str_jg = str(jg1) + ',' + str(jg2)
                    # print(str(ycl)+str(jg[0]))
                    # processend=time.time()
                    tcpCliSock.send(str(str_jg).encode())
                    print(str_jg)
                    sleep(0.005)

                # with open(path+"processtime3.txt","a+")as file:
                # 	file.write(str(processend)+'\r\n')
                # file.close()

            else:
                None
            # initialend=time.time()
            # with open(path+"initialtime3.txt","a+")as file:
            # 	file.write(str(initialend-initialbegin)+'\r\n')
            # file.close()
            print(ycl)
            ycl = ycl + 1
        # print(ycl)
        else:
            None
        tmp = []
now = int(round(time.time() * 1000))
now02 = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(now / 1000))[:-3]
path = "./save/" + now02 + '/'
if not os.path.exists(path):
    os.makedirs(path)
sio.savemat(path + now02 + 'rawdata1', {'pcradar1': data})

xep.module_reset()
