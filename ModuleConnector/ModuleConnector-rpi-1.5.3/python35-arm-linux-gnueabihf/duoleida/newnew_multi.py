#-*-coding:utf-8 -*-
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
from scipy import signal
import  scipy
import cmath
from sklearn.cluster import KMeans
def l_m(Pure1,Pure2,Pure3,M,L):
    pnum=float(156)
    c1=Pure1.shape
    c2 = Pure2.shape
    c3 = Pure3.shape



######################radar1##############################
    print('radar1')
    tmp_dist = []
    tmp_num = []
    Pure1[Pure1 < 0] = 0
    Pure2[Pure2 < 0] = 0
    Pure3[Pure3 < 0] = 0

    for i in range(c1[0]):
        peaked = signal.find_peaks_cwt(Pure1[i, :], np.arange(5, 30))
        sh = peaked.size
        pr = 0

        for ii in range(sh):
            m = np.argmax(Pure1[i, :][max(peaked[ii] - 10, 0):min(peaked[ii] + 10, 600)])
            if (peaked[ii] - 10 < 0):
                pr = 0
            else:
                pr = peaked[ii] - 10

            # print('第'+str(ii)+'次         '+str(m))
            peaked[ii] = m + pr

        nn = 0
        thrs_dis = np.argmax(Pure1[i,:])
        thrs = 0.20 * Pure1[i,:][thrs_dis]

        for jj in range(sh):
            if Pure1[i,:][peaked[jj]] > thrs:
                tmp_dist.append(int(peaked[jj]+L+0.2*pnum))
                nn = nn + 1
                print(int(peaked[jj] + L + 0.212 * pnum))
        # print(str(nn)+'*******************************')

        tmp_num.append(nn)


    # print('radar3      dist' + str(tmp_dist))
        ###################################
       #  fig = plt.figure()
       #  plt.plot(Pure1[i, :])
       # # plt.scatter(peaked[tmp_dist], Pure1[i, :][peaked[tmp_dist]], color='red')
       #  plt.scatter(peaked, Pure1[i, :][peaked],color='red')
       #  plt.show()
    ######################radar1##############################
    ######################radar2##############################
    print('radar2')
    tmp_dist2 = []
    tmp_num2 = []
    for i in range(c2[0]):
        peaked = signal.find_peaks_cwt(Pure2[i, :], np.arange(5, 30))
        sh = peaked.size
        pr = 0

        for ii in range(sh):
            m = np.argmax(Pure2[i, :][max(peaked[ii] - 10, 0):min(peaked[ii] + 10, 600)])
            if (peaked[ii] - 10 < 0):
                pr = 0
            else:
                pr = peaked[ii] - 10

            # print('第'+str(ii)+'次         '+str(m))
            peaked[ii] = m + pr

        nn2 = 0
        thrs_dis = np.argmax(Pure2[i, :])
        thrs = 0.25 * Pure2[i, :][thrs_dis]
        for jj in range(sh):
            if Pure2[i,:][peaked[jj]] > thrs:
                tmp_dist2.append(int(peaked[jj]+L+0.2*pnum))
                nn2 = nn2 + 1
                print(int(peaked[jj] + L + 0.212 * pnum))
        # print(str(nn2) + '*******************************')
        tmp_num2.append(nn2)
    # print('radar3      dist' + str(tmp_dist2))
    ######################radar2##############################
    ######################radar3##############################
    print('radar3')

    tmp_dist3 = []
    tmp_num3 = []
    for i in range(c3[0]):
        peaked = signal.find_peaks_cwt(Pure3[i, :], np.arange(5, 30))
        sh = peaked.size
        pr = 0

        for ii in range(sh):
            m = np.argmax(Pure3[i, :][max(peaked[ii] - 10, 0):min(peaked[ii] + 10, 600)])
            if (peaked[ii] - 10 < 0):
                pr = 0
            else:
                pr = peaked[ii] - 10

            # print('第'+str(ii)+'次         '+str(m))
            peaked[ii] = m + pr

        nn3 = 0
        thrs_dis = np.argmax(Pure3[i, :])
        thrs = 0.2 * Pure3[i, :][thrs_dis]
        for jj in range(sh):
            if Pure3[i,:][peaked[jj]] > thrs:
                tmp_dist3.append(int(peaked[jj]+L+0.2*pnum))
                nn3 = nn3 + 1
                print(int(peaked[jj] + L + 0.19 * pnum))
        # print(str(nn3) + '*******************************')
        tmp_num3.append(nn3)
    # print('radar3      dist'+str(tmp_dist3))
    ######################radar3##############################
    spot = [0, 0]
    spot_12 = [0, 0]
    spot_13 = [0, 0]
    spot_23 = [0, 0]
    nn = 0
    mm = 0
    pp = 0


    tmp_dist=np.array(tmp_dist)
    tmp_dist2 = np.array(tmp_dist2)
    tmp_dist3 = np.array(tmp_dist3)
    tmp_dist = np.reshape(tmp_dist, [-1])
    tmp_dist2 = np.reshape(tmp_dist2, [-1])
    tmp_dist3 = np.reshape(tmp_dist3, [-1])
    return tmp_dist,tmp_dist2,tmp_dist3
















#############################################################################################################################


    # print(spot)
    #
    # print(spot.shape)
    #
    #
    # estimator = KMeans(n_clusters=k)
    # estimator.fit(spot[1:,:])
    # centroids = estimator.cluster_centers_
    #
    #
    #
    # color = ['b', 'r']
    # fig = plt.figure()
    #
    # for i in range(spot.shape[0]):
    #
    #
    #     plt.scatter(spot[i, 0], spot[i, 1], color='b')
    #
    # print('********************************')
    # print(centroids)
    # plt.scatter(spot[:, 0], spot[:, 1], color='r'
    #             )
    # plt.show()
    # spot=spot[1:,:]
    spot=np.array(spot)
    print('spot shape!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(spot.shape)
    print(spot)

    if(spot.size<3):
        spot=array([[0,0],[1,1],[1,1]])

    spot=spot[1:,:]
    return spot


