#This was used to format the sherer data into a format that could be imported into cytoscape
import pandas as pd

##import the original sherer data
sherer = pd.read_csv("/Users/annikacleven/SARS2_Vero_2Bio_Proteins Enriched in Each Capture.xlsx - Short List4.csv")

#pull out the columns dealing with 8 hours
sherer8 = sherer[["8Hr gRNA (u)","8Hr gRNA (s)","8Hr SRNA (u)","8Hr SRNA (s)","8Hr ORF8 RNA (u)","8Hr ORF8 RNA (s)","8Hr NRNA (u)","8Hr NRNA (s)"]]

### this loop captures the unique protein id, the symbol id, and the rna interaction for each of the columns
prot_id = []
symbol_id = []
rna_interaction = []

for (columnName, columnData) in sherer8.iteritems():
    if columnName[-2] == "u":
        prot_id = prot_id + columnData.values.tolist()
        rna_interaction = rna_interaction + list(98 * (columnName[4:8] , ))
    if columnName[-2] == "s":
        symbol_id = symbol_id + columnData.values.tolist()


##this takes the lists with the extracted data from above and puts it into a data frame and adds a column marking the hour as 8
sherercyto = pd.DataFrame(
    {'unique_protein_id': prot_id,
    'symbol_id': symbol_id,
    'interacting_RNA': rna_interaction})
sherercyto = sherercyto.dropna()
sherercyto8 = sherercyto.assign(hour = 8)
#print(sherercyto8)

#export the dataframe
#sherercyto8.to_csv('/Users/annikacleven/sherercyto24.csv',index=False)

#pull out the columns dealing with 24 hours
sherer24 = sherer[["24Hr gRNA (u)","24Hr gRNA (s)","24Hr SRNA (u)","24Hr SRNA (s)","24Hr ORF8 RNA (u)","24Hr ORF8 RNA (s)","24Hr NRNA (u)","24Hr NRNA (s)"]]



### this loop captures the unique protein id, the symbol id, and the rna interaction for each of the columns
prot_id = []
symbol_id = []
rna_interaction = []

for (columnName, columnData) in sherer24.iteritems():
    if columnName[-2] == "u":
        prot_id = prot_id + columnData.values.tolist()
        rna_interaction = rna_interaction + list(98 * (columnName[5:9] , ))
    if columnName[-2] == "s":
        symbol_id = symbol_id + columnData.values.tolist()

##this takes the lists with the extracted data from above and puts it into a data frame and adds a column marking the hour as 24
sherercyto = pd.DataFrame(
    {'unique_protein_id': prot_id,
    'symbol_id': symbol_id,
    'interacting_RNA': rna_interaction})
sherercyto = sherercyto.dropna()
sherercyto24 = sherercyto.assign(hour = 24)

#print(sherercyto24)
#export the dataframe
#sherercyto24.to_csv('/Users/annikacleven/sherercyto24.csv',index=False)

#concatenating the data frame with the 8 hr and the 24 hour together to make a dataframe with all the data from both time periods
#that were in the sherer data 
sherercytoall = pd.concat([sherercyto8, sherercyto24], axis=0)

print(sherercytoall)

#export dataframe as a csv
#sherercytoall.to_csv('/Users/annikacleven/sherercytoall.csv',index=False)