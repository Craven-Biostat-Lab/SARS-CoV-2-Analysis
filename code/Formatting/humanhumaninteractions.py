###PART 1: Creating a dataframe formatting all the human human interactions listed in the original BIOGRID file

import pandas as pd
biogridorganism = pd.read_csv("/Users/annikacleven/BIOGRID-ORGANISM-Homo_sapiens-4.2.193.mitab.csv")
threestudy = pd.read_csv("/Users/annikacleven/schmidtflynnshererstandard_v4.csv")
gumo = pd.read_csv("/Users/annikacleven/gene_with_protein_product.csv")

biogridorganism = biogridorganism.rename(columns={"Alt IDs Interactor A": "Alt_IDs_Interactor_A", "Alt IDs Interactor B": "Alt_IDs_Interactor_B"})
#biogridorganism

#splitting the Alt_IDS_Interactor_A column to extract the unique protein id A
split1 = biogridorganism["Alt_IDs_Interactor_A"].str.split("uniprot/swiss-prot:", n = 2, expand = True)
split2 = split1[1].str.split("|", n = 1, expand = True)
split2[0]
biogridorganism["unique_protein_id_A"]=split2[0]


#splitting the Alt_IDS_Interactor_B column to extract the unique protein id B
split1b = biogridorganism["Alt_IDs_Interactor_B"].str.split("uniprot/swiss-prot:", n = 2, expand = True)
split2b = split1b[1].str.split("|", n = 1, expand = True)
split2b[0]
biogridorganism["unique_protein_id_B"]=split2b[0]
#print(biogridorganism)

#selecting the useful columns 
usefulcolumns = biogridorganism[["unique_protein_id_A","unique_protein_id_B",'Interaction Types','Source Database']]

#Creating a dictionary of uniprots/symbols to use in next loop
##threestudyselect = threestudy[["symbol_id", "unique_protein_id"]]
##threestudydict = threestudyselect.set_index("unique_protein_id").T.to_dict('list')
gumoselect = gumo[["symbol","uniprot_ids"]]
gumodict = gumoselect.set_index("uniprot_ids").T.to_dict('list')

#for asssigning symbol to all proteins in the BIOGRID human/human file
symbol_id_A = []
for uniprot in usefulcolumns['unique_protein_id_A']:
    if uniprot in gumodict:
        symbol_id_A = symbol_id_A + gumodict[uniprot]
    else:
        symbol_id_A = symbol_id_A + ['-']

symbol_id_B = []
for uniprot in usefulcolumns['unique_protein_id_B']:
    if uniprot in gumodict:
        symbol_id_B = symbol_id_B + gumodict[uniprot]
    else:
        symbol_id_B = symbol_id_B + ['-']


##adding the symbols to the dataframe with unique protein ids, interaction types, and source database
symbols = pd.DataFrame(
    {'symbol_id_A': symbol_id_A,
    'symbol_id_B': symbol_id_B})
humanproteins = pd.concat([usefulcolumns, symbols], axis=1)[["unique_protein_id_A", "symbol_id_A", 'unique_protein_id_B', 'symbol_id_B','Interaction Types','Source Database' ]]


#Assigning the species, cell line, hour, interacting _RNA, ordering columns, and changing names so it is standard format 
humanproteins2 = humanproteins.assign(species_A = "homo sapien", species_B = "homo sapien", cell_line = '-', hour = '-', interaction_type = 'Protein Protein')
humanproteinsstandard = humanproteins2[['unique_protein_id_A','symbol_id_A', 'species_A','unique_protein_id_B', 'symbol_id_B', 'species_B', 'cell_line', 'hour','Source Database', 'interaction_type']]
humanproteinsstandardname = humanproteinsstandard.rename(columns={"Source Database": "study"})

#filtering out any row that has a nullvalue for either unique protein id
nonullA = humanproteinsstandardname[humanproteinsstandardname.unique_protein_id_A.notnull()]
nonullAB = nonullA[nonullA.unique_protein_id_B.notnull()]

#exporting dataframe with all the human human protein interactions
print(nonullAB)
#nonullAB.to_csv('/Users/annikacleven/allhumanproteininteractions_v2.csv',index=False)

###PART 2: Creating a dataframe of human human interactions that only involve proteins in the 3 studies

#creating variables that show if the symbol_id is in the three study data and filtering for when both are true
humanproteinsstandardname['exist_symbol_A']=humanproteinsstandardname['symbol_id_A'].isin(threestudy["symbol_id"])
humanproteinsstandardname['exist_symbol_B']=humanproteinsstandardname['symbol_id_B'].isin(threestudy["symbol_id"])
humanhuman = humanproteinsstandardname.loc[humanproteinsstandardname['exist_symbol_A'] == True].loc[humanproteinsstandardname['exist_symbol_B'] == True]

#To select columns we want (dropping the columns that acknowledge the symbol is in the three studies )
humanhumanfinal = humanhuman[["unique_protein_id_A", "symbol_id_A", "species_A", "unique_protein_id_B", "symbol_id_B", "species_B", "cell_line", "hour", "study", "interaction_type"]]

print(humanhumanfinal)

#exporting the dataframe 
#humanhumanfinal.to_csv('/Users/annikacleven/selectedhumanhumanproteins_v1.csv',index=False)




