#!/afs/cern.ch/eng/sl/lintrack/Python-2.5/bin//python2.5

########!#######/afs/cern.ch/eng/sl/lintrack/Python-2.4.3/bin/python2.4
import __init__
import sussix4drivexxNoO
from numpy import *
from random import gauss
from string import *
import os

#######################################################
def sussix_inp(ir=1, turns=500, tunex=0.1, tuney=0.2, istun=0.05, idam=2, narm=2):
#######################################################
    
    si=open("sussix_v4.inp", "w")
    si.write('C\nC INPUT FOR SUSSIX_V4 ---17/09/1997---\n')
    si.write('C DETAILS ARE IN THE MAIN PROGRAM SUSSIX_V4.F\nC\n\n')
    si.write('ISIX  = 0\nNTOT  = 1\nIANA  = 1\nICONV = 0\n')
    si.write('TURNS = 1 '+str(turns)+'\n')
    si.write('NARM  = '+str(narm)+'\nISTUN = 1 '+str(istun)+'  '+str(istun)+'\n')
    si.write('TUNES = '+str(tunex)+'  '+str(tuney)+' .07\n')
    si.write('NSUS  = 0\nIDAM  = '+ str(idam)+ '\n')
    si.write('NTWIX = 1\nIR    = '+str(ir) + '\nIMETH = 2\nNRC   = 6\nEPS   = 1D-3\n')
    si.write('NLINE = 0\nL,M,K = \nIDAMX = 1\nNFIN  = 500\nISME  = 1\n')
    si.write('IUSME = 200\nINV   = 0\nIINV  = 250\nICF   = 0\nIICF  = 350\n')
    si.close()     
    return



#####################
class sussixout:
#####################
    "Structure for sussix output"
    def __init__(self, z):
        self.tunexy=z[0]
        self.amplitude=z[1]
        self.phase=z[2]
        self.ox=z[3]
        self.ax=z[4]
        self.oy=z[5]
        self.ay=z[6]

        


#####################
def fillorcut(vec, n):
####################
    lv=len(vec)
    if (lv>n):
        return vec[0:n]
    elif   (lv<n):
        return concatenate([vec, zeros(n-lv)])
    elif   (lv==n):
        return vec


################################################
def sussix(x0,x1,x2):
################################################
    #dim=(4404, 2, 14,14,300,300,300,300)
    #y0=fillorcut(x0, 1100)
    #y1=fillorcut(x1, 1100)
    
    if len(x0) == len(x1):
        y3=fillorcut(concatenate([x0,x1,x2]), 4*len(x0))
        print "calling sussix", len(y3), len(x0)
        z=sussixout(sussix4drivexxNoO.sussix4drivenoise(y3, len(x0)))
        return z
    else:
        print "Different number of turns in x and y"
        return 0

################################################
def sussixBPM(x0,x1,x2,x3):
################################################
    #dim=(4404, 2, 14,14,300,300,300,300)
    #y0=fillorcut(x0, 1100)
    #y1=fillorcut(x1, 1100)

    y3=fillorcut(concatenate([x0,x1,zeros(len(x2)), zeros(len(x3))]), 4*len(x0))
    z1=sussixout(sussix4drivexxNoO.sussix4drivenoise(y3, len(x0)))
    y3=fillorcut(concatenate([x2,x3,zeros(len(x2)), zeros(len(x3))]), 4*len(x0))
    z2=sussixout(sussix4drivexxNoO.sussix4drivenoise(y3, len(x0)))
    ratiox=z1.amplitude[0]/z2.amplitude[0]
    ratioy=z1.amplitude[3]/z2.amplitude[3]
    dphix=(z2.phase[0]-z1.phase[0])*pi/180.
    dphiy=(z2.phase[3]-z1.phase[3])*pi/180.
    if len(x0) == len(x1):
        x2=(x2*ratiox - x0*cos(dphix) )/sin(dphix)
        x3=(x3*ratioy - x1*cos(dphiy) )/sin(dphiy)
        y3=fillorcut(concatenate([x0,x1,x2,x3]), 4*len(x0))
        print "calling sussix", len(y3), len(x0)
        z=sussixout(sussix4drivexxNoO.sussix4drivenoise(y3, len(x0)))
        return z
    else:
        print "Different number of turns in x and y"
        return 0


def read_BPM_data_from_SDDS_file(bpm_name, sdds_file_path, normalization_factor=1, start_turn=None, end_turn=None):
    bpm_data = {}

    assert os.path.exists(sdds_file_path)
    with open(sdds_file_path) as sdds_file:
        for line in sdds_file:
            line = line.split()
            if line[1] == bpm_name:
                assert line[0] in ['0', '1']
                if line[0] == '0':
                    plane = 'X'
                else:
                    plane = 'Y'
                if not start_turn: start_turn = 0
                if not end_turn: end_turn = len(line)
                bpm_data[plane] = [float(d) * normalization_factor for d in line[3 + start_turn:end_turn]]
    return bpm_data


if __name__ == '__main__':

    sdds_model = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned'
    sussix_inp(ir=1, turns=2000, tunex=0.28, tuney=0.31, istun=0.05, idam=2)

    bpm1 = 'BPM.17R2.B2'
    bpm2 = 'BPM.16R2.B2'
    bpm_data1 = read_BPM_data_from_SDDS_file(bpm1, sdds_model)
    bpm_data2 = read_BPM_data_from_SDDS_file(bpm2, sdds_model)
    print bpm_data1['X']
    # res = sussixBPM(bpm_data1['X'],bpm_data2['X'],bpm_data1['Y'],bpm_data2['Y'])



    # fig = plt.figure(figsize=(20, 7))
    # fig.patch.set_facecolor('white')
    # t1 = fig.add_subplot(111)
    # markerline, stemlines, baseline = t1.stem(res.ox, res.ax, '-.', bottom=1e-9, markerfmt = " ")
    # plt.setp(baseline, 'color','r', 'linewidth', 2)
    # plt.setp(stemlines, 'color', 'r', 'linewidth', 2, 'linestyle', 'solid')



#x=array(map(cos ,  0.35*2*pi*array(range(0,10000))))
#y=array(map(cos ,  0.14*2*pi*array(range(0,10000))))


#a=sussix(x,y)
#print a.tunexy
#print a.amplitude
#for i in range(100):
#    print a.ox[i], a.ax[i],a.oy[i], a.ay[i]


