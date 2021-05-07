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
        thrs = 0.4 * Pure1[i,:][thrs_dis]

        for jj in range(sh):
            if Pure1[i,:][peaked[jj]] > thrs:
                tmp_dist.append(int(peaked[jj]+L+0.2*pnum))
                nn = nn + 1
        #         print(int(peaked[jj] + L + 0.212 * pnum))
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
        thrs = 0.15 * Pure2[i, :][thrs_dis]
        for jj in range(sh):
            if Pure2[i,:][peaked[jj]] > thrs:
                tmp_dist2.append(int(peaked[jj]+L+0.2*pnum))
                nn2 = nn2 + 1
        #         print(int(peaked[jj] + L + 0.212 * pnum))
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
        #         print(int(peaked[jj] + L + 0.19 * pnum))
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
    # k = int(mean(num))
    k = 2
    l=4
    zuobiao=[0,0,0]
    nnn=0
    mmm=0
    vvv=0
    for iii in range(c1[0]):
        for r1_1 in range(tmp_num[iii]):
            l1 = tmp_dist[r1_1+nnn]
            for r2_1 in range(tmp_num2[iii]):
                l2 = tmp_dist2[r2_1+mmm]
                for r3_1 in range(tmp_num3[iii]):
                    l3=tmp_dist3[r3_1+vvv]
                    zuobiao_tmp=[l1,l2,l3]
                    zuobiao = np.vstack((zuobiao, zuobiao_tmp))
        print()
        nnn=int(sum(tmp_num[0:iii]))
        mmm = int(sum(tmp_num2[0:iii]))
        vvv = int(sum(tmp_num3[0:iii]))

    zuobiao=zuobiao[1:-1,:]/156

    AP=[[0.5*l,-0.5*l,0],[0.886*l,0.886*l,0]]
    AP=np.array(AP)

    A1=[[2*(AP[0,1]-AP[0,0]),2*(AP[1,1]-AP[1,0])],[2*(AP[0,2]-AP[0,0]),2*(AP[1,2]-AP[1,0])],[2*(AP[0,2]-AP[0,1]),2*(AP[1,2]-AP[1,1])]]
    A1=np.array(A1)
    B1=[AP[0,1]*AP[0,1]+AP[1,1]*AP[1,1]-AP[0,0]*AP[0,0]-AP[1,0]*AP[1,0],AP[0,2]*AP[0,2]+AP[1,2]*AP[1,2]-AP[0,0]*AP[0,0]-AP[1,0]*AP[1,0],AP[0,2]*AP[0,2]+AP[1,2]*AP[1,2]-AP[0,1]*AP[0,1]-AP[1,1]*AP[1,1]]
    B1 = np.array(B1)

    B=[zuobiao[:,1]*zuobiao[:,1]-zuobiao[:,0]*zuobiao[:,0],zuobiao[:,2]*zuobiao[:,2]-zuobiao[:,0]*zuobiao[:,0],zuobiao[:,2]*zuobiao[:,2]-zuobiao[:,1]*zuobiao[:,1]]
    B = np.array(B)
    bs=B.shape

    print('***************************************')

    B1=np.tile(B1,[bs[1],1])
    B1=np.transpose(B1)
    # print(B1[:,1])
    # print(B1.shape)
    A2=np.array([[0,125,0],[0.0705,-0.0705,0.0705]])
    A2 = np.array(A2)


    AP0=np.tile(AP[:,0],[bs[1],1])
    AP0 = np.transpose(AP0)
    AP1 = np.tile(AP[:, 1], [bs[1], 1])
    AP1 = np.transpose(AP1)
    XY=np.dot(scipy.linalg.pinv(A1),(B1-B))
    # for i in range(XY.shape[1]):
    #     print(XY[:,i])
    XY2=np.dot([[cos(np.pi*2/3),sin(np.pi*2/3)],[-sin(np.pi*2/3),cos(np.pi*2/3)]],XY)+AP0
    XY3=np.dot([[cos(-np.pi*2/3),sin(-np.pi*2/3)],[-sin(-np.pi*2/3),cos(-np.pi*2/3)]],XY)+AP1

    thetaX=abs(sin(np.arctan(XY[1,:]/XY[0,:])))  #3
    thetaX2=abs(sin(np.arctan(XY2[1,:]/XY2[0,:]))) #2
    thetaX3 = abs(sin(np.arctan(XY3[1, :] / XY3[0, :]))) # 1
    th=sin(np.pi / 6)
    for i in range(XY.shape[1]):
        if(thetaX[i]>th and thetaX2[i]>th and thetaX3[i]>th ):

            spot=np.vstack((spot,XY[:,i]))

















    # print('计算计算计算计算计算计算计算计算计算')
    # #################计算radar1和radar2交点#################
    # for r1_1 in range(tmp_dist.size):
    #     l1=tmp_dist[r1_1]
    #     len1=tmp_dist[r1_1]/pnum
    #     # print('r1_1    ' + str(r1_1))
    #     for r2_1 in range(tmp_dist2.size):
    #         # print('r2_1    '+str(r2_1))
    #         l2=tmp_dist2[r2_1]
    #         len2=tmp_dist2[r2_1]/pnum
    #         if(len1+len2>=l):
    #             # print(len1)
    #             # print(len2)
    #             # print(l1)
    #             # print(l2)
    #             x=(len2*len2-len1*len1)/2*l
    #             y11=0.866*l+cmath.sqrt(len1*len1-(x-0.5*l)*(x-0.5*l))
    #             y21=0.866*l-cmath.sqrt(len1*len1-(x-0.5*l)*(x-0.5*l))
    #             x = complex(x)
    #
    #             y11 = complex(y11)
    #
    #             y21 = complex(y21)
    #             if(x.imag==0 and y11.imag==0 and y21.imag==0):
    #                 x = x.real
    #                 y11 = y11.real
    #                 y21 = y21.real
    #                 x_y11=np.array([x,y11])
    #                 x_y21 = np.array([x, y21])
    #                 if(x<=0.5*l and x>=-0.5*l and (y11-0.58*x)>=0 and (y11+0.58*x)>=0 and(y11-0.58*x)<=3.47 and (y11+0.58*x)<+3.47):
    #                     spot=np.vstack((spot,x_y11))
    #                 if (x <= 1.5 and x >= -1.5 and (y21 - 0.58 * x) >= 0 and (y21 + 0.58 * x) >= 0 and (
    #                         y21 - 0.58 * x) <= 3.47 and (y21 + 0.58 * x) < +3.47):
    #                     spot=np.vstack((spot, x_y21))
    #
    #                 # print('**************************1,2*************')
    #                 # print(x_y11)
    #                 # print(x_y21)
    #
    # #################计算radar1和radar3交点#################
    # for r1_2 in range(tmp_dist.size):
    #     l1 = tmp_dist[r1_2]
    #     len1=tmp_dist[r1_2]/pnum
    #     # print('r1_2    ' + str(r1_2))
    #     for r3_2 in range(tmp_dist3.size):
    #         # print('r3_2    ' + str(r3_2))
    #         l2 = tmp_dist3[r3_2]
    #         len3=tmp_dist3[r3_2]/pnum
    #         if(len1+len3>=3):
    #             # print(len1)
    #             # print(len3)
    #             # print(l1)
    #             # print(l2)
    #             y12=0.145*(len3*len3-len1*len1+9.01)*(len3*len3-len1*len1+9.01)+len3/2
    #             y22 = 0.145 * (len3 * len3 - len1 * len1 + 9.01) * (len3 * len3 - len1 * len1 + 9.01) - len3 / 2
    #             x12=cmath.sqrt(len3*len3-y12*y12)
    #             x22 = cmath.sqrt(len3 * len3 - y22 * y22)
    #             y12 = complex(y12)
    #             y22 = complex(y22)
    #             x12 = complex(x12)
    #             x22 = complex(x22)
    #             if (x22.imag==0 and x12.imag == 0 and y12.imag == 0 and y22.imag == 0):
    #                 y22 = y22.real
    #                 x12 = x12.real
    #                 y12 = y12.real
    #                 x22 = x22.real
    #                 x_y12=np.array([x12,y12])
    #                 x_y22 = np.array([x22, y22])
    #                 if (x12 <= 1.5 and x12 >= -1.5 and (y12 - 0.58 * x12) >= 0 and (y12 + 0.58 * x12) >= 0 and (
    #                         y12 - 0.58 * x12) <= 3.47 and (y12 + 0.58 * x12) < +3.47):
    #                     spot=np.vstack((spot,x_y12))
    #                 if (x22 <= 1.5 and x22>= -1.5 and (y22 - 0.58 * x22) >= 0 and (y22 + 0.58 * x22) >= 0 and (
    #                             y22 - 0.58 * x22) <= 3.47 and (y22 + 0.58 * x22) < +3.47):
    #                     spot=np.vstack((spot, x_y22))
    #
    #                 # print('**************************1,3*************')
    #                 # print(x_y12)
    #                 # print(x_y22)
    #
    # print('#####################################################')
    # #################计算radar2和radar3交点#################
    # for r2_3 in range(tmp_dist2.size):
    #     # print('r2_3    ' + str(r2_3))
    #     l1 = tmp_dist2[r2_3]
    #     len2=tmp_dist2[r2_3]/pnum
    #     for r3_3 in range(tmp_dist3.size):
    #         # print('r3_3    ' + str(r3_3))
    #         l2 = tmp_dist3[r3_3]
    #         len3=tmp_dist3[r3_3]/pnum
    #         if(len2+len3>=3):
    #             # print(len2)
    #             # print(len3)
    #             # print(l1)
    #             # print(l2)
    #             y13 = 0.145 * (len3 * len3 - len2 * len2 + 9.01) * (len3 * len3 - len2 * len2 + 9.01) + len3 / 2
    #             y23 = 0.145 * (len3 * len3 - len2 * len2 + 9.01) * (len3 * len3 - len2 * len2 + 9.01) - len3 / 2
    #             x13 = cmath.sqrt(len3 * len3 - y12 * y12)
    #             x23 = cmath.sqrt(len3 * len3 - y22 * y22)
    #             y13 = complex(y13)
    #
    #             y23 = complex(y23)
    #
    #             x13 = complex(x13)
    #
    #             x23 = complex(x23)
    #             if (x23.imag == 0 and x13.imag == 0 and y13.imag == 0 and y23.imag == 0):
    #                 y13 = y13.real
    #                 y23 = y23.real
    #                 x13 = x13.real
    #                 x23 = x23.real
    #                 x_y13 = np.array([x13, y13])
    #                 x_y23 = np.array([x23, y23])
    #                 if (x13 <= 1.5 and x13 >= -1.5 and (y13 - 0.58 * x13) >= 0 and (y13 + 0.58 * x13) >= 0 and (
    #                         y13 - 0.58 * x13) <= 3.47 and (y13 + 0.58 * x13) < +3.47):
    #                     spot = np.vstack((spot, x_y13))
    #                 if (x23 <= 1.5 and x23 >= -1.5 and (y23 - 0.58 * x23) >= 0 and (y23 + 0.58 * x23) >= 0 and (
    #                         y23- 0.58 * x23) <= 3.47 and (y23 + 0.58 * x23) < +3.47):
    #                     spot = np.vstack((spot, x_y23))
    #
    #                 # print('**************************3,2*************')
    #                 # print(x_y13)
    #                 # print(x_y23)
#############################################################################################################################


    # print(spot)

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
    # plt.scatter(centroids[:, 0], centroids[:, 1], color='r'
    #             )
    # plt.show()
    spot=spot[1:,:]









    return spot


