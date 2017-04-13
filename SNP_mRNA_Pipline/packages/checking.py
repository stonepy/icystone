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



# _ Checking _________________________________________
print("\nChecking the necessary packages and other items before running...\n")
try:
    # Alternative way: import packages.settings
    from packages import settings
    from packages import config_producer
    from packages import excel
    from packages import format
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

    print("\nEverything is OK. Start running right away.\n")

except ImportError as e:
    print(">>> Warning: Lack of package\n    %s\n" % e)
    print(">>> You can stop this Pipline right now and fix it, or just let it be...\n")



