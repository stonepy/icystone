__Name__         = "Differential_expression_miRNA_fasta_select"
__Description__  = "For selecting differetial 'miRNA' fasta"
__Usage__        = "\n>>> Error: No enough argument\n\n    Usage:\n        python %s <Reference Fasta> <DE miRNA list> <Output Fasta>\n" % __file__
__Author__       = "Hwx"
__DevEnv__       = "Python3.5.1/Ubuntu16.04 LTS"
__Date__         = "2017-05-12"


import sys
import time


refFastaPATH   = "hsa_mature_dna.fa"
miListPATH     = "hsa_miRNA_target_20170509"
seldFastaPATH  = "hsa_selected.fa"

if len(sys.argv) < 4:
    print(__Usage__)
    exit()

refFastaPATH   = sys.argv[1]
miListPATH     = sys.argv[2]
seldFastaPATH  = sys.argv[3]

miRNA = []
with open(miListPATH, "r") as mi:
    for l in mi:
        miRNA.append(l.strip())


with open(refFastaPATH, "r") as rf:
        with open(seldFastaPATH, "w") as sf:

            record = False
            for rl in rf:
                # Compare name of ref fasta and miRNA list
                if ">" in rl:
                    for mi in miRNA:
                        # If they share the same name, start record
                        if mi in rl:
                            sf.write(rl)
                            record = True
                    continue

                # Record the sequence when names are the same
                if record == True:
                    sf.write(rl)
                    record = False





"""
_ Example _________________________________________________________________________

2017-05-12
    1) Reference Fasta file:

    '
        >hsa-let-7a-5p
        TGAGGTAGTAGGTTGTATAGTT
        >hsa-let-7a-3p
        CTATACAATCTACTGTCTTTC
        >hsa-let-7a-2-3p
        CTGTACAGCCTCCTAGCTTTCC
        >hsa-let-7b-5p
        TGAGGTAGTAGGTTGTGTGGTT
        >hsa-let-7b-3p
        CTATACAACCTACTGCCTTCCC
        >hsa-let-7c-5p
        TGAGGTAGTAGGTTGTATGGTT
        >hsa-let-7c-3p
        CTGTACAACCTTCTAGCTTTCC
        ...
    '

    2) miRNA list:

    '
        let-7c-5p
        let-7d-5p
        let-7e-5p
        let-7i-3p
        miR-100-5p
        miR-101-3p
        miR-106a-5p
        miR-10a-5p
        miR-10b-5p
        miR-1246
        miR-1248
        miR-125b-1-3p
        miR-125b-2-3p
        ...
    '

    3) Selected Fasta file:

    '
        >hsa-let-7c-5p
        TGAGGTAGTAGGTTGTATGGTT
        >hsa-let-7d-5p
        AGAGGTAGTAGGTTGCATAGTT
        >hsa-let-7e-5p
        TGAGGTAGGAGGTTGTATAGTT
        >hsa-miR-19a-3p
        TGTGCAAATCTATGCAAAACTGA
        >hsa-miR-19b-3p
        TGTGCAAATCCATGCAAAACTGA
        >hsa-miR-20a-5p
        TAAAGTGCTTATAGTGCAGGTAG
    ...
    '
___________________________________________________________________________________
"""