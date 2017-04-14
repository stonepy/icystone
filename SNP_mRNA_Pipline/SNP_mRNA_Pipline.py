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









# _ 1. Get WTS 'config.txt' path from command line __________________________________________________

try:
    # Make sure the 'config.txt' exists
    if os.path.isfile(sys.argv[1]):
        print("\nLauching the SNP_mRNA Pipline...\n")
        WTSconfig_path = sys.argv[1]

    else:
        print("\n>>> Error: 'config' file can't be found, make sure you use the right path.\n")
        raise

except:
    # If 'config.txt' can not be found, tell user how to use this Pipline
    print(Description)
    print(Usage)
    exit()


# + Test Zone +++++++++++++++++++++++++++++++++++++++++++++++++
def test():
    try:
        from packages import config_processor
        config_processor.WTS_cfg(WTSconfig_path)
        config_dict = config_processor.configini()
        # run_dict = config_processor.runini(WTSconfig_path)
        print(config_dict)

        # print(config_dict,run_dict)

        print("\nIt works...\n")
        exit()


    except Exception as e:
        print(e)
        print("\nIt's not going to work...\n")


    exit()

test()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++





# _ 2. Preparation for Pipline _____________________________________________

# Generate configs and parse them
try:
    from packages import config_processor

except Exception as e:
    print(">>> Warning: lack of package\n      %s\n" % e)
    print(">>> SNP_mRNA_Pipline will be shut down right away.\n")
    exit()

    # Parse the config Info and store in dictionary
    config_dict = config_processor.configini(WTSconfig_path)
    run_dict    = config_processor.runini(WTSconfig_path)
    print(config_dict, run_dict)

    # Pathes
    # WTSconfig_path = sys.argv[1]
    # SNPconfig_path = ""
    # SNPrun_path    = ""
    # SNPdata_path   = ""
    # SNPreport_path = ""

# Check everything that is needed to make sure Pipline will work properly
try:
    print("\nChecking the necessary packages and other necessary items before running...\n")
    from packages import checking

except Exception as e:
    print(">>> Warning: lack of package\n      %s\n" % e)
    print(">>> Checking function can not work properly. You can stop(Ctrl+C) this Pipline right now and fix it, or just let it be. If you lucky, everything will be fine, but you are not...Good luck!\n")





# _ 3. Main _________________________________________





# _ ALl modules needed ____


modules_dict = """

settings
config_producer

# _ need to be develop ________________
check

config_parser
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
excel
format

"""






"""
_ Log ___________________________________________________________________________

2017-04-13
    0) Start
    1) self-package configparser, to read
    2) Finish 'settings.py', not test
    3) Finish package part of 'checking.py'

2017-04-14
    1) Finish '2.Preparation', tested


_________________________________________________________________________________
"""