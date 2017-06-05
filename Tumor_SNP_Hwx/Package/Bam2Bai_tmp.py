import os
from subprocess import call

bamdir = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Test_DIR/BAM/tmp"

javaPATH   = "java"
picardPATH = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Software/picard.jar"

bamList = os.listdir(bamdir)

for bam in bamList:

    bamPATH = "%s/%s" % (bamdir, bam)
    baiPATH = "%s/%s.bai" % (bamdir, bam)

    cmd = "{java} -jar {picard} BuildBamIndex I={bamPATH} O={baiPATH}".format(java=javaPATH, picard=picardPATH, bamPATH=bamPATH, baiPATH=baiPATH)

    print(cmd + "\n")
    call(cmd, shell=True)
