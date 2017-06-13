
"""
Select 'GATK_UnifiedGenotyper' unique results and 'GATK_UnifiedGenotyper/GATK_MuTect2 common'

"""

import sys
import time
import pandas as pd



input_1_PATH  = sys.argv[1]
input_2_PATH  = sys.argv[2]

# output_1_PATH = sys.argv[3]
# output_2_PATH = sys.argv[4]

outputPATH = sys.argv[3]


df_tumorI = pd.read_csv(input_1_PATH, header=None, sep="\t", comment="#")
df_normalI = pd.read_csv(input_2_PATH, header=None, sep="\t", comment="#")


commonList = []

tumorList  = []
normalList = []


for idx_t, row_t in df_tumorI.iterrows():
    # print("\n\n\ntumor: %s" % row_t)
    # time.sleep(1.5)

    pos_t = row_t[1]
    alt_t = row_t[4]
    gt_t  = row_t[9].split(":")[0]

    for idx_n, row_n in df_normalI.iterrows():
        # print("\nnormal: %s" % row_n)
        # time.sleep(0.5)

        pos_n = row_n[1]
        alt_n = row_n[4]
        gt_n  = row_n[9].split(":")[0]

        if pos_t == pos_n and alt_t == alt_n and gt_t == gt_n:
            # print("tumor: %s" % row_t)
            # time.sleep(0.5)
            commonList.append(row_t)

        # if alt_t != alt_n or (alt_t != alt_n and gt_t != gt_n):
        #     tumorList.append(row_t)
        #     normalList.append(row_n)


df_common = pd.DataFrame(commonList)

# df_tumorO  = pd.DataFrame(tumorList)
# df_normalO = pd.DataFrame(normalList)


# print(df_common, df_tumorO, df_normalO)


df_common.to_csv(outputPATH, header=None, index=None, sep="\t")

# df_tumorO.to_csv(output_1_PATH, header=None, index=None, sep="\t")
# df_normalO.to_csv(output_2_PATH, header=None, index=None, sep="\t")