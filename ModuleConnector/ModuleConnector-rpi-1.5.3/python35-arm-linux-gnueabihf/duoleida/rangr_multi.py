#-*-coding:utf-8 -*-
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
from scipy import signal
import cmath
from sklearn.cluster import KMeans
def l_m(Pure1,Pure2,Pure3,M,L):
    pnum=156
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
        for ii in range(sh):
            m = np.argmax(Pure1[i,:][max(peaked[ii] - 9,0):min(peaked[ii] + 9,c1[1])])
            peaked[ii] = m + peaked[ii] - 9

        nn = 0
        thrs_dis = np.argmax(Pure1[i,:])
        thrs = 0.4 * Pure1[i,:][thrs_dis]

        for jj in range(sh):
            if Pure1[i,:][peaked[jj]] > thrs:
                tmp_dist.append(int(peaked[jj]+L+0.2*pnum))
                nn = nn + 1
                print(int(peaked[jj]+L+0.2*pnum))
        print(str(nn)+'*******************************')

        tmp_num.append(nn)


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
        for ii in range(sh - 1):
            m = np.argmax(Pure2[i, :][max(peaked[ii] - 11, 0):min(peaked[ii] + 11, c1[1])])
            peaked[ii] = m + peaked[ii] - 11

        nn2 = 0
        thrs_dis = np.argmax(Pure2[i, :])
        thrs = 0.085 * Pure2[i, :][thrs_dis]
        for jj in range(sh):
            if Pure2[i,:][peaked[jj]] > thrs:
                tmp_dist2.append(int(peaked[jj]+L+0.2*pnum))
                nn2 = nn2 + 1
                print(int(peaked[jj] + L + 0.2 * pnum))
        print(str(nn2) + '*******************************')
        tmp_num2.append(nn2)

    ######################radar2##############################
    ######################radar3##############################
    print('radar3')

    tmp_dist3 = []
    tmp_num3 = []
    for i in range(c3[0]):
        peaked = signal.find_peaks_cwt(Pure3[i, :], np.arange(5, 30))
        sh = peaked.size
        for ii in range(sh - 1):
            m = np.argmax(Pure3[i, :][max(peaked[ii] - 11, 0):min(peaked[ii] + 11, c1[1])])
            peaked[ii] = m + peaked[ii] - 11

        nn3 = 0
        thrs_dis = np.argmax(Pure3[i, :])
        thrs = 0.19 * Pure3[i, :][thrs_dis]
        for jj in range(sh):
            if Pure3[i,:][peaked[jj]] > thrs:
                tmp_dist3.append(int(peaked[jj]+L+0.2*pnum))
                nn3 = nn3 + 1
                print(int(peaked[jj] + L + 0.2 * pnum))
        print(str(nn3) + '*******************************')
        tmp_num3.append(nn3)

    spot=[]
    spot_1 = [0, 0]
    spot_1 = [0, 0]
    spot_1 = [0, 0]


    ######################radar3##############################
    nn = 0
    mm = 0
    pp = 0

    tmp_dist=np.array(tmp_dist)
    tmp_dist2 = np.array(tmp_dist2)
    tmp_dist3 = np.array(tmp_dist3)
    tmp_dist = np.reshape(tmp_dist, [-1])
    tmp_dist2 = np.reshape(tmp_dist2, [-1])
    tmp_dist3 = np.reshape(tmp_dist3, [-1])

    tmp_rows_tp=[1,1,1]
    for j in range(c1[0]):
        tt =tmp_num[j]*tmp_num2[j]*tmp_num3[j]


        tmp_rows=np.zeros((tt,3),dtype=int32)
        tmp_rows=np.reshape(tmp_rows,[tt,3])


        tt=0
        for iiii in range(tmp_num[j]):
            for ii in range(tmp_num2[j]):
                for iii in range(tmp_num3[j]):

                    tmp_rows[tt,0]=tmp_dist[iiii+nn]
                    tmp_rows[tt, 1]= tmp_dist2[ii + mm]
                    tmp_rows[tt, 2]=tmp_dist3[iii + pp]

                    tt=tt+1
        nn=int(sum(tmp_num[0:j]))
        mm = int(sum(tmp_num2[0:j]))
        pp = int(sum(tmp_num3[0:j]))
        tmp_rows_2=np.vstack((tmp_rows_tp,tmp_rows))
        tmp_rows_tp=tmp_rows_2
        # spot.append(tmp_rows)
    spot=tmp_rows_tp[1:-1,:]

    spot=np.array(spot)

    num = np.hstack((tmp_num, tmp_num2, tmp_num3))
    #k = int(mean(num))
    k=2
    print('k//////////////////////'+str(k))


    estimator=KMeans(n_clusters=k)
    estimator.fit(spot)
    centroids=estimator.cluster_centers_
    color=['b','r']
    fig = plt.figure()

    for i, l in enumerate(estimator.labels_):
        print(spot[i,0])
        plt.scatter(spot[i,1],spot[i,2] ,color=color[l]
                  )

    print('********************************')
    print(centroids)
    plt.show()
    return centroids


