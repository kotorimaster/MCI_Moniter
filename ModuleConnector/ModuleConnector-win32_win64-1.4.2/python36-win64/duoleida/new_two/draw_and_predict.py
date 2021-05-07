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


####################################################################

yuce_x=[]
yuce_xx=[]
yuce_xxx=[]
yuce_y=[]
quan=[]
fig=plt.figure()
h=1
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


for i in range(380):

	print("===========" + str(i) + "===========")


	def chuli(a3):
		a3 = np.array(a3)
		a3 = a3 / 15.6
		quan.append(a3)

		a3 = np.reshape(a3, [a3.shape[0], 1])

		a3_list = a3.tolist()

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
	rrrr2 = chuli(a1)



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



	print "**************************************"+str(len(rrrr_list))
	print "**************************************"+str(len(rrrr_new_list))
	# for jjjj in range(len(rrrr_list)):
	# 	plt.scatter(i, rrrr_list[jjjj]/10.0, color='r')
	# 	# plt.scatter(i, rrrr_new_list[jjjj], color='b')
	for jjjj in range(len(rrrr_new_list)):

		plt.scatter(i, rrrr_new_list[jjjj], color='r',s=area)
	end2=time.clock()









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

plt.show()

