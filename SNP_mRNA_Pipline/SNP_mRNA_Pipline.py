Description = """

_ Information ____________________________________________________________________

    Name         : main_SNP_mRNA
    Description  :
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS/Python3.5.3, virtualenv15.1.0
    Finish Date  : 2017_04_
__________________________________________________________________________________
"""

Usage = """

        Usage:

            python SNP_mRNA.py <WTS_CongfigPATH>


"""

k = "helloe world"

# + Test Zone +++++++++++++++++++++++++++++++++++++++++++++++++
def test():
    try:
        # Alternative way: import packages.settings
        from packages import checking

        print("\nIt works...\n")

        checking.mapping_STAR(k)

    except:
        print("\nIt's not going to work...\n")


    exit()

# test()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



import sys
import os

# _ Get WTS 'config.txt' path from command line __________________________________________________


try:
    # Make sure the 'config.txt' exists
    if os.path.isfile(sys.argv[1]):
        print("\nStart the SNP_mRNA Pipline immediately\n")
    else:
        print("\n>>> Error: 'config' file can't be found, make sure you use the right path.\n")
        raise

except:
    # If 'config.txt' can not be found, tell user how to use this Pipline
    print(Description)
    print(Usage)
    exit()



# _ Pathes ____________________

WTSconfig_path = sys.argv[1]
SNPconfig_path = ""
SNPrun_path    = ""
SNPdata_path   = ""
SNPreport_path = ""



# _ ALl modules needed ____


modules_dict = """

check
config_producer
excel
format

settings
config_producer

# _ need to be develop ________________
mapping

gatk
calling
library
gender
genotyping
database
annotation
analysis

report

"""



# _ Main _________________________________________











"""
_ Log ___________________________________________________________________________

2017-04-13
    0) Start
    1) self-package configparser
    2) Finish 'settings.py', did not test
    3) Finish package part of 'checking.py'

_________________________________________________________________________________
"""