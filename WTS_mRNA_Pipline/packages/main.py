Info = """

_ Information ____________________________________________________________________

    Name         : Main__Whole_Transcriptome_Sequencing_Pipline
    Description  : For Whole_Transcriptome_Sequencing analysis
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0
    Finish Date  : 2017_05_
__________________________________________________________________________________
"""



import sys
import os
import time



Usage = """

        Usage:

            python %s <WTS_CongfigPATH>


""" % __file__



""" _ 1. Preparation for Pipline ___________________________________________________________________________________ """
class preparation:

    def __init__(self):
        # Start Note
        self.note_start = """

               ---------------------------------------
===============     Lauching the WTS_mRNA Pipline     ===============
               ---------------------------------------
                    [ %s ]\n
          """ % time.ctime()

        # Running Note
        self.note_running = """
                -------------------------------------
================     WTS_mRNA Pipline is running     ================
                -------------------------------------
                    [ %s ]\n
          """ % time.ctime()

        # Finish note
        self.note_finish = """

                  ---------------------------------
==================    WTS_mRNA Pipline finished    ==================
                  ---------------------------------
                    [ %s ]\n
          """ % time.ctime()


    # 1) Get WTS 'config.txt' path from command line
    def get_args(self):
        try:
            # Make sure the 'config.txt' exists
            if os.path.isfile(sys.argv[1]):
                self.WTSconfig_path = sys.argv[1]

            else:
                print("\n>>> Error: 'config.txt' file can't be found, make sure you use the right path.\n")
                raise

        except:
            # If 'config.txt' can not be found, tell user how to use this Pipline
            print(Info)
            print(Usage)

            exit()


    # 2) Generate configs and parse them
    def config(self):
        try:
            from Packages import config_processor

            # Parse the config Info, then store in a dictionary
            self.WTS_cfg_dict = config_processor.WTS_cfg(self.WTSconfig_path)
            # time.sleep(0.5)

            print("\n\n")
            return self.WTS_cfg_dict

        except Exception as e:
            print(">>> Something goes wrong, when parsing 'config':\n      %s\n" % e)
            print(">>> WTS_mRNA_Pipline is shutting down.\n")

            exit()


    # 3) Check everything that is needed to make sure Pipline will work properly
    def check(self):
        try:
            print("\nChecking the necessary packages and other items before running...\n")
            from Packages import checking
            checking.baseDIR_check(self.WTS_cfg_dict)    # Check 'raw_data','data_analysis' and 'report' directory
            checking.package_check()

        except Exception as e:
            print(">>> Warning:\n      %s\n" % e)
            print(">>> Encounter some problems as above while checking. You can stop(Ctrl+C) this Pipline right now and fix it, or just let it be. If you lucky, everything will be fine, but you are not...Good luck!\n")


    def timer(self, t_start):
        t_finish = time.time()  # Finish time
        total_time = t_finish - t_start  # Total time
        # Convert second to minute, hour and day.
        day = total_time // (3600 * 24)
        hour = total_time // (3600) % 24
        minute = total_time / 60 % 60
        second = total_time % (60)

        return day, hour, minute, second, total_time



""" _ 2. Main ______________________________________________________________________________________________________ """
class workflow(preparation):

    def __init__(self, WTS_cfg_dict):
        self.WTS_cfg_dict  = WTS_cfg_dict

    # def mapping(self):
    #     from Packages import mapping_STAR
    #     mapping_STAR.main(self.config_dict)






""" Test Zone +++++++++++++++++++++++++++++++++++++++++++++++++++ """
def test(main,config_dict, run_dict):
    try:
        main = main(config_dict, run_dict)      # Comment this line to shut whole Pipline function down and test the workflow
        main.mapping()
        exit()

    except Exception as e:
        print(e)
        print("\nIt's not going to work...\n")

    exit()

# test(main,config_dict, run_dict)
""" ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ """


""" Don't use this block while testing (Excution control)"""
# try:
#     prep = preparation()       # Comment this line to skip whole preparation then test the Pipline manually
#
#     prep.get_args()
#     config_dict, run_dict = prep.config()
#     prep.check()
#
# except Exception as e:
#     print("\nPreparation of Pipline is Skipped or there is something wrong with it.\n")
#     print("%s\n" % e)

# try:
#     print("\nWTS_mRNA Pipline is running...\n")
#     main = main(config_dict, run_dict)      # Comment this line to shut whole Pipline function down and test the workflow
#
#     # main.mapping()
#     main.gatk()
#
#
# except Exception as e:
#     print("\n>>> Error: Main workflow goes wrong...\n")
#     print("    %s\n" % e)



""" _ END __________________________________________________________________________________________________________ """



# _ ALl modules needed ________________
modules_dict = """

_ need to be developed ________________

"""


"""
_ Log ___________________________________________________________________________

2017-05-12
    1) Start Today
    2) Revised from 'SNP_mRNA_Pipline.py'

_________________________________________________________________________________
"""
