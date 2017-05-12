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
                            sf.write(mi+"\n")
                            record = True
                    continue

                # Record the sequence when names are the same
                if record == True:
                    print(rl)
                    sf.write(rl)
                    record = False