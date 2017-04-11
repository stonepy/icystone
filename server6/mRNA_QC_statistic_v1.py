#!/usr/local/bin/python
###########################################################
# Author  : Hwx                                           #
# Date    : 2016-12-02                                    #
# Name    : mRNA_QC_statistic                             #
# Version : v1                                            #
# Description : Merge seqs QC before and after triming    #
###########################################################



import pandas as pd
import sys

class fun:

    def __init__(self):

        if len(sys.argv) < 2:

            print ""
            print "Usage:"
            print "     Command:   'python <read_length_path> <quality_control_path> <QC_output_dir>'"
            print ""

            sys.exit()

        self.raw_QC_path    = sys.argv[1]
        self.trimed_QC_path = sys.argv[2]
        self.output_path    = sys.argv[3]

    def run(self):

        cols_readIn   = ["sample", "Total_reads", "Total_bases"]
        cols_writeOut = ["sample", "Raw_reads", "Raw_bases", "Trimed_reads", "Trimed_bases"]

        read_length     = pd.read_csv(self.raw_QC_path, sep="\t", usecols=cols_readIn)
        quality_control = pd.read_csv(self.trimed_QC_path, sep="\t", usecols=cols_readIn)

        df = pd.merge(read_length, quality_control, on="sample")
        df.columns = cols_writeOut

        df.to_csv(self.output_path+"/"+"mRNA_QC.xls", sep="\t", index=None)
        print df


if __name__ == "__main__":
    fun().run()
