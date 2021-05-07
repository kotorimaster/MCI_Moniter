#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 数据采集
from __future__ import print_function
import numpy as np
from numpy import *
import time
from pymoduleconnector import create_mc
import threading
import cv2
from dface.core.detect import create_mtcnn_net, MtcnnDetector
import scipy.io as sio
tmp1 = []
tmp1 = np.array(tmp1)

# 时间戳和雷达对齐，最好设置成20Hz
# 数据格式：.mat(长1，宽1，面积1，长2，宽2，面积2，长3，宽3，面积3，时间戳（如91410）)无对应目标则置零
# 参照77-95行

def radar(com):
    # count=8

    # print(count)
    with create_mc(com) as mc:
        xep = mc.get_xep()

        # inti x4driver
        xep.x4driver_init()

        # Set enable pin
        xep.x4driver_set_enable(1)

        # Set iterations
        xep.x4driver_set_iterations(64)
        # Set pulses per step
        xep.x4driver_set_pulses_per_step(14)
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
        # offset = xep.x4driver_get_frame_area_offset()

        # Set frame area
        xep.x4driver_set_frame_area(0.2, 3)
        # frame_area = xep.x4driver_get_frame_area()

        # Set TX center freq
        xep.x4driver_set_tx_center_frequency(3)

        # Set PRFdiv
        xep.x4driver_set_prf_div(16)
        # prf_div = xep.x4driver_get_prf_div()

        # Start streaming
        xep.x4driver_set_fps(20)

        # fps = xep.x4driver_get_fps()

        def read_frame():
            """Gets frame data from module"""
            d = xep.read_message_data_float()
            frame = np.array(d.data)
            # Convert the resulting frame to a complex array if downconversion is enabled
            return frame

        # Stop streaming

        print( " wait")
        save1 = np.ones((1300, 438))

        for jj in range(1300):

            frame2 = read_frame()

            save1[jj, 0:437] = frame2
            ll2 = time.asctime(time.localtime(time.time()))

            ll21 = ll2[11:13]
            ll22 = ll2[14:16]
            ll23 = ll2[17:19]

            lll = int(ll21) * 10000 + int(ll22) * 100 + int(ll23)
            save1[jj, -1] = lll

            print("count:{},time:{}".format(jj,str(lll)))

        sio.savemat('1.5m_radar_zxy.mat',{'radar':save1})
        # count+=1
        print('radar!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        xep.module_reset()


def video():
    cap = cv2.VideoCapture(0)
    count = 0
    # recording = False

    pnet, rnet, onet = create_mtcnn_net(p_model_path="./model_store/pnet_epoch.pt",
                                        r_model_path="./model_store/rnet_epoch.pt",
                                        o_model_path="./model_store/onet_epoch.pt", use_cuda=False)
    mtcnn_detector = MtcnnDetector(pnet=pnet, rnet=rnet, onet=onet, min_face_size=24)

    save2 = np.zeros((550, 10))
    start = time.asctime(time.localtime(time.time()))

    while count < 550:
        # Capture frame-by-frame
        ret, frame = cap.read()
        img_bg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # print(frame.shape)
        # b, g, r = cv2.split(img)
        # img2 = cv2.merge([r, g, b])

        bboxs, landmarks = mtcnn_detector.detect_face(frame)
        bboxs, landmarks = np.round(bboxs).astype(int), np.round(landmarks).astype(int)

        for i in range(bboxs.shape[0]):
        # while 1:
            if i > 2:
                break
            bbox = bboxs[i, :4]
            height = bbox[3] - bbox[1]
            width = bbox[2] - bbox[0]
            area = width * height
            # print(bbox)
            # print(landmarks[0][0])
            # boxes and landmarks
            # cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            # cv2.circle(frame, (landmarks[i][0], landmarks[i][1]), 1, (0, 0, 255), 4)
            # cv2.circle(frame, (landmarks[i][2], landmarks[i][3]), 1, (0, 0, 255), 4)
            # cv2.circle(frame, (landmarks[i][4], landmarks[i][5]), 1, (0, 0, 255), 4)
            # cv2.circle(frame, (landmarks[i][6], landmarks[i][7]), 1, (0, 0, 255), 4)
            # cv2.circle(frame, (landmarks[i][8], landmarks[i][9]), 1, (0, 0, 255), 4)

            # print info
            # cv2.putText(src, text, place, Font, Font_Size, Font_Color, Font_Overstriking)
            # cv2.putText(AddText, text, (200, 100), cv.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
            # cv2.putText(frame, 'width: ' + str(width), (bbox[0], bbox[1] + round(30 * width / 400)),
            #             cv2.FONT_HERSHEY_COMPLEX, width / 400, (0, 0, 255), 1)
            # cv2.putText(frame, 'height: ' + str(height), (bbox[0], bbox[1] + round(60 * width / 400)),
            #             cv2.FONT_HERSHEY_COMPLEX, width / 400, (0, 0, 255), 1)
            # cv2.putText(frame, 'area: ' + str(area), (bbox[0], bbox[1] + round(90 * width / 400)),
            #             cv2.FONT_HERSHEY_COMPLEX, width / 400, (0, 0, 255), 1)
            # cv2.imshow('frame',frame)
            # cv2.waitKey(1)

            ll = time.localtime(time.time())
            timestamp = ll.tm_hour * 10000 + ll.tm_min * 100 + ll.tm_sec
            print('width:', str(width), 'height:', str(height), 'area:', str(area), timestamp)
            save2[count, i * 3], save2[count, i * 3 + 1], save2[count, i * 3 + 2] = width, height, area

        ll = time.localtime(time.time())
        timestamp = ll.tm_hour * 10000 + ll.tm_min * 100 + ll.tm_sec
        save2[count, 9] = timestamp
        count += 1

    sio.savemat('1.5m_camera_zxy.mat', {'camera': save2})
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__=='__main__':
    com='COM11'
    t1=threading.Thread(name='radar',target=radar,args=(com,))
    t2=threading.Thread(name='video',target=video)

    t1.start()
    t2.start()



