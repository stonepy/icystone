import sys


try:
    input1PATH  = sys.argv[1]
    input2PATH  = sys.argv[2]
    outputPATH  = sys.argv[3]

except:
    input1PATH  = "mutect1.call_stats.txt"
    input2PATH  = "Varscan2_chr1.vsn"
    outputPATH  = "test.vcf"


with open(outputPATH, "w") as outf:

    inf1 = open(input1PATH, "r")
    inf2 = open(input2PATH, "r")

    inf2List = []
    for l2 in inf2:
        inf2List.append(l2)

    n = 0
    for l1 in inf1:

        if l1.startswith("#"):
            continue

        l1_split = l1.split("\t")
        pos1 = l1_split[1]

        for l2 in inf2List:
            l2_split = l2.split("\t")
            pos2 = l2_split[1]

            if pos1 == pos2:
                newl = l1.strip() + "\t" + l2
                print(newl)
                outf.write(newl)


inf1.close()
inf2.close()