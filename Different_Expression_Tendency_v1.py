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


dir_files = "/home/daniel/PycharmProjects/fishbone/files/"
dir_output = dir_files + "output/"


def diff_tendency():

    path_output = dir_output + "lncList.txt"
    path_B = dir_files + "lncRNA_B_vs_A/B_cuffdiff.xls"
    path_C = dir_files + "lncRNA_C_vs_A/C_cuffdiff.xls"

    df_B = pd.read_table(path_B, usecols=["gene_id", "Type", "log2(fold_change)"])
    df_C = pd.read_table(path_C, usecols=["gene_id", "Type", "log2(fold_change)"])

    df_B = df_B[df_B["log2(fold_change)"] >= 1]
    df_C = df_C[df_C["log2(fold_change)"] >= 1]

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

    df_lncList = pd.read_table(path_lncList)
    df_lnc2m   = pd.read_table(path_lnc2m, usecols=["Query", "Target"])


    with open(path_output, "w") as lncTgene:

        for index, lnc in df_lncList.iterrows():

            for index, row in df_lnc2m.iterrows():

                if row[0].split("(")[1].strip(")") == lnc:

                    gene_id = row[1].split("(")[1].strip(")") + "\n"
                    lncTgene.write(gene_id)



    # with open(path_lnc2m, "r") as lnc2m:
    #
    #     for l in lnc2m:
    #         try:
    #             lnc2m_list.append(l)
    #         except:
    #             lnc2m_list = []
    #
    #     lnc2m_dict      = {}
    #     for l in lnc2m_list:
    #
    #         # print(l.split("\t")[0].split("(")[1].strip(")"))
    #         try:
    #             key   = l.split("\t")[0].split("(")[1].strip(")")
    #             value = l.split("\t")[2].split("(")[1].strip(")")
    #
    #         except:
    #             continue
    #
    #
    #         try:
    #             lnc2m_dict[key].append(value+"\t")
    #             # print(key, value)
    #
    #         except:
    #             lnc2m_dict[key] = []
    #             lnc2m_dict[key].append(value)
    #
    #     # for key in lnc2m_dict.keys():
    #     #     print(key)
    #     print(lnc2m_dict)
    #
    #
    # with open(path_output, "w") as lncTgene:
    #     for l in lnc2m_dict.items():
    #         lncTgene.write(l+"\n")



if __name__ == "__main__":
    # diff_tendency()
    lnc2mRNA_Target()

