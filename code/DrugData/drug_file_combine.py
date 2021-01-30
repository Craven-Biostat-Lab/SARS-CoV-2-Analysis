# combines files into one large file 
# (use to recombine drug files seperated because of API limits)

import os
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))
filenum = 1000

while filenum < 22000:
    AllData = []
    with open(dir_path+'/protien_drug_data_'+str(filenum)+'_v2.csv') as fh:
        rd = csv.DictReader(fh, delimiter=',')
        for row in rd:
            AllData.append(row)



    with open(dir_path+'/full_list_protien_drug_data_v1.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["symbol_id","drug_name","approved","approval_source"])

        for item in AllData:
            writer.writerow((item["symbol_id"],item["drug_name"],item["approved"],item["approval_source"]))

    filenum = filenum + 1000

