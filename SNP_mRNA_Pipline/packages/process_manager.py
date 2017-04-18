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
import time





def call_func(CMD):
    print("\nExecuting command: %s\n" % CMD)
    call(CMD, shell=True)

def multiP(para_dict, call_func):

    start_t = time.time()


    P = Pool(para_dict["nProcess"])

    for i in para_dict["CMDs"]:
        P.apply_async(call_func, args=(i,))
    P.close()
    P.join()


    total_t = time.time() - start_t
    print("Time concumed: %0.2fs" % total_t)



# Execution part
# multiP(para_dict, call_func)





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
_________________________________________________________________________________
"""