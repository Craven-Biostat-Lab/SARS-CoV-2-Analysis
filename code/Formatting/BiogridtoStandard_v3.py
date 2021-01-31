# converts biogrid data set to standard format
# only add interactions between SARS-CoV-2:SARS-CoV-2 and human-SARS-CoV-2

import csv
import os 


dir_path = os.path.dirname(os.path.realpath(__file__))


AllData = []
protienDB = []
with open(dir_path+'/biogrid_data.csv') as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        AllData.append(row)

with open(dir_path+'/gene_with_protein_product.csv') as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        protienDB.append(row)


with open('biogridstandard_v3.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["symbol_id_A", "unique_protein_id_A","species_A","interactor_B","species_B","cell_line","hour","study","interaction_type"])

    for item in AllData:
        species_A = item['Organism Name Interactor B']
        species_B = item['Organism Name Interactor A']

        if((species_A == 'Homo sapiens' and species_B == 'Severe acute respiratory syndrome coronavirus 2') or (species_A == 'Severe acute respiratory syndrome coronavirus 2' and species_B == 'Homo sapiens') or (species_A == 'Severe acute respiratory syndrome coronavirus 2' and species_B == 'Severe acute respiratory syndrome coronavirus 2')):
            # print("A:", species_A, "    B: ",species_B)

            symbol_id_A = item['Official Symbol Interactor B']
            interactor_B = item['Official Symbol Interactor A']
            study = item['Author']

            standard_symbol = False

            for protien in protienDB:
                if symbol_id_A == protien['symbol']:
                    protienID_A = protien['uniprot_ids']
                    standard_symbol = True
            if standard_symbol == False:
                # print(protien['symbol'])
                for protien in protienDB:
                    if protien['prev_symbol'] != "":
                        prev_symbol_array = protien['prev_symbol'].split("|")
                        # print(prev_symbol_array)
                        for prev_symbol in prev_symbol_array:
                            if prev_symbol == symbol_id_A:
                                symbol_id_A = protien['symbol']
                    protienID_A = protien['uniprot_ids']

            writer.writerow((symbol_id_A,protienID_A,species_A,interactor_B,species_B,'-','-',study,'Protein Protein'))

