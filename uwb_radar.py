# created by Xikang Jiang
from pymoduleconnector import create_mc
from pymoduleconnector import ModuleConnector
import logging
import numpy as np
import sys
from VMDHRBR import VMDHRBR
import pca_filter
import threading
from time import sleep


class uwb_radar:
    leiji = None
    pure_data = None
    xep = None
    can_read = False
    read_condition = None
    logger = None
    end = False
    list_length = 0
    range = [0, 0]
    # count = 0

    # logger = logging.getLogger('radar_camera_demo')
    # logger.setLevel(logging.INFO)
    # rf_handler = logging.StreamHandler(sys.stderr)  # 默认是sys.stderr
    # rf_handler.setLevel(logging.DEBUG)
    # rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(message)s"))
    # logger.addHandler(rf_handler)

    def __init__(self, com, logger, range):
        self.range = range
        self.mc = ModuleConnector(com, log_level=0)
        self.xep = self.mc.get_xep()
        # xep = moduleconnector('')

        # inti x4driver
        self.xep.x4driver_init()

        # Set enable pin
        self.xep.x4driver_set_enable(1)

        # Set iterations
        self.xep.x4driver_set_iterations(64)
        # Set pulses per step
        self.xep.x4driver_set_pulses_per_step(5)
        # Set dac step
        self.xep.x4driver_set_dac_step(1)
        # Set dac min
        self.xep.x4driver_set_dac_min(949)
        # Set dac max
        self.xep.x4driver_set_dac_max(1100)
        # Set TX power
        self.xep.x4driver_set_tx_power(2)

        # Enable downconversion
        self.xep.x4driver_set_downconversion(0)

        # Set frame area offset
        self.xep.x4driver_set_frame_area_offset(0.18)
        offset = self.xep.x4driver_get_frame_area_offset()

        # Set frame area
        self.xep.x4driver_set_frame_area(range[0], range[1])
        frame_area = self.xep.x4driver_get_frame_area()

        # Set TX center freq
        self.xep.x4driver_set_tx_center_frequency(3)

        # Set PRFdiv
        self.xep.x4driver_set_prf_div(16)
        prf_div = self.xep.x4driver_get_prf_div()

        # Start streaming
        self.xep.x4driver_set_fps(20)
        fps = self.xep.x4driver_get_fps()

        self.logger = logger
        self.logger.info("wait radar")
        self.read_condition = threading.Condition()

        self.list_length = len(self.read_frame())

        self.read_frame_circulation = threading.Thread(
            name='read frame circulation', target=self.read_circulation, args=())
        # read_frame_circulation.setDaemon(True)
        self.preprocess = threading.Thread(
            name='preprocess', target=self.preprocessing, args=())
        # preprocess.setDaemon(True)
        self.read_frame_circulation.start()
        self.preprocess.start()

        print('End init')

    def preprocessing(self):
        ycl = 1
        M = 20
        L = 50
        # global leiji, pure_data
        self.logger.info('ready')
        while not self.end:
            sleep(0.001)
            if True:
            # with self.read_condition:
                # print(self.leiji.shape[0])
                if self.leiji is not None and self.leiji.shape[0] > 240:
                    if ycl == 1:
                        self.logger.info('init')
                    self.leiji = self.leiji[-221:-1, :]
                    leijitmp = self.leiji[-221:-1, :].copy()
                    rawdata = leijitmp[-221:-1, :-3].copy()
                    self.pure_data = pca_filter.p_f(rawdata, M, L)
                    ycl += 1
                    self.can_read = True
                # self.read_condition.notify()
            sleep(0.001)

    def read_circulation(self):
        # global leiji, pure_data
        while not self.end:
            if True:
            # with self.read_condition:
                # print(hex(self.xep.ping()))
                save = self.get_data()
                if self.leiji is None:
                    self.leiji = save.copy()
                    # print(leiji)
                else:
                    self.leiji = np.vstack((self.leiji, save))
                # print('Read frame')
                # self.read_condition.notify()
            sleep(0.001)

    def read_frame(self):
        """Gets frame data from module"""
        d = self.xep.read_message_data_float()
        frame = np.array(d.data)
        # Convert the resulting frame to a complex array if downconversion is enabled
        return frame

    def get_data(self):
        save1 = np.ones((1, self.list_length))
        # print(len(self.read_frame()))

        for jj in range(1):
            frame2 = self.read_frame()

            save1[jj, :] = frame2
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
        return save1

    def max_energy(self, puredata):
        data = puredata
        energyOfLocation = [0] * data.shape[1]
        for i in range(data.shape[1]):
            energyOfLocation[i] = sum(data[:, i] * data[:, i])
        sig = puredata[:, energyOfLocation.index(max(energyOfLocation))]
        return sig

    def vital_signs(self, range_low, range_high):
        if range_low <= self.range[0] or range_high >= self.range[1]:
            return 0, 0
        beginindex = round((range_low - self.range[0])*156 - 50)
        endindex = round((range_high - self.range[0])*156 - 50)
        if self.can_read and self.pure_data is not None:
            PureData3 = self.pure_data[:, beginindex:endindex].copy()
            sig1 = self.max_energy(PureData3)
            out = VMDHRBR(sig1)
            hr = int(round(out[0]))
            br = int(round(out[1]))
            return hr, br
        else:
            return 0, 0

    def reset(self):
        # self.count = self.count + 1
        # print('destruction', self.count)
        self.end = True
        # self.read_frame_circulation.join()
        # self.preprocess.join()
        if self.read_frame_circulation.is_alive():
            self.read_frame_circulation.join()
        if self.preprocess.is_alive():
            self.preprocess.join()

        # while self.read_frame_circulation.is_alive() or self.preprocess.is_alive():
        #     sleep(0.1)
        self.xep.module_reset()


if __name__ == '__main__':
    # global logger
    logger = logging.getLogger('radar_camera_demo')
    logger.setLevel(logging.INFO)
    rf_handler = logging.StreamHandler(sys.stderr)  # 默认是sys.stderr
    rf_handler.setLevel(logging.DEBUG)
    rf_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(message)s"))
    logger.addHandler(rf_handler)
    uwb = uwb_radar('COM3', logger, [0.2, 4])
    # print('Start reading')
    i = 0
    while i<40:
        # if uwb.PureData.shape[0] > 1 and uwb.can_read:
        #     if result[tag]['state'] and (result[tag]['endindex'] != result[tag]['beginindex']) :
        #         PureData3 = uwb.PureData[:, result[tag]['beginindex']:result[tag]['endindex']].copy()
        #         tmp_vs = uwb.vital_signs(PureData3)
        #         result[tag]['heartbeat'] = tmp_vs[0] if tmp_vs[0] != -1 else result[tag]['heartbeat']
        #         result[tag]['breath'] = tmp_vs[1] if tmp_vs[1] != -1 else result[tag]['breath']
        #         # result[tag]['heartbeat']=tmp_vs[0] if tmp_vs[0] != -1 else None
        #         # result[tag]['breath']=tmp_vs[1] if tmp_vs[1] != -1 else None
        # print(uwb.vital_signs(110, 130)
        print(uwb.vital_signs(1.10, 1.30))
        sleep(1)
        i += 1
        print(i + 1)
        # print('ready')
        pass
    uwb.reset()
