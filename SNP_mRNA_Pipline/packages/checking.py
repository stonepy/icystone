Description = """

_ Information ____________________________________________________________________

    Name         : Checking_SNP_mRNA
    Description  :
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS/Python3.5.3, virtualenv15.1.0
    Finish Date  : 2017-04-
__________________________________________________________________________________
"""


import os


""" _ 1. Directory Check ________________________________________________________________________________ """
def path_check(config_dict):

    rawd_dataDIR     = config_dict["section_1"]["4_"].split(" ")[-1]
    data_analysisDIR = config_dict["section_1"]["5_"].split(" ")[-1]
    reportDIR        = config_dict["section_1"]["6_"].split(" ")[-1]


    if not os.path.isdir(rawd_dataDIR):
        print("\n>>> Warning:\n      %s does not exist, creating it..." % rawd_dataDIR)
        os.makedirs(rawd_dataDIR)

    if not os.path.isdir(data_analysisDIR):
        print("\n>>> Warning:\n      %s does not exist, creating it..." % data_analysisDIR)
        os.makedirs(data_analysisDIR)

    if not os.path.isdir(reportDIR):
        print("\n>>> Warning:\n      %s does not exist, creating it..." % reportDIR)
        os.makedirs(reportDIR)


""" _ 2. Package Check ___________________________________________________________________________________ """
def package_check():
    try:
        # Alternative way: import packages.settings


        from packages import settings
        from packages import process_manager

        from packages import mapping_STAR
        # from packages import gatk
        # from packages import calling
        # from packages import library
        # from packages import gender
        # from packages import genotyping
        # from packages import database
        # from packages import annotation
        # from packages import analysis
        #
        # from packages import report
        # from packages import excel
        # from packages import format

        print("\nEverything is OK. Start running right away.\n")

    except ImportError as e:
        print(">>> Warning:\n      %s\n" % e)
        print(
            ">>> You can stop(Ctrl+C) this Pipline right now and fix it, or just let it be, but you may encounter some problems during Pipline running.\n")



def mapping_STAR():
    pass
































"""
_ Log ___________________________________________________________________________

2017-04-13
    1) Finish packages check

    2) check list
        packages
        dirs(I/O)
        soft
        database
        config

2017-04-21
    1) Add 'path_check' module,

_________________________________________________________________________________
"""