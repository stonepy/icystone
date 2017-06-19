"""
Select 'GATK_UnifiedGenotyper' Tumor/Normal unique results (For all sites, VCFs include both SNP/INDEL and None sites)

"""


import sys



def sep_snp_indel_all():

    inf1 = open(input_1_PATH, "r")
    inf2 = open(input_2_PATH, "r")

    outf1 = open(output_1_PATH, "w")
    outf2 = open(output_2_PATH, "w")
    outf3 = open(output_3_PATH, "w")


    while True:
        try:
            l1 = next(inf1)
            l2 = next(inf2)
        except:
            break

        if l1.startswith("#"):
            continue


        l1_split = l1.split("\t")
        l2_split = l2.split("\t")

        l1_chr = l1_split[0]
        l2_chr = l2_split[0]

        l1_alt = l1_split[4]
        l2_alt = l2_split[4]

        l1_gt  = l1_split[-1].split(":")[0]
        l2_gt  = l2_split[-1].split(":")[0]


        if l1_chr == l2_chr and l1_alt == l2_alt and l1_gt == l2_gt:
            outf3.write(l1)
        else:
            outf1.write(l1)
            outf2.write(l2)


    inf1.close()
    inf2.close()
    outf1.close()
    outf2.close()


def select_chr():
    pass



if __name__ == "__main__":

    input_1_PATH  = sys.argv[1]
    input_2_PATH  = sys.argv[2]
    output_1_PATH = sys.argv[3]
    output_2_PATH = sys.argv[4]
    output_3_PATH = sys.argv[5]

    sep_snp_indel_all()

    # try:
    #     select_opt = sys.argv[3]
    #     print("\nSelect chromosome %s\n" % select_opt)
    #     select_chr()
    # except:
    #     print("\nSeparate all SNP/INDEL sites\n")
    #     sep_snp_indel_all()