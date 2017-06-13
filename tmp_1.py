"""
Select 'GATK_UnifiedGenotyper' unique results

"""

import pandas as pd


inputDIR  = "/home/daniel/PycharmProjects/fishbone/1_GATK_UnifiedGenotyper/"
outputDIR = inputDIR



tumorI  = open(inputDIR + "0808_1_filtered.vcf", "r")
normalI = open(inputDIR + "0808_2_filtered.vcf", "r")

tumorO  = open(outputDIR + "0808_1_filtered_unique.vcf", "w")
normalO = open(outputDIR + "0808_2_filtered_unique.vcf", "w")


while True:

    try:
        tl = next(tumorI)
        nl = next(normalI)

        if tl.startswith("#"):
            tumorO.write(tl)
            normalO.write(nl)
            continue

    except:
        break


    tl_split = tl.split("\t")
    nl_split = nl.split("\t")


    tl_Alt = tl_split[4]
    nl_Alt = nl_split[4]

    tl_GT = tl_split[-1].split(":")[0]
    nl_GT = nl_split[-1].split(":")[0]

    print(tl_Alt, tl_GT)


    if tl_Alt != nl_Alt and tl_GT != nl_GT:
        tumorO.write(tl)
        normalO.write(nl)


tumorO.close()
normalO.close()

tumorI.close()
normalI.close()













