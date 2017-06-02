
# _ Information ________________________________________________________________________

__Name__           = """ QC Toolkits for GPU/CPU """
__Description__    = """ GPU/CPU self-adaptive QC tools """
__Author__         = """ Hwx """
__Version__        = """ 0 """
__DevEnv__         = """ Red Hat 4.8.5-11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0 """
__FirstCreate__    = """ 2017-05-31"""
__LastModificate__ = """ 2017-05-31"""
__Notes__          = """ None """
# _ Information ________________________________________________________________________



# _ Packages ___________________________________________________________________________

import argparse
import logging
import os
import sys
import subprocess
import multiprocessing

# _ Packages ___________________________________________________________________________



# _ Arguments __________________________________________________________________________

def get_args():
    parser = argparse.ArgumentParser(description=__Description__)

    parser.add_argument("arg1", help="ThisIsThePositionalArgument1", )
    parser.add_argument("-arg2", help="ThisIsTheOptionalArgument2", default=None)
    parser.add_argument("-a3", "--arg3", help="ThisIsTheOptionalArgument3", default=None)

    args = parser.parse_args()

    sCMD = "python %s %s %s" % (__file__, args.arg1, '-arg2 ' + str(args.arg2))
    print("\n    Running command: %s\n" % sCMD)

    return args

# _ Arguments __________________________________________________________________________



# _ Main _______________________________________________________________________________

class quality_assessment:
    def __init__(self, config_dict):
        pass

class quality_control:
    def __init__(self):
        pass



# _ Main _______________________________________________________________________________



# _ Execution Control __________________________________________________________________

if __name__ == "__main__":
    args = get_args()



# _ Execution Control __________________________________________________________________





# - Log --------------------------------------------------------------------------------
Log = """

2017-06-
    1)



"""
# - Log --------------------------------------------------------------------------------