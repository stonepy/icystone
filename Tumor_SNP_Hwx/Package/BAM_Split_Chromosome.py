from multiprocessing import Pool
from subprocess import call

import os
import re
import time
import pysam



bamPATH     = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Test_DIR/BAM/0808_3/0808_3_final.bam"
bamSplitDIR = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Test_DIR/tmp"

bamdir = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Test_DIR/BAM/tmp"
javaPATH   = "java"
picardPATH = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Software/picard.jar"




try:
    assert chrNames

except:
    chrNames = []
    for i in range(1,23):
        chrNames.append(i)
    chrNames.append("X")
    chrNames.append("Y")


max_ProcessNum = 10



class chrSplit_BAM:

    def __init__(self):
        self.BAM_path     = bamPATH
        self.BAMSplit_dir = bamSplitDIR
        self.bam          = pysam.AlignmentFile(self.BAM_path, mode="rb")


    def chrSplit(self, chr_name):
        bamName = re.split("[/.]", self.BAM_path)[-2]
        print(bamName)
        BAMSplit_path = "%s/%s_%s.bam" % (self.BAMSplit_dir, bamName, chr_name)

        with open(BAMSplit_path, "w") as bamSplit:
            for l in self.bam.fetch(chr_name):
                bamSplit.write(l)


    def index_splitedBAM(self, chr_name):
        bamName = re.split("[/.]", self.BAM_path)[-2]
        for bam in bamList:
            bamPATH = "%s/%s" % (bamdir, bam)
            baiPATH = "%s/%s.bai" % (bamdir, bam)

            cmd = "{java} -jar {picard} BuildBamIndex I={bamPATH} O={baiPATH}".format(java=javaPATH, picard=picardPATH, bamPATH=bamPATH, baiPATH=baiPATH)

            print(cmd + "\n")
            call(cmd, shell=True)


class manager:

    def multiP_1(self, para_list, max_ProcessNum, func):

        P = Pool(max_ProcessNum)

        for i in para_list:
            P.apply_async(func, args=(i,))

        P.close()
        P.join()





chrS = chrSplit_BAM()
mgr  = manager()

mgr.multiP_1(chrNames, max_ProcessNum, chrS.chrSplit)
