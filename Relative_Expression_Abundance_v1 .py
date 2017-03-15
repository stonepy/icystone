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


def main():
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

    # Calculate the
    for col in df_exprMerged:
        Sum = df_exprMerged.ix[["Total_Expression"], col]
        df_exprMerged[col] = df_exprMerged[col].apply(lambda x: x / Sum)


    df_exprMerged.to_csv(path_output, index="miRNA")






if __name__ == "__main__":

    main()
