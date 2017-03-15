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
import time

dir_files = "/home/daniel/PycharmProjects/fishbone/files/"
dir_output = dir_files + "output/"


def diff_tendency():

    path_output = dir_output + "lncList.txt"
    path_B = dir_files + "lncRNA_B_vs_A/B_cuffdiff.xls"
    path_C = dir_files + "lncRNA_C_vs_A/C_cuffdiff.xls"

    df_B = pd.read_table(path_B, usecols=["gene_id", "Type", "log2(fold_change)"])
    df_C = pd.read_table(path_C, usecols=["gene_id", "Type", "log2(fold_change)"])

    df_B = df_B[abs(df_B["log2(fold_change)"]) >= 1]
    df_C = df_C[abs(df_C["log2(fold_change)"]) >= 1]

    df_BC = pd.merge(df_B, df_C, on="gene_id")

    with open(path_output, "w") as tend:

        # tend.write("gene_id\tType\tB_log2(fold_change)\tC_log2(fold_change)\n")

        for index, row in df_BC.iterrows():

            if row[2] == row[4] and row[2] != "Not DEG":
                l = row[0] + "\n"
                # l = "{}{}{}{}{}{}{}{}".format(row[0], "\t", row[2], "\t", row[1], "\t", row[3], "\n")
                # l = "\t".join([row[0], row[2], str(row[1]), str(row[3]), "\n"])

                tend.write(l)


def lnc2mRNA_Target():
    path_lncList = dir_output + "lncList.txt"
    path_lnc2m   = dir_files + "lncRNA.target.xls"

    path_output  = dir_files + "/output/lncTgeneList.txt"

    df_lncList = open(path_lncList,"r")
    df_lnc2m   = open(path_lnc2m,"r")

    for l in df_lncList:
        try:
            lncList_list.append(l)
        except:
            lncList_list = []
            lncList_list.append(l)



    for l in df_lnc2m:
        try:
            lnc2m_list.append(l)
        except:
            lnc2m_list = []
            lnc2m_list.append(l)



    with open(path_output, "w") as lncTgene:
        mRNA_list = []

        for lnc in lncList_list:

            for row in lnc2m_list:

                if lnc.strip("\n") in row:

                    try:
                        mRNA = row.split("\t")[2].split("(")[1].strip(")")
                        mRNA_list.append(mRNA)
                    except:
                        mRNA_list = []
                        mRNA_list.append(mRNA)

        mRNA_unique = set(mRNA_list)
        for l in mRNA_unique:
            lncTgene.write(l+"\n")

        print(len(mRNA_unique))




if __name__ == "__main__":
    diff_tendency()
    lnc2mRNA_Target()