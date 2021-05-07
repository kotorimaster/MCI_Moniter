#-*-coding:utf-8 -*-
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from numpy import *
from scipy import signal
import  scipy
import cmath
from sklearn.cluster import KMeans
def l_m(Pure1,Pure2,M,L):
    pnum=float(156)
    c1=Pure1.shape
    c2 = Pure2.shape

    valueplace1 = zeros(c1[0])
    valueplace2 = zeros(c2[0])



######################radar1##############################

    for i in range(c1[0]):

        valueplace1[i]=np.argmax(Pure1[i,:])+L + 0.2 * 156





    ######################radar1##############################
    ######################radar2##############################

    for ii in range(c2[0]):

        valueplace2[ii]=np.argmax(Pure2[ii,:])+L + 0.2 * 156

    ######################radar2##############################


    return valueplace1,valueplace2



