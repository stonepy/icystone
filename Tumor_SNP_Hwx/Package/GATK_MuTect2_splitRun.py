# _ Information ________________________________________________________________________

__Name__           = """ TGATK MuTect2 ChromosomeSeparate Running """
__Description__    = """ \n Running GATK Mutect2 with separated chromosomes. Developed in Python3 \n """
__Author__         = """ Hwx """
__Version__        = """ 0 """
__DevEnv__         = """ Red Hat 4.8.5-11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0 """
__FirstCreate__    = """ 2017-06-02"""
__LastModificate__ = """ 2017-06-"""
__Notes__          = """ None """
# _ Information ________________________________________________________________________



# _ Packages ___________________________________________________________________________

import argparse
import logging
import os
import sys
import subprocess
import multiprocessing

from subprocess import call
from multiprocessing import Pool

# _ Packages ___________________________________________________________________________



# _ Arguments __________________________________________________________________________


def get_args():

    parser = argparse.ArgumentParser(description=__Description__)

    parser.add_argument("InputDir", help="Folder contains all Inuput BAM files, both Tumor and Normal")
    parser.add_argument("OutputDir", help="Folder for Outputing result VCF files")
    parser.add_argument("Tumor", help="Name of Tumor samples")
    parser.add_argument("Normal", help="Name of Normal samples")

    args = parser.parse_args()

    return args

# _ Arguments __________________________________________________________________________





# // Main //////////////////////////////////////////////////////////////////////////////

chrNum    = 23
chrSpcial = ("X", "Y")

for i in range(1, chrNum):

    try:
        chrList.append(str(i))

    except:
        chrList = []
        chrList.append(str(i))

for i in chrSpcial:
    chrList.append(i)


projDir = "/home/icystar/DevPipline/Tumor_SNP_Hwx/"



def MuTect2_CMDs(pDict):

    # CMD_example:

    """
    java -jar GenomeAnalysisTK.jar \
     -T MuTect2 \
     -R reference.fasta \
     -I:tumor tumor.bam \
     -I:normal normal.bam \
     -o output.vcf
    """

    CMDs = []
    for i in pDict["chrList"]:

        tumorBAM  = "%s/%s_%s.bam" % (pDict["BAMsplDir"], pDict["tumorName"], str(i))
        normalBAM = "%s/%s_%s.bam" % (pDict["BAMsplDir"], pDict["normalName"], str(i))
        outVCF    = "%s/%s_Versus_%s_%s.vcf" % (pDict["vcfDir"], pDict["tumorName"], pDict["normalName"], str(i))

        cmd = "{java} -jar {gatk} -T MuTect2 -R {refFasta} -I:tumor {tumorBAM} -I:normal {normalBAM} -o {outVCF}".format(java=pDict["java"], gatk=pDict["gatk"], refFasta=pDict["ref"], tumorBAM=tumorBAM, normalBAM=normalBAM, outVCF=outVCF)

        CMDs.append(cmd)


    return CMDs



def multiCall(CMDs, max_Process):
    print("\n   Using Multiple Processes\n")
    print(CMDs)

    def callFunc(cmd):
        # call(cmd)
        print(cmd, "\n")


    P = Pool(max_Process)

    for cmd in CMDs:
        P.apply_async(callFunc, args=(cmd, ))

    P.close()
    P.join()



# // Main //////////////////////////////////////////////////////////////////////////////





# _ Execution Control __________________________________________________________________

if __name__ == "__main__":
    args = get_args()


    pDict = {

        "tumorName"  : args.Tumor,
        "normalName" : args.Normal,

        "java"      : "/usr/bin/java",
        "gatk"      : projDir + "Software/GenomeAnalysisTK.jar",
        "ref"       : projDir + "Database/hg19.fa",
        "BAMsplDir" : args.InputDir,
        "vcfDir"    : args.OutputDir,

        "chrList"   : chrList,

        'nProcess'  : 8,

    }


    multiCall(MuTect2_CMDs(pDict), 8)





# _ Execution Control __________________________________________________________________





# - Log --------------------------------------------------------------------------------
Log = """
2017-06-
    1)
"""
# - Log
#
#
# --------------------------------------------------------------------------------
