#!/usr/bin/env python
# -*- coding: utf8 -*-

class ResonanceLines:
	resonanceLines = []
	
	def __init__(self, qx=0.28, qy=0.31, orderOfResonances=2, oneMinus=True):
		self.resonanceLines = self.computeResonanceLines(qx, qy, orderOfResonances, oneMinus)

	def getResonanceLines(self):
		return self.resonanceLines

	def computeResonanceLines(self, qx, qy, orderOfResonances, oneMinus):
		resonanceLines = []
		for i in range(-orderOfResonances, orderOfResonances+1):
			for j in range(-orderOfResonances, orderOfResonances+1):
				if oneMinus:
					resonanceLines.append([1.-abs(i*qx+j*qy), (i,j)])
				else:
					resonanceLines.append([abs(i*qx+j*qy), (i,j)])
		return resonanceLines