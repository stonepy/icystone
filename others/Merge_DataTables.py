"""
- Information --------------------------------------------------------------------
 Name         : Merge_DataTables
 Description  : Merge two data tables on the specific column
 Formulation  : None
 Author       : Hwx
 Version      : V1
 Dev Env      : Red Hat 4.8.5-11/Ubuntu16.04 LTS, Python3.5.3, virtualenv15.1.0
 Finish Date  : 2017-03-27
-----------------------------------------------------------------------------------
"""


# System Packages
import os
import sys
import time
from subprocess import call
from multiprocessing import Pool

# Functional Packages
import pandas as pd


scriptName = "Merge_DataTables"

# Get arguments
args = sys.argv

# Check if user didn't provide valid path
try:
    path_table1      = args[1]
    path_table2      = args[2]
    dir_tableMerged  = args[3]
    column_name      = args[4]

except IndexError as e:
    print("\n>>> Error :\n    Sorry, you didn't provide enough parameters\n")
    print("\n===============================================\n[ Usage ]\n    python %s.py <Table1_path> <Table2_path> <Output_path> <Column_Name>\n===============================================\n" % scriptName)
    exit()


class main:
    def __init__(self):
        pass

    def merge(self, path_table1, path_table2, dir_tableMerged, column_name):
        df_table1, df_table2    = pd.read_table(path_table1), pd.read_table(path_table2)

        name_table1, name_table2= path_table1.split("/")[-1], path_table2.split("/")[-1]
        path_tableMerged = dir_tableMerged + "/%s_%s_Common" % (name_table1, name_table2)

        try:
            df_tableMerged = pd.merge(df_table1, df_table2, on=column_name)
            df_tableMerged.to_csv(path_tableMerged, index=None, sep="\t")
        except Exception as e:
            print(e)

        print(df_tableMerged)


# ----------------------------------------------------------------
# ----------------------------------------------------------------
class management:
    def __init__(self):
        pass

    def testFunction(self, word):

        def t():
            print(word)
            time.sleep(1)
        t()


    """
        Note:
        Apply multiple processes in different ways
            1) no arg
            2) one arg
            3) more than one arg (list)
        Usage:
        This function accepts 2 positional and 1 optional args:
            1) the name of the function
            2) the arg(s)
            3) optional, numbers of processes
    """
    def multiP(self, function_name, process_num=1, args=None):

        start_t = time.time()

        # No argumnet passed
        if args== None :
            p = Pool(process_num)
            for i in range(process_num):
                p.apply_async(function_name)
            p.close()
            p.join()

        # Only one argument passed
        elif isinstance(args, list) == False :
            p = Pool(process_num)
            for i in range(process_num):
                p.apply_async(function_name, args=(args,))
            p.close()
            p.join()

        # Mutiple arguments passed
        elif isinstance(args, list) == True:
            p = Pool(process_num)
            for i in args:
                p.apply_async(function_name, args=(i,))
            p.close()
            p.join()

        total_t = time.time() - start_t
        print("Time concumed: %0.2fs" % total_t)


    def singleP(self, **kwargs):
        start_t = time.time()




        total_t = time.time() - start_t
        print("Time concumed: %0.2fs" % total_t)



if __name__ == "__main__":

    # Parameter Section
    args_list = [path_table1, path_table2, dir_tableMerged, column_name]
    process_num = 1


    # Instantiation
    function_name = management().testFunction

    # Execution part
    management().multiP(main().merge, process_num, args_list)