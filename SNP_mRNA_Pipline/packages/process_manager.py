Description = """

- Information --------------------------------------------------------------------
 Name         : ProcessManager_SNP_mRNA_Pipline
 Description  : Run modules with single or multiple processes automatically
 Author       : Hwx
 Version      : V0
 Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS, Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-04-18
-----------------------------------------------------------------------------------

"""

Usage = """

        Usage:

            python %s <WTS_CongfigPATH>


""" % __file__



from multiprocessing import Pool
from subprocess      import call
import signal
import time
import sys



def call_func(CMD):
    print("\nExecuting command:\n[>>>] %s\n" % CMD)
    call(CMD, shell=True)

# Temporary for testing, 2017-04-25
def ctrlC():
    while 1 != 0:
        try:
            pass
        except KeyboardInterrupt:
            sys.exit()


def multiP_1(para_dict, func):

    start_t = time.time()


    P = Pool(para_dict["nProcess"])

    for i in para_dict["CMDs"]:
        P.apply_async(func, args=(i,))
    # P.apply_async(ctrlC)        # Temporary for testing, 2017-04-25
    P.close()
    P.join()


    total_t = time.time() - start_t
    print("Time consumed: %0.2fs" % total_t)






""" _ Test Module ___________________________________________________________________________________________

# Need to rebuild a class to use this module to test
if __name__ == "__main__":

    # Parameter dictionary
    para_dict = {
        "nRun"      : 4,
        "nProcess"  : 4,
        "CMDs"      : ["python python_s1.py", "python python_s2.py", "python python_s3.py", "python python_s4.py"]
    }

    # Instantiation
    call_func = main().call_func

    # Execution part
    main().multiP(para_dict, call_func)     # Must not use 'main = main()', I don't know why, but it works.

"""

"""
_ Log ___________________________________________________________________________

2017-04-18
    1) Revised from 'Script_Framework_v1.py', tested as individual script
    2) Multiple processes or single process are both OK
    3) Use dictionary to pass parameter only!

2017-04-21
    1) With 'mapping_STAR.py' locally, tested

2017-04-24
    1) Multiple processes can't be terminated by 'Ctrl+C' normally

2017-04-25
    1) 
_________________________________________________________________________________
"""
