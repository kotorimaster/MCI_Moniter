import threading
import time
import copy
import numpy as np
from binocular_camera import binocular_camera
from thermal_camera import thermal_camera
from uwb_radar import uwb_radar
import cv2
import logging
import sys

dy = -60  # vertical distance between binocular camera and thermal camera
dx = 0  # horizontal distance between binocular camera and thermal camera
b_camera = None
t_camera = None
u_radar = None

binocular_frame_left = None
binocular_frame_right = None
thermal_frame = None

people = None
person = {'id': 0, 'face': {'Left': None, 'Right': None}, 'thermal_face': None, 'distance': 0.0, 'temperature': 0.0,
          'RR': 0, 'HR': 0, 'timestamp': 0}

con = threading.Condition()

cv2.namedWindow('Left_frame', 0)
cv2.moveWindow("Left_frame", 0, 0)
cv2.resizeWindow('Left_frame', 640, 480)
cv2.namedWindow('Thermal_frame', 0)
cv2.resizeWindow('Thermal_frame', 640, 480)
cv2.moveWindow('Thermal_frame', 650, 0)

logger = logging.getLogger('multi-thread')
logger.setLevel(logging.INFO)
rf_handler = logging.StreamHandler(sys.stderr)  # 默认是sys.stderr
rf_handler.setLevel(logging.DEBUG)
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(message)s"))
logger.addHandler(rf_handler)


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK & (t_camera is not None):
        print(t_camera.thermal_data[y, x])


def info_present(frame, thermal_frame, people):
    if frame is not None:
        if people is not None:
            for p in people:
                bbox_left = p['face']['Left']
                cv2.rectangle(frame, (bbox_left[0], bbox_left[1]), (bbox_left[2], bbox_left[3]), (0, 0, 255))
                cv2.putText(frame, str(format(p['temperature'], '.1f')) + 'C',
                            (bbox_left[0], bbox_left[1] + 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
                cv2.putText(frame, 'HR: ' + str(p['HR']),
                            (bbox_left[0], bbox_left[1] + 50),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
                cv2.putText(frame, 'RR: ' + str(p['RR']),
                            (bbox_left[0], bbox_left[1] + 70),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
    if thermal_frame is not None:
        if people is not None:
            for p in people:
                if p['thermal_face'] is not None:
                    bbox = p['thermal_face']
                    cv2.rectangle(thermal_frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255))

    return frame, thermal_frame


class thread_binocular_camera(threading.Thread):
    def run(self):
        global person, people, b_camera, binocular_frame_left, binocular_frame_right
        while True:
            con.acquire()
            faces, landmarks, couples, binocular_frame_left, binocular_frame_right, timestamp = b_camera.camera()
            people = []
            if faces['Left'].shape[0] > 0:
                for i in range(faces['Left'].shape[0]):
                    p = copy.deepcopy(person)
                    p['face']['Left'] = faces['Left'][i]
                    p['id'] = i + 1
                    p['timestamp'] = timestamp
                    for j in range(couples.shape[0]):
                        if i == couples[j][0]:
                            coupled_right = int(couples[j][1])
                            distance = couples[j][2]
                            p['face']['Right'] = faces['Right'][coupled_right]
                            p['distance'] = distance
                    people.append(p)

            con.notify()
            con.wait()


class thread_thermal_camera(threading.Thread):
    def run(self):
        global people, thermal_frame, b_camera, t_camera
        while True:
            con.acquire()
            thermal_data, thermal_frame, timestamp = t_camera.camera()
            if people is not None:
                for p in people:
                    if p['distance'] > 0.01:
                        p['thermal_face'] = t_camera.from_b_to_t(b_camera, t_camera, p['face']['Left'], dx, dy,
                                                                 p['distance'])
                        thermal_left, thermal_up, thermal_right, thermal_down = p['thermal_face'][0], p['thermal_face'][
                            1], p['thermal_face'][2], p['thermal_face'][3]
                        if thermal_left != thermal_right and thermal_up != thermal_down and thermal_down < b_camera.height and thermal_right < b_camera.width / 2:
                            face_thermal = thermal_data[thermal_up:thermal_down, thermal_left:thermal_right]
                            p['temperature'] = np.max(face_thermal)
                        people[p['id'] - 1] = p

            con.notify()
            con.wait()


class thread_uwb_radar(threading.Thread):
    def run(self):
        global people, u_radar

        while True:
            # con.acquire()
            save = u_radar.get_data()
            # data[i,:]=save
            # tmp = save[:, 0:437]
            # tmp = save
            u_radar.leiji = np.vstack((u_radar.leiji, save))
            u_radar.preprocess()
            if people is not None and u_radar.pure_data.shape[0] > 1:
                for p in people:
                    if 321 < p['distance'] < 2801:
                        index = p['distance'] / 1000 - 50
                        data = u_radar.pure_data[:, index - 25:index + 25].copy()
                        tmp_vs = u_radar.vital_signs(data)
                        p['HR'] = tmp_vs[0] if tmp_vs[0] != -1 else 0
                        p['RR'] = tmp_vs[1] if tmp_vs[1] != -1 else 0
                        people[p['id'] - 1] = p

            # con.notify()
            # con.wait()


class thread_present(threading.Thread):
    def run(self):
        while True:
            global binocular_frame_left, thermal_frame
            frame, t_frame = info_present(binocular_frame_left, thermal_frame, people)
            if frame is not None:
                print('Frame is not None!')
                cv2.imshow('Left_frame', frame)
            if t_frame is not None:
                print('Thermal frame is not None!')
                cv2.imshow('Thermal_frame', t_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    b_camera = binocular_camera(1)
    t_camera = thermal_camera()
    # u_radar = uwb_radar('COM3', logger)

    t1 = thread_binocular_camera()
    t2 = thread_thermal_camera()
    # t3 = thread_uwb_radar()

    t1.start()
    t2.start()
    # t3.start()

    while True:
        frame, t_frame = info_present(binocular_frame_left, thermal_frame, people)
        if frame is not None:
            # print('Frame is not None!')
            cv2.imshow('Left_frame', frame)
        if t_frame is not None:
            # print('Thermal frame is not None!')
            cv2.imshow('Thermal_frame', t_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
