#-*-coding:utf-8 -*-
import scipy.io as sio

import pca_filter
import numpy as np
import matplotlib.pyplot as plt

from sympy import*

import single_new_multi
from kalman import *
import cmath
from pykalman import KalmanFilter
from kalman_two import *

import matplotlib.pyplot as plt
import cmath
import numpy as np
import copy
from kalman_mul import *
area = np.pi * 3.8

data1=[]
data2=[]
data3=[]
data11=[]
data22=[]
data33=[]
file=open('C:/Users/yyb/Desktop/brss/s_r3.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data3.append(line)
file.close()

file=open('C:/Users/yyb/Desktop/brss/s_r1.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data1.append(line)
file.close()

file=open('C:/Users/yyb/Desktop/brss/s_r2.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data2.append(line)
file.close()
file=open('C:/Users/yyb/Desktop/brss/s_rr3.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data33.append(line)
file.close()

file=open('C:/Users/yyb/Desktop/brss/s_rr1.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data11.append(line)
file.close()

file=open('C:/Users/yyb/Desktop/brss/s_rr2.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data22.append(line)
file.close()
h=0
area=np.pi*3.8
##############################################
for i in range(100):
    print i
    aq = str(data1[h + i])
    aq = aq[1:len(aq) - 1]
    aq=float(aq)
    aa = str(data11[h + i])
    aa = aa[1:len(aa) - 1]
    aa = float(aa)


    bq = str(data2[h + i])
    bq = bq[1:len(bq) - 1]
    bq = float(bq)
    bb = str(data22[h + i])
    bb = bb[1:len(bb) - 1]
    bb = float(bb)

    cq = str(data3[h + i])
    cq = cq[1:len(cq) - 1]
    cq = float(cq)
    cc = str(data33[h + i])
    cc = cc[1:len(cc) - 1]
    cc = float(cc)

    plt.scatter(i,aq,color='b',s=area)
    plt.scatter(i, aa, color='g',s=area)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xticks([0, 16, 32, 48, 64, 80, 96], [0, 2, 4, 6, 8, 10, 12])
#     a = 1.5
#     b = -1.5
#     jg=aq
#     jg2=bq
#     jg3=cq
#     jgg=aa
#     jgg2=bb
#     jgg3=cc
#     x1 = (jg * jg - jg2 * jg2 - a * a) / (2 * a)
#     if (jg2 * jg2 - x1 * x1 >= 0):
#         y1 = cmath.sqrt(jg2 * jg2 - x1 * x1).real
#     else:
#         y1 = 0
#
#     # #######################radar1,radar3############################
#     x2 = (jg * jg - jg3 * jg3) / (4 * a)
#     if (jg * jg - (x2 + a) * (x2 + a) >= 0):
#         y2 = cmath.sqrt(jg * jg - (x2 + a) * (x2 + a)).real
#     else:
#         y2 = 0
#
#     # #######################radar2,radar3############################
#     x3 = (jg3 * jg3 - jg2 * jg2 + a * a) / (2 * a)
#     if (jg2 * jg2 - x3 * x3 >= 0):
#         y3 = cmath.sqrt(jg2 * jg2 - x3 * x3).real
#     else:
#         y3 = 0
#     x = (x1 + x2 + x3) / 3
#
#     y = (y1 + y2 + y3) / 3
#     plt.scatter(x, y, color='b',s=area)
# ###############################################
#     x1 = (jgg * jgg - jgg2 * jgg2 - a * a) / (2 * a)
#     if (jgg2 * jgg2 - x1 * x1 >= 0):
#         y1 = cmath.sqrt(jgg2 * jgg2 - x1 * x1).real
#     else:
#         y1 = 0
#
#     # #######################radar1,radar3############################
#     x2 = (jgg * jgg - jgg3 * jgg3) / (4 * a)
#     if (jgg * jgg - (x2 + a) * (x2 + a) >= 0):
#         y2 = cmath.sqrt(jgg * jgg - (x2 + a) * (x2 + a)).real
#     else:
#         y2 = 0
#
#     # #######################radar2,radar3############################
#     x3 = (jgg3 * jgg3 - jgg2 * jgg2 + a * a) / (2 * a)
#     if (jgg2 * jgg2 - x3 * x3 >= 0):
#         y3 = cmath.sqrt(jgg2 * jgg2 - x3 * x3).real
#     else:
#         y3 = 0
#     xx = (x1 + x2 + x3) / 3
#
#     yy = (y1 + y2 + y3) / 3
#
#     plt.scatter(xx, yy, color='g',s=area)
#     plt.grid(True)

plt.show()




