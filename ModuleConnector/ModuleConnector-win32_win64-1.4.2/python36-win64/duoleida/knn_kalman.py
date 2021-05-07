# -*-coding:utf-8 -*-
# 将雷达测得的多个距离值聚类为两条轨迹
import scipy.io as sio
from kalman import *
# from sympy import *

# load_r1 = sio.loadmat('D:/MyData/20190301/distances/proKNN/radar1.mat')
# r1 = load_r1['new']
# print(size(r1, 1))
# print(size(r1, 0))


def knn_kalman(observ, km_rg1, km_rg2, start1, start2):
    lcs1 = start1  # 目标1的当前（估计）距离
    lcs2 = start2  # 目标2的当前（估计）距离
    estimate_a = []  # 目标1的估计值
    estimate_b = []  # 目标2的估计值
    result = []  # 目标的估计值矩阵

    rang1 = 0  # 目标1的估计距离
    rang2 = 0  # 目标2的估计距离
    ####################################################################
    # renshu = 2
    dist_list = []
    ttmm = []
    # print("===========" + str(i) + "===========")
    mmii1 = []
    mmii2 = []
    mmii1_na = []
    mmii2_na = []
    wg1 = []
    wg2 = []

    for j in range(len(observ)):
        if (observ[j]) > 0:
            print(j / 156.0)
            dist_list.append(j / 156.0 + 0.5)  # 校准距离值

    
    # 当只检测到一个点时
    if len(dist_list) == 1:
        # print("1111111111111111111111111111111111111111")
        # print(dist_list[0])
        delta1 = abs(dist_list[0] - lcs1)
        delta2 = abs(dist_list[0] - lcs2)
        if delta1 >= delta2:
            if delta2 < 0.4:
                rang2 = dist_list[0]
                rang1 = lcs1
        else:
            rang2 = lcs2
            rang1 = dist_list[0]
        # print("////////////////////////////////////////")
        # print(rang1)
        # print(rang2)
        # Kalman滤波
        km_rg1.z = np.array([rang1])
        km_rg1.kf_update()
        km_rg2.z = np.array([rang2])
        km_rg2.kf_update()
        # estimate_a.append(km_rg1.x[0, 0])
        # estimate_b.append(km_rg2.x[0, 0])
        # ttmm.append(km_rg1.x[0, 0])
        # ttmm.append(km_rg2.x[0, 0])
        # ttmm = np.array(ttmm)
        # result.append(ttmm)
        lcs1 = km_rg1.x[0, 0]
        lcs2 = km_rg2.x[0, 0]

    # 当检测到2个点时
    if len(dist_list) == 2:
        # print("2222222222222222222222222222222222222222")
        delta1 = abs(dist_list[0] - lcs1)
        delta2 = abs(dist_list[0] - lcs2)
        delta11 = abs(dist_list[1] - lcs1)
        delta22 = abs(dist_list[1] - lcs2)
        print(lcs1)
        print(lcs2)
        print(dist_list[0])
        dmin = min(delta1, delta2, delta11, delta22)  # 最小差值
        if delta1 == dmin:
            if dmin < 0.4:
                rang1 = dist_list[0]
                if delta22 < 0.4:
                    rang2 = dist_list[1]
                else:
                    rang2 = lcs2
            else:
                rang1 = lcs1
                rang2 = lcs2
        elif delta2 == dmin:
            if dmin < 0.4:
                rang2 = dist_list[0]
                if delta11 < 0.4:
                    rang1 = dist_list[1]
                else:
                    rang1 = lcs1
            else:
                rang1 = lcs1
                rang2 = lcs2
        elif delta11 == dmin:
            if dmin < 0.4:
                rang1 = dist_list[1]
                if delta2 < 0.4:
                    rang2 = dist_list[0]
                else:
                    rang2 = lcs2
            else:
                rang1 = lcs1
                rang2 = lcs2
        else:
            if dmin < 0.4:
                rang2 = dist_list[1]
                if delta1 < 0.4:
                    rang1 = dist_list[0]
                else:
                    rang1 = lcs1
            else:
                rang1 = lcs1
                rang2 = lcs2
        # print("////////////////////////////////////////")
        # print(lcs1)
        # print(lcs2)
        # Kalman滤波
        km_rg1.z = np.array([rang1])
        km_rg1.kf_update()
        km_rg2.z = np.array([rang2])
        km_rg2.kf_update()
        # estimate_a.append(km_rg1.x[0, 0])
        # estimate_b.append(km_rg2.x[0, 0])
        # ttmm.append(km_rg1.x[0, 0])
        # ttmm.append(km_rg2.x[0, 0])
        # ttmm = np.array(ttmm)
        # result.append(ttmm)
        lcs1 = km_rg1.x[0, 0]
        lcs2 = km_rg2.x[0, 0]

    # 检测点多于2个
    if len(dist_list) > 2:
        # print("333333333333333333333333333333333333333")
        # print(lcs1)
        # print(lcs2)

        for iii in range(len(dist_list)):
            mmii1.append(abs(dist_list[iii] - lcs1))
            mmii2.append(abs(dist_list[iii] - lcs2))
            mmii1_na.append(dist_list[iii] - lcs1)
            mmii2_na.append(dist_list[iii] - lcs2)
        th = min(mmii1)
        TT = mmii1.index(th)
        # print("------------------------")
        # print(TT)

        th2 = min(mmii2)
        # print(th)
        # print(th2)
        for itt in range(1 + int((len(dist_list) - 2) // 1.5)):
            # print(mmii1_na)
            # print(mmii2_na)
            index1 = mmii1.index(min(mmii1))
            index2 = mmii2.index(min(mmii2))

            if min(mmii1) <= th * 3:
                wg1.append(mmii1_na[index1] + lcs1)

            if min(mmii2) <= th2 * 3:
                wg2.append(mmii2_na[index2] + lcs2)
            mmii1.remove(min(mmii1))
            mmii2.remove(min(mmii2))
            mmii1_na.pop(index1)
            mmii2_na.pop(index2)
        junzhi1 = 0
        junzhi2 = 0
        if len(wg1) != 0 and len(wg2) != 0:
            # print(len(wg2))
            for iiii in range(len(wg1)):
                junzhi1 = junzhi1 + wg1[iiii]
            for iiiii in range(len(wg2)):
                junzhi2 = junzhi2 + wg2[iiiii]
            if abs(junzhi1 / len(wg1) - lcs1) < 0.6:
                rang1 = junzhi1 / len(wg1)
            else:
                rang1 = lcs1
            if abs(junzhi2 / len(wg2) - lcs2) < 0.6:
                rang2 = junzhi2 / len(wg2)
            else:
                rang2 = lcs2
        else:
            rang1 = lcs1
            rang2 = lcs2

        km_rg1.z = np.array([rang1])
        km_rg1.kf_update()
        km_rg2.z = np.array([rang2])
        km_rg2.kf_update()
        # estimate_a.append(km_rg1.x[0, 0])
        # estimate_b.append(km_rg2.x[0, 0])
        # ttmm.append(km_rg1.x[0, 0])
        # ttmm.append(km_rg2.x[0, 0])
        # ttmm = np.array(ttmm)
        # result.append(ttmm)
        lcs1 = km_rg1.x[0, 0]
        lcs2 = km_rg2.x[0, 0]
    return km_rg1, km_rg2, lcs1, lcs2


# if __name__ == '__main__':
#     s1 = 0.9  # 目标1的当前距离
#     s2 = 4.2  # 目标2的当前距离
#     km_rg1 = Kalman(s1, 0)  # Kalman滤波后的目标1距离值
#     km_rg2 = Kalman(s2, 0)  # Kalman滤波后的目标2距离值
#
#     fig = plt.figure()
#     plt.ion()
#     estimate1 = s1
#     estimate2 = s2
#     plt.scatter(0, estimate1, color='b')
#     plt.scatter(0, estimate2, color='b')
#     # 设置坐标轴范围
#     plt.xlim(0, 400)
#     plt.ylim(0, 4.5)
#     plt.pause(0.05)
#
#     for i in range(1, size(r1, 0)):
#         print("===========" + str(i) + "===========")
#         r1_x = r1[i, 0:-1]
#         km_rg1, km_rg2, s1, s2 = knn_kalman(r1_x, km_rg1, km_rg2, s1, s2)
#         estimate1 = s1
#         estimate2 = s2
#         plt.scatter(i, estimate1, color='b')
#         plt.scatter(i, estimate2, color='b')
#         # 设置坐标轴范围
#         plt.xlim(0, 400)
#         plt.ylim(0, 4.5)
#         plt.pause(0.05)
#     plt.ioff()
#     plt.show()
