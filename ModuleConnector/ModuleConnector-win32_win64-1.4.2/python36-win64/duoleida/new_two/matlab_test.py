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

PureData1=pca_filter.p_f(RawData1,M,L)

####################################################################
mlab.path(mlab.path(),r'C:\Users\yyb\Desktop\python_matlab')
print("!!!!!!!!!!!!!")
start=time.clock()
hrs,brs=mlab.respiration_multi2(PureData1,nout=2)

hrs,brs=mlab.respiration_multi2(PureData1,nout=2)

hrs,brs=mlab.respiration_multi2(PureData1,nout=2)

end=time.clock()
print(hrs)
print(brs)
print(end-start)
