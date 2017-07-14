"""

"""


import pandas as pd


input_1_path  = "senseDR.txt.xls"
input_2_path  = "GeneFiltered_List.txt"

output_path = "test.txt"


df_senseDR      = pd.read_table(input_1_path)
df_GeneFiltered = pd.read_table(input_2_path)


df = pd.merge(df_senseDR, df_GeneFiltered, how="outer", on="Gene ID")
df.to_csv(output_path, index=None, sep="\t")