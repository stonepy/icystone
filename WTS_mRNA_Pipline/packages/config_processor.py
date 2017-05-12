Info = """

_ Information ____________________________________________________________________
 Name         : ConfigProcessor_WTS_mRNA
 Description  : Produce 'config.ini' and 'run.ini' for
                Whole Transcription Sequecing(WTS) mRNA SNP pipline,
                using WTS pipline's 'config.txt'
 Author       : Hwx
 Version      : V4
 Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS/Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-04-15
___________________________________________________________________________________

"""


import os
import re

from os.path import join as pjoin



# _ 1. Process the WTS config and get Info ___________________________________
def WTS_cfg(WTS_cfg_path):
    with open(WTS_cfg_path, "r") as WTS_config:

        WTS_cfg_dict = {
            "project_dir": "",
            "data_analysis_dir" : "",
            "report_dir": "",
            "raw_data_dir": "",
            "species": "",
            "sample": [],
            "group": [],
        }


        print("\n  ============= Config Info =============\n")
        # Get WTS config information and store in dictionary 'WTS_cfg_dict'
        for l in WTS_config:

            # 1. Project, Data_analysis, Report and Raw_data path
            if l.lower().strip().startswith("project"):
                WTS_cfg_dict["project_dir"] = l.split("=")[-1].strip()
                WTS_cfg_dict["data_analysis_dir"] = pjoin(l.split("=")[-1].strip(), "Data_analysis")
                WTS_cfg_dict["report_dir"]  = pjoin(l.split("=")[-1].strip(), "Report")

            elif l.lower().strip().startswith("raw_data"):
                WTS_cfg_dict["raw_data_dir"] = l.split("=")[-1].strip()

            # 2. Species
            elif l.lower().strip().startswith("species"):
                WTS_cfg_dict["species"] = l.split("=")[-1].strip()

            # 3. Sample
            elif l.lower().strip().startswith("sample"):
                sample_all = re.split("[ ,;:]", l.split("=")[-1].strip())
                for i in sample_all:
                    if len(i) > 1:
                        WTS_cfg_dict["sample"].append(i)

            # 4. Group
            elif l.lower().strip().startswith("group"):
                WTS_cfg_dict["group"].append(l.strip())

            else:
                continue

            print(l)
        print("  ============= =========== =============\n")

    return WTS_cfg_dict





__Example__ = """

1. ====== Path =========

    Project  = /home/hwx/Development/WTS_mRNA_Hwx/WTS_mRNA_Pipline/
    Raw_data = /home/hwx/Development/WTS_mRNA_Hwx/WTS_mRNA_Pipline/raw_data

2. ====== Species ======

    Species = human

3. ====== Sample =======

    Sample = TWJRS_test , TWJRX_test

4. ====== Group ========

    Group_1 = TWJRS_test ; TWJRX_test



# __ Note ____________________________________________________________________________________________________

# You must not change any character prior to the equal sign, except for 'Group' option.
#
# 1) Sample note
#   If 'Sample' option is empty, Pipline will use all samples in 'Raw_data' directory.
#   You can seperate samples with characters including(" ", ",", ";", ":") -> (space, comma, semicolon, colon).
#
# 2) Group note
#   Group information, example as below:
#     "Group Name : Control sample 1, Control sample 2, ... ; Case sample 1, Case sample 2, ..."
#
#   No quotation mark is needed, but space and tab seperation are both OK.
#   'Group' name must start with 'Group' or 'group', or it will not be recognized.

"""



"""
_ Log _____________________________________________________________________________

2017-04-14
    1) Revised argument input part

2017-04-15
    1) Split name and value in 'WTS_cfg' part

___________________________________________________________________________________

"""
