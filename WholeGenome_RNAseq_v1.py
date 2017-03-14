"""
- Information --------------------------------------------------------------------
 Name         :   mRNA-seq-QC
 Description  :   For mRNA-seq sample quality assess and control. Consist of
                  these parts:
 Author       :   Hwx
 Version      :   V1
 Dev Env      :   Red Hat 4.8.5-11, Python3.5.3, virtualenv15.1.0
 Finish Date  :   2017-01-2
-----------------------------------------------------------------------------------
"""

"""
                  ---------------- Pipline starts Here ----------------
"""

"""-- Packages --------------------------------------------------------------------"""

# Import required packages
try:

    import os
    import time
    import sys
    import shutil
    import subprocess
    import multiprocessing
    import argparse
    import warnings
    import logging

    import pandas as pd

# Warn when importing encounters problems
except ImportError as e:
    print(">>> Warning :\n    There is something wrong with importing packages : %s\n" % e)

"""-- Main ------------------------------------------------------------------------"""


class Quality_Control:
    """-- Preprocess -------------------------------------------------------"""

    def __init__(self):

        print(
            "\n\n====================================== Start mRNA_QC Pipline ======================================\n\n")

        # Waiting time
        self.timeout = 0.5

        # Arguments input
        args = sys.argv

        # Base Directory
        self.info_userSet = {

            "Project": "tmp",
            "dir_WorkPath": "tmp",
            "dir_RawData": "/home/hwx/tmp/rawData/16B0620C",
            "dir_Result": "/home/hwx/tmp/Analysis",
            "dir_Report": "/home/hwx/tmp/Report",
            "species": "human",
        }

        # Reference information
        self.info_reference = {

            "path_human_hisat2_db": "/home/hwx/reference/hg19_hisat2_db/hg19",
            "path_mouse_hisat2_db": "/home/hwx/reference/mm10_hisat2_db/mm10",
            "path_mouse_gencode": "/home/hwx/reference/gencode/gencode.vM12.annotation.gtf",
        }

        # Python compiler information
        self.info_Python = {

            "version": "Python3.5.3",
            "path_bin": "/home/hwx/virtualenvironment/VE_python3/bin/python",
            "arguments": "vp3",
        }

        # R compiler information
        self.info_R = {

            "version": "R version 3.2.1 (2015-06-18)",
            "path_bin": "/usr/bin/R",
            "path_Rscript": "/usr/bin/Rscript",
            "arguments": "",
        }

        # Java compiler information
        self.info_Java = {

            "version": "openjdk version 1.8.0_91",
            "path_bin": "/usr/local/bin/java",
            "arguments": "-jar",
        }

        # Path of used softwares
        self.path_softwares = {

            "Python": "~/virtualenvironment/VE_python3/bin/python",
            "R": "",
            "Java": "/usr/local/bin/java",
            "FastQC": "/home/hwx/software/FastQC-v0.11.5/fastqc",
            "fastx_toolkit": "/home/hwx/software/fastx_toolkit-0.0.14/src/",
            "seq_crumbs": "/home/hwx/software/seq_crumbs-0.1.9/bin/",
            "seq_crumbs-calculate_stats": "/home/hwx/software/seq_crumbs-0.1.9/bin/calculate_stats",
            "iTools": "/home/hwx/software/iTools_Code/iTools",
            "iTools-Fqtools-stat": "/home/hwx/software/iTools_Code/iTools Fqtools stat",
            "Trim_Galore": "/home/hwx/software/Trim_Galore_0.4.2/trim_galore",
            "HISAT2": "/home/hwx/software/HISAT2-2.0.5/hisat2",
            "Samtools": "/home/hwx/software/samtools-1.3.1/samtools",
            "Picard": "/home/hwx/software/picard.jar",
            "RNA_SeQC": "/home/hwx/software/RNA-SeQC_v1.1.8.jar",
        }

        # Path of each module results
        self.path_results = {

            "FastQC": self.info_userSet["dir_Result"] + "/FastQC",
            "iTools_Fqtools": self.info_userSet["dir_Result"] + "/iTools_Fqtools",
            "Trim_Galore": self.info_userSet["dir_Result"] + "/Trim_Galore",
            "HISAT2": self.info_userSet["dir_Result"] + "/HISAT2",
        }

        # Path of each module reports
        self.path_reports = {

            "Quality_Control_I": self.info_userSet["dir_Report"] + "/Quality_Control_I",
            "Alignment": self.info_userSet["dir_Report"] + "/Alignment",

            "FastQC": self.info_userSet["dir_Report"] + "/Quality_Control_I/FastQC",
            "iTools_Fqtools": self.info_userSet["dir_Report"] + "/Quality_Control_I/iTools_Fqtools",
            "Trim_Galore": self.info_userSet["dir_Report"] + "/Quality_Control_I/Trim_Galore",
            "HISAT2": self.info_userSet["dir_Report"] + "/Alignment/HISAT2",
        }

        # Check [Analysis] directory
        try:

            # Try to create the directory
            print("\n|- Create '%s' directory" % self.info_userSet["dir_Result"])
            os.mkdir(self.info_userSet["dir_Result"])

        # If directory exists, remove old files and recreate directory
        except Exception as e:
            print(
                "\n>>> Warning :\n    Directory '%s' already exists,\n    Indicate this project may has been run before.\n" %
                self.info_userSet["dir_Result"])

        # Check [Report] directory
        try:

            # Try to create the directory
            print("\n|- Create '%s' directory" % self.info_userSet["dir_Report"])
            os.mkdir(self.info_userSet["dir_Report"])

        # If directory exists, remove old files and recreate directory
        except Exception as e:
            print(
                "\n>>> Warning :\n    Directory '%s' already exists,\n    Indicate this project may has been run before.\n" %
                self.info_userSet["dir_Report"])

    """Part I : Quality Control I  -----------------------------------------------"""
    """------ FastQC ------"""

    def FastQC(self, dir_samples):
        print("\n====== This is FastQC module ======")
        # Check [Quality_Control_I] directory
        try:

            # Try to create the directory
            print("\n|- Create '%s' directory" % self.path_reports["Quality_Control_I"])
            os.mkdir(self.path_reports["Quality_Control_I"])

        # If directory exists, remove old files and recreate directory
        except Exception as e:
            print(
                "\n>>> Warning :\n    Directory '%s' already exists,\n    Indicate this project may has been run before.\n" %
                self.path_reports["Quality_Control_I"])

        # FastQC Information
        info = {
            "path_bin": self.path_softwares["FastQC"],
            "dir_input": dir_samples,
            "dir_Result": self.path_results["FastQC"],
            "dir_report": self.path_reports["FastQC"],
            "version": "FastQC v0.9.2",
            "threads": "50",
            "arguments": "",
        }

        # ============<< CORE OF FastQC function >>============#
        # =====================================================#
        # Build running command
        cmd = " ".join(
            [info["path_bin"], "-t", info["threads"], "-o", info["dir_Result"], " ", info["dir_input"] + "/*"])
        # =====================================================#
        # =====================================================#

        # Check [Analysis/] directory
        ppc.dir_check_1(info["dir_Result"])

        # Show the command that will be called on the screen
        print("Execute Command : %s\n" % cmd)

        # Tip for starting running
        print("------ Start running FastQC ------\n")
        print("FastQC is running ...\n")

        # Call the commad

        subprocess.call(cmd, shell=True)

        # Tip for finishing running
        print("------ Finish running FastQC ------\n")

        # Check [Analysis/] directory
        ppc.dir_check_1(info["dir_report"])

        # From [Analysis/] copy results to [Report/]
        print("Copying results to 'Report' directory ...\n")
        for f in os.listdir(info["dir_Result"]):
            shutil.copy(os.path.join(info["dir_Result"], f), info["dir_report"])

        # Provide results path for other modules
        return info["dir_Result"]

    """------ iTools_Fqtools ------"""

    def iTools_Fqtools(self, dir_samples):

        print("\n====== This is iTools_Fqtools module ======")

        # Check [Quality_Control_I] directory
        try:

            # Try to create the directory
            print("\n|- Create '%s' directory" % self.path_reports["Quality_Control_I"])
            os.mkdir(self.path_reports["Quality_Control_I"])

        # If directory exists, remove old files and recreate directory
        except Exception as e:
            print(
                "\n>>> Warning :\n    Directory '%s' already exists\n" %
                self.path_reports["Quality_Control_I"])

        # <iTools-Fqtools> Information
        info = {
            "path_bin": self.path_softwares["iTools-Fqtools-stat"],
            "dir_input": dir_samples,
            "dir_Result": self.path_results["iTools_Fqtools"],
            "dir_report": self.path_reports["iTools_Fqtools"],
            "threads": "50",
        }

        # Check [Analysis/] directory
        ppc.dir_check_1(info["dir_Result"])
        print(info["dir_Result"])

        with open(os.path.join(info["dir_Result"], "raw_data_list.txt"), "w") as list:
            raw_samples = []
            for f in os.listdir(info["dir_input"]):
                if f.endswith("fq") or f.endswith("fastq") or f.endswith("fastq.gz"):
                    list.write(os.path.join(info["dir_input"], f) + "\n")

        # =============<< CORE OF iTools-Fqtools function >>============#
        # ==============================================================#
        # Build running command
        cmd = "%s -InFqList %s -OutStat %s -CPU %s" % (
            info["path_bin"], info["dir_Result"] + "/raw_data_list.txt", info["dir_Result"] + "/itools_fq_stat.txt",
            info["threads"])
        # ==============================================================#
        # ==============================================================#

        # Show command that will be called on the screen
        print("Executing Command : %s\n" % cmd)

        # Tip for starting running
        print("------ Start running iTools-Fqtools ------\n")
        print("iTools-Fqtools is running ...\n")

        # Call the command

        subprocess.call(cmd, shell=True)

        # Tip for finishing running
        print("------ Finish running iTools-Fqtools ------\n")

        # From [Analysis/] copy results to [Report/]
        ppc.dir_check_1(info["dir_report"])

        # From [Analysis/] copy results to [Report/]
        print("Copying results to 'Report' directory ...\n")
        for f in os.listdir(info["dir_Result"]):
            if "stat" in f:
                shutil.copy(os.path.join(info["dir_Result"], f), info["dir_report"])

        # Provide results path for other modules
        return info["dir_Result"]

    """------ Trim_Galore ------"""

    def Trim_Galore(self, dir_samples, sample_name, sample_suffix):
        print("\n====== This is Trim_Galore module ======")

        # Check [Quality_Control_I] directory
        try:

            # Try to create the directory
            print("\n|- Create '%s' directory" % self.path_reports["Quality_Control_I"])
            os.mkdir(self.path_reports["Quality_Control_I"])

        # If directory exists, remove old files and recreate directory
        except Exception as e:
            print(
                "\n>>> Warning :\n    Directory '%s' already exists,\n    Indicate this project may has been run before.\n" %
                self.path_reports["Quality_Control_I"])

        # <Trim_Galore> Information
        info = {
            "path_bin": self.path_softwares["Trim_Galore"],
            "dir_input": dir_samples,
            "dir_Result": self.path_results["Trim_Galore"],
            "dir_report": self.path_reports["Trim_Galore"],
            "version": "version 0.3.3",
            "arguments": {
                "input": "--paired ",
                "output": "--output_dir ",
                "threads": "",
                # %%%%%%%%%%%%%%% lack of fastq argument %%%%%%%%%%%%% #
                "other_set": "--dont_gzip  -q 10 --length 35 -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC -a2 AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT --retain_unpaired --keep ",
            }
        }

        # For R1/R2 data name
        sample_PE = []

        # Find R1 and R2 ends data
        for f in os.listdir(info["dir_input"]):
            if f.startswith(sample_name) and f.endswith(sample_suffix):
                sample_PE.append(f)

        # Get sample path
        path_R1 = os.path.join(info["dir_input"], sample_PE[0])
        path_R2 = os.path.join(info["dir_input"], sample_PE[1])

        # Check if paired-end sample data exist
        if not os.path.exists(path_R1) and not os.path.exists(path_R2):
            print(">>> Error : \n    Can not find %s or %s\n" % (path_R1, path_R2))
            exit()

        # Check if two files belong to the same sample
        elif not sample_PE[0].split("R1")[0] == sample_PE[1].split("R2")[0]:
            print(">>> Error : \n    Two files belong to different samples %s or %s\n" % (sample_PE[0], sample_PE[0]))
            exit()

        else:
            print("|-These two files of reads will be trimmed :\n    %s\n    %s\n" % (sample_PE[0], sample_PE[1]))

        # ============<< CORE OF Trim_Galore function >>============#
        # ==========================================================#
        # Build running command
        cmd = " ".join(
            [info["path_bin"], info["arguments"]["other_set"], info["arguments"]["output"], info["dir_Result"],
             info["arguments"]["input"], path_R1, path_R2])
        # ==========================================================#
        # ==========================================================#

        # Check [Analysis/] directory
        ppc.dir_check_1(info["dir_Result"])

        # Show command that will be called on the screen
        print("Execute Command : %s\n" % cmd)

        # Tip for starting running
        print("------ Start running Trim_Galore ------\n")
        print("Trim_Galore is running ...\n")

        # Call the command

        subprocess.call(cmd, shell=True)

        # Tip for finishing running
        print("------ Finish running Trim_Galore ------\n")

        # Check [Analysis/] directory
        ppc.dir_check_1(info["dir_report"])

        # From [Analysis/] copy results to [Report/]
        print("Copying results to 'Report' directory ...\n")
        for r in os.listdir(info["dir_Result"]):
            if r.endswith("trimming_report.txt"):
                shutil.copy(os.path.join(info["dir_Result"], r), info["dir_report"])

        # Provide results path for other modules
        return info["dir_Result"]

    def fastx_toolkits(self):
        pass

    """Part II : Mapping ---------------------------------------------------------"""
    """------ HISAT2 ------"""

    def HISAT2(self, sample_name, sample_suffix):
        print("\n====== This is HISAT2 module ======")

        # Check [Alignment] directory
        try:

            # Try to create the directory
            print("\n|- Create '%s' directory" % self.path_reports["Alignment"])
            os.mkdir(self.path_reports["Alignment"])

        # If directory exists, remove old files and recreate directory
        except Exception as e:
            print(
                "\n>>> Warning :\n    Directory '%s' already exists,\n    Indicate this project may has been run before.\n" %
                self.path_reports["Alignment"])

        ref = None
        # Judge which speices the samples belong
        for s in self.info_reference:
            if self.info_userSet["species"] in s:
                ref = self.info_reference[s]
                print("\n|- '%s' reference '%s' will be used to mapping\n" % (self.info_userSet["species"], ref))
                break

        # Check if reference exist
        if ref == None:
            print(">>> Error :\n    There is no reference of %s, please check ...\n" % self.info_userSet["species"])
            exit()

        # <HISAT2> Information
        info = {
            "path_bin": self.path_softwares["HISAT2"],
            "dir_input": self.path_results["Trim_Galore"],
            "dir_Result": self.path_results["HISAT2"],
            "dir_report": self.path_reports["HISAT2"],
            "dir_refIndex": ref,
            "version": "version 2.0.5",
            "arguments": {
                "threads": "30",
            }
        }

        # For storing R1/R2 data name
        sample_PE = []

        # Find R1 and R2 ends data
        for f in os.listdir(info["dir_input"]):
            if f.startswith(sample_name) and f.endswith(sample_suffix):
                sample_PE.append(f)

        # Get sample path
        path_R1 = os.path.join(info["dir_input"], sample_PE[0])
        path_R2 = os.path.join(info["dir_input"], sample_PE[1])

        # Name HISAT2 results files
        name_sam = "%s/%s_hisat2.sam" % (info["dir_Result"], sample_name)
        name_stat = "%s/%s_hisat2_Report.txt" % (info["dir_Result"], sample_name)

        # Check if paired-end sample data exist
        if not os.path.exists(path_R1) and not os.path.exists(path_R2):
            print(">>> Error : \n    Can not find %s or %s\n" % (path_R1, path_R2))
            exit()

        # Check if two files belong to the same sample
        elif not sample_PE[0].split("R1")[0] == sample_PE[1].split("R2")[0]:
            print(">>> Error : \n    Two files belong to different samples %s or %s\n" % (sample_PE[0], sample_PE[0]))
            exit()

        else:
            print(
                "|-These two files of reads will be used to mapping :\n    %s\n    %s\n" % (sample_PE[0], sample_PE[1]))

        # =============<< CORE OF HISAT2 function >>============#
        # ======================================================#
        # Build running command
        cmd = "%s -p %s --dta-cufflink -q -x %s -1 %s -2 %s -S %s 2> %s" % (
            info["path_bin"], info["arguments"]["threads"], info["dir_refIndex"], path_R1, path_R2, name_sam, name_stat)
        # ======================================================#
        # ======================================================#

        # Check [Analysis/] directory
        ppc.dir_check_1(info["dir_Result"])

        # Show command that will be called on the screen
        print("Execute Command : %s\n" % cmd)

        # Tip for starting running
        print("------ Start running HISAT2 ------\n")
        print("HISAT2 is running ...\n")

        # Call the command
        subprocess.call(cmd, shell=True)

        # Tip for finishing running
        print("------ Finish running HISAT2 ------\n")

        # From [Analysis/] copy results to [Report/]
        ppc.dir_check_1(info["dir_report"])

        # From [Analysis/] copy results to [Report/]
        print("Copying results to 'Report' directory ...\n")
        for f in os.listdir(info["dir_Result"]):
            if "Report" in f:
                shutil.copy(os.path.join(info["dir_Result"], f), info["dir_report"])

        # Provide results path for other modules
        return info["dir_Result"]

    """Part III : Quality Control II ---------------------------------------------"""

    def RSeQC(self):
        pass

    def RNA_SeQC(self):
        pass


"""-- Pipline Control -------------------------------------------------------------"""


# Control the function execution like timing and multiprocess
class Pipline_Control:
    def __init__(self):

        # Numbers of process
        self.processes = 50

        # Waiting time
        self.timeout = 0

    """-- Single process control ------------------------------------------"""

    # Single process running module
    def single_Process(self, func, *args):
        # Show starting time on the screen
        print("\n------ Module start time ------\n %s \n" % time.asctime())

        # Start time-point
        t1 = time.time()

        # ===<< CALL FUNCTION HERE >>===#
        # ==============================#
        try:

            # Execute the function
            func(*args)

        # In case there is something goes wrong
        except Exception as e:
            # Block ' exc_type, exc_obj, exc_tb = sys.exc_info() ' refers to web page below:
            # http://stackoverflow.com/questions/1278705/python-when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
            print(">>> Error :\n    %s \n    Line rasise exception: %s" % (e, sys.exc_info()))
            exit()
        # ==============================#
        # ==============================#

        # Finish time-point
        t2 = time.time()

        # Calculate the consumed time
        consumed_time = round((t2 - t1), 2)

        # Show finishing time on the screen
        print("------ Finish time ------\n %s \n" % time.asctime())

        # Show consumed time on the screen
        print("|-Run time : %s \n" % consumed_time)
        print("=========================\n\n")

    """-- Multiprocess controll -------------------------------------------"""

    # This module refers to the website('site of liaoxuefeng') below:
    # http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431927781401bb47ccf187b24c3b955157bb12c5882d000

    # Multple process running module
    def multi_Processes(self, func, samples, *args):
        # Show starting time on the screen
        print("\n------ Module start time ------\n %s \n" % time.asctime())

        # Start time-point
        t1 = time.time()

        # ===<< MULTIPLE PROCESSES FUNCTION HERE >>===#
        # ==============================#
        try:

            p = multiprocessing.Pool(self.processes)

            for sample_name in samples:
                p.apply_async(func, args=(sample_name, *args))

            p.close()
            p.join()
            # Execute the function


        # In case there is something goes wrong
        except Exception as e:
            # Block ' exc_type, exc_obj, exc_tb = sys.exc_info() ' refers to web page below:
            # http://stackoverflow.com/questions/1278705/python-when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(">>> Error :\n    %s \n    Line rasise exception: %s\n    %s, %s" % (e, exc_tb.tb_lineno, exc_type, exc_obj))
            exit()
            # ==============================#
            # ==============================#

            # Finish time-point
            t2 = time.time()

            # Calculate the consumed time
            consumed_time = round((t2 - t1), 2)

            # Show finishing time on the screen
            print("------ Finish time ------\n %s \n" % time.asctime())

            # Show consumed time on the screen
            print("|-Run time : %s \n" % consumed_time)
            print("=========================\n\n")

            """-- Directory Check -------------------------------------------------"""

    def dir_check_1(self, dir):

        # Check the directory
        try:

            # Try to create the directory
            os.mkdir(dir)
            print("    Create '%s' directory\n\n" % dir)

        # If directory exists, remove old files and recreate directory
        except Exception:

            # Show warnning info and count down
            print("\n>>> Warning :\n")
            for i in range(self.timeout + 1):
                t = str(self.timeout - i)
                print("    Directory '/%s' already exists, it will be remove and recreated in %s s...\n" % (dir, t))
                time.sleep(self.timeout)

            # If the directory already exists, then remove and recreate it
            print("    Delete old directory '/%s' ...\n" % dir)
            try:
                shutil.rmtree(dir)
            except Exception as e:
                print(e)
                print(sys.exc_info())

            # Recreate directory
            print("    Create new directory '/%s' ...\n" % dir)
            try:
                os.mkdir(dir)
            except Exception as  e:
                print(e)
                print(sys.exc_info())

    def dir_check_2(self, dir):

        try:
            # Check if the directory exist
            os.mkdir(dir)

        except Exception:

            # Show warnning info and count down
            print("\n>>> Warning :\n")
            for i in range(self.timeout + 1):
                t = str(self.timeout - i)
                print("    Directory '/%s' already exists, it will be removed and recreated in %s s...\n" % (dir, t))
                time.sleep(0)

            # Remove the existing directory
            shutil.rmtree(dir)

    """-- Sample name acquire ---------------------------------------------"""

    # Check if the directory path assigned by user is exist
    def get_SampleNames(self, path_input):

        # Check if the directory assigned by user is exist
        while not os.path.exists(path_input):
            path_input = input(
                ">>> Error : \n    Raw data directory can't be found, please enter the right path : ")

        # For store sample names and suffixs
        names = []
        suffixs = []
        uniq_names = []
        uniq_suffixs = []

        # When there is no qualified data go on collecting
        while len(names) == 0:

            # List all samples in rawData directory
            files = os.listdir(path_input)

            # Abstract sample name
            for f in files:

                # Exclude other files than ".fastq" and ".fastq.gz"
                if f.endswith(".fastq.gz") or f.endswith(".fastq") or f.endswith(".fasta") or f.endswith(
                        ".fq") or f.endswith(".fa"):

                    try:

                        # Split out names and suffixs
                        name = f.split("_")[0]
                        suffix = f.split(".")[-1]

                        # Collect names and suffixs
                        names.append(name)
                        suffixs.append(suffix)

                    # If there something goes wrong, warn user
                    except Exception as e:
                        print(e)
                        print(sys.exc_info())

            # Remove duplicated names
            uniq_names = list(set(names))
            uniq_suffix = list(set(suffixs))

            # Check if the type of sample files is unique
            if len(uniq_suffix) > 1:
                print(
                    ">>> Warning :\n    There are more than 1 type of file among the sample data : %s\n    Please make sure there is only one type ..." % uniq_suffix)

                # If there are more than one type , then exit
                exit()

            # Check if there is enough sample data or if sample data is single-end
            elif len(suffixs) % 2 != 0:
                print(">>> Warning :\n    These samples are 'Single-End' or lack of sample.\n")

            # Check if sample data is in the directory that user assigned
            elif len(uniq_names) == 0:
                path_input = input(
                    ">>> Error :\n    Sample data can not be found in directory \" %s \", please input a directory that store sample data : " % path_input)
                print()

            # If all things goes well, then tell user this :
            else:
                print("|- These samples are 'Paired-End'\n")

        # Show sample names
        print(
            "|- Samples will be analysis :\n    Sample : %s \n    File Types : %s \n" % (uniq_names, uniq_suffix))

        # Return the names and suffixs
        return uniq_names, uniq_suffix

    """-- Copy files ------------------------------------------------------"""

    def file_copy(self):
        pass


"""-- Running ---------------------------------------------------------------------"""

if __name__ == "__main__":
    start_time = time.time()

    # Instance classes
    ppc = Pipline_Control()
    qc = Quality_Control()

    """-- Execute functions -------------------------------------------------"""

    # Raw data quality assessment
    # ppc.single_Process(qc.FastQC, qc.info_userSet["dir_RawData"])  # FastQC QA
    # ppc.single_Process(qc.iTools_Fqtools, qc.info_userSet["dir_RawData"])  # iTools_Fqtools_Fq_stat include Q20 Q30 GC

    # Trim raw reads(raw data)
    sample_name, sample_suffix = ppc.get_SampleNames(qc.info_userSet["dir_RawData"])  # Acquire raw data names and suffixs
    # ppc.single_Process(qc.Trim_Galore, qc.info_userSet["dir_RawData"], sample_name[0], sample_suffix[0])

    ppc.multi_Processes(qc.Trim_Galore, qc.info_userSet["dir_RawData"], sample_name, sample_suffix[0])

    # Align reads with HISAT2
    # sample_name, sample_suffix = ppc.get_SampleNames(qc.path_results["Trim_Galore"])  # Acquire trimmed data names and suffixs
    # ppc.single_Process(qc.HISAT2, sample_name[0], sample_suffix[0])

    finish_time = time.time()

    pipline_totalTime = round((finish_time - start_time), 2)
    print(
        "\n-----------------------------\nPipline comsumed time: %s s\n-----------------------------\n" % pipline_totalTime)

    print(
        "\n\n====================================== Finish mRNA_QC Pipline ======================================\n\n")

"""
                     ---------------- Pipline ends Here ----------------
"""

"""
- Appendix ------------------------------------------------------------------------





-< Model of software information storing information >-

info = {
    "version"       :   "",
    "dir_input"     :   "",
    "dir_tmp"       :   "",
    "dir_report"    :   "",
    "path_bin"      :   "",
    "arguments"     :   "",
    "threads"       :   "",
}


-< List of softwares >-

self.bin = {
    "Python2.7": "",
    "R": "",
    "Java": "",
    "FastQC": "",
    "Trim_Galore": "",
    "fastx_toolkits": "",
    "HISAT2": "",
    "RSeQC": "",
}


-< Problem left behind >-

>>> Analysis and Report folders will be deleted completely when the pipline restart again, but actually I only need the specific folder to be deleted
>>> Directory removal can not be disrupted
>>> Didn't output excute commands
>>> Didn't have logs
>>> Class ineritant
>>> Cutadapt on server 6# can't be used
>>> FastQC and Trim_Galore can not run at the same time
>>> Trim_Galore can not automatically start FastQC after trimming

2017-02-06
>>> Write another module to check dir at the head of each module

2017-02-07
>>> Write a copy results module
>>> HISAT2 is using rawdata now

2017-02-09
>>> Use makedirs() instead of mkdir(), cause makedirs() can build cascading directories

2017-02-10
>>> Log doesn't exit.
>>> Argument can not be passed.

"""