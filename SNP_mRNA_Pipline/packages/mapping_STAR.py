Description = """

_ Information ____________________________________________________________________

    Name         : mapping_STAR_SNP_mRNA
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



# Test Zone +++++++++++++++++++++++++++++++++++++++++++++++++
def test():
    try:
        # Alternative way: import packages.settings
        from packages import settings

        print("\nIt works...\n")

        print(settings.software_dict)

    except:
        print("\nIt's not going to work...\n")


    exit()

# test()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# Get WTS 'config.txt' path from command line __________________________________________________
import sys
import os

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



# Pathes ____________________

WTSconfig_path = sys.argv[1]
SNPconfig_path = ""
SNPrun_path    = ""
SNPdata_path   = ""
SNPreport_path = ""

