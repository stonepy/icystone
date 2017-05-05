import pandas as pd
import os
import sys



result_dir = sys.argv[1]
output_dir = sys.argv[2]
project_NO = sys.argv[3]
output_path = os.path.join(output_dir, project_NO+".xlsx")

Samples = os.listdir(result_dir)

df_1st = None
for spl in Samples:
    if "." in spl:
        continue

    path = os.path.join(result_dir, spl, "metrics.tsv")

    if df_1st == None:
        df_1st = pd.read_table(path)
        continue
    df = pd.read_table(path)
    df_sum = pd.concat([df_1st, df])

df_out = df_sum.T

writer = pd.ExcelWriter(output_path)
df_out.to_excel(writer, "sheet1")
writer.save()