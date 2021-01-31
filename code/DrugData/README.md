# Drug Data
**This folder contains the files for everything related to Guide to Pharmacology data**
 
 
`get_drug_data.py` It takes a file in the standard format and then call the Guide to Pharmacology database for every protein in the file and then it creates a new file called `schmidtflynnsherer_protien_drug_data_v1.csv` with the protein symbol id, drug name, if it is approved and the who approved it / what year. There is a limit on how many times in a row you can use the API to hit the database. I recommend not doing more than 1000.
 
`large_file_split.py` splits files into multiple sub files which needs to be used if you are going to use the Guide to Pharmacology API over 1000 times in a row
 
` > SplitBiogrid3StudyData` contains the contents of the split biogrid 3 study file separated into sets of 1000
 
`drug_file_combine.py` recombines the drug data files that had to be seperated for the API to not error.
 
`Conserved_graphs.cys` the Cytoscape file that contains all the drug related graphs related to conservation
 
`study_combine_drug_data_with_schmidtflynnsherer.py` Generates the file `study_schmidtflynnsherer_drug_protein_rows_v1.csv` which has the data correctly formatted to be put into Cytoscape with the study being used as the target node. To correctly put it into Cytoscape use this format:
 
| symbol id | Uniq Prot Id | Species | Interactor | cell line | hour | study | interaction type | drug approved |
| ----- | ----- | ----- | ------ | ------ | --- | ------ | ------- | ----- |
| Source node (SN)| SN Attribute  |SN Attribute | SN Attribute | SN Attribute | SN Attribute | target node |SN Attribute |interaction type |
 
 
`cell_line_combine_drug_data_with_schmidtflynnsherer.py` Generates the file `cell_line_schmidtflynnsherer_drug_protein_rows_v1.csv` which has the data correctly formated to be put into Cytoscape with the cell line being used as the target node. To correctly put it into Cytoscape use this format:
 
| symbol id | Uniq Prot Id | Species | Interactor | cell line | hour | study | interaction type | drug approved |
| ----- | ----- | ----- | ------ | ------ | --- | ------ | ------- | ----- |
| Source node (SN)| SN Attribute  |SN Attribute | SN Attribute | target node| SN Attribute | SN Attribute |SN Attribute |interaction type |
 
 
`hour_combine_drug_data_with_schmidtflynnsherer.py` Generates the file `hour_schmidtflynnsherer_drug_protein_rows_v1.csv` which has the data correctly formated to be put into Cytoscape with the study being used as the target node. To correctly put it into Cytoscape use this format:
 
| symbol id | Uniq Prot Id | Species | Interactor | cell line | hour | study | interaction type | drug approved |
| ----- | ----- | ----- | ------ | ------ | --- | ------ | ------- | ----- |
| Source node (SN)| SN Attribute  |SN Attribute | SN Attribute | SN Attribute| target node | SN Attribute |SN Attribute |interaction type |
