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

# Get config parameters from main script



def mapping_STAR():
    pass




















# _ Checking ___________________________________________________________________________________

try:
    # Alternative way: import packages.settings


    from packages import settings

    from packages import mapping_STAR
    from packages import gatk
    from packages import calling
    from packages import library
    from packages import gender
    from packages import genotyping
    from packages import database
    from packages import annotation
    from packages import analysis

    from packages import report
    from packages import excel
    from packages import format

    print("\nEverything is OK. Start running right away.\n")

except ImportError as e:
    print(">>> Warning: lack of package\n      %s\n" % e)
    print(">>> You can stop(Ctrl+C) this Pipline right now and fix it, or just let it be, but you may encounter some problems during Pipline running.\n")















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

_________________________________________________________________________________
"""