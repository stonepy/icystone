
"""
Select 'GATK_UnifiedGenotyper', 'GATK_UnifiedGenotyper/GATK_MuTect2 and 'Varscan2-Somatic' common results

"""



import pandas as pd



df_u = pd.read_csv("UnifiedGenotyper_chr1.vcf", index_col=False, sep="\t")

df_m = pd.read_csv("MuTect2_chr1.vcf", index_col=False, sep="\t")

df_v = pd.read_csv("Varscan2_chr1.vsn", index_col=False, sep="\t")



df_merge_um = pd.merge(df_u, df_m, on="position")
df_merge_uv = pd.merge(df_u, df_v, on="position")
df_merge_mv = pd.merge(df_m, df_v, on="position")
df_merge_umv = pd.merge(df_merge_um, df_v, on="position")

df_merge_um.to_csv("UM_chr1.tsv", header=None, index=None, sep="\t")
df_merge_uv.to_csv("UV_chr1.tsv", header=None, index=None, sep="\t")
df_merge_mv.to_csv("MV_chr1.tsv", header=None, index=None, sep="\t")
df_merge_umv.to_csv("UMV_chr1.tsv", header=None, index=None, sep="\t")



df_merge_um = pd.merge(df_u, df_m, on="position", how="outer")
df_merge_uv = pd.merge(df_u, df_v, on="position", how="outer")
df_merge_mv = pd.merge(df_m, df_v, on="position", how="outer")
df_merge_umv = pd.merge(df_merge_um, df_v, on="position", how="outer")

df_merge_um.to_csv("UM_diff_chr1.tsv", header=None, index=None, sep="\t")
df_merge_uv.to_csv("UV_diff_chr1.tsv", header=None, index=None, sep="\t")
df_merge_mv.to_csv("MV_diff_chr1.tsv", header=None, index=None, sep="\t")
df_merge_umv.to_csv("UMV_diff_chr1.tsv", header=None, index=None, sep="\t")