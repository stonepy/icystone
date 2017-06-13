"""
Select GATK-UnifiedGenotyper SNP site of VCF

"""


import sys



def select_snp_indel():
    with open(outputPATH, "w") as outf:

        inf = open(inputPATH, "r")

        for l in inf:

            l_split = l.split("\t")

            if l.startswith("#") or l_split[4] == ".":
                continue

            outf.write(l)

        inf.close()



def select_chr():
    with open(outputPATH, "w") as outf:

        inf = open(inputPATH, "r")

        for l in inf:

            l_split = l.split("\t")

            if l.startswith("#") or l_split[0] != str(select_opt):
                continue

            outf.write(l)

        inf.close()



if __name__ == "__main__":

    inputPATH  = sys.argv[1]
    outputPATH = sys.argv[2]

    try:
        select_opt = sys.argv[3]
        select_chr()
    except:
        select_snp_indel()