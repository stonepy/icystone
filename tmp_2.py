"""
Remove the header of the result

"""


import sys


inputPATH  = sys.argv[1]
outputPATH = sys.argv[2]


with open(inputPATH, "r") as inf:

    outf = open(outputPATH, "w")

    for l in inf:
        if l.startswith("#"):
            continue

        outf.write(l)

    outf.close()






import pandas as pd
import sys


inputPATH  = sys.argv[1]
outputPATH = sys.argv[2]


df_m = pd.DataFrame()
df_v = pd