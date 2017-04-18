###########################################################
# Author  : Hwx                                           #
# Date    : 2016-12-26                                    #
# Name    : mRNA_Expression_merge                         #
# Version : v1                                            #
# Description : Merge multiple data sheetspreed spread in #
# a serie folders                                         #
###########################################################


import os
import pandas as pd
import time



def merge():
    # Path and parameters
    dirs     = "/home/hwx/work/RNA_seq/mRNA_16AABV004_20161222/data_analysis/cufflinks/cuffnorm"
    filename = "genes.count_table"
    keyword  = "tracking_id"
	usecol   = [:]

    # List all folders containing filenams need to be merged
    dir_list = os.listdir(dirs)
    # Control parameters
    df_set = pd.DataFrame()
    n = 0

    # Start merging one by one
    for dir in dir_list:

        try:
            # Generate corresponding file path
            file_path = os.path.join(dirs, dir, filename)
            print "File path : %s" %file_path

            # Read file
            df_tmp = pd.read_csv(file_path, usecol=usecol, sep="\t")
            if len(df_set) == 0:
                df_set = df_tmp
                print "Finish merging {} : {}\n".format(n, file_path)
                continue

            # Merge counter
            n += 1

            # -{ Core Step }- : Merge files
            df_set = pd.merge(df_set, df_tmp, on=keyword)

            print "Finish merging {} : {}\n".format(n, file_path)
            time.sleep(0.5)

        except IOError as e:
            print "There might be some problem :", e
            dir_list.remove(dir)
            time.sleep(0.5)
            continue

    # Output merged file
    df_set.to_csv(os.path.join(dirs, "diff_agreggation.xls"), index=None, sep="\t")

    print "Merged files : {}".format(dir_list)


if __name__ == "__main__":
    merge()
