#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 数据采集
from __future__ import print_function
import numpy as np
from numpy import *
import time
from pymoduleconnector import create_mc
import threading
import scipy.io as sio
import cv2
from dface.core.detect import create_mtcnn_net, MtcnnDetector
import time

tmp1 = []
tmp1 = np.array(tmp1)

# 时间戳和雷达对齐，最好设置成20Hz
# 数据格式：.mat(长1，宽1，面积1，长2，宽2，面积2，长3，宽3，面积3，时间戳（如91410）)无对应目标则置零
# 参照77-95行




def video():
    cap = cv2.VideoCapture(0)
    count = 0
    pnet, rnet, onet = create_mtcnn_net(p_model_path="./model_store/pnet_epoch.pt",
                                        r_model_path="./model_store/rnet_epoch.pt",
                                        o_model_path="./model_store/onet_epoch.pt", use_cuda=False)
    mtcnn_detector = MtcnnDetector(pnet=pnet, rnet=rnet, onet=onet, min_face_size=24)
    save2 = np.ones((100, 10))

    while count < 100:
        # Capture frame-by-frame
        ret, frame = cap.read()
        img_bg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # print(frame.shape)

        bboxs, landmarks = mtcnn_detector.detect_face(frame)
        bboxs, landmarks = np.round(bboxs).astype(int), np.round(landmarks).astype(int)
        save2[count, 9] = count

        start = time.time()

        for i in range(bboxs.shape[0]):
            if i > 2:
                break
            bbox = bboxs[i, :4]
            height = bbox[3] - bbox[1]
            width = bbox[2] - bbox[0]
            area = width * height
            # print(bbox)
            # print(landmarks[0][0])
            # boxes and landmarks
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            cv2.circle(frame, (landmarks[i][0], landmarks[i][1]), 1, (0, 0, 255), 4)
            cv2.circle(frame, (landmarks[i][2], landmarks[i][3]), 1, (0, 0, 255), 4)
            cv2.circle(frame, (landmarks[i][4], landmarks[i][5]), 1, (0, 0, 255), 4)
            cv2.circle(frame, (landmarks[i][6], landmarks[i][7]), 1, (0, 0, 255), 4)
            cv2.circle(frame, (landmarks[i][8], landmarks[i][9]), 1, (0, 0, 255), 4)

            # print info
            # cv2.putText(src, text, place, Font, Font_Size, Font_Color, Font_Overstriking)
            # cv2.putText(AddText, text, (200, 100), cv.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
            cv2.putText(frame, 'width: ' + str(width), (bbox[0], bbox[1] + round(30 * width / 400)),
                        cv2.FONT_HERSHEY_COMPLEX, width / 400, (0, 0, 255), 1)
            cv2.putText(frame, 'height: ' + str(height), (bbox[0], bbox[1] + round(60 * width / 400)),
                        cv2.FONT_HERSHEY_COMPLEX, width / 400, (0, 0, 255), 1)
            cv2.putText(frame, 'area: ' + str(area), (bbox[0], bbox[1] + round(90 * width / 400)),
                        cv2.FONT_HERSHEY_COMPLEX, width / 400, (0, 0, 255), 1)
            print('width:', str(width), 'height:', str(height), 'area:', str(area))
            save2[count, i*3], save2[count, i*3 + 1], save2[count, i*3 + 2] = width, height, area

        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        now = time.time()
        # if now - (start + count * 0.005)< 0.005:
        #     time.sleep(0.005 - now + (start + count * 0.005))
        count += 1

    sio.savemat('D:\\PyWork\\DFace-master\\test_camera.mat', {'data': save2})
    cap.release()
    cv2.destroyAllWindows()


if __name__=='__main__':
    com='COM4'
    # t1=threading.Thread(name='radar',target=radar,args=(com,))
    t2=threading.Thread(name='video',target=video)

    # t1.start()
    t2.start()



