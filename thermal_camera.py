# created by Xikang Jiang
import numpy as np
import matlab.engine
import os
import cv2
import time


class thermal_camera:
    """A class for thermal camera

    Description:

    Attributes:

    Methods:

    """
    fx = None
    fy = None

    matlab_engine = None
    thermal_image = None    # thermal image
    thermal_data = None    # thermal data for each pixel in thermal image (Unit: Celsius)

    timestamp = None
    width = None
    height = None

    def __init__(self, fx=1500, fy=1500):
        self.fx = fx
        self.fy = fy
        print('Starting MatLab...')
        self.matlab_engine = matlab.engine.start_matlab()
        self.matlab_engine.addpath(os.path.dirname(os.path.realpath(__file__)))
        self.matlab_engine.addpath('.\\Fluke\\MATLAB Toolkit\\Source Code\\FlukeStreamingGUI\\')
        print('MatLab running. Starting thermal streaming...')
        isReadingThermal = self.matlab_engine.StartStream(nargout=1)
        if not isReadingThermal:
            raise Exception('No Camera Found!')
        print('Thermal streaming...')
        self.width = 480
        self.height = 640

    def camera(self):
        data, image = self.matlab_engine.GetThermalData(nargout=2)
        ll = time.localtime(time.time())
        timestamp = ll.tm_hour * 10000 + ll.tm_min * 100 + ll.tm_sec
        if image is not None:
            data = np.array(data._data).reshape(data.size, order='F')
            image = np.array(image._data, dtype='uint8').reshape(image.size, order='F')
            image = cv2.UMat(image)

            self.thermal_data = data
            self.thermal_image = image
            self.timestamp = timestamp
            return self.thermal_data, self.thermal_image, self.timestamp

    @staticmethod
    def from_b_to_t(b_camera, t_camera, face, dx, dy, distance):
        thermal_fx = t_camera.fx
        thermal_fy = t_camera.fy
        fx = b_camera.fx
        fy = b_camera.fy
        dual_width = b_camera.width
        dual_height = b_camera.height
        width = t_camera.width
        height = t_camera.height
        # print(dual_width, dual_height)

        left, up, right, down = face[0], face[1], face[2], face[3]
        thermal_left = int(thermal_fx / fx * left + width / 2 - dual_width / 4 * thermal_fx / fx + thermal_fx * dx / distance)
        thermal_up = int(thermal_fy / fy * up + height / 2 + dy * thermal_fy / distance - dual_height / 2 * thermal_fy / fy)
        thermal_right = int(thermal_fx / fx * right + width / 2 - dual_width / 4 * thermal_fx / fx + thermal_fx * dx / distance)
        thermal_down = int(thermal_fy / fy * down + height / 2 + dy * thermal_fy / distance - dual_height / 2 * thermal_fy / fy)
        # print('(', thermal_left, ',', thermal_up, ')', '(', thermal_right, ',', thermal_down, ')')
        if thermal_left < 0:
            thermal_left = int(0)
        if thermal_up < 0:
            thermal_up = int(0)
        if thermal_down < 0:
            thermal_down = int(0)
        if thermal_right < 0:
            thermal_right = int(0)

        thermal_face = np.zeros(4).astype(int)
        thermal_face[0], thermal_face[1], thermal_face[2], thermal_face[3] = \
            thermal_left, thermal_up, thermal_right, thermal_down
        return thermal_face

    def __del__(self):
        self.matlab_engine.StopStream(nargout=0)


if __name__ == '__main__':
    # Left button click callback on thermal image
    data = None

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK & (data is not None):
            print(data[y, x])

    # Presentation UI
    cv2.namedWindow('Thermal_frame', 0)
    cv2.resizeWindow('Thermal_frame', 640, 480)
    cv2.moveWindow('Thermal_frame', 650, 0)
    cv2.setMouseCallback('Thermal_frame', mouse_callback)

    cam = thermal_camera()

    while True:
        data, image, timestamp = cam.camera()
        print(timestamp)
        cv2.imshow('Thermal_frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
