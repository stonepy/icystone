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