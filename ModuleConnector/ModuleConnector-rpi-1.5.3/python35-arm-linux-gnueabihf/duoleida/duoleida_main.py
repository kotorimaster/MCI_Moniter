#-*-coding:utf-8 -*-
import scipy.io as sio

import location_multi
import pca_filter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from sympy import*
load_r1=sio.loadmat('C:/Users/yyb/Desktop/X4_2/1/radar_2.mat')
r1=load_r1['radar2']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/x4_1/1/radar1.mat')
r2=load_r2['radar1']
M=0
L=100
RawData1=r1[:,0:750]
RawData2=r2[:,0:750]
PureData1=pca_filter.p_f(RawData1,M,L)
PureData2=pca_filter.p_f(RawData2,M,L)

def main():
#########################################################################
    fig, ax = plt.subplots()

    dot, = ax.plot([], [], 'ro')

    def init():
        x = [-2, 2]
        y = [0, 0]
        l=ax.scatter(x, y, color='b')
        plt.axis([-3, 3, 0, 5])
        plt.grid(True)
        return l

    def gen_dot():
        for i in range(10000):
            r1_len, r2_len, xx, yy = location_multi.l_m(PureData1, PureData2, M, L)
            newdot = [xx+0.02*i,yy+0.02*i]
            yield newdot

    def update_dot(newd):
        dot.set_data(newd[0], newd[1])
        return dot,

    ani = animation.FuncAnimation(fig, update_dot, frames = gen_dot, interval = 100, init_func=init)


    plt.show()
if __name__ == "__main__":
    main()