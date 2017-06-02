

from multiprocessing import Pool

import multiprocessing as mp
import re
import time
import pysam


# bamPATH     = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Test_DIR/BAM/0808_3/0808_3_final.bam"
# bamSplitDIR = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Test_DIR/tmp"
bamPATH     = "0808_1_final.bam"
bamSplitDIR = "tmp"

# bam_list = []
bam = pysam.AlignmentFile(bamPATH, mode="rb")
# for l in bam:
#     bam_list.append(l)

try:
    assert chrNames
    assert chrNames > 0

except:
    chrNames = []
    for i in range(1,2):
        chrNames.append(i)
    chrNames.append("X")
    chrNames.append("Y")


max_ProcessNum = 2





class chrSplit_BAM:

    def __init__(self):
        self.BAM_path     = bamPATH
        self.BAMSplit_dir = bamSplitDIR
        self.bam          = pysam.AlignmentFile(self.BAM_path, mode="rb")

        self.a = "w"


    def chrSplit(self, chr_name):
        bamName = re.split("[/.]", self.BAM_path)[-2]
        print(bamName)
        BAMSplit_path = "%s/%s_%s.bam" % (self.BAMSplit_dir, bamName, chr_name)

        with open(BAMSplit_path, "w") as bamSplit:
            for l in bam.fetch(str(chr_name)):
                # print(l)
                # time.sleep(0.5)

                bamSplit.write(l)


    def test(self, x):
        print("This is %s" % str(x))


def mpCall(bam_list, xs, func):
    p = Pool(4)

    for x in xs:
        print(x)
        p.apply_async(func, args=(bam_list, x,))

    p.close()
    p.join()


# mpCall(bam, chrNames, chrSplit_BAM().chrSplit)

chrSplit_BAM().chrSplit(3)
