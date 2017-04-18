#!/usr/local/bin/python
###########################################################
# Author  : Hwx                                           #
# Date    : 2016-12-20                                    #
# Name    : HTSeq-count_maSigPro                          #
# Version : v1(Untested)                                  #
# Description : mRNA count and Time Series Analysis       #
###########################################################



import os
import sys
import time
import signal
import multiprocessing as mp
import subprocess as sp
import pandas as pd


class fun:
    def __init__(self):


        # Paths Dictionary : all dirs included
        self.dir = {
            "Project"           : "",
            "BAM_Store"         : "/home/hwx/work/RNA_seq/mRNA_16AABV004_20161222/data_analysis",
            "htCount_Store"     : "/home/hwx/work/RNA_seq/mRNA_16AABV004_20161222/data_analysis/htseq_count",
            "maSigPro_Store"    : "/home/hwx/work/RNA_seq/mRNA_16AABV004_20161222/data_analysis/maSigPro",
            "maSigPro_Report"   : "/home/hwx/work/RNA_seq/mRNA_16AABV004_20161222/data_analysis/maSigPro",
            "Genome_GTF"        : "/home/pub/database/Mouse/mm10/genes.gtf",
            "Group_Info"        : "/home/hwx/work/RNA_seq/mRNA_16AABV004_20161222/work_path/group_TSE.txt",
        }

        ################################################################################################################

        # Part 1) : Deal with group information input

        # Obtain group information from group.txt
        with open(self.dir["Group_Info"], "r") as g:
            # Build a Dict to store information
            group_dict = {
                "group_1":    [],
                "group_2":    [],
                "G1_samples": [],
                "G2_samples": [],
                "Time_point": [],
            }

            # Split the information and assign them into dict
            for l in g:
                ctrl_lab, case_lab, samples, time_p = l.split(" ")[0], l.split(" ")[1], l.split(" ")[2], l.split(" ")[3]
                ctrl_smps, case_smps = samples.split(";")[0], samples.split(";")[1]
                # Assign information
                group_dict["group_1"].append(ctrl_lab)
                group_dict["group_2"].append(case_lab)
                group_dict["G1_samples"].append(ctrl_smps)
                group_dict["G2_samples"].append(case_smps)
                group_dict["Time_point"].append(time_p.strip())

        # Transform group_dict into DataFrame
        df_group = pd.DataFrame(group_dict, columns=["group_1", "group_2", "G1_samples", "G2_samples", "Time_point"])

        ################################################################################################################

        TSE_path = {
		"edesign"	:	"/home/hwx/work/RNA_seq/mRNA_16AABV004_20161222/data_analysis/maSigPro/edesign",
		"countData"	:	"/home/hwx/work/RNA_seq/mRNA_16AABV004_20161222/data_analysis/maSigPro/countData",
		"htCount"	:	"/home/hwx/work/RNA_seq/mRNA_16AABV004_20161222/data_analysis/cufflinks/cuffnorm/cufflinks_count"
		}
        # Part 2) : Generate edesign

        # Dict for edesign data
        edesign_dict = {
            "Sample"    : [],
            "Time"      : [],
            "Replicate" : [],
            "Control"   : [],
            "Case"      : [],
        }

        # Transform df_group into edesign_dict
        replicate = 0
        # Obtain Group_1 samples
        for idx, row in df_group.iterrows():
            # Distinguish different subgroups
            replicate += 1

            # Obtain Group_1 correlated information
            for samp in row["G1_samples"].split(","):
                edesign_dict["Sample"].append(samp)
                edesign_dict["Time"].append(row["Time_point"])
                edesign_dict["Replicate"].append(replicate)
                edesign_dict["Control"].append(1)
                edesign_dict["Case"].append(0)

        # Obtain Group_2 samples
        for idx, row in df_group.iterrows():
            # Distinguish different subgroups
            replicate += 1

            # Obtain Group_1 correlated information
            for samp in row["G2_samples"].split(","):
                edesign_dict["Sample"].append(samp)
                edesign_dict["Time"].append(row["Time_point"])
                edesign_dict["Replicate"].append(replicate)
                edesign_dict["Control"].append(0)
                edesign_dict["Case"].append(1)

        # Transform edesign_dict into DataFrame
        df_edesign = pd.DataFrame(edesign_dict, columns=["Sample", "Time", "Replicate", "Control", "Case"]).set_index(keys="Sample")
        print df_edesign

        # Output edesign
        df_edesign.to_csv(TSE_path["edesign"], index_label=False, header=True, sep="\t")

        ################################################################################################################

        # Part 3) : Generate counts_data sheet

        df_CountSet = ""
        #
        for samp in df_edesign.index.values:
            htCount = os.path.join(TSE_path["htCount"], samp + ".htCount")
            # Read the first counts_data sheet
            if len(df_CountSet) == 0:
                df_CountSet = pd.read_csv(htCount, names=["Gene", samp], sep="\t")
            # Read the reast of counts_data sheets and merge all sheets
            else:
                df_CountTmp = pd.read_csv(htCount, names=["Gene", samp], sep="\t")
                # Merge latest sheet into aggregated one
                df_CountSet = pd.merge(df_CountSet, df_CountTmp, on="Gene")

        # Clean data and assign index
        df_CountData = df_CountSet[0:-5].set_index(keys="Gene")
        # Output counts_data sheet
        df_CountData.to_csv(TSE_path["countData"], index_label=False, sep="\t")

        ################################################################################################################

        # Part 4) : Run maSigPro

        # Generate maSigPro.R script
        with open(TSE_path["maSigPro_R"], "w+") as maSigPro_Rscript:

            # Get degree of the experiment
            degree = len(group_dict["Time_point"])

            # Write the Rscrpt
            maSigPro_Rscript.write(
                """
                library(maSigPro)

                # Path of data and edesign
                countData_path    = %s/countData.csv
                countEdesign_path = %s/countEdesign.csv

                # Read in data and edesign
                countData    = read.csv(countData_path, sep = "\t")
                countEdesign = read.csv(countEdesign_path, sep = "\t")

                #
                design = make.design.matrix(countEdesign, degree = %d)

                # Finding significant genes
                pVector = p.vector(countData, design, Q = 0.05, MT.adjust = "BH", counts = TRUE, family = poisson())

                # Finding significant differences
                Tfit = T.fit(pVector, alfa = 0.05)

                # Obtaining lists of significant genes
                sigs = get.siggenes(Tfit, rsq = 0.6, vars="groups")

                # PDF
                pdf(%s)

                # Visualization
                see.genes(sigs$sig.genes$CasevsControl, show.fit = T, dis = design$dis, cluster.method = "hclust", cluster.data = 1, newX11 = FALSE, k = 9)
                dev.off()
                """ % (TSE_path["countData"], TSE_path["edesign"], degree, TSE_path["maSigPro_pdf"])
            )

        # Generate running command
        cmd = "Rscript %s" %self.TSE_path["maSigPro_R"]
        return cmd



        ################################################################################################################



#############################
if __name__ == "__main__":
    f = fun()
    maSigPro_cmd = f.maSigPro_cmds()




