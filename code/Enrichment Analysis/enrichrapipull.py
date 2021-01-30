#Enrichr api pull and then filtering the data from all libraries so that it returns a csv with only results that had an 
###adjusted p value less than .01

import json
import requests
import pandas as pd

### Step 1: This section uses the API to create a userlistID for list of proteins 

ENRICHR_URL = 'http://maayanlab.cloud/Enrichr/addList'
importedproteins = pd.read_csv("/Users/annikacleven/schmidtflynnshererstandard_v4.csv")

#Creating a gene list from the three studies based on one of the columns: study, hour, cell line, interacting_RNA
genelist = importedproteins.loc[importedproteins["hour"] == 24]["symbol_id"].to_list()

genestring = '\n'.join(genelist)


description = 'Example gene list'
payload = {
    'list': (None, genestring),
    'description': (None, description)
}

response = requests.post(ENRICHR_URL, files=payload)
if not response.ok:
    raise Exception('Error analyzing gene list')

data = json.loads(response.text)
userListId = data['userListId']

#A list of the to date libraries in Enrichr as of Jan 25, 2021
#'Genes_Associated_with_NIH_Grants', 
libraries = ['Genes_Associated_with_NIH_Grants','Cancer_Cell_Line_Encyclopedia', 'Achilles_fitness_decrease',
'Achilles_fitness_increase', 'Aging_Perturbations_from_GEO_down', 'Aging_Perturbations_from_GEO_up','Allen_Brain_Atlas_10x_scRNA_2021',
'Allen_Brain_Atlas_down','Allen_Brain_Atlas_up','ARCHS4_Cell-lines','ARCHS4_IDG_Coexp','ARCHS4_Kinases_Coexp','ARCHS4_TFs_Coexp',
'ARCHS4_Tissues','BioCarta_2016','BioPlanet_2019','BioPlex_2017','CCLE_Proteomics_2020','ChEA_2016','Chromosome_Location','Chromosome_Location_hg19',
'ClinVar_2019','CORUM','COVID-19_Related_Gene_Sets','Data_Acquisition_Method_Most_Popular_Genes','dbGaP','DepMap_WG_CRISPR_Screens_Broad_CellLines_2019',
'DepMap_WG_CRISPR_Screens_Sanger_CellLines_2019','Disease_Perturbations_from_GEO_down','Disease_Perturbations_from_GEO_up','Disease_Signatures_from_GEO_down_2014',
'Disease_Signatures_from_GEO_up_2014','DisGeNET','Drug_Perturbations_from_GEO_2014','Drug_Perturbations_from_GEO_down','Drug_Perturbations_from_GEO_up',
'DrugMatrix','DSigDB','Elsevier_Pathway_Collection','ENCODE_and_ChEA_Consensus_TFs_from_ChIP-X','ENCODE_Histone_Modifications_2015',
'ENCODE_TF_ChIP-seq_2015','Enrichr_Libraries_Most_Popular_Genes','Enrichr_Submissions_TF-Gene_Coocurrence','Enrichr_Users_Contributed_Lists_2020',
'Epigenomics_Roadmap_HM_ChIP-seq','ESCAPE','Gene_Perturbations_from_GEO_down','Gene_Perturbations_from_GEO_up','GeneSigDB','Genome_Browser_PWMs',
'GO_Biological_Process_2018','GO_Cellular_Component_2018','GO_Molecular_Function_2018','GTEx_Tissue_Sample_Gene_Expression_Profiles_down',
'GTEx_Tissue_Sample_Gene_Expression_Profiles_up','GWAS_Catalog_2019','HMDB_Metabolites','HMS_LINCS_KinomeScan','HomoloGene','Human_Gene_Atlas',
'Human_Phenotype_Ontology','HumanCyc_2016','huMAP','InterPro_Domains_2019','Jensen_COMPARTMENTS','Jensen_DISEASES','Jensen_TISSUES',
'KEA_2015','KEGG_2019_Human','KEGG_2019_Mouse','Kinase_Perturbations_from_GEO_down','Kinase_Perturbations_from_GEO_up',
'L1000_Kinase_and_GPCR_Perturbations_down','L1000_Kinase_and_GPCR_Perturbations_up','Ligand_Perturbations_from_GEO_down',
'Ligand_Perturbations_from_GEO_up','LINCS_L1000_Chem_Pert_down','LINCS_L1000_Chem_Pert_up','LINCS_L1000_Ligand_Perturbations_down',
'LINCS_L1000_Ligand_Perturbations_up','lncHUB_lncRNA_Co-Expression'	,'MCF7_Perturbations_from_GEO_down','MCF7_Perturbations_from_GEO_up',
'MGI_Mammalian_Phenotype_2017','MGI_Mammalian_Phenotype_Level_3','MGI_Mammalian_Phenotype_Level_4_2019','Microbe_Perturbations_from_GEO_down',
'Microbe_Perturbations_from_GEO_up','miRTarBase_2017','Mouse_Gene_Atlas','MSigDB_Computational','MSigDB_Hallmark_2020','MSigDB_Oncogenic_Signatures',
'NCI-60_Cancer_Cell_Lines','NCI-Nature_2016','NIH_Funded_PIs_2017_AutoRIF_ARCHS4_Predictions','NIH_Funded_PIs_2017_GeneRIF_ARCHS4_Predictions',
'NIH_Funded_PIs_2017_Human_AutoRIF','NIH_Funded_PIs_2017_Human_GeneRIF','NURSA_Human_Endogenous_Complexome','Old_CMAP_down','Old_CMAP_up','OMIM_Disease',
'OMIM_Expanded','Panther_2016','Pfam_Domains_2019','Pfam_InterPro_Domains','PheWeb_2019','Phosphatase_Substrates_from_DEPOD','PPI_Hub_Proteins','ProteomicsDB_2020',
'Rare_Diseases_AutoRIF_ARCHS4_Predictions','Rare_Diseases_AutoRIF_Gene_Lists','Rare_Diseases_GeneRIF_ARCHS4_Predictions','Rare_Diseases_GeneRIF_Gene_Lists',
'Reactome_2016','RNA-Seq_Disease_Gene_and_Drug_Signatures_from_GEO','SILAC_Phosphoproteomics','SubCell_BarCode','SysMyo_Muscle_Gene_Sets',
'Table_Mining_of_CRISPR_Studies','TargetScan_microRNA_2017','TF-LOF_Expression_from_GEO','TF_Perturbations_Followed_by_Expression',
'TG_GATES_2020','Tissue_Protein_Expression_from_Human_Proteome_Map','Tissue_Protein_Expression_from_ProteomicsDB','Transcription_Factor_PPIs',
'TRANSFAC_and_JASPAR_PWMs','TRRUST_Transcription_Factors_2019','UK_Biobank_GWAS_v1','Virus-Host_PPI_P-HIPSTer_2020','Virus_Perturbations_from_GEO_down',
'Virus_Perturbations_from_GEO_up','VirusMINT','WikiPathways_2019_Human','WikiPathways_2019_Mouse']

##Step 2: Use the API to pull information from one library at a time and format the data
##step A gets data into format where the first column is the library name and the second column is the list
##that the api spits out 

df = pd.DataFrame({'A' : []})
ENRICHR_URL = 'http://maayanlab.cloud/Enrichr/enrich'
query_string = '?userListId=%s&backgroundType=%s'
user_list_id = userListId
for library in libraries:
    gene_set_library = library
    response = requests.get(
        ENRICHR_URL + query_string % (user_list_id, gene_set_library)
    )
    if not response.ok:
        raise Exception('Error fetching enrichment results', gene_set_library)
    data = json.loads(response.text)
    apidataset = pd.DataFrame.from_dict(data).rename(columns={gene_set_library: "info"})

    length = len(apidataset["info"])
    alist = list(length * (gene_set_library, ))
    from pandas import DataFrame
    listdatafr = DataFrame (alist,columns=['Library_Name'])

    datafr = pd.concat([listdatafr, apidataset], axis = 1 )
    #print(datafr)
    df = pd.concat([df,datafr], axis = 0)
    #print(df)



import pandas as pd


#splits the information the API spit out to 
df1 = pd.DataFrame(df['info'].values.tolist(), index=df.index).rename(columns={0: "rank_within_library", 1: "term_name", 2:"p_value", 3: "z_score", 4: "combined_score", 5: "overlapping_genes", 6:"adjusted_p_value", 7: "old_p_value", 8: "old_adjusted_p_value"})


##this parses each of the values from strings to floats
df1['p_value'] = df1['p_value'].astype(float)
df1['adjusted_p_value'] = df1['adjusted_p_value'].astype(float)
df1['z_score'] = df1['z_score'].astype(float)
df1['combined_score'] = df1['combined_score'].astype(float)

#concatenating the library name to the information given by the API
df1_total = pd.concat([df["Library_Name"], df1], axis = 1)

df1_adjpfilter = df1_total.loc[df1_total["adjusted_p_value"] <= .01]
df1_adjpfilter = df1_adjpfilter.sort_values("adjusted_p_value")

#exporting as a .csv

#df1_adjpfilter.to_csv("/Users/annikacleven/enrichr_24hrproteins.csv",index=False)













