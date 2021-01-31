# converts Flynn data to standard format

import csv
import os 

def get_protien_id(majProtX):
    if(majProtX != 'NA'):
        return majProtX.split("|")[1]
    else:
        return 'NA'

dir_path = os.path.dirname(os.path.realpath(__file__))


AllData = []
protienDB = []
with open(dir_path+'/Flynn.csv') as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        AllData.append(row)

with open(dir_path+'/gene_with_protein_product.csv') as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        protienDB.append(row)

with open('flynnstandard_v3.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["symbol_id", "unique_protein_id","interacting_RNA","cell_line","hour","species","study"])
    
    for item in AllData:
        if item['species.x'] =='HUMAN' and (item['huh_d1'] == 'TRUE' or item['vero_d2'] == 'TRUE' or item['huh_d1'] == 'TRUE' or item['vero_d1'] == 'TRUE'):
            proteinId = get_protien_id(item['majority.protein.x'])
            symbol_id = item['name']
            standard_symbol = False

            for protien in protienDB:
                if symbol_id == protien['symbol']:
                    # protienID = protien['uniprot_ids']
                    standard_symbol = True
            if standard_symbol == False:
                # print(protien['symbol'])
                for protien in protienDB:
                    if protien['prev_symbol'] != "":
                        prev_symbol_array = protien['prev_symbol'].split("|")
                        # print(prev_symbol_array)
                        for prev_symbol in prev_symbol_array:
                            if prev_symbol == symbol_id:
                                symbol_id = protien['symbol']
                    # protienID = protien['uniprot_ids']
            
            
            cellLine_Hr_Arr = {'huh_d1': item['huh_d1'],'huh_d2': item['huh_d2'],'vero_d1': item['vero_d1'],'vero_d2': item['vero_d2']}
            for cellLineHr, value in cellLine_Hr_Arr.items():
                if(value == 'TRUE'):
                    if(cellLineHr[:3] == 'huh'):
                        cellLine = 'Huh7.5'
                    if(cellLineHr[:4] == 'vero'):
                        cellLine = 'VeroE6'
                    if(cellLineHr[-2:] == 'd1'):
                        hr = 24
                    if(cellLineHr[-2:] == 'd2'):
                        hr = 48                    
                    writer.writerow((symbol_id,proteinId,'genomic',cellLine,hr,'homo sapien','Flynn'))


