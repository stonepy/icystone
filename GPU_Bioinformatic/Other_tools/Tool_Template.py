
# _ Information ________________________________________________________________________

__Name__           = """ Tool Template """
__Description__    = """ \n This is the Demo !!! Developed in Python3 \n """
__Author__         = """ Hwx """
__Version__        = """ 0 """
__DevEnv__         = """ Red Hat 4.8.5-11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0 """
__FirstCreate__    = """ 2017-05-31"""
__LastModificate__ = """ 2017-05-31"""
__Notes__          = """ None """
# _ Information ________________________________________________________________ End ___



# _ Packages ___________________________________________________________________________

import argparse
import logging
import os
import sys
import subprocess
import multiprocessing

# _ Packages ___________________________________________________________________ End ___



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

# _ Arguments __________________________________________________________________ End ___



# // Main //////////////////////////////////////////////////////////////////////////////

class model:

    def __init__(self):
        pass



# // Main ////////////////////////////////////////////////////////////////////// End ///



# _ Execution Control __________________________________________________________________

if __name__ == "__main__":
    args = get_args()



# _ Execution Control __________________________________________________________ End ___





# - Log --------------------------------------------------------------------------------
Log = """

2017-06-
    1)



"""
# - Log ------------------------------------------------------------------------ End ---