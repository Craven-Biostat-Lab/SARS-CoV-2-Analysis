# combine biogrid human-covid with sherer, flynn and schmidt data

import csv
import os 
import shutil

dir_path = os.path.dirname(os.path.realpath(__file__))

# copies biogrid data (in correct format) into new file for combine data
shutil.copy2(dir_path+'/biogridstandard_v3.csv', dir_path+'/biogrid_3study_standard_v3.csv')
AllData = []

# reads each row in the 3 study data into an dict object into an array
with open(dir_path+'/schmidtflynnshererstandard_v4.csv') as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        AllData.append(row)

# appends 3 study to new biogrid file with format changed to match
with open(dir_path+'/biogrid_3study_standard_v3.csv','a', newline='') as file:
    writer = csv.writer(file)
    for item in AllData:  
        writer.writerow((item['symbol_id'],item['unique_protein_id'],item['species'],item['interacting_RNA'],'Severe acute respiratory syndrome coronavirus 2',item['cell_line'],item['hour'],item['study'],'Protien RNA'))