Description = """

- Information --------------------------------------------------------------------
 Name         : ProcessManager_SNP_mRNA_Pipline
 Description  : Run modules with single or multiple processes automatically
 Author       : Hwx
 Version      : V0
 Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS, Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-04-
-----------------------------------------------------------------------------------

"""

Usage = """

        Usage:

            python %s <WTS_CongfigPATH>


""" % __file__



from multiprocessing import Pool
from subprocess      import call
import time



class main:

    def __init__(self):
        pass

    def call_func(self, arg):
        call(arg, shell=True)

    def multiP(self, para_dict, call_func):

        start_t = time.time()


        p = Pool(para_dict["nProcess"])
        for i in para_dict["args"]:
            p.apply_async(call_func, args=(i,))
        p.close()
        p.join()

        total_t = time.time() - start_t
        print("Time concumed: %0.2fs" % total_t)



if __name__ == "__main__":

    # Parameter Section
    para_dict = {
        "nRun"      : None,
        "nProcess"  : None,
        "args"      : [],
    }


    # Instantiation
    main = main()


    # Execution part
    main.multiP(main.call_func)
