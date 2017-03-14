"""
- Information --------------------------------------------------------------------
 Name         :   Different_Expression_Tendency
 Description  :
 Author       :   Hwx
 Version      :   V1
 Dev Env      :   Red Hat 4.8.5-11, Python3.5.3, virtualenv15.1.0
 Finish Date  :   2017-03-14
-----------------------------------------------------------------------------------
"""


import pandas as pd

def diff_tendency():
    dir_files    = "/home/daniel/PycharmProjects/fishbone/files/"
    dir_output   = dir_files +"output/"
    path_case    = dir_files + "B_vs_A/cuffdiff.xls"
    path_control = dir_files + "C_vs_A/cuffdiff.xls"

    df_case    = pd.read_table(path_case, usecols=["gene_id", "Type"])
    df_control = pd.read_table(path_control, usecols=["gene_id", "Type"])

    df_CaCo = pd.merge(df_case, df_control, on="gene_id")
    with open(dir_output+"tend.xls", "w") as tend:
        tend.write("gene_id\tType\n")

        for index, row in df_CaCo.iterrows():

            if row[1] == row[2] and row[1] != "Not DEG":
                l = row[0] + "\t" + row[1] + "\n"
                tend.write(l)



if __name__ == "__main__":
    diff_tendency()