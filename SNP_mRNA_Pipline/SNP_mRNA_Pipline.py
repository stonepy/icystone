Description = """

_ Information ____________________________________________________________________

    Name         : Main_SNP_mRNA
    Description  :
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0
    Finish Date  : 2017_04_
__________________________________________________________________________________
"""



import sys
import os
import time

Usage = """

        Usage:

            python %s <WTS_CongfigPATH>


""" % __file__



# + Test Zone +++++++++++++++++++++++++++++++++++++++++++++++++
def test():
    try:
        from packages import config_processor

        print("\nIt works...\n")
        exit()


    except Exception as e:
        print(e)
        print("\nIt's not going to work...\n")


    exit()

# test()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# _ 1. Preparation for Pipline __________________________________________________________________________
class preparation:

    def __init__(self):
        pass

    # Get WTS 'config.txt' path from command line
    def get_args(self):
        try:
            # Make sure the 'config.txt' exists
            if os.path.isfile(sys.argv[1]):
                self.WTSconfig_path = sys.argv[1]

            else:
                print("\n>>> Error: 'config' file can't be found, make sure you use the right path.\n")
                raise

        except:
            # If 'config.txt' can not be found, tell user how to use this Pipline
            print(Description)
            print(Usage)
            exit()

    # Generate configs and parse them
    def config(self):
        try:
            from packages import config_processor
            # Parse the config Info and store in dictionary
            WTS_cfg_dict, SNPoutput_dir = config_processor.WTS_cfg(self.WTSconfig_path)
            config_dict = config_processor.configini(WTS_cfg_dict, SNPoutput_dir)
            run_dict    = config_processor.runini(WTS_cfg_dict, SNPoutput_dir)

        except Exception as e:
            print(">>> Warning: lack of package\n      %s\n" % e)
            print(">>> SNP_mRNA_Pipline will be shut down right away.\n")
            exit()
        return config_dict, run_dict

    # Check everything that is needed to make sure Pipline will work properly
    def check(self):
        try:
            print("\nChecking the necessary packages and other items before running...\n")
            from packages import checking

        except Exception as e:
            print(">>> Warning:\n      %s\n" % e)
            print(">>> Encounter some problems as above while checking. You can stop(Ctrl+C) this Pipline right now and fix it, or just let it be. If you lucky, everything will be fine, but you are not...Good luck!\n")





# _ 2. Main _________________________________________
class main(preparation):

    def __init__(self, config_dict, run_dict):
        self.config_dict = config_dict
        self.run_dict    = run_dict



# _ Exxcution Control ________________________________
if __name__ == "__main__":

    t_start = time.time()

    note_0 = """

                      **************************************
                      *                                    *
                      *  Lauching the SNP_mRNA Pipline...  *
                      *                                    *
                      **************************************


%s
    """ % time.ctime()
    print(note_0)




    try:
        prep = preparation()       # Comment this line to skip whole preparation then test the Pipline manually

        prep.get_args()
        config_dict, run_dict = prep.config()
        prep.check()
    except Exception as e:
        print("\nPreparation of Pipline is Skipped or there is something wrong with it.\n")
        print("%s\n" % e)



    try:
        main = main(config_dict, run_dict)       # Comment this line to shut whole Pipline function down and test the Preparation part
        print("\nSNP_mRNA Pipline is running...\n")

    except Exception as e:
        print("\nMain workflow is going wrong...\n")
        print("%s\n" % e)




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

2017-04-15
    1) Finish 'Config_porcessor.py', tested
    2) Add class to the main script
    *3) Passing parameters between classes issue

2017-04-16
    1)


_________________________________________________________________________________
"""
