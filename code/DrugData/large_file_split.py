# use to split up large files for get_drug_data.py so does not error out 
# because hitting the API too many times in a row

import os
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))

lines_per_file = 1000
smallfile = None
with open(dir_path+'/biogrid_3study_standard_v3.csv') as bigfile:
    for lineno, line in enumerate(bigfile):
        if lineno % lines_per_file == 0:
            if smallfile:
                smallfile.close()
            small_filename = 'TEST-biogrid_3study_small_file_{}.txt'.format(lineno + lines_per_file)
            smallfile = open(small_filename, "w")
        smallfile.write(line)
    if smallfile:
        smallfile.close()