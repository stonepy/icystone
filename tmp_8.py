
"""
BED position expandation

"""


import sys

inputPATH  = sys.argv[1]
outputPATH = sys.argv[2]
distance = sys.argv[3]


with open(inputPATH, "r") as inf:

    outf = open(outputPATH, "w")

    for l in inf:
        l_split = l.strip().split("\t")
        l_split[1] = int(l_split[1]) - int(distance)
        l_split[2] = int(l_split[2]) + int(distance)

        newl = ""
        for i in l_split:
            i = str(i)
            newl += i + "\t"
        newl = newl.strip() + "\n"
        outf.write(newl)

    outf.close()
