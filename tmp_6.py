
"""
Select 'GATK_MuTect2/Varscan2 common'

"""

import sys
import time
import pandas as pd



input_MuTect2_PATH  = sys.argv[1]
input_Varscan2_PATH = sys.argv[2]

outputPATH = sys.argv[3]


df_tumorI = pd.read_csv(input_MuTect2_PATH, header=None, sep="\t", comment="#")
df_normalI = pd.read_csv(input_Varscan2_PATH, header=None, sep="\t", comment="#")


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

        pos_n = int(row_n[1])
        alt_n = row_n[3]

        if pos_t == pos_n and alt_t == alt_n:
            # print("tumor: %s" % row_t)
            # time.sleep(0.5)
            commonList.append(row_t)



df_common = pd.DataFrame(commonList)


df_common.to_csv(outputPATH, header=None, index=None, sep="\t")
