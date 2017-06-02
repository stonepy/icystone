
# _ Information ________________________________________________________________________

__Name__           = """ GTF_GFF_mutualConversion """
__Description__    = """ \n Use this tool for converting GTF and GFF mutually  \n """
__Author__         = """ Hwx """
__Version__        = """ 0 """
__DevEnv__         = """ Red Hat 4.8.5-11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0 """
__FirstCreate__    = """ 2017-05-31"""
__LastModificate__ = """ 2017-05-31"""
__Notes__          = """ None """
# _ Information ________________________________________________________________________



# _ Packages ___________________________________________________________________________

import argparse     # Reference of 'Argparse': https://docs.python.org.tw/3/howto/argparse.html
import logging
import re
import os
import sys
import time
import subprocess
import multiprocessing

import pandas as pd

# _ Packages ___________________________________________________________________________



# _ Arguments __________________________________________________________________________


def get_args():

    parser = argparse.ArgumentParser(description=__Description__)

    parser.add_argument("GTF_PATH", help="GTF file path")
    parser.add_argument("GFF_PATH", help="GFF file path")
    parser.add_argument("-t", "--gtf2gff", help="Convert GTF to GFF", action="store_true", default=True)
    parser.add_argument("-f", "--gff2gtf", help="Convert GFF to GTF", action="store_true", default=False)

    args = parser.parse_args()

    return args

# _ Arguments __________________________________________________________________________



# _ Main _______________________________________________________________________________

class gtf2gff:

    def __init__(self):
        pass


    def convertor(self, gtf_PATH, gff_PATH):
        print("\n\tConverting GTF to GFF ...\n")

        with open(gff_PATH, "w") as gff:
            gtf = open(gtf_PATH, "r")

            for l in gtf:
                if l.startswith("#"):
                    gff.write(l)
                    continue

                l_spl = l.split("\t")

                gff.write(l)

            gtf.close()

        print("\tFinish GTF to GFF conversion.\n")








class gff2gtf:

    def __init__(self):
        pass


    def convertor(self, gff_PATH, gtf_PATH):
        print("\n\tConverting GFF to GTF ...\n")

        with open(gtf_PATH, "w") as gtf:
            gff = open(gff_PATH, "r")

            for l in gff:
                if l.startswith("#"):
                    gtf.write(l)
                    continue

                l_spl = re.split("[ \t]", l)

                gtf.write()

            gff.close()

        print("\tFinish GFF to GTF conversion.\n")



# _ Main _______________________________________________________________________________



# _ Execution Control __________________________________________________________________

if __name__ == "__main__":

    args = get_args()
    gtf2gff = gtf2gff()
    gff2gtf = gff2gtf()


    s = time.time()
    if args.gff2gtf == True:
        gff2gtf.convertor(args.GFF_PATH, args.GTF_PATH)

    else:
        gtf2gff.convertor(args.GTF_PATH, args.GFF_PATH)
    e = time.time()
    print(e-s)






# _ Execution Control __________________________________________________________________





# - Log --------------------------------------------------------------------------------
Log = """

2017-06-01
    1) Start this script



"""
# - Log --------------------------------------------------------------------------------