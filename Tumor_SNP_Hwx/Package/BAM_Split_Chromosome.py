
# _ Information ________________________________________________________________________

__Name__           = """ BAM Split Chromosome """
__Description__    = """ \n This Script is developed for preparing splited BAM files for GATK_MuTect2 \n """
__Author__         = """ Hwx """
__Version__        = """ 1 """
__DevEnv__         = """ Red Hat 4.8.5-11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0 """
__FirstCreate__    = """ 2017-06-01"""
__LastModificate__ = """ 2017-06-07"""
__Notes__          = """ None """

# _ Information ________________________________________________________________ End ___




from multiprocessing import Pool
from subprocess import call

import os
import re
import time




# _ Arguments __________________________________________________________________________

def get_args():

    import argparse
    parser = argparse.ArgumentParser(description=__Description__)

    #
    parser.add_argument("Input_BAM_PATH", help="")
    parser.add_argument("Output_BAM_DIR", help="")
    parser.add_argument("-p", "--nSample", help="", default=6)

    args = parser.parse_args()

    return args

# _ Arguments __________________________________________________________________ End ___




# _ Arguments __________________________________________________________________________


class chrSplit_BAM:


    def __init__(self):
        self.BAM_path     = bamPATH
        self.BAMSplit_dir = bamSplitDIR

        self.samtools   = samtoolsPATH
        self.picardPATH = picardPATH


    def chrSplitIndex(self, chr_name):

        bamName = re.split("[/.]", self.BAM_path)[-2]
        BAMSplit_path = "%s/%s_%s.bam" % (self.BAMSplit_dir, bamName, chr_name)
        BAISplit_path = "%s/%s_%s.bam.bai" % (self.BAMSplit_dir, bamName, chr_name)

        # Must use '-h' option to include header in every output file, or following steps nay not work
        cmd_split = "{samtools} view -h -b {BAM_input} {chr} > {BAM_output}".format(samtools=self.samtools, BAM_input=self.BAM_path, chr=chr_name, BAM_output=BAMSplit_path)
        cmd_index = "{java} -jar {picard} BuildBamIndex I={BAMSplit_path} O={baiPATH}".format(java=javaPATH, picard=picardPATH, BAMSplit_path=BAMSplit_path, baiPATH=BAISplit_path)


        print(cmd_split + "\n")
        print(cmd_index + "\n")

        call(cmd_split, shell=True)
        call(cmd_index, shell=True)



class manager:

    def multiP_1(self, para_list, max_ProcessNum, func):

        P = Pool(max_ProcessNum)

        for i in para_list:
            P.apply_async(func, args=(i,))

        P.close()
        P.join()


# _ Arguments __________________________________________________________________ End ___




# _ Execution Manage ___________________________________________________________________

if __name__ == "__main__":

    bamPATH = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Test_DIR/BAM/0808_3/0808_3_final.bam"
    bamSplitDIR = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Test_DIR/tmp"

    javaPATH = "java"
    samtoolsPATH = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Software/samtools-1.4.1/samtools"
    picardPATH = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Software/picard.jar"

    max_ProcessNum = 25


    args = get_args()

    bamPATH     = args.Input_BAM_PATH
    bamSplitDIR = args.Output_BAM_DIR
    max_ProcessNum = int(args.nSample)

    try:
        assert chrNames

    except:
        chrNames = []
        for i in range(1, 23):
            chrNames.append(i)
        chrNames.append("X")
        chrNames.append("Y")


    chrS = chrSplit_BAM()
    mgr  = manager()


    mgr.multiP_1(chrNames, max_ProcessNum, chrS.chrSplitIndex)


# _ Execution Manage ___________________________________________________________ End ___
