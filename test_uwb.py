# from pymoduleconnector import ModuleConnector
# device_name = "COM3" # The module device name.
# mc = ModuleConnector(device_name, log_level = 0)
# xep = mc.get_xep()
# # xep.set_sensor_mode_idle()
# xep.x4driver_init()
# print(xep.x4driver_get_fps())
# xep.module_reset()
# test

import threading
import time


class uwb:
    set = 14
    th = None
    end = False

    def circulation(self):
        while not self.end:
            print('this is not a test!')
            print(self.set)
            print(self.end)
            time.sleep(1)


    def __init__(self, num):
        self.set = num
        self.th = threading.Thread(name = '非自然死亡', target=self.circulation, args=())
        self.th.start()


    def __del__(self):
        self.end = True
        self.th.join()
        print(self.set, ': corrupted')

u = uwb(27)
del u
