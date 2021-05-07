from mlab.releases import R2014a as mlab
#-*-coding:utf-8 -*-
import scipy.io as sio
from kalman import *
import location_multi
import pca_filter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from sympy import*
import rangr_multi
import time
load_r1=sio.loadmat('C:/Users/yyb/Desktop/track/radar3_1.mat')
r1=load_r1['radar3']

M=10
L=100
RawData1=r1[:,0:750]
hrs=[]

RawData11=RawData1[10:110,0:750]
print(RawData1.shape)

####################################################################
mlab.path(mlab.path(),r'C:\Users\yyb\Desktop\python_matlab')
print("!!!!!!!!!!!!!")
start=time.clock()

pure=mlab.pca_filter_x4(RawData11,2,1,10,100,1)



end=time.clock()
start2=time.clock()
PureData1=pca_filter.p_f(RawData11,M,L)
end2=time.clock()
print(type(pure))
print(pure.shape)
print(end-start)
print(end2-start2)
