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
    libraryPath = "tmp/Mutect1_whole_T2N2_KEEP.call_stats.library"
    AnnovarDir  = "tmp/Mutect1_whole_T2N2_KEEP/"
    outputPath  = "test.xls"

    # print("\nUsage:\n    python  %s  <libraryPath>  <AnnovarDir>  <outputPath>" % __file__)
    # exit()

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
    lib_title = ["Chrs", "pos", "pos", "RefAllele", "AltAllele"]

    for l in lib:

        l_split = l.split("\t")

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
        l_chro  = l_split[-5]
        l_pos   = l_split[-4]

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
        l_chro  = l_split[-5]
        l_pos   = l_split[-4]

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
            l_chro  = l_split[-5]
            l_pos   = l_split[-4]

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
                l_chro  = l_split[-5]
                l_pos   = l_split[-4]

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
brary Annovar annotation
"""

from multiprocessing import Pool
from subprocess import call

import sys
import time


inputPath = sys.argv[1]
print("\n %s \n" % inputPath)
time.sleep(1)
refDir = "/home/pub/database/Human/hg19/Annotation/"
outputDir = ""


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
