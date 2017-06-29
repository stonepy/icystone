"""
    Compare 'HaplotypeCaller' and 'MuTect.x' result
"""


import sys
import pandas as pd


try:
    assert len(sys.argv) > 1
    hapPath = sys.argv[1]
    mutPath = sys.argv[2]
    outputPath = sys.argv[3]
except:
    # hapPath    = "/home/daniel/PycharmProjects/fishbone/TumorUnique/17B0106A_wjc_SpecialMutation.xlsx"
    # mutPath    = "Mutect1_chr1_T2N2_KEEP.xlsx"
    # outputPath = "Mutect1_chr1_T2N2_compare.xlsx"

    print("\nUsage:\n    python  %s  <HaplotypeCallerResultPath>  <MuTectResultPath>  <OutputPath>\n" % __file__)
    exit()


# Read the data sheets
hap_sheet = "SNV Information"
mut_sheet = mutPath.split("/")[-1].split(".")[-2]
df_hap = pd.read_excel(hapPath, sheetname=hap_sheet)
df_mut = pd.read_excel(mutPath, sheetname=mut_sheet)


# Deal with 'HaplotypeCaller' result
delIndex_list = []
for i, row in df_hap.iterrows():

    # Ex: df_hap.iloc['rowNum', 'colNum']
    chr = df_hap.iloc[i, 7]
    chr = row[7]
    if chr != 1:
        delIndex_list.append(i)

# Keep chromosome 1
df_hapChr1 = df_hap.drop(delIndex_list, axis=0)

# Tumor/Normal reads columns 'hap'
hapChr1_Treads = df_hapChr1.columns.values[-1]
hapChr1_Nreads = df_hapChr1.columns.values[-3]


# Deal with 'MuTect.x' result
df_mutChr1 = df_mut
# Merge 'HaplotypeCaller' and 'MuTect*' results
df_hapmutChr1 = pd.merge(df_hapChr1, df_mutChr1, how="inner", on="Position")


# Get reads count from 'HaplotypeCaller' and 'MuTect.x' results individually
mutChr1_T_refcount = df_hapmutChr1["Tumor_ref_count"]
mutChr1_T_altcount = df_hapmutChr1["Tumor_alt_count"]
mutChr1_N_refcount = df_hapmutChr1["Normal_ref_count"]
mutChr1_N_altcount = df_hapmutChr1["Normal_alt_count"]

hapChr1_T_reads = df_hapmutChr1[hapChr1_Treads]
hapChr1_N_reads = df_hapmutChr1[hapChr1_Nreads]


# Deal with reads count
Tumor_reads  = []
Nomarl_reads = []
for i in range(len(mutChr1_T_refcount)):
    Tumor_reads.append(str(hapChr1_T_reads[i]) + " | " + (str(mutChr1_T_refcount[i]) + ":" +  str(mutChr1_T_altcount[i])))
    Nomarl_reads.append(str(hapChr1_N_reads[i]) + " | " + (str(mutChr1_N_refcount[i]) + ":" +  str(mutChr1_N_altcount[i])))

# Insert to the last two columns
df_hapmutChr1["Tumor_Hap | Mut"]  = Tumor_reads
df_hapmutChr1["Normal_Hap | Mut"] = Nomarl_reads


# Select unique results
df_hapChr1Unique = df_hapChr1
df_mutChr1Unique = df_mutChr1
hapIndex_list = []
mutIndex_list = []

for p in df_hapmutChr1["Position"]:

    for i, row in df_hapChr1Unique.iterrows():
        if p == row[8]:
            hapIndex_list.append(i)

    for i, row in df_mutChr1Unique.iterrows():
        if p == row[1]:
            mutIndex_list.append(i)

# Keep unique results
df_hapChr1Unique = df_hapChr1Unique.drop(hapIndex_list, axis=0)
df_mutChr1Unique = df_mutChr1Unique.drop(mutIndex_list, axis=0)


# Save results as '*.xlsx' file
writer = pd.ExcelWriter(outputPath)
df_hapmutChr1.to_excel(writer, 'HaploptypeCaller|MuTect.x', index=False)
df_hapChr1Unique.to_excel(writer, 'HaploptypeCaller_Unique', index=False)
df_mutChr1Unique.to_excel(writer, 'MuTect.x_Unique', index=False)
df_hapChr1.to_excel(writer, 'HaploptypeCaller', index=False)
df_mutChr1.to_excel(writer, 'MuTect.x', index=False)
writer.save()







"""
   Library Annovar annotation summary
"""


import sys

try:
    assert len(sys.argv) > 1
    libraryPath = sys.argv[1]
    AnnovarDir  = sys.argv[2]
    outputPath  = sys.argv[3]
except:
    # libraryPath = "/home/daniel/PycharmProjects/fishbone/tmp_2/Mutect2_chr1_wjc_BED/Mutect2_chr1_wjc_BED.library"
    # AnnovarDir  = "/home/daniel/PycharmProjects/fishbone/tmp_2/Mutect2_chr1_wjc_BED"
    # outputPath  = "test.xls"

    print("\nUsage:\n    python  %s  <libraryPath>  <AnnovarDir>  <outputPath>\n" % __file__)
    exit()

summary_dict = {

    # "SIFT Score"          : "hg19_dbnsfp33a_sift_dropped",
    # "POLYPhen V2 Score"   : "hg19_dbnsfp33a_pp2_dropped",
    # "MutationTaster"      : "hg19_dbnsfp33a_mt_dropped",
    "Cadd"                : "hg19_cadd13_dropped",
    "Dann"                : "hg19_dann_dropped",
    "Eigen"               : "hg19_eigen_dropped",
    "Hrcr1"               : "hg19_hrcr1_dropped",
    "Kaviar"              : "hg19_kaviar_20150923_dropped",
    "1000g_chbs"          : "hg19_ALL.sites.2012_02_dropped",
    "esp6500"             : "hg19_esp6500siv2_all_dropped",
    "tfbsConsSites Score" : "hg19_tfbsConsSites",
    "ExAC03"              : "hg19_exac03_dropped",
    "gnomAD"              : "hg19_gnomad_exome_dropped",
    "ClinVar"             : "hg19_clinvar_20170130_dropped",
    "COSMIC"              : "hg19_cosmic70_dropped",
    "ICGC"                : "hg19_icgc21_dropped",
    "NCI60"               : "hg19_nci60_dropped",

}


# Build the index
with open(libraryPath, "r") as lib:
    lib_dict  = {}
    lib_title = ["Chrs", "Pos", "Pos", "RefAllele", "AltAllele", "Tumor_ref_count", "Tumor_alt_count", "Normal_ref_count", "Normal_alt_count"]

    for l in lib:

        l_split = l.split("\t")
        i_chro  = l_split[0]
        i_pos   = l_split[1]

        try:
            lib_dict[l_split[0]][l_split[1]] = l.strip()
        except:
            lib_dict[l_split[0]] = {}
            lib_dict[l_split[0]][l_split[1]] = l.strip()


libName = libraryPath.split("/")[-1]

# Five special annotation: "*.exonic_variant_function", "*.variant_function"
path_exo = "%s/%s.exonic_variant_function" % (AnnovarDir, libName)
path_var = "%s/%s.variant_function" % (AnnovarDir, libName)
path_SIFT = "%s/%s.hg19_dbnsfp33a_sift_dropped" % (AnnovarDir, libName)
path_POLY = "%s/%s.hg19_dbnsfp33a_pp2_dropped" % (AnnovarDir, libName)
path_MuTR = "%s/%s.hg19_dbnsfp33a_mt_dropped" % (AnnovarDir, libName)


# For "Function", "Predicted Protein Variants" columns
with open(path_exo, "r") as f:

    for l in f:

        l_split = l.split("\t")
        l_chro  = l_split[-9]
        l_pos   = l_split[-8]

        for chro in lib_dict:
            if chro == l_chro:
                for pos in lib_dict[chro]:
                    if pos == l_pos:
                        lib_dict[chro][pos] += "\t%s\t%s\t" % (l_split[1],l_split[2])


    lib_title.append("Function")
    lib_title.append("Predicted Protein Variants")

    # If some annotation are not avaible for some sites, it make sure that cells will not be fill by other value
    for chro in lib_dict:
        for pos in lib_dict[chro]:
            if not lib_dict[chro][pos].endswith("\t"):
                lib_dict[chro][pos] += "\t\t\t"


# For "Gene Region", "Gene" columns
with open(path_var, "r") as f:

    for l in f:
        l_split = l.split("\t")
        l_chro  = l_split[-9]
        l_pos   = l_split[-8]

        for chro in lib_dict:
            if chro == l_chro:
                for pos in lib_dict[chro]:
                    if pos == l_pos:
                        lib_dict[chro][pos] += "%s\t%s" % (l_split[0], l_split[1])

    lib_title.append("Gene Region")
    lib_title.append("Gene")

    # If some annotation are not avaible for some sites, it make sure that cells will not be fill by other value
    for chro in lib_dict:
        for pos in lib_dict[chro]:
            if not lib_dict[chro][pos].endswith("\t"):
                lib_dict[chro][pos] += "\t"
            else:
                lib_dict[chro][pos] += "\t\t"


OptSplit_dict = {

    # For "SIFT Score", "SIFT Score Pred" columns
    "SIFT Score"    :{
        "path"  :   path_SIFT,
        "title" :   ["SIFT Score", "SIFT Score Pred"],
    },
    # For "POLYPhen V2 Score", "POLYPhen V2 Score Pred" columns
    "POLYPhen V2 Score" :{
        "path"  :   path_POLY,
        "title" :   ["POLYPhen V2 Score", "POLYPhen V2 Score Pred"],
    },
    # For "MutationTaster", "MutationTaster Pred" columns
    "MutationTaster"    :{
        "path"  :   path_MuTR,
        "title" :   ["MutationTaster", "MutationTaster Pred"],
    },

}


def score_pred(path, score, pred):

    with open(path, "r") as f:

        for l in f:
            l_split = l.split("\t")
            l_chro  = l_split[-9]
            l_pos   = l_split[-8]

            for chro in lib_dict:
                if chro == l_chro:
                    for pos in lib_dict[chro]:
                        if pos == l_pos:
                            Score, Pred = l_split[1].split(";")
                            lib_dict[chro][pos] += "%s\t%s" % (Score, Pred)

        lib_title.append(score)
        lib_title.append(pred)

        # If some annotation are not avaible for some sites, it make sure that cells will not be fill by other value
        for chro in lib_dict:
            for pos in lib_dict[chro]:
                if not lib_dict[chro][pos].endswith("\t"):
                    lib_dict[chro][pos] += "\t"
                else:
                    lib_dict[chro][pos] += "\t\t"

for key in OptSplit_dict:
    score_pred(OptSplit_dict[key]["path"], OptSplit_dict[key]["title"][0], OptSplit_dict[key]["title"][1])


# Summarize the rest of annotations.
for key in summary_dict:

    try:
        AnnovarPath = "%s/%s.%s" % (AnnovarDir, libName, summary_dict[key])

        with open(AnnovarPath, "r") as anno:
            lib_title.append(key)

            # Find out the right cell to store the value
            for l in anno:
                l_split = l.split("\t")
                l_chro  = l_split[-9]
                l_pos   = l_split[-8]

                for chro in lib_dict:
                    if chro == l_chro:
                        for pos in lib_dict[chro]:
                            if pos == l_pos:
                                lib_dict[chro][pos] += l_split[1]

    except:
        print("%s: %s is not available." % (key, AnnovarPath))
        continue

    # If some annotation are not avaible for some sites, it makes sure that cells will not be fill by other value
    for chro in lib_dict:
        for pos in lib_dict[chro]:
            lib_dict[chro][pos] += "\t"


with open(outputPath, "w") as outf:
    title = ""
    for i in lib_title:
        title += i + "\t"
    outf.write(title+"\n")

    for chro in lib_dict:

        for pos in lib_dict[chro]:
            l = lib_dict[chro][pos] + "\n"
            outf.write(l)







"""
    library Annovar annotation
"""

from multiprocessing import Pool
from subprocess import call

import sys
import time


try:
    assert len(sys.argv) == 2
    inputPath = sys.argv[1]

except:
    print("\nUsage:\n    python  %s  <libraryPath>\n" % __file__)
    exit()

print("\n %s \n" % inputPath)
time.sleep(1)


# Server 6#
refDir = "/home/pub/database/Human/hg19/Annotation/"

opt_list = [

    "--hgvs --splicing_threshold 15",
    "-filter -dbtype avsnp147",
    "-filter -dbtype 1000g2015aug_all",
    "-filter -dbtype dbnsfp33a_sift",
    "-filter -dbtype dbnsfp33a_pp2",
    "-filter -dbtype dbnsfp33a_mt",
    "-filter -dbtype esp6500siv2_all",
    "-filter -dbtype cadd13",
    "-filter -dbtype dann",
    "-filter -dbtype eigen",
    "-filter -dbtype hrcr1",
    "-filter -dbtype kaviar_20150923",
    "-regionanno -dbtype tfbsConsSites",
    "-filter -dbtype 1000g2014oct_chbs",
    "-filter -dbtype exac03 --otherinfo",
    "-filter -dbtype clinvar_20170130 -otherinfo",
    "-filter -dbtype cosmic70",
    "-filter -dbtype nci60",
    "-filter -dbtype gnomad_exome",
    "-filter -dbtype icgc21 -otherinfo",

]


Log = open("log_%s.txt" % time.ctime(), "w")
cmd_list = []

for opt in opt_list:
    cmd = "perl /home/pub/software/annovar/annotate_variation.pl {opt} --buildver hg19 {library} {ref_dir}".format(opt=opt, library=inputPath, ref_dir=refDir)
    cmd_list.append(cmd)

P = Pool(10)
for cmd in cmd_list:
    print("\n %s \n" % cmd)
    Log.write("\n %s \n" % cmd)
    P.apply_async(call(cmd, shell=True))
P.close()
P.join()

Log.close()







"""
    Convert 'MuTect*' result into '*library' for Annovar Annotation
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

            Tumor_ref_count  = l_split[25]
            Tumor_alt_count  = l_split[26]
            Normal_ref_count = l_split[37]
            Normal_alt_count = l_split[38]

            wl = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (chro, pos, pos, ref, alt, Tumor_ref_count, Tumor_alt_count, Normal_ref_count, Normal_alt_count)
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






"""
    Samtools tview
"""

from multiprocessing import Pool
from subprocess import call

import sys


SNV_Path  = sys.argv[1]
BAM_Path  = sys.argv[2]
outputDir = sys.argv[3]

refPATH = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Database/hg19/hg19.fa"    # Server 2#


with open(SNV_Path, "r") as inf:

    site_list = {}
    cmd_list  = []
    for l in inf:
        l_split = l.split("\t")
        pos = "%s:%s" % (l_split[0], l_split[1])

        # If the file name does not start with letter 't', it won't work properly
        output_Path = outputDir + "/tchr%s_%s.tview" % (l_split[0], l_split[1])
        cmd = "/home/hwx/DevPipline/Tumor_SNP_Hwx/Software/samtools-1.4.1/samtools tview -d t -p {pos} {BAM} {ref} > {output}".format(pos=pos, BAM=BAM_Path, ref=refPATH, output=output_Path)
        # print("\n %s \n" % cmd)
        cmd_list.append(cmd)

P = Pool(15)
for cmd in cmd_list:
    P.apply_async(call(cmd, shell=True))
    print(cmd)
P.close()
P.join()