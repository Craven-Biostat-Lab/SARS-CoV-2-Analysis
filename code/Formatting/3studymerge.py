##This script is used to merge all three of the study data together into one dataframe 

import pandas as pd


schmidt = pd.read_csv("/Users/annikacleven/schmidtstandard_v4.csv")
flynn = pd.read_csv("/Users/annikacleven/flynnstandard_v3.csv")
sherer = pd.read_csv("/Users/annikacleven/shererstandard_v3.csv")

schmidtflynnsherer = pd.concat([schmidt, flynn, sherer], axis=0)

#print(schmidtflynnsherer)
#schmidtflynnsherer.to_csv('/Users/annikacleven/schmidtflynnshererstandard_v4.csv',index=False)