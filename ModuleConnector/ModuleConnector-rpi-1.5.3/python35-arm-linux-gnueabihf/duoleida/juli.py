#-*-coding:utf-8 -*-
import scipy.io as sio
import numpy as np
from numpy import *
import cmath
def l_m(Pure,L):
    pnum=156
    c1=Pure.shape
    valueplace1=zeros(c1[0])
    for i in range(c1[0]):

        valueplace1[i]=np.argmax(Pure[i,:])

    r1_len=int(np.median(valueplace1)+L+0.2163*156)


    len1=float(r1_len)

    l1=len1/float(pnum)




    return l1
