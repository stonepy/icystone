"""
- Information --------------------------------------------------------------------
 Name         : Heatmap_Median_Shrink
 Description  : If the amount of samples is too small and the ranges of samples are
                too large, use this script to make the data more close to the median
 Formulation  :
                if val > median:
                    val = val * shrink_rate
                if val < median:
                    val = val * (2 - shrink_rate)
 Author       : Hwx
 Version      : V1
 Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS, Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-03-24
-----------------------------------------------------------------------------------
"""

import os
import sys
import pandas as pd


path_DEGs = "C:\\Users\\GiantStone-Hwx\\Desktop\\de_genes.tsv"



# Get arguments
args = sys.argv

# Check if user didn't provide valid path
try:
    path_DEGs = args[1]
except IndexError as e:
    print("\n>>> Error :\n    Sorry, you didn't provide valid path\n")
    print("\n===============================================\n[ Usage ]\n    python Heatmap_Median_Shrink.py <geneTable_path>\n===============================================\n")

    path_rawdata = input("\nYou can provide availabe input_path here, please input the path : \n")

    if not os.path.exists(path_rawdata):
        print("\n>>> Error :\n    Sorry, you didn't provide valid path\n")
        exit()


df_DEGs = pd.read_table(path_DEGs)          # Read gene table as DataFrame

obj_median = df_DEGs.median()               # Aquire the median of every columns, result is a Series
obj_sum = df_DEGs.sum().pop("gene_name")    # Sum of every column, result is a Series
rows_num, columns_num = df_DEGs.shape       # (rows_num, columns_nums)


def shrink_median(val, median):

    shrink_rate = 0.03

    val = float(val)

    if val > median:
        val = val * shrink_rate
    elif val < median:
        val = val * (2 - shrink_rate)

    return val


srkAll_list = []
for col in df_DEGs:
    if col == "gene_name":
        continue

    median = obj_median[col]

    srkCol_list = []
    for val in df_DEGs[col]:
        srkCol_list.append(shrink_median(val, median))

    srkAll_list.append(srkCol_list)

df_DEGs_srk = pd.DataFrame(srkAll_list).T

df_DEGs_srk.to_csv("C:\\Users\\GiantStone-Hwx\\Desktop\\srk.txt", index=None, sep="\t")

print(df_DEGs_srk)
