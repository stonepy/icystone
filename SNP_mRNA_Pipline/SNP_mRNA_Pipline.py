Description = """

_ Information ____________________________________________________________________

    Name         : main_SNP_mRNA
    Description  :
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0
    Finish Date  : 2017_04_
__________________________________________________________________________________
"""



import sys
import os


Usage = """

        Usage:

            python %s <WTS_CongfigPATH>


""" % __file__



# + Test Zone +++++++++++++++++++++++++++++++++++++++++++++++++
def test():
    try:
        # Alternative way: import packages.settings
        from packages import config_parser

        print("\nIt works...\n")

        print(config_parser.Description)

    except Exception as e:
        print(e)
        print("\nIt's not going to work...\n")


    exit()

# test()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++





# _ 1. Get WTS 'config.txt' path from command line __________________________________________________

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


# _ 2. Preparation for Pipline _____________________________________________

# Generate configs and parse them
try:
    from packages import config_producer
    from packages import config_parser
except Exception as e:
    print(">>> Warning: lack of package\n      %s\n" % e)
    print(">>> %s will be shut down right away.\n" % __file__)
    exit()

    # Parse the config Info and store in dictionary
    config_dict = config_parser.configini
    run_dict    = config_parser.runini

    # Pathes
    WTSconfig_path = sys.argv[1]
    SNPconfig_path = ""
    SNPrun_path    = ""
    SNPdata_path   = ""
    SNPreport_path = ""

# Check everything that is needed to make sure Pipline will work properly
try:
    from packages import checking
except Exception as e:
    print(">>> Warning: lack of package\n      %s\n" % e)
    print(">>> Checking function can not work properly. You can stop(Ctrl+C) this Pipline right now and fix it, or just let it be. If you lucky, everything will be fine, but you are not...Good luck!\n")





# _ Main _________________________________________





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






"""
_ Log ___________________________________________________________________________

2017-04-13
    0) Start
    1) self-package configparser
    2) Finish 'settings.py', did not test
    3) Finish package part of 'checking.py'

_________________________________________________________________________________
"""