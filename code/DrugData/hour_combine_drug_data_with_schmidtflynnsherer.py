# formats data so hour can be used as the taget node in Cytoscape
import os
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))
AllData = []
DrugProteins = []

with open(dir_path+'/schmidtflynnshererstandard_v4.csv') as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        AllData.append(row)

with open(dir_path+'/schmidtflynnsherer_protien_drug_data_v1.csv') as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        DrugProteins.append(row)


with open('hour_schmidtflynnsherer_drug_protein_rows_v1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # symbol_id,unique_protein_id,interacting_RNA,cell_line,hour,species,study
    writer.writerow(["symbol_id", "unique_protein_id","species","interactor","cell_line","hour","study","interaction_type","drug_approved"])

    for item in AllData:
        for prot in DrugProteins:
            if item['symbol_id'] == prot['symbol_id']:
                # writer.writerow((item["symbol_id"],item["unique_protein_id"],item["species"],prot['drug_name'],prot['drug_name'],"-",item["study"],"Protien Drug",prot["approved"]))
                writer.writerow((prot['drug_name'],item["unique_protein_id"],item["species"],item["symbol_id"],"-",item["symbol_id"],item["study"],"Protien Drug",prot["approved"]))
        writer.writerow((item["symbol_id"],item["unique_protein_id"],item["species"],item["interacting_RNA"],item["cell_line"],item["hour"],item["study"],"Protien RNA",'-'))