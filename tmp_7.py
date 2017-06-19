
"""
Select 'Somatic' & 'LOH' of 'Varscan2' result

"""


import sys

inputPATH  = sys.argv[1]
outputPATH = sys.argv[2]


with open(inputPATH, "r") as inf:

    outf = open(outputPATH, "w")

    for l in inf:
        l_split = l.split("\t")
        if l_split[12] == "Somatic" or l_split[12] == "LOH":
            outf.write(l)

    outf.close()