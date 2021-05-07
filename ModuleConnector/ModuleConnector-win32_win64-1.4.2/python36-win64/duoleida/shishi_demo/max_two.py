#-*-coding:utf-8 -*-
import scipy.io as sio
import numpy as np
from sympy import*
from gmphd_single import *
from scipy.signal.wavelets import cwt, ricker
from scipy import signal
pnum = float(156)
M=10
L=100
def mt(PD3):

    PD3 = np.reshape(PD3, [1, -1])
    c3 = PD3.shape
    PD3[PD3 < 0] = 0

    for i in range(c3[0]):
        peaked = signal.find_peaks_cwt(PD3[i, :], np.arange(5, 30))

        sh = peaked.size
        pr = 0

        for ii in range(sh):
            m = np.argmax(PD3[i, :][max(peaked[ii] - 10, 0):min(peaked[ii] + 10, 600)])
            if (peaked[ii] - 10 < 0):
                pr = 0
            else:
                pr = peaked[ii] - 10

            peaked[ii] = m + pr
        print(peaked)
        peaked = peaked.tolist()
        ttmmpp3 = []
        for iii in range(len(peaked)):
            ttmmpp3.append(PD3[0, peaked[iii]])

        max1 = peaked[argmax(ttmmpp3)]
        ttmmpp3.remove(ttmmpp3[argmax(ttmmpp3)])
        peaked.remove(max1)
        max2 = peaked[argmax(ttmmpp3)]
        print(max1)
        print(max2)
        # plt.plot(PD3[0, :].tolist())
        # for iii in range(len(peaked)):
        #     plt.scatter(peaked[iii], PD3[0, peaked[iii]])

        max1 = max1 + L + 0.2 * pnum
        max2 = max2 + L + 0.2 * pnum
        max1 = max1 / 156.0+0.5
        max2 = max2 / 156.0+0.5

    xiao = min(max1, max2)
    da = max(max1, max2)
    return xiao ,da