# Enrichment Analysis
###### This folder contains files for the Enrichment Analysis using the Enrichr website

**enrichrapipull.py** : This python file uses the API from https://maayanlab.cloud/Enrichr/help#api . A csv must be read in to be saved as *imported proteins*.  This csv must have a column of protein symbols in a column labeled *symbol_id*. You can then filter to select a certain group of proteins that will go through enrichment testing.  This python file will use the API to give the chosen group of proteins a userListId.  That userListId is then used to check that list of proteins against all of the the most updated libraries in Enrichr. This returns a dataframe of all the results from all libraries.  These results include the *Library_Name*, *rank_within_library*, *term_name*, *p_value*, *z_score*, *combined_score*, *overlapping_genes*, *adjusted_p_value*, *old_p_value*, and *old_adjusted_p_value*. This dataframe is filtered to select only results that have an adjusted p value less than .01.  Then this dataframe is exported as a csv to where you specify. 

Inside the **csv** folder:
**conservationanalysis.csv** : This csv has three columns labeled *symbol_id*, *unique_protein_id*, *conservation_across* respectively.  This csv lists the symbol id and the unique protein id of proteins that were conserved across either hour, cell_line, or study. What the protein is conserved across is desginated in the *conservation_across* column. If the protein was conserved in different ways it is listed once for each way it is conserved. This csv can be read into **enrichrapipull.py** and a certain group of proteins can be selected to go through enrichment testing. 
**schmidtflynnshererstandard_v4** : This csv has columns labeled *symbol_id*, *unique_protein_id*, *unique_protein_id*, *interacting_RNA*, *cell_line*, *hour*, *species*, and *study*.  This csv contains all the proteins that were found in the sherer, schmidt, and flynn study. This csv can be read into **enrichrapipull.py** and a certain group of proteins can be selected to go through enrichment testing. 

Inside the **exported analysis csv** folder:

This folder includes the csv's that have already been analyzed. 
**enrichr_24hrproteins.csv** is an enrichment analysis of all proteins in the studies that were found at 24 hours
**enrichr_8hrproteins.csv** is an enrichment analysis of all proteins in the studies that were found at 8 hours
**enrichr_Nproteins.csv** is an enrichment analysis of all proteins in the studies that binded to the Nrna 
**enrichr_ORF8proteins.csv** is an enrichment analysis of all proteins in the studies that binded to the ORF8 rna 
**enrichr_hourconservedproteins.csv** is an enrichment analysis of all proteins in the studies that were conserved across all hours 
**enrichr_studyconservedproteins.csv** is an enrichment analysis of all proteins in the studies that were conserved across all studies