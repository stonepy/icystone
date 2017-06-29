"""
    Convert 'MuTect*' result into '*library' for Annovar Annotation
    V2
"""


import sys


try:
    assert len(sys.argv) > 1
    inputPath  = sys.argv[1]
    outputPath = sys.argv[2]
    MTtype     = sys.argv[3]

except:
    inputPath  = "Mutect1_wjc_chr1.call_stats.txt"
    outputPath = "Mutect1_wjc_chr1.call_stats.txt.library"
    MTtype     = "1"

    print("\nUsage:\n    python  %s  <MuTectResultPaht> <outputPath> <MuTectVersion>\n" % __file__)
    exit()


# For MuTect1
def MT1():

    with open(inputPath, "r") as inf:

        outf = open(outputPath, "w")
        for l in inf:

            if l.startswith("#") or l.startswith("contig"):
                continue

            l_split = l.split("\t")

            chro = l_split[0]
            pos  = l_split[1]
            ref  = l_split[3]
            alt  = l_split[4]
            status = l_split[-1]

            Tumor_ref_count  = l_split[25]
            Tumor_alt_count  = l_split[26]
            Normal_ref_count = l_split[37]
            Normal_alt_count = l_split[38]

            wl = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (chro, pos, pos, ref, alt, Tumor_ref_count, Tumor_alt_count, Normal_ref_count, Normal_alt_count, status)
            outf.write(wl)

        outf.close()


# For MuTect2
def MT2():

    with open(inputPath, "r") as inf:

        outf = open(outputPath, "w")
        for l in inf:

            if l.startswith("#"):
                continue

            l_split = l.split("\t")

            chro = l_split[0]
            pos  = l_split[1]
            ref  = l_split[3]
            alt  = l_split[4]

            Tumor_ref_count  = l_split[-2].split(":")[1].split(",")[0]
            Tumor_alt_count  = l_split[-2].split(":")[1].split(",")[1]
            Normal_ref_count = l_split[-1].split(":")[1].split(",")[0]
            Normal_alt_count = l_split[-1].split(":")[1].split(",")[1]

            wl = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (chro, pos, pos, ref, alt, Tumor_ref_count, Tumor_alt_count, Normal_ref_count, Normal_alt_count)
            outf.write(wl)

        outf.close()


if "1" in MTtype:
    MT1()

elif "2" in MTtype:
    MT2()