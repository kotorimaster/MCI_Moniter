#!/usr/bin/env python

from gmphd import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from syntheticexamplestuff import *
################################################################
###############################################################
###############################################################
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
import newnew_multi
from gmphd import *
from numpy import *
import numpy.linalg
import time
from scipy.signal.wavelets import cwt, ricker
import cmath
load_r1=sio.loadmat('C:/Users/yyb/Desktop/brs/x11111.mat')
r1=load_r1['radar1']
load_r2=sio.loadmat('C:/Users/yyb/Desktop/brs/x22222.mat')
r2=load_r2['radar2']
load_r3=sio.loadmat('C:/Users/yyb/Desktop/2_man_demo/track/radar3_1.mat')
r3=load_r3['radar3']
M=10
L=100
RawData1=r1[:,0:750]
RawData2=r2[:,0:750]
RawData3=r3[:,0:750]

PureData1=pca_filter.p_f(RawData1,M,L)
PureData2=pca_filter.p_f(RawData2,M,L)
PureData3=pca_filter.p_f(RawData3,M,L)
result=[]
####################################################################

yuce_x=[]
yuce_xx=[]
yuce_xxx=[]
yuce_y=[]
quan=[]
fig=plt.figure()
h=0
km1 = Kalman(1.0, 0)

lcs1=1.1
lcs2=3.8
rang1=0
rang2=0
####################################################################
km2=Kalman(1.1,0)
km3=Kalman(3.8,0)
################################################################
###############################################################
###############################################################
# user config options:
niters = 1#20
birthprob = 0.1  # 0.05 # 0 # 0.2
survivalprob = 0.975 # 0.95 # 1
detectprob =  0.95#  0.999
clutterintensitytot = 5 #2 #4   # typical num clutter items per frame
bias = 2 #8   # tendency to prefer false-positives over false-negatives in the filtered output
initcount = 1#2  # 4
obsntype = 'chirp' # 'chirp' or 'spect'
transntype = 'vibrato' # 'fixedvel' or 'vibrato'

###############################################################
# setting up variables
transnmatrix = transntypes[transntype]
obsnmatrix = obsntypes[obsntype]['obsnmatrix']
directlystatetospec = dot(obsntypes[obsntype]['obstospec'], obsnmatrix)

directlystatetospec001 = array([[0., 0., 1.]])

birthintensity1 = birthprob / len(birthgmm)
# print "birthgmm: each component has weight %g" % birthintensity1
for comp in birthgmm:
	comp.weight = birthintensity1

clutterintensity = clutterintensityfromtot(clutterintensitytot, obsntype)
print "clutterintensity: %g" % clutterintensity


g = Gmphd(birthgmm, survivalprob, 0.7, transnmatrix, 1e-9 * array([[1,0,0], [0,1,0], [0,0,1]]), obsnmatrix, obsntypes[obsntype]['noisecov'], clutterintensity)

###############################################################
results = []

area=np.pi*3.8
for i in range(110):

	print("===========" + str(i) + "===========")
	mmii1 = []
	mmii2 = []
	mmii1_na = []
	mmii2_na = []
	wg1 = []
	wg2 = []

	PD1 = PureData1[i + h, :]

	PD2 = PureData2[i + h, :]

	PD3 = PureData3[i + h, :]
	PD1 = np.reshape(PD1, [1, -1])
	PD2 = np.reshape(PD2, [1, -1])
	PD3 = np.reshape(PD3, [1, -1])
	a1, a2, a3 = newnew_multi.l_m(PD1, PD2, PD3, M, L)

    



	def chuli(a3):
		a3 = np.array(a3)
		a3 = a3 / 15.6
		quan.append(a3)

		a3 = np.reshape(a3, [a3.shape[0], 1])

		a3_list = a3.tolist()
		for jjjj in range(len(a3_list)):
			tt=a3_list[jjjj][0]/10

			plt.scatter(i, tt, color='y', s=area)
			plt.xticks(fontsize=20)
			plt.yticks(fontsize=20)
			plt.xticks([0, 20, 40, 60, 80, 100, 120], [0, 2, 4, 6, 8, 10, 12])

		a3_ll = np.zeros((len(a3_list), 2))
		for hang in range(len(a3_list)):
			a3_ll[hang, 0] = float(a3_list[hang][0])
			a3_ll[hang, 1] = float(a3_list[hang][0])
		a3_ll = np.reshape(a3_ll, [-1, 2, 1])
		obsset = a3_ll.tolist()
		start = time.clock()
		updateandprune(g, obsset)

		resultdict = collateresults(g, obsset, bias, obsntype, directlystatetospec)
		print "resultresultresultresultresultresultresult"
		resultdict=np.array(resultdict)
		rrrr=resultdict.nonzero()
		rrrr=np.array(rrrr)
		rrrr=np.reshape(rrrr,[-1])
		return rrrr


	# rrrr = chuli(a3)
	# rrrr1 = chuli(a2)
	rrrr2 = chuli(a3)



	shangyg=0
	rrrr_new=[]
	##fanwei
	shangxian=4.0

	for ii in range(rrrr2.shape[0]):
		if rrrr2[ii]/10.0<shangxian:
			if (rrrr2[ii]/10.0-shangyg)>0.36:
				rrrr_new.append(rrrr2[ii]/10.0)
				shangyg=rrrr2[ii]/10.0

	print rrrr2/10.0

	rrrr_new = np.array(rrrr_new)
	rrrr_new = np.reshape(rrrr_new, [-1])
	print rrrr_new
	results.append(rrrr_new)

	rrrr_list = rrrr2.tolist()
	rrrr_new_list=rrrr_new.tolist()
	area=np.pi*3.8


	end1=time.clock()
	print "**************************************"+str(len(rrrr_list))
	print "**************************************"+str(len(rrrr_new_list))
	# for jjjj in range(len(rrrr_list)):
	# 	plt.scatter(i, rrrr_list[jjjj]/10.0, color='r')
	# 	# plt.scatter(i, rrrr_new_list[jjjj], color='b')
	result.append(rrrr_new_list)
	for jjjj in range(len(rrrr_new_list)):
		if(jjjj==0):
			plt.scatter(i, rrrr_new_list[jjjj], color='b')
		else:
			plt.scatter(i, rrrr_new_list[jjjj], color='r')
		plt.xticks(fontsize=20)
		plt.yticks(fontsize=20)
		plt.xticks([0, 20, 40, 60, 80, 100, 120], [0, 2, 4, 6, 8, 10, 12])
	end2=time.clock()



################################################################################################
	# def js_12(jg,jg2):
	# 	a = 1.5
	# 	b = -1.5
	# 	# #######################radar1,radar2############################
	# 	x1 = (jg * jg - jg2 * jg2 - a * a) / (2 * a)
	# 	if (jg2 * jg2 - x1 * x1 >= 0):
	# 		y1 = cmath.sqrt(jg2 * jg2 - x1 * x1).real
	# 	else:
	# 		y1 = 0
	# 	return x1,y1
	# def js_12(jg,jg3):
	# 	a = 1.5
	# 	b = -1.5
	# 	# #######################radar1,radar3############################
	# 	x2 = (jg * jg - jg3 * jg3 - a * a + b * b) / (2 * a - 2 * b)
	# 	if (jg * jg - (x2 + a) * (x2 + a) >= 0):
	# 		y2 = cmath.sqrt(jg * jg - (x2 + a) * (x2 + a)).real
	# 	else:
	# 		y2 = 0
	# 	return x2,y2
	# def js_23(jg2,jg3):
	# 	a = 1.5
	# 	b = -1.5
	# 	# #######################radar2,radar3############################
	# 	x3 = (jg3 * jg3 - jg2 * jg2 - b * b) / (2 * b)
	# 	if (jg2 * jg2 - x3 * x3 >= 0):
	# 		y3 = cmath.sqrt(jg2 * jg2 - x3 * x3).real
	# 	else:
	# 		y3 = 0
	# 	return x3,y3





##############################################################
# print(end1-start)
# print(end2-start)
# plot the results
# fig = plt.figure()
#
# ax = fig.add_subplot(111)
# ax.imshow(array([map(lambda x: min(x,1.0), moment['estspec']) for moment in results]).T, aspect='auto', interpolation='nearest', cmap=cm.binary)
# plt.ylabel('Estimated', fontsize='x-small')
# plt.xticks( fontsize='x-small' )
# plt.yticks( arange(0, 60, 10), ('', '', '', '', '', '') )
#
# file=open('C:/Users/yyb/Desktop/brss/p2_1.txt','w')
# for fp in results:
# 	file.write(str(fp))
# 	file.write('\n')
# file.close()
plt.show()

