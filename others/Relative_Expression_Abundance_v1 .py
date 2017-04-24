"""
- Information --------------------------------------------------------------------
 Name         : Relative_Expression_Abundance
 Description  : Formulation:
                REA = each_gene_expression_of_each_sample / sample_expression_sum
 Author       : Hwx
 Version      : V1
 Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS, Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-03-15
-----------------------------------------------------------------------------------
"""


import pandas as pd


def REA():

    sampleType  = "tRNA_id"
    path_expr   = "/home/daniel/PycharmProjects/fishbone/files/miRNA_tRNA/tRNA.expression.xls"
    path_output = "/home/daniel/PycharmProjects/fishbone/files/output/tRNA.REA.xls"

    # Read the expression data sheet
    df_expr = pd.read_table(path_expr)

    # Calculate the sum of each sample
    obj_exprSum    = df_expr.sum()
    obj_exprSum[0] = "Total_Expression"
    df_exprSum     = pd.DataFrame(obj_exprSum).T

    # merge into original sheet
    df_exprMerged = pd.concat([df_expr, df_exprSum]).set_index(sampleType)

    # Calculate the REA
    for col in df_exprMerged:
        Sum = df_exprMerged.ix[["Total_Expression"], col]
        df_exprMerged[col] = df_exprMerged[col].apply(lambda x: x / Sum)

    # Output result
    df_exprMerged.to_csv(path_output, index="miRNA")



def Add_fastaSeq():

    path_fasta  = "/home/daniel/PycharmProjects/fishbone/files/miRNA_tRNA/hg19-tRNAs.fa"
    path_REA    = "/home/daniel/PycharmProjects/fishbone/files/output/tRNA.REA.xls"
    path_output = "/home/daniel/PycharmProjects/fishbone/files/output/tRNA.REAseq.xls"

    # Read REA data sheet
    df_REA = pd.read_csv(path_REA)

    # Read reference fasta file
    with open(path_fasta, "r") as fas:
        fa_list = []
        for fa in fas:
            fa_list.append(fa)

    # Select sequences by tRNA ID
    df_fas_list = []
    for index, row in df_REA.iterrows():

        fa_seq = ""
        for fa in fa_list:

            # When ID line, stop collect
            if fa.startswith(">"):
                collect_switch = False

            #  Find corresponding sequence
            if row[0] in fa:
                collect_switch = True
                continue

            # When corresponding sequence found,
            if collect_switch:
                fa_seq += fa.strip()

        # Put all selected sequences in a list
        df_fas_list.append(fa_seq)

    # Convert to DataFrame and merge into REA sheet
    df_fas = pd.DataFrame(df_fas_list, columns=["sequence"])
    df_REAseq = pd.concat([df_REA, df_fas], axis=1)

    df_REAseq.to_csv(path_output, index=None)



if __name__ == "__main__":

    REA()
    Add_fastaSeq()