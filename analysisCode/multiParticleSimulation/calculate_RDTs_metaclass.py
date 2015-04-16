import __init__
import numpy as np
import logging, time
import time
import os
from Utilities import tfs_file_writer
from Python_Classes4MAD import metaclass


def calc_RDTs(twiss_file_path, output_file_path, bpm_name):
    a = metaclass.twiss(twiss_file_name)
    a.fterms()
    NAME = a.NAME
    positions = a.S
#     my_3000 = a.f3000
#     my_2100 = a.f2100
#     my_1020 = a.f1020
#     my_1002 = a.f1002
#     my_1011 = a.f1011
#     my_2000 = a.f2000
    my_4000 = a.f4000
    my_3100 = a.f3100
#     my_0120 = a.f0120
#     my_0111 = a.f0111
#     my_1200 = a.f1200
    
    b = metaclass.twiss(twiss_file_name)
    b.fterms_generic(fterms_list=['3000','2100','1020','1002','1011','2000','4000','3100'], conjugate_list=['0120','0111','1200'])    
    NAME_generic = b.NAME
    positions_generic = b.S    
#     my_3000_generic = b.f3000
#     my_2100_generic = b.f2100
#     my_1020_generic = b.f1020
#     my_1002_generic = b.f1002
#     my_1011_generic = b.f1011
#     my_2000_generic = b.f2000
    my_4000_generic = b.f4000
    my_3100_generic = b.f3100
#     my_0120_generic = b.f0120
#     my_0111_generic = b.f0111
#     my_1200_generic = b.f1200

    # OLD
    fterms_file = tfs_file_writer.TfsFileWriter.open(output_file_path)
    fterms_file.set_column_width(33)
 
    fterms_file.add_column_names([      "NAME",     "S",  '4000', '3100'])#  '3000','2100','1020','1002','1011','2000','4000','0120','0111','1200'])
    fterms_file.add_column_datatypes(["%bpm_s",     "%le","%le","%le"])#,"%le","%le",  "%le",  "%le",  "%le",  "%le",  "%le",  "%le"])
 
    for i in range(len(NAME)):
        fterms_file.add_table_row([NAME[i], positions[i], my_3100[i], my_4000[i]])# my_3000[i], my_2100[i], my_1020[i], my_1002[i], my_1011[i], my_2000[i], my_4000[i], my_0120[i], my_0111[i], my_1200[i] ])
         
    fterms_file.write_to_file()
    
    # GENERIC
    fterms_file_gen = tfs_file_writer.TfsFileWriter.open(output_file_path+'.generic')
    fterms_file_gen.set_column_width(33)

    fterms_file_gen.add_column_names([      "NAME",     "S",  '4000', '3100'])#  '3000','2100','1020','1002','1011','2000','4000','0120','0111','1200'])
    fterms_file_gen.add_column_datatypes(["%bpm_s",     "%le","%le","%le"])#,"%le","%le",  "%le",  "%le",  "%le",  "%le",  "%le",  "%le"])

    for i in range(len(NAME_generic)):
        fterms_file_gen.add_table_row([NAME_generic[i], positions_generic[i], my_3100_generic[i], my_4000_generic[i]])# my_3000_generic[i], my_2100_generic[i], my_1020_generic[i], my_1002_generic[i], my_1011_generic[i], my_2000_generic[i], my_4000_generic[i], my_0120_generic[i], my_0111_generic[i], my_1200_generic[i] ])
        
    fterms_file_gen.write_to_file()

#     header = '''
# # RESONANT DRIVING TERMS DETERMINED BY METACLASS IN Python_Classes4MAD
# # Beam 2
# # Normal octupolar RDT terms
# $ ELEMENT    f4000    f3100    f2020    f1102    f2002    f0031    f0040
# '''
#     
#     with open(output_file_path, 'w') as RDT_results:
#         RDT_results.write(header)
#         print len(my_f4000)
#         for i in range(len(my_f4000)):
#             line = "{0:10f}\n".format(my_f4000[i])# {1:10f}  {2:10f} {3:10f} {4:10f} {5:10f} {6:10f}\n".format(my_f4000[i],my_f3100[i],my_f2020[i],my_f1102[i],my_f2002[i],my_f0031[i],my_f0040[i])
#             RDT_results.write(line)


if __name__ == '__main__':
    working_directory   = '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/'
    twiss_file_name     = 'twiss_elements_gen.dat'
    bpm_name            = 'BPM.33R3.B2'
    output_file_name    = 'RDT'

    twiss_file_path = os.path.join(working_directory,twiss_file_name) 
    output_file_path= os.path.join(working_directory,output_file_name)

    calc_RDTs(twiss_file_path, output_file_path, bpm_name)
