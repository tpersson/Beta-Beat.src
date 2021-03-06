import sys
if "/afs/cern.ch/eng/sl/lintrack/Python_Classes4MAD/" not in sys.path: # add internal path for python scripts to current environment (tbach, 2012/05)
    sys.path.append("/afs/cern.ch/eng/sl/lintrack/Python_Classes4MAD/")

try:
    from Numeric import *
    from LinearAlgebra import *
except:
    from numpy import *
    from numpy import dot as matrixmultiply
from os import system
import math
import pickle
from metaclass import twiss
from optparse import OptionParser

def shell_command(cmd):
    ret=system(cmd)
    if ret:
        raise ValueError("COMMAND: %s finished with exit value %i" % (cmd,ret))

##### optionparser
parser = OptionParser()
parser.add_option("-a", "--accel",
                help="Which accelerator: LHCB1 LHCB2 SPS RHIC SOLEIL",
                metavar="ACCEL", default="LHCB1",dest="accel")
parser.add_option("-p", "--path",
                help="path to save",
                metavar="path", default="./",dest="path")
parser.add_option("-c", "--core",
                help="core files",
                metavar="core", default="/afs/cern.ch/eng/sl/lintrack/Beta-Beat.src/MODEL/LHCB/fullresponse/",dest="core")
parser.add_option("-k", "--deltak",
                help="delta k to be applied to quads for sensitivity matrix",
                metavar="core", default="0.00002",dest="k")


(options, args) = parser.parse_args()

# paths
corepath=options.core
accel=options.accel
path=options.path


#
# Chromatic coupling
#

FullResponse={}   #Initialize FullResponse
execfile(corepath+"/"+accel+'/AllLists_chromcouple.py')
exec('variables=kss()')           #Define variables
delta1=zeros(len(variables))*1.0   #Zero^th of the variables
incr=ones(len(variables))*0.05    #increment of variables
dpp=0.0001
FullResponse['incr']=incr           #Store this info for future use
FullResponse['delta1']=delta1


######## loop over normal variables
f=open(path+'/iter.madx','w')
for i in range(0,len(delta1)) : #Loop over variables
    delta=array(delta1)
    delta[i]=delta[i]+incr[i]
    var=variables[i]
    print >>f, var,"=", var, "+(",delta[i],");"
    print >>f, "twiss, deltap= "+str(dpp)+",file=\""+path+"/twiss.dp+."+var+"\";"
    print >>f, "twiss, deltap=-"+str(dpp)+",file=\""+path+"/twiss.dp-."+var+"\";"
    print >>f, var,"=", var, "-(",delta[i],");"

print >>f, "twiss, deltap= "+str(dpp)+",file=\""+path+"/twiss.dp+.0\";"
print >>f, "twiss, deltap=-"+str(dpp)+",file=\""+path+"/twiss.dp-.0\";"
f.close()
print "Runing MADX"
shell_command('/afs/cern.ch/group/si/slap/bin/madx < '+path+'/job.iterate.madx')


varsforloop=variables+['0']
for i in range(0,len(varsforloop)) : #Loop over variables

    var=varsforloop[i]
    print  "Reading twiss.dp+."+var
    xp=twiss(path+"/twiss.dp+."+var)
    xp.Cmatrix()
    print  "Reading twiss.dp-."+var
    xm=twiss(path+"/twiss.dp-."+var)
    xm.Cmatrix()
    # Initializing and Calculating chromatic coupling for every BPM
    xp.Cf1001r=[]
    xp.Cf1001i=[]
    xp.Cf1010r=[]
    xp.Cf1010i=[]
    for j in range(len(xp.NAME)):

        vvv=(xp.F1001R[j]-xm.F1001R[j])/(2*dpp)
        xp.Cf1001r.append(vvv)

        vvv=(xp.F1001I[j]-xm.F1001I[j])/(2*dpp)
        xp.Cf1001i.append(vvv)

        vvv=(xp.F1001R[j]-xm.F1001R[j])/(2*dpp)
        xp.Cf1010r.append(vvv)

        vvv=(xp.F1010I[j]-xm.F1010I[j])/(2*dpp)
        xp.Cf1010i.append(vvv)

    FullResponse[var]=xp
    system('rm '+path+'/twiss.dp+.'+var)
    system('rm '+path+'/twiss.dp-.'+var)


#FullResponse['0']=twiss(path+'/twiss.0') # already in the loop

pickle.dump(FullResponse,open(path+'/FullResponse_chromcouple','w'),-1)


# sys.exit()


#
# Coupling
#

FullResponse={}   #Initialize FullResponse
execfile(corepath+"/"+accel+'/AllLists_couple.py')
exec('variables=Qs()')           #Define variables
delta1=zeros(len(variables))*1.0   #Zero^th of the variables
incr=ones(len(variables))*0.0001    #increment of variables


FullResponse['incr']=incr           #Store this info for future use
FullResponse['delta1']=delta1       #"     "     "

######## loop over normal variables
f=open(path+'/iter.madx','w')
for i in range(0,len(delta1)) : #Loop over variables
    delta=array(delta1)
    delta[i]=delta[i]+incr[i]
    var=variables[i]
    print >>f, var,"=", var, "+(",delta[i],");"
    print >>f, "twiss, file=\""+path+"/twiss."+var+"\";"
    print >>f, var,"=", var, "-(",delta[i],");"

print >>f, "twiss, file=\""+path+"/twiss.0\";"

f.close()

shell_command('/afs/cern.ch/group/si/slap/bin/madx < '+path+'/job.iterate.madx')


for i in range(0,len(delta1)) : #Loop over variables
    delta=array(delta1)
    delta[i]=delta[i]+incr[i]
    var=variables[i]
    print "Reading twiss."+var
    x=twiss(path+"/twiss."+var)
    x.Cmatrix()
    FullResponse[var]=x
    system('rm '+path+'/twiss.'+var)


FullResponse['0']=twiss(path+'/twiss.0') #Response to Zero, base , nominal

pickle.dump(FullResponse,open(path+'/FullResponse_couple','w'),-1)



#
#
# Beta
#
#
FullResponse={}   #Initialize FullResponse
execfile(corepath+"/"+accel+'/AllLists.py')
exec('variables=Q()')           #Define variables
delta1=zeros(len(variables))*1.0   #Zero^th of the variables
#incr=ones(len(variables))*0.00005    #increment of variables    #### when squeeze low twiss fails because of to big delta
incr=ones(len(variables))*float(options.k)


FullResponse['incr']=incr           #Store this info for future use
FullResponse['delta1']=delta1       #"     "     "

######## loop over normal variables
f=open(path+'/iter.madx','w')
for i in range(0,len(delta1)) : #Loop over variables
    delta=array(delta1)
    delta[i]=delta[i]+incr[i]
    var=variables[i]
    print >>f, var,"=", var, "+(",delta[i],");"
    print >>f, "twiss, file=\""+path+"/twiss."+var+"\";"
    print >>f, var,"=", var, "-(",delta[i],");"

print >>f, "twiss,file=\""+path+"/twiss.0\";"
f.close()

shell_command('/afs/cern.ch/group/si/slap/bin/madx < '+path+'/job.iterate.madx')


for i in range(0,len(delta1)) : #Loop over variables
    delta=array(delta1)
    delta[i]=delta[i]+incr[i]
    var=variables[i]
    print "Reading twiss."+var
    FullResponse[var]=twiss(path+"/twiss."+var)
    system('rm '+path+'/twiss.'+var)


FullResponse['0']=twiss(path+'/twiss.0') #Response to Zero, base , nominal

pickle.dump(FullResponse,open(path+'/FullResponse','w'),-1)
