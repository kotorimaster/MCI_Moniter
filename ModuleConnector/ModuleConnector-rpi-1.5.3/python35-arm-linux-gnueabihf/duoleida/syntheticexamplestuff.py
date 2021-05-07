#!/usr/bin/env python


from gmphd import *
from numpy.random import rand


# The range of the space
span = (0, 60)
slopespan = (-2, 3)  # currently only used for clutter generation / inference

################################################################################
# pre-made transition/observation setups:

# state is [x, dx, offset].T, where the actual "location" in the physical sense is x+offset.
resfac = 0.95
transntypes = {
	'fixedvel': array([[1, 1, 0], [0, 1, 0], [0, 0, 1]]),  # simple fixed-velocity state update
	'vibrato': array([[1-resfac,1,0], [0-resfac,1,0], [0,0,1]])  # simple harmonic motion
	}

obsntypes = {
	# 1D spectrum-type - single freq value per bin
	'spect': {'obsnmatrix': array([[1, 0, 1]]), 
		  'noisecov': [[0.5]], 
		  'obstospec': array([[1]])
	},
	# 2D chirp-type [start, end]
	'chirp': {'obsnmatrix': array([[1, -0.5, 1], [1, 0.5, 1]]), 
		  'noisecov': [[0.5], [0.5]], 
		  'obstospec':  array([[0.5, 0.5]])
	}
	}

# Note: I have noticed that the birth gmm needs to be narrow/fine, because otherwise it can lead the pruning algo to lump foreign components together
birthgmm = [GmphdComponent(1.0, [0, 0, centre + 0.5], [[10.0, 0, 0], [0, 0.1, 0], [0, 0, 3]]) for centre in range(5, 80, 1)]  # fine carpet
# birthgmm = [GmphdComponent(1.0, [2, 0, offset], [[10.0, 0, 0], [0, 0.1, 0], [0, 0, 3]]) \
# 	for offset in range(0, 20, 1) ]  # fine carpet

###############################################################
class TrackableThing:
	def __init__(self, obsnmatrix, transnmatrix):
		self.state = sampleGm(birthgmm)		
		self.state = reshape(self.state, (size(self.state), 1)) # enforce column vec
		self.alive = True
		self.obsnmatrix = obsnmatrix
		self.transnmatrix = transnmatrix
	def updateState(self):
		self.state = dot(self.transnmatrix, self.state)
	def observe(self):
		return dot(self.obsnmatrix, self.state)

############################################################################
# utility functions

def clutterintensityfromtot(clutterintensitytot, obsntype):
	"from the total clutter, calculate the point-density of it"
	if obsntype == 'spect':
		clutterrange = (span[1] - span[0])
	else:
		clutterrange = (span[1] - span[0]) * (slopespan[1] - slopespan[0])
	return float(clutterintensitytot) / float(clutterrange)

def updatetrueitems(trueitems, survivalprob, birthprob, obsnmatrix, transnmatrix):
	"update true state of ensemble - births, deaths, movements"
	for item in trueitems:
		item.updateState()
		if (rand() >= survivalprob) or (int(round(item.observe()[0])) >= span[1]) or (int(round(item.observe()[0])) < span[0]):
			item.alive = False
	trueitems = filter(lambda x: x.alive, trueitems)
	if rand() < birthprob:
		trueitems.append(TrackableThing(obsnmatrix, transnmatrix))
	# print "True states:"
	# for item in trueitems:
	# 	# print list(item.state.flat)
	return trueitems


def updateandprune(g, obsset):
	# print "-------------------------------------------------------------------"
	g.update(obsset) # here we go!

	g.prune(maxcomponents=100, mergethresh=0.25)


def collateresults(g, obsset, bias, obsntype, directlystatetospec):
	#meh: intensity = g.gmmevalalongline([[-5,5], [0,0], [span[0]+5,span[1]-5]], span[1]-span[0])
	intensity = g.gmmevalgrid1d(span, span[1]-span[0], 2)  # "2" means just use the "offset" dimension

	integral = sum(array([comp.weight for comp in g.gmm]))

	# Get the estimated items, and also convert them back to vector representation for easy plotting
	#estitems = g.extractstates(bias=bias)
	estitems = g.extractstatesusingintegral(bias=bias)
	print "estimated %i items present" % len(estitems)
	# print estitems
	estspec = [0 for _ in range(span[0], span[1])]
	for x in estitems:
		# print('x***********&&&&&&&&&&&&&&&&&&&&&&&&&&&')
		# print x
		bin = int(round(dot(directlystatetospec, x)))   # project state space directly into spec
		if bin > -1 and bin < len(estspec):
			estspec[bin] += 1

	obsspec = obsFrameToSpecFrame(obsset, obsntype)
	return estspec


def obsFrameToSpecFrame(obsset, obsntype):
	"Convert an observation frame (a SET of observation data) into a specgram-type VECTOR frame, for easiest plotting."
	obsspec = [0 for _ in range(span[0], span[1])]
	transform = obsntypes[obsntype]['obstospec']
	for anobs in obsset:

		bin = int(round(dot(transform, anobs).flat[0]))##transform*anobs


		if bin > -1 and bin < len(obsspec):
			obsspec[bin] = 1


	return obsspec



