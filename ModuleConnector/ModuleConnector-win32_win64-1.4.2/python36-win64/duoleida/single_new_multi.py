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
    valueplace1 = zeros(c1[0])
    valueplace2 = zeros(c2[0])
    valueplace3 = zeros(c3[0])
    # Pure1[Pure1 < 0] = 0
    # Pure2[Pure2 < 0] = 0
    # Pure3[Pure3 < 0] = 0


######################radar1##############################

    for i in range(c1[0]):

        valueplace1[i]=np.argmax(Pure1[i,:])+L + 0.2 * 156





    ######################radar1##############################
    ######################radar2##############################

    for ii in range(c2[0]):

        valueplace2[ii]=np.argmax(Pure2[ii,:])+L + 0.2 * 156

    ######################radar2##############################
    ######################radar3##############################


    for iii in range(c3[0]):

        valueplace3[iii]=np.argmax(Pure3[iii,:])+L + 0.2 * 156

    ######################radar3##############################

    return valueplace1,valueplace2,valueplace3
















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


