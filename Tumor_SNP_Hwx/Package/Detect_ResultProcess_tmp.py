"""
    Strelka INDEL results split
"""

strelkaVCF_path = "somatic.indels.vcf"
output_paht     = "somatic.indels.Splited.vcf"


with open(strelkaVCF_path, "r") as inf:

    outf = open(output_paht , "w")

    for l in inf:

        if l.startswith("##"):
            continue

        elif l.startswith("#C"):

            l_split = l.strip().split("\t")

            CHROM  = l_split[0] + "\t"
            POS    = l_split[1] + "\t"
            ID     = l_split[2] + "\t"
            REF    = l_split[3] + "\t"
            ALT    = l_split[4] + "\t"
            QUAL   = l_split[5] + "\t"
            FILTER = l_split[6] + "\t"

            INFO   = l_split[7]  + "\t" * 13
            # FORMAT = l_split[8]  + "\t" * 8
            NORMAL = l_split[9]  + "\t" * 9
            TUMOR  = l_split[10] + "\t" * 9

            INFO_tt   = "Type\tQSI\tTQSI\tNT\tQSI_NT\tTQSI_NT\tSGT\tMQ\tMQ0\tRU\tRC\tIC\tIHP\t"
            # FORMAT_tt = ""
            NORMAL_tt = "N_DP\tN_DP2\tN_TAR\tN_TIR\tN_TOR\tN_DP50\tN_FDP50\tN_SUBDP50\tN_BCN50\t"
            TUMOR_tt  = "T_DP\tT_DP2\tT_TAR\tT_TIR\tT_TOR\tT_DP50\tT_FDP50\tT_SUBDP50\tT_BCN50\t"

            # outf.write(CHROM+POS+ID+REF+ALT+QUAL+FILTER+INFO+FORMAT+NORMAL+TUMOR + "\n")
            outf.write("\t"+"\t"+"\t"+"\t"+"\t"+"\t"+"\t"+INFO+NORMAL+TUMOR + "\n")
            outf.write(CHROM+POS+ID+REF+ALT+QUAL+FILTER+INFO_tt+NORMAL_tt+TUMOR_tt + "\n")


        else:

            l_split = l.strip().split("\t")

            CHROM_val  = l_split[0] + "\t"
            POS_val    = l_split[1] + "\t"
            ID_val     = l_split[2] + "\t"
            REF_val    = l_split[3] + "\t"
            ALT_val    = l_split[4] + "\t"
            QUAL_val   = l_split[5] + "\t"
            FILTER_val = l_split[6] + "\t"

            INFO_val   = l_split[7].split(";")
            # FORMAT_val = l_split[8].split(":")
            NORMAL_val = l_split[9].split(":")
            TUMOR_val  = l_split[10].split(":")

            INFO_ln   = ""
            # FORMAT_ln = ""
            NORMAL_ln = ""
            TUMOR_ln  = ""

            for i in INFO_val:
                if i == "OVERLAP":
                    INFO_ln = INFO_ln.strip() + ";"

                INFO_ln   += i.split("=")[-1] + "\t"

            #     INFO_tt   += i.split("=")[0] + "\t"
            # print(INFO_tt)

            # for i in FORMAT_val:
                # FORMAT_ln += i + "\t"
            # print(FORMAT_ln)

            for i in NORMAL_val:
                NORMAL_ln += i + "\t"

            for i in TUMOR_val:
                TUMOR_ln  += i + "\t"

            outf.write(CHROM_val+POS_val+ID_val+REF_val+ALT_val+QUAL_val+FILTER_val+INFO_ln+NORMAL_ln+TUMOR_ln + "\n")


    outf.close()







"""
    Select chromosome1 from 'Mutect.X' result
"""


import sys

inputPath = sys.argv[1]
outputPath = sys.argv[2]

with open(inputPath, "r") as inf:
    outf = open(outputPath, "w")

    for l in inf:
        l_split = l.split("\t")

        if l_split[0] == "1":
            outf.write(l)

    outf.close()







"""
    Convert 'MuTect*' result into '*library' for Annovar Annotation
    V2: Add 'status' column,
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
            # Different from V1
            status = l_split[-1].strip()

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







"""
    Compare 'HaplotypeCaller' and 'MuTect.x' result
    V2
"""


import sys


try:
    assert len(sys.argv) > 1
    hapPath = sys.argv[1]
    mutPath = sys.argv[2]
    outputPath = sys.argv[3]
except:
    # hapPath    = "/home/daniel/PycharmProjects/fishbone/TumorUnique/17B0106A_wjc_SpecialMutation.xlsx"
    # mutPath    = "Mutect1_chr1_wjc.summary.xls"
    # outputPath = "teat.xls"

    print("\nUsage:\n    python  %s  <HaplotypeCallerResultPath>  <MuTectResultPath>  <OutputPath>\n\nNote:\n    HaplotypeCallerResultPath  ==>    '*xlsx'\n    MuTectResultPath           ==>   '*.xls'\n"% __file__)
    exit()




import pandas as pd

# Read the data sheets
hap_sheet = "SNV Information"
df_hap = pd.read_excel(hapPath, sheetname=hap_sheet)
df_mut = pd.read_csv(mutPath, sep="\t")

# mut_sheet = mutPath.split("/")[-1].split(".")[-2]
# df_mut = pd.read_excel(mutPath, sheetname=mut_sheet)


# Deal with 'HaplotypeCaller' result
delIndex_list = []
for i, row in df_hap.iterrows():

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

# Move 'Status' to the last column
try:
    df_hapmutChr1["MuTect1_Status"] = df_hapmutChr1["Status"]
    del df_hapmutChr1["Status"]
except:
    print("\nNotice: Using other result than 'MuTect1\n'")



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
   For MuTect2
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
    lib_title = ["Chrs", "Position", "Position", "RefAllele", "AltAllele", "Tumor_ref_count", "Tumor_alt_count", "Normal_ref_count", "Normal_alt_count"]

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
   Library Annovar annotation summary
   For MuTect1: Add 'Status'
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
    # This line is different from 'MuTect2' version, add 'Status'
    lib_title = ["Chrs", "Position", "Position", "RefAllele", "AltAllele", "Tumor_ref_count", "Tumor_alt_count", "Normal_ref_count", "Normal_alt_count", "Status"]

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
        # These two lines are different from 'MuTect2' version
        l_chro  = l_split[-10]
        l_pos   = l_split[-9]

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
        # These two lines are different from 'MuTect2' version
        l_chro  = l_split[-10]
        l_pos   = l_split[-9]

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
            # These two lines are different from 'MuTect2' version
            l_chro  = l_split[-10]
            l_pos   = l_split[-9]

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
                # These two lines are different from 'MuTect2' version
                l_chro  = l_split[-10]
                l_pos   = l_split[-9]

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
    V1
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

    print("\nUsage:\n    python  %s  <MuTectResultPath> <outputPath> <MuTectVersion>\n" % __file__)
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








"""
BED position expandation

"""


import sys

inputPATH  = sys.argv[1]
outputPATH = sys.argv[2]
distance = sys.argv[3]


with open(inputPATH, "r") as inf:

    outf = open(outputPATH, "w")

    for l in inf:
        l_split = l.strip().split("\t")
        l_split[1] = int(l_split[1]) - int(distance)
        l_split[2] = int(l_split[2]) + int(distance)

        newl = ""
        for i in l_split:
            i = str(i)
            newl += i + "\t"
        newl = newl.strip() + "\n"
        outf.write(newl)

    outf.close()









"""
Select 'Somatic' & 'LOH' of 'Varscan2' result

"""


import sys

inputPATH  = sys.argv[1]
outputPATH = sys.argv[2]


with open(inputPATH, "r") as inf:

    outf = open(outputPATH, "w")

    for l in inf:
        l_split = l.split("\t")
        if l_split[12] == "Somatic" or l_split[12] == "LOH":
            outf.write(l)

    outf.close()








"""
Select 'GATK_MuTect2/Varscan2 common'

"""

import sys
import time
import pandas as pd



input_MuTect2_PATH  = sys.argv[1]
input_Varscan2_PATH = sys.argv[2]

outputPATH = sys.argv[3]


df_tumorI = pd.read_csv(input_MuTect2_PATH, header=None, sep="\t", comment="#")
df_normalI = pd.read_csv(input_Varscan2_PATH, header=None, sep="\t", comment="#")


commonList = []

tumorList  = []
normalList = []


for idx_t, row_t in df_tumorI.iterrows():
    # print("\n\n\ntumor: %s" % row_t)
    # time.sleep(1.5)

    pos_t = row_t[1]
    alt_t = row_t[4]
    gt_t  = row_t[9].split(":")[0]

    for idx_n, row_n in df_normalI.iterrows():
        # print("\nnormal: %s" % row_n)
        # time.sleep(0.5)

        pos_n = int(row_n[1])
        alt_n = row_n[3]

        if pos_t == pos_n and alt_t == alt_n:
            # print("tumor: %s" % row_t)
            # time.sleep(0.5)
            commonList.append(row_t)



df_common = pd.DataFrame(commonList)


df_common.to_csv(outputPATH, header=None, index=None, sep="\t")








"""
Select GATK-UnifiedGenotyper SNP site of VCF

"""


import sys



def select_snp_indel():
    with open(outputPATH, "w") as outf:

        inf = open(inputPATH, "r")

        for l in inf:

            l_split = l.split("\t")

            if l.startswith("#") or l_split[4] == ".":
                continue

            outf.write(l)

        inf.close()



def select_chr():
    with open(outputPATH, "w") as outf:

        inf = open(inputPATH, "r")

        for l in inf:

            l_split = l.split("\t")

            if l.startswith("#") or l_split[0] != str(select_opt):
                continue

            outf.write(l)

        inf.close()



if __name__ == "__main__":

    inputPATH  = sys.argv[1]
    outputPATH = sys.argv[2]

    try:
        select_opt = sys.argv[3]
        print("\nSelect chromosome %s\n" % select_opt)
        select_chr()
    except:
        print("\nSelect all SNP/INDEL sites\n")
        select_snp_indel()









"""
Select 'GATK_UnifiedGenotyper', 'GATK_UnifiedGenotyper/GATK_MuTect2 and 'Varscan2-Somatic' common results

"""



import pandas as pd



df_u = pd.read_csv("UnifiedGenotyper_chr1.vcf", index_col=False, sep="\t")

df_m = pd.read_csv("MuTect2_chr1.vcf", index_col=False, sep="\t")

df_v = pd.read_csv("Varscan2_chr1.vsn", index_col=False, sep="\t")



df_merge_um = pd.merge(df_u, df_m, on="position")
df_merge_uv = pd.merge(df_u, df_v, on="position")
df_merge_mv = pd.merge(df_m, df_v, on="position")
df_merge_umv = pd.merge(df_merge_um, df_v, on="position")

df_merge_um.to_csv("UM_chr1.tsv", header=None, index=None, sep="\t")
df_merge_uv.to_csv("UV_chr1.tsv", header=None, index=None, sep="\t")
df_merge_mv.to_csv("MV_chr1.tsv", header=None, index=None, sep="\t")
df_merge_umv.to_csv("UMV_chr1.tsv", header=None, index=None, sep="\t")



df_merge_um = pd.merge(df_u, df_m, on="position", how="outer")
df_merge_uv = pd.merge(df_u, df_v, on="position", how="outer")
df_merge_mv = pd.merge(df_m, df_v, on="position", how="outer")
df_merge_umv = pd.merge(df_merge_um, df_v, on="position", how="outer")

df_merge_um.to_csv("UM_diff_chr1.tsv", header=None, index=None, sep="\t")
df_merge_uv.to_csv("UV_diff_chr1.tsv", header=None, index=None, sep="\t")
df_merge_mv.to_csv("MV_diff_chr1.tsv", header=None, index=None, sep="\t")
df_merge_umv.to_csv("UMV_diff_chr1.tsv", header=None, index=None, sep="\t")







"""
Select 'GATK_UnifiedGenotyper' Tumor/Normal unique results (For all sites, VCFs include both SNP/INDEL and None sites)

"""


import sys



def sep_snp_indel_all():

    inf1 = open(input_1_PATH, "r")
    inf2 = open(input_2_PATH, "r")

    outf1 = open(output_1_PATH, "w")
    outf2 = open(output_2_PATH, "w")
    outf3 = open(output_3_PATH, "w")


    while True:
        try:
            l1 = next(inf1)
            l2 = next(inf2)
        except:
            break

        if l1.startswith("#"):
            continue


        l1_split = l1.split("\t")
        l2_split = l2.split("\t")

        l1_chr = l1_split[0]
        l2_chr = l2_split[0]

        l1_alt = l1_split[4]
        l2_alt = l2_split[4]

        l1_gt  = l1_split[-1].split(":")[0]
        l2_gt  = l2_split[-1].split(":")[0]


        if l1_chr == l2_chr and l1_alt == l2_alt and l1_gt == l2_gt:
            outf3.write(l1)
        else:
            outf1.write(l1)
            outf2.write(l2)


    inf1.close()
    inf2.close()
    outf1.close()
    outf2.close()


def select_chr():
    pass



if __name__ == "__main__":

    input_1_PATH  = sys.argv[1]
    input_2_PATH  = sys.argv[2]
    output_1_PATH = sys.argv[3]
    output_2_PATH = sys.argv[4]
    output_3_PATH = sys.argv[5]

    sep_snp_indel_all()

    # try:
    #     select_opt = sys.argv[3]
    #     print("\nSelect chromosome %s\n" % select_opt)
    #     select_chr()
    # except:
    #     print("\nSeparate all SNP/INDEL sites\n")
    #     sep_snp_indel_all()







"""
Remove the header of the result

"""


import sys


inputPATH  = sys.argv[1]
outputPATH = sys.argv[2]


with open(inputPATH, "r") as inf:

    outf = open(outputPATH, "w")

    for l in inf:
        if l.startswith("#"):
            continue

        outf.write(l)

    outf.close()








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
