#!/usr/bin/env pythonafs

#from Numeric import *
#from LinearAlgebra import *
import sys
from os import system
import math
from numpy import *
#from pymadtable import madtable
from metaclass25 import twiss
import pickle


##############
def myvars():
##############
   variables=[   ' kqd.a81 ' ,
                  ' ktqx2.r5 ' ,
                  ' kq6.l5b1 ' ,
                  ' kqtl11.l7b1 ' ,
                  ' kq4.r2b1 ' ,
                  ' kqt13.l1b1 ' ,
                  ' kqt12.r8b1 ' ,
                  ' ktqx2.r8 ' ,
                  ' ktqx1.l1 ' ,
                  ' ktqx1.l2 ' ,
                  ' kqtd.a67b1 ' ,
                  ' kqtf.a78b1 ' ,
                  ' kq6.r4b1 ' ,
                  ' kq9.l8b1 ' ,
                  ' kqtl7.r3b1 ' ,
                  ' kqtl11.r6b1 ' ,
                  ' kq7.r5b1 ' ,
                  ' ktqx1.l5 ' ,
                  ' kq4.l8b1 ' ,
                  ' kq8.r6b1 ' ,
                  ' kq10.r8b1 ' ,
                  ' ktqx1.l8 ' ,
                  ' kqt12.l5b1 ' ,
                  ' kq4.lr3 ' ,
                  ' kq6.l1b1 ' ,
                  ' kqt13.l6b1 ' ,
                  ' kq5.r8b1 ' ,
                  ' kqtl11.l3b1 ' ,
                  ' kq7.l2b1 ' ,
                  ' kqt12.r4b1 ' ,
                  ' kq4.lr7 ' ,
                  ' kq10.l5b1 ' ,
                  ' kqt13.r5b1 ' ,
                  ' kqf.a23 ' ,
                  ' kqtd.a78b1 ' ,
                  ' kqtl11.r2b1 ' ,
                  ' kq9.l4b1 ' ,
                  ' kq7.r1b1 ' ,
                  ' kq8.r2b1 ' ,
                  ' kq10.r4b1 ' ,
                  ' ktqx1.r1 ' ,
                  ' kq5.l5b1 ' ,
                  ' ktqx1.r2 ' ,
                  ' kqtl10.l7b1 ' ,
                  ' kqt12.l1b1 ' ,
                  ' kqf.a45 ' ,
                  ' ktqx1.r5 ' ,
                  ' kqtl11.l8b1 ' ,
                  ' kqt13.l2b1 ' ,
                  ' kq5.r4b1 ' ,
                  ' ktqx1.r8 ' ,
                  ' kq8.l8b1 ' ,
                  ' kqtl9.l7b1 ' ,
                  ' kq6.r5b1 ' ,
                  ' kqtl11.r7b1 ' ,
                  ' kq5.lr3 ' ,
                  ' kq10.l1b1 ' ,
                  ' kqt13.r1b1 ' ,
                  ' kq5.lr7 ' ,
                  ' kqf.a67 ' ,
                  ' kqf.a81 ' ,
                  ' kqd.a12 ' ,
                  ' kq9.r8b1 ' ,
                  ' kq5.l1b1 ' ,
                  ' kqt12.l6b1 ' ,
                  ' kq4.r8b1 ' ,
                  ' kqtl10.l3b1 ' ,
                  ' kqt13.l7b1 ' ,
                  ' kq6.l2b1 ' ,
                  ' kqtl11.l4b1 ' ,
                  ' kqt12.r5b1 ' ,
                  ' kq8.l4b1 ' ,
                  ' kq10.l6b1 ' ,
                  ' kq6.r1b1 ' ,
                  ' kqd.a34 ' ,
                  ' kqt13.r6b1 ' ,
                  ' kqtl9.l3b1 ' ,
                  ' kq9.l5b1 ' ,
                  ' kqtl11.r3b1 ' ,
                  ' kqtf.a81b1 ' ,
                  ' kq7.r2b1 ' ,
                  ' kq10.r5b1 ' ,
                  ' kq4.l5b1 ' ,
                  ' kqx.l1 ' ,
                  ' kqx.l2 ' ,
                  ' kq5.l6b1 ' ,
                  ' kq9.r4b1 ' ,
                  ' kq6.l7b1 ' ,
                  ' kqt12.l2b1 ' ,
                  ' kqd.a56 ' ,
                  ' kqx.l5 ' ,
                  ' kqt13.l3b1 ' ,
                  ' kq7.l8b1 ' ,
                  ' kqtf.a12b1 ' ,
                  ' kq5.r5b1 ' ,
                  ' kqtl8.l7b1 ' ,
                  ' kqx.l8 ' ,
                  ' kqtl10.r7b1 ' ,
                  ' kqt12.r1b1 ' ,
                  ' kq10.l2b1 ' ,
                  ' kqtl11.r8b1 ' ,
                  ' kqt13.r2b1 ' ,
                  ' kq9.l1b1 ' ,
                  ' kqtd.a81b1 ' ,
                  ' kq8.r8b1 ' ,
                  ' kqd.a78 ' ,
                  ' kqtl9.r7b1 ' ,
                  ' kq4.l1b1 ' ,
                  ' kq10.r1b1 ' ,
                  ' kqt12.l7b1 ' ,
                  ' kq5.l2b1 ' ,
                  ' kqt13.l8b1 ' ,
                  ' kq6.l3b1 ' ,
                  ' kqtl11.l5b1 ' ,
                  ' kqtd.a12b1 ' ,
                  ' kqtf.a23b1 ' ,
                  ' kq7.l4b1 ' ,
                  ' kqt12.r6b1 ' ,
                  ' kqtl8.l3b1 ' ,
                  ' kqx.r1 ' ,
                  ' kq5.r1b1 ' ,
                  ' kq8.l5b1 ' ,
                  ' kqtl10.r3b1 ' ,
                  ' kqx.r2 ' ,
                  ' kqt13.r7b1 ' ,
                  ' kq6.r2b1 ' ,
                  ' kqtl11.r4b1 ' ,
                  ' kq9.l6b1 ' ,
                  ' kqx.r5 ' ,
                  ' kqf.a12 ' ,
                  ' kq4.l6b1 ' ,
                  ' kq8.r4b1 ' ,
                  ' kq10.r6b1 ' ,
                  ' kqx.r8 ' ,
                  ' kqtl9.r3b1 ' ,
                  ' kq9.r5b1 ' ,
                  ' kq6.l8b1 ' ,
                  ' kqt12.l3b1 ' ,
                  ' kq4.r5b1 ' ,
                  ' kqtl7.l7b1 ' ,
                  ' kqt13.l4b1 ' ,
                  ' kqt4.lr3 ' ,
                  ' kq5.r6b1 ' ,
                  ' kqtl11.l1b1 ' ,
                  ' kqtf.a34b1 ' ,
                  ' kqtd.a23b1 ' ,
                  ' kqf.a34 ' ,
                  ' kqt12.r2b1 ' ,
                  ' kq6.r7b1 ' ,
                  ' kq8.l1b1 ' ,
                  ' kqt13.r3b1 ' ,
                  ' kqt4.lr7 ' ,
                  ' kq7.r8b1 ' ,
                  ' kq9.l2b1 ' ,
                  ' kqtl8.r7b1 ' ,
                  ' kq4.l2b1 ' ,
                  ' kq10.r2b1 ' ,
                  ' kqf.a56 ' ,
                  ' kq9.r1b1 ' ,
                  ' kqt12.l8b1 ' ,
                  ' kq6.l4b1 ' ,
                  ' kq4.r1b1 ' ,
                  ' kqtl11.l6b1 ' ,
                  ' kqtl7.l3b1 ' ,
                  ' kq7.l5b1 ' ,
                  ' kq5.r2b1 ' ,
                  ' kqtd.a45b1 ' ,
                  ' kqt12.r7b1 ' ,
                  ' ktqx2.l1 ' ,
                  ' ktqx2.l2 ' ,
                  ' kq8.l6b1 ' ,
                  ' kqtf.a45b1 ' ,
                  ' kqtd.a34b1 ' ,
                  ' kq10.l8b1 ' ,
                  ' kq6.r3b1 ' ,
                  ' kqt13.r8b1 ' ,
                  ' kqtl11.r5b1 ' ,
                  ' ktqx2.l5 ' ,
                  ' kq7.r4b1 ' ,
                  ' kqf.a78 ' ,
                  ' kqt5.lr3 ' ,
                  ' kqtl8.r3b1 ' ,
                  ' kqd.a23 ' ,
                  ' kq8.r5b1 ' ,
                  ' ktqx2.l8 ' ,
                  ' kq9.r6b1 ' ,
                  ' kq5.l8b1 ' ,
                  ' kqt5.lr7 ' ,
                  ' kqt12.l4b1 ' ,
                  ' kq4.r6b1 ' ,
                  ' kqt13.l5b1 ' ,
                  ' kqtl11.l2b1 ' ,
                  ' kqd.a45 ' ,
                  ' kq7.l1b1 ' ,
                  ' kqtd.a56b1 ' ,
                  ' kqt12.r3b1 ' ,
                  ' kqtf.a67b1 ' ,
                  ' kq6.r8b1 ' ,
                  ' kqtf.a56b1 ' ,
                  ' kq10.l4b1 ' ,
                  ' kq8.l2b1 ' ,
                  ' kqtl7.r7b1 ' ,
                  ' kqt13.r4b1 ' ,
                  ' kqtl11.r1b1 ' ,
                  ' kq8.r1b1 ' ,
                  ' ktqx2.r1 ' ,
                  ' ktqx2.r2 ' ,
                  ' kq9.r2b1 ' ,
                  ' kq5.l4b1 ' ,
                  ' kqd.a67 ' ]

   return variables


#########################
def writeparams(deltafamilie):
#########################
    global variables
    g = open ('changeparameters', 'w')
    i=0
    for var in variables:
        g.write(var+' ='+ var+'+ ('+str(deltafamilie[i])+');\n')
        i +=1
    g.close()
    return



#########################
def justtwiss(deltafamilies):
#########################
    print deltafamilies
    writeparams(deltafamilies)
    system('madx < job.iterate.madx > scum')
    x=twiss('twiss.dat')
    return x






FullResponse={}   #Initialize FullResponse
variables=myvars()            #Define variables
delta1=zeros(len(variables))*1.0   #Zero^th of the variables
incr=ones(len(variables))*0.0001    #increment of variables


FullResponse['incr']=incr           #Store this info for future use
FullResponse['delta1']=delta1       #"     "     "
FullResponse['0']=justtwiss(delta1) #Response to Zero, base , nominal


for i in range(0,len(delta1)) : #Loop over variables
        delta=array(delta1)
        delta[i]=delta[i]+incr[i]
        FullResponse[variables[i]]=justtwiss(delta)

pickle.dump(FullResponse,open('FullResponse','w'),-1)


