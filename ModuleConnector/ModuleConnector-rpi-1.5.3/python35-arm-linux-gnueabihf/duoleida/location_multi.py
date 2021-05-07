#-*-coding:utf-8 -*-
import scipy.io as sio
import numpy as np
from numpy import *
import cmath
def l_m(Pure1,Pure2,M,L):
    pnum=156
    c1=Pure1.shape
    # print("c1*******************")
    # print(c1)
    valueplace1=zeros(c1[0])
    for i in range(c1[0]):

        valueplace1[i]=np.argmax(Pure1[i,:])

        # print("valueplace/////////"+str( valueplace1[i]))

    r1_len=int(np.median(valueplace1)+L+0.2163*156)

    c2 = Pure2.shape
    valueplace2 = zeros(c2[0])

    for ii in range(c2[0]):
        valueplace2[ii] = np.argmax(Pure2[ii, :])

    r2_len = int(np.median(valueplace2) + L + 0.2207 * 156)
    len1=float(r1_len)
    len2= float(r2_len)
    l1=len1/float(pnum)
    l2 = len2 / float(pnum)
    print("l1///////"+str(l1))
    print("l2///////" + str(l2))
    xx=(l1*l1-l2*l2)/4#x坐标
    yy=cmath.sqrt(l1*l1-(xx+1)*(xx+1))
    xx=complex(xx)
    xx=xx.real
    yy= complex(yy)
    yy = yy.real


    return r1_len,r2_len,xx,yy
