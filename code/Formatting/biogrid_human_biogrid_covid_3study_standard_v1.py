# combines the biogrid human, biogrid covid / humans interactions file and the schmidt, flynn sherer data 

import csv
import os 
import shutil

dir_path = os.path.dirname(os.path.realpath(__file__))
shutil.copy2(dir_path+'/biogridstandard_v3.csv', dir_path+'/biogrid_human_biogrid_covid_3study_standard_v1.csv')
AllData3Study = []
BiogridHuman = []

with open(dir_path+'/schmidtflynnshererstandard_v4.csv') as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        AllData3Study.append(row)

with open(dir_path+'/humanproteininteractionstandard_v1.csv') as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        BiogridHuman.append(row)

# appends 3 study to new biogrid file with format changed to match
with open(dir_path+'/biogrid_human_biogrid_covid_3study_standard_v1.csv','a', newline='') as file:
    writer = csv.writer(file)
    for item in AllData3Study:  
        writer.writerow((item['symbol_id'],item['unique_protein_id'],item['species'],item['interacting_RNA'],'Severe acute respiratory syndrome coronavirus 2',item['cell_line'],item['hour'],item['study'],'Protien RNA'))


with open(dir_path+'/biogrid_human_biogrid_covid_3study_standard_v1.csv','a', newline='') as file:
    writer = csv.writer(file)
    for item in BiogridHuman:  
        writer.writerow((item['symbol_id_A'],item['unique_protein_id_A'],item['species_A'],item['symbol_id_B'],item['species_A'],item['cell_line'],item['hour'],item['study'],'Protien Protien Human'))
