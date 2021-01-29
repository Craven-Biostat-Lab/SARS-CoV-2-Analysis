#This file transfers the schmidt data into the standard format 
import pandas as pd

#imports the original schmidt data
schmidt = pd.read_csv("/Users/annikacleven/Schmidt-media-1.xlsx - Two-sample mod T.csv")
pd.set_option('display.max_columns', None)

#Filters to get results only from adjusted p value of less than .05 and 'logFC.SCoV2.over.RMRP' greater than 0
schmidt["adj.P.Val.SCoV2.over.RMRP"] = schmidt["adj.P.Val.SCoV2.over.RMRP"].astype(float)
schmidtselect = schmidt.loc[schmidt["adj.P.Val.SCoV2.over.RMRP"] < .05] 
schmidtcore = schmidtselect.loc[schmidtselect['logFC.SCoV2.over.RMRP'] > 0]

#pulls out the id(unique_protein_id) and gene symbol(symbol_id) column 
#assigns values for hour, cell_line, study, and interacting RNA as described in the experiment
schmidtcore1 = schmidtcore[["id", "geneSymbol"]].assign(hour = 24, cell_line = "Huh7", study = "Schmidt", interacting_RNA = "genomic").reset_index()

#imported the gene with protein product data
#creating two data frames: gumoselect has the symbol and uniprot_ids and gumosymbolselect has current and previous symbols
gumo = pd.read_csv("/Users/annikacleven/gene_with_protein_product.csv")
gumoselect = gumo[["symbol", "uniprot_ids"]]
gumosymbolselect = gumo[["symbol", "prev_symbol"]]

#a list made of all the symbols in the gene_with_protein_product data
symbollist = gumo['symbol'].tolist()
#a list made of all the previous symbols in the gene_with_protein_product data
prev_symbol_list = gumo['prev_symbol'].tolist() 
#a dictionary with the previous symbol as the key
prevsymboldict = gumosymbolselect.set_index('prev_symbol').T.to_dict('list')

#a loop that finds the proteins that arent in the current symbol list because they are either viral or outdated
#then if checks to see if it is a previous symbol (meaning it is outdated)
#if it is then it will use a dictionairy to replace it with the equivalent current symbol 
#returns a dataframe 'updatedschmidt' with the most current symbol_ids
for protein in schmidtcore1['geneSymbol']:
    if protein not in symbollist:
        #print(protein)
        if protein in prev_symbol_list:
            #print(('').join(prevsymboldict[protein]))
            updatedschmidt = schmidtcore1.replace(protein, ('').join(prevsymboldict[protein]))


#this takes the symbol found in 'updatedschmidt' and uses the gumo data to map its unique protein id
#if it does not have a unique protein id, then it will put a "-"
#this loop returns a list of the unique protein ids in order
gumodict = gumoselect.set_index('symbol').T.to_dict('list')
uni_prot_list = []
for symbol in updatedschmidt["geneSymbol"]:
    if symbol in gumodict:
        uni_prot_list = uni_prot_list + gumodict[symbol]
    else:
        uni_prot_list = uni_prot_list + ['-']


#turns the unique protein id list into a data frame and then concatenated it to the data frame that includes:
#hour, study, cell_line, interacting_RNA, and symbol_id
schmidtuniprot = pd.DataFrame(
    {'uni_prot': uni_prot_list,})
core = pd.concat([schmidtuniprot, updatedschmidt], axis=1)
#print("core")

#this creates a list that returns whether the protein his SARS-COV-2 or is human
#if there is a unique protein id, then it is human, otherwise it is assumed to be SARS-COV-2

species = []
for uni_prot in core["uni_prot"]:
    if uni_prot == "-":
        species = species + ["Severe acute respiratory syndrome coronavirus 2"]
    else:
        species = species + ["homo sapien"]
#turns the list into a data frame and then concatenates it to the data frame that includes:
#hour, study, cell_line, interacting_RNA, and symbol_id, uni_prot
schmidtspecies = pd.DataFrame({'species': species})
#print(schmidtspecies)
core1 = pd.concat([core,schmidtspecies], axis = 1)
#print(core1)


#orders and renames the columns to be in proper format
coreordered = core1[["geneSymbol","uni_prot","interacting_RNA","cell_line", "hour", "species","study" ]]
coreordered = coreordered.rename(columns={"geneSymbol": "symbol_id", "uni_prot": "unique_protein_id"})
#print(coreordered)

#export dataframe as a csv
#coreordered.to_csv('/Users/annikacleven/schmidtstandard_v4.csv',index=False)