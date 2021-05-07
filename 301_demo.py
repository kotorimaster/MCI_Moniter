# -*- coding: utf-8 -*-
from __future__ import print_function
import threading
from numpy import *
from time import sleep
from pymoduleconnector import create_mc
import pca_filter
import numpy as np
from VMDHRBR import VMDHRBR
from socket import *
import logging
import warnings
# import globaldefine
import select
import cv2
from dface.core.detect import create_mtcnn_net, MtcnnDetector
from PIL import Image, ImageDraw, ImageFont
import time
import os
import sys
from binocular_camera import binocular_camera
from thermal_camera import thermal_camera
from image_match.goldberg import ImageSignature
import matlab.engine
import Face_Distance_Mosaic


warnings.filterwarnings('ignore')
# sys.path.append("/home/pi/ModuleConnector/ModuleConnector-rpi-1.5.3/python35-arm-linux-gnueabihf/duoleida")
dy = -60  # vertical distance between binocular camera and thermal camera
dx = 0  # horizontal distance between binocular camera and thermal camera
# b_camera = binocular_camera([1])
# t_camera = None

left_frame = None
thermal_image = None

# cv2.namedWindow('Left_frame', 0)
# cv2.moveWindow("Left_frame", 0, 0)
# cv2.resizeWindow('Left_frame', 1000, 1000)
# cv2.namedWindow('Thermal_frame', 0)
# cv2.resizeWindow('Thermal_frame', 640, 480)
# cv2.moveWindow('Thermal_frame', 1010, 0)


def vital_signs(puredata):
    sig1 = maxEnergy(puredata)
    out = VMDHRBR(sig1)
    hr = int(round(out[0]))
    br = int(round(out[1]))

    return hr, br


def maxEnergy(puredata):
    data = puredata
    energyOfLocation = [0] * data.shape[1]
    for i in range(data.shape[1]):
        energyOfLocation[i] = sum(data[:, i] * data[:, i])
    sig = puredata[:, energyOfLocation.index(max(energyOfLocation))]
    return sig


def radar(com):
    # global data

    # data = np.zeros((3000, 438))
    global leiji
    with create_mc(com) as mc:
        xep = mc.get_xep()

        # inti x4driver
        xep.x4driver_init()

        # Set enable pin
        xep.x4driver_set_enable(1)

        # Set iterations
        xep.x4driver_set_iterations(64)
        # Set pulses per step
        xep.x4driver_set_pulses_per_step(5)
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
        xep.x4driver_set_frame_area(0.2, 3)
        frame_area = xep.x4driver_get_frame_area()

        # Set TX center freq
        xep.x4driver_set_tx_center_frequency(3)

        # Set PRFdiv
        xep.x4driver_set_prf_div(16)
        prf_div = xep.x4driver_get_prf_div()

        # Start streaming
        xep.x4driver_set_fps(20)
        fps = xep.x4driver_get_fps()
        # Stop streaming
        logger.info("wait radar")

        # -----------------------------------读取数据与处理-------------------------------------#
        def read_frame():
            """Gets frame data from module"""
            d = xep.read_message_data_float()
            frame = np.array(d.data)
            # Convert the resulting frame to a complex array if downconversion is enabled
            return frame

        def get_data():
            save = np.ones((1, 436))

            for jj in range(1):
                frame2 = read_frame()

                save[jj, :] = frame2
                # ll2=time.clock()-start
                # ll2 = time.asctime(time.localtime(time.time()))
                #
                # ll21 = ll2[11:13]
                # ll22 = ll2[14:16]
                # ll23 = ll2[17:19]
                #
                # lll = int(ll21) * 10000 + int(ll22) * 100 + int(ll23)
                # save[jj, -1] = lll
                # print(leiji.shape[0],lll)
            return save

        ################################数据处理##################################

        while 1:
            save = get_data()
            # print('Get Radar Data.')
            # data[i,:]=save
            # tmp = save[:, 0:437]
            # tmp = save
            leiji = np.vstack((leiji, save))
            sleep(0.001)
            # tmp = []
            # print(i)
        # now02 = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))[:-3]
        # path = "./save/" + now02 + '/'
        # if not os.path.exists(path):
        #     os.makedirs(path)
        # sio.savemat(path + now02 + 'rawdata.mat', {'pcradar': data})

        xep.module_reset()


def oximeter(port_oximeter):
    global result
    tcpCliSock3= socket(AF_INET,SOCK_STREAM)
    tcpCliSock3.setblocking(False)
    tcpCliSock3.bind(('', port_oximeter))
    tcpCliSock3.listen()
    logger.info('oximeter is ready.')
    inputs = [tcpCliSock3, ]
    while 1:
        r_list, w_list, e_list = select.select(inputs, [], [],0.005)
        for event in r_list:
            if event == tcpCliSock3:
                new_sock, addr = event.accept()
                inputs=[tcpCliSock3,new_sock,]
            else:
                data = event.recv(1024)
                # logger.info(data)
                if data!=b'' and data!=b'socket connected':
                    logger.info(data)
                    oximeter_result=data.split()
                    try:
                        oximeter_tag_num=bytes.decode(oximeter_result[-1])[-1] #1,2
                        # if oximeter_list[oximeter_tag_num - 1] in result.keys():
                        if result[oximeter_tag_num]['state'] and result[oximeter_tag_num]['heartbeat']>0:
                            result[oximeter_tag_num]['oximeter'] = int(oximeter_result[-2])
                        else:
                            logger.info('oximeter wrong')
                    except:
                        logger.info('oximeter id wrong')


def socket_vitalsigns(tag):
    global PureData, result
    while 1:
        if PureData.shape[0] > 1:
            if result[tag]['state'] and (result[tag]['endindex'] != result[tag]['beginindex']) :
                PureData3 = PureData[:, result[tag]['beginindex']:result[tag]['endindex']].copy()
                tmp_vs = vital_signs(PureData3)
                result[tag]['heartbeat'] = tmp_vs[0] if tmp_vs[0] != -1 else result[tag]['heartbeat']
                result[tag]['breath'] = tmp_vs[1] if tmp_vs[1] != -1 else result[tag]['breath']
                # result[tag]['heartbeat']=tmp_vs[0] if tmp_vs[0] != -1 else None
                # result[tag]['breath']=tmp_vs[1] if tmp_vs[1] != -1 else None
        sleep(0.1)


def preprocessing():
    ycl = 1
    M = 20
    L = 50
    global leiji, PureData, result
    logger.info('ready')
    while 1:
        sleep(0.001)
        if leiji.shape[0] > 240:
            # flag = 1
        # if flag:
            if ycl == 1:
                logger.info('init')
            leiji=leiji[-221:-1,:]
            # leijitmp = np.zeros((leiji[-1001:-1,:].shape))
            leijitmp = leiji[-221:-1, :].copy()
            rawdata = leijitmp[-221:-1, :-3].copy()
            PureData = pca_filter.p_f(rawdata, M, L)
            ycl += 1
            # logger.info(result)

            sleep(0.001)


def cv2ImgAddText(img, target, left, top, textColor=(0, 255, 0), textSize=20):
    global result
    # if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
    #     img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # # 创建一个可以在给定图像上绘图的对象
    # draw = ImageDraw.Draw(img)
    # # 字体的格式
    # fontStyle = ImageFont.truetype(
    #     "simhei"
    #     ".ttf", textSize, encoding="utf-8")
    # # 绘制文本
    if result[target]['state'] and result[target]['heartbeat'] > 0:
        # draw.text((left, top+10), '心率：'+str(result[target]['heartbeat']), textColor, font=fontStyle)
        # draw.text((left, top+30), '呼吸率：'+str(result[target]['breath']), textColor, font=fontStyle)
        # draw.text((left, top+50), '体温：' + str(format(result[target]['temperature'], '.1f')) + '摄氏度', textColor, font=fontStyle)
        # # draw.text((left, top-20), '血氧仪：'+str(result[target]['oximeter']), textColor, font=fontStyle)

        cv2.putText(img, 'HR: ' + str(result[target]['heartbeat']),
                    (left, top + 50),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
        cv2.putText(img, 'RR: ' + str(result[target]['breath']),
                    (left, top + 100),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
        cv2.putText(img, 'T:' + str(format(result[target]['temperature'], '.1f')) + 'C',
                    (left, top + 150),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)


    # 转换回OpenCV格式
    # img.show()
    # return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    return img

def camera():
    global result, left_frame, thermal_image
    beginflag = 0

    while True:
        faces = None
        record_id = []
        if b_camera is not None:
            faces, couples, left_frame, right_frame, timestamp = b_camera.camera()

        if t_camera is not None:
            # print('face detected!')
            thermal_data, thermal_image, timestamp = t_camera.camera()
        else:
            thermal_data = np.zeros((480, 640))
            thermal_image = None
            # print('thermal get!')
        # result[str(1)]['state'] = False
        # result[str(2)]['state'] = False
        # result[str(3)]['state'] = False
        if faces is not None:
            for i in range(faces['Left'].shape[0]):
                face = faces['Left'][i]
                distance = 500
                for j in range(couples.shape[0]):
                    if couples[j][0] == i:
                        distance = couples[j][2]
                        if distance < 500:
                            distance = 500
                # print('face detected!')
                temperature = 0.0
                width = b_camera.width / 2
                height = b_camera.height
                ll = time.localtime(time.time())
                timestamp = ll.tm_hour * 10000 + ll.tm_min * 100 + ll.tm_sec
                if (face[0] + face[2]) / 2 < width / 3:
                    i = 1
                    if thermal_data is not None:
                        temperature = np.max(thermal_data[:, :int(480 / 3)])
                elif width / 3 < (face[0] + face[2]) / 2 < width * 2 / 3:
                    i = 0
                    if thermal_data is not None:
                        temperature = np.max(thermal_data[:, int(480 / 3):int(480 * 2 / 3)])
                else:
                    i = 2
                    if thermal_data is not None:
                        temperature = np.max(thermal_data[:, int(480 * 2 / 3):])

                record_id.append(i + 1)
                # area = width * height
                # distance = (63.5+1.75*7)/(width+7)
                # logger.info(distance)
                index = int(distance / 1000 * 156 - 50)

                cv2.rectangle(left_frame, (face[0], face[1]), (face[2], face[3]), (0, 255, 0), 2)
                # print('faced bounded')

                left_frame = cv2ImgAddText(left_frame, str(i + 1), face[0], face[3])
                # print('text added')

                result[str(i + 1)]['state'] = True
                result[str(i + 1)]['temperature'] = temperature

                # 这里确定区间
                result[str(i + 1)]['beginindex'], result[str(i + 1)]['endindex'] = index - 25, index + 25
                # print('target info added')
        for i in range(3):
            if i + 1 not in record_id:
                result[str(i + 1)]['state'] = False
            # for i in range(faces['Left'].shape[0]+1, 4):
            #     result[str(i)]['state'] = False
            #     result[str(i)]['beginindex'] = 0
            #     result[str(i)]['endindex'] = 0


if __name__ == '__main__':
    #############################################log#################################
    global logger
    logger = logging.getLogger('radar_camera_demo')
    logger.setLevel(logging.INFO)
    rf_handler = logging.StreamHandler(sys.stderr)  # 默认是sys.stderr
    rf_handler.setLevel(logging.DEBUG)
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(message)s"))
    logger.addHandler(rf_handler)

    '''
    id（int）:目标编号（1-3）
    state（boolen）：是否有人（True有人，False没人）
    heartbeat（int）：雷达心率
    oximeter（int）：血氧仪心率
    temperature (float): 热成像体温
    breath（int）：雷达呼吸
    '''

    target1 = {'id': 1,
               'state': False,
               'heartbeat': 0,
               'oximeter': 0,
               'breath': 0,
               'temperature': 0.0,
               'beginindex': 0,
               'endindex': 0,
               }

    target2 = {'id': 2,
               'state': False,
               'heartbeat': 0,
               'oximeter': 0,
               'breath': 0,
               'temperature': 0.0,
               'beginindex': 0,
               'endindex': 0,
               }

    target3 = {'id': 3,
               'state': False,
               'heartbeat': 0,
               'oximeter': 0,
               'breath': 0,
               'temperature': 0.0,
               'beginindex': 0,
               'endindex': 0,
               }

    result = {
        '1': target1,
        '2': target2,
        '3': target3,
    }

    leiji = np.zeros((1, 436))
    PureData = leiji
    # frame_gen = sio.loadmat('frame_gen.mat')['frame_gen']
    # temp = frame_gen

    com = 'COM11'
    port_oximeter=10001
    # oximeter_list=['1', '2', '3'] #有血氧仪的目标
    oximeter_list = []  # 有血氧仪的目标

    t1 = threading.Thread(name="radar", target=radar, args=(com,))
    t2 = threading.Thread(name="preprocessing", target=preprocessing)
    t3 = threading.Thread(name="oximeter", target=oximeter, args=(port_oximeter,))
    # t4 = threading.Thread(name="socket_state",target=socket_state)
    t5 = threading.Thread(name="socket_vitalsigns", target=socket_vitalsigns, args=('1'))
    t6 = threading.Thread(name="socket_vitalsigns", target=socket_vitalsigns, args=('2'))
    t7 = threading.Thread(name="socket_vitalsigns", target=socket_vitalsigns, args=('3'))
    # t8 = threading.Thread(name="camera", target=camera)

    t1.start()
    t2.start()
    t3.start()
    # t4.start()
    t5.start()
    t6.start()
    t7.start()
    # t8.start()

    # def init_t_camera():
    #     global t_camera
    #     t_camera = thermal_camera()

    # t_init = threading.Thread(target=init_t_camera())
    # t_init.start()

    # if result['1']['heartbeat'] or result['2']['heartbeat'] or result['3']['heartbeat']:
    while True:
        # if result['1']['heartbeat'] or result['2']['heartbeat'] or result['3']['heartbeat']:
        if left_frame is not None:
            cv2.imshow('Left_frame', left_frame)
        if thermal_image is not None:
            cv2.imshow('Thermal_frame', thermal_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            # beginflag = 1
        # logger.info(result)

    t1.join()
    t2.join()
    t3.join()
    # t4.join()
    t5.join()
    t6.join()
    t7.join()
    # t8.join()