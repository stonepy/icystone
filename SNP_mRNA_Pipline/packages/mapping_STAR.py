Description = """

_ Information ____________________________________________________________________

    Name         : MappingSTAR_SNP_mRNA
    Description  :
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0
    Finish Date  : 2017_04_
__________________________________________________________________________________

"""


from packages.process_manager import call_func
from packages.process_manager import multiP_1
from packages.checking        import branchDIR_check
from packages.checking        import finish_check
from packages                 import settings
import time
import os
import re


class main:

    # Run all parts as the class 'main' being called
    def __init__(self, config_dict):

        # Start Note ___________________________________________________________________________________________________
        note_start = """

                              =======================================
                              |                                     |
                              |  Start mapping with STAR programme  |
                              |                                     |
                              =======================================


        %s
        """ % time.ctime()
        print(note_start)


        """ _ 0. Parameter preparation _____________________________________________________________________________ """
        # Get necessery Info from 'config.ini' and 'settings.py'
        FastqDir    = config_dict["section_1"]["4_"].split(" ")[-1]     # Split out the FastqDir value
        OutputDir   = config_dict["section_1"]["5_"].split(" ")[-1]     # Split out the OutputDir value
        ReportDir   = config_dict["section_1"]["6_"].split(" ")[-1]     # Split out the ReportDir value
        Species     = config_dict["section_2"]["2_"].split(" ")[-1]     # Split out the Species value
        Samples     = config_dict["section_4"]["2_samples"].split("\n")[0:-1]   # Convert sample string to sample list

        # Get parameters from 'setting.py'
        STAR_path   = settings.software_dict["STAR"]
        GenomeSTAR  = settings.species_dict[Species]["GenomeSTAR"]
        GTF         = settings.species_dict[Species]["GTF"]

        nProcess    = int(settings.software_dict["Mapping"][0])     # Value of 'nProcess' is a string
        Threshold   = int(settings.software_dict["Mapping"][1])     # Value of 'Threadhold' is a string
        # nRun        =
        tab         = ""

        # Adjust the process numbers according to the default set and the numbers of samples
        if len(Samples) > nProcess:
            nProcess = len(Samples)

        # Use for passing parameters to 'process_manager.py'
        para_dict = {
            "Samples"  : Samples,
            "nProcess" : nProcess,
            "CMDs"     : []
        }

        # Make sure the directory for mapping result files exists
        MappingDir = OutputDir + "/1_Mapping"
        branchDIR_check(MappingDir)


        Step1 = \
            """ _ STAR alignment Step1 ______________________________________________________________________________________ """

        print("\n%s\n>>> Executing command:\n" % Step1)
        for sample in Samples:
            DIR = "{MappingDir}/{sample}".format(MappingDir=MappingDir, sample=sample)
            branchDIR_check(DIR)
            tab += " {MappingDir}/{sample}/{sample}.step1.SJ.out.tab ".format(MappingDir=MappingDir, sample=sample)     # Very vital, for step 2
            cmd = "{STAR_path} --runThreadN {Threshold} --genomeDir {GenomeSTAR} --readFilesIn {FastqDir}/{sample}_R1.fastq.gz {FastqDir}/{sample}_R2.fastq.gz --readFilesCommand zcat --sjdbGTFfile {GTF} --sjdbOverhang 149 --outFileNamePrefix {MappingDir}/{sample}/{sample}.step1.".format(STAR_path=STAR_path, Threshold=Threshold, GenomeSTAR=GenomeSTAR, FastqDir=FastqDir, sample=sample, GTF=GTF, MappingDir=MappingDir)

            para_dict["CMDs"].append(cmd)
            # print(cmd+"\n")    # for testing

        # Assign STAR step1 tasks
        multiP_1(para_dict, call_func)


        Step2 = \
            """ _ STAR alignment Step2 ______________________________________________________________________________________ """

        print("\n%s\n>>> Executing command:\n" % Step2)
        para_dict["CMDs"] = []
        for sample in Samples:
            DIR = "{MappingDir}/{sample}".format(MappingDir=MappingDir, sample=sample)
            branchDIR_check(DIR)
            cmd = "{STAR_path} --runThreadN {Threshold} --genomeDir {GenomeSTAR} --readFilesIn {FastqDir}/{sample}_R1.fastq.gz {FastqDir}/{sample}_R2.fastq.gz --readFilesCommand zcat --sjdbGTFfile {GTF} --sjdbFileChrStartEnd {tab} --sjdbOverhang 149 --outFileNamePrefix {MappingDir}/{sample}/{sample}.step2.".format(STAR_path=STAR_path, Threshold=Threshold, GenomeSTAR=GenomeSTAR, FastqDir=FastqDir, sample=sample, GTF=GTF, tab=tab, MappingDir=MappingDir)

            para_dict["CMDs"].append(cmd)
            # print(cmd+"\n")    # for testing

        # Assign STAR step2 tasks
        multiP_1(para_dict, call_func)



        """# Finish marker file, haven't developed"""
        # finish_path = os.path.join(OutputDir, "log/%s.finish" % re.split("[/.]", __file__)[-2])
        # with open(finish_path, "w") as finish:
        #     finish.write("Congratulation !")


        # Finish Note __________________________________________________________________________________________________
        note_finish = """

                              ========================================
                              |                                      |
                              |  Finish mapping with STAR programme  |
                              |                                      |
                              ========================================


        %s
        """ % time.ctime()
        print(note_finish)





"""
_ Log _____________________________________________________________________________

2017-04-17
    1) Import 'settings.py' and get 'congfig_dict' from 'Main_SNP_mRNA'

2017-04-21
    1) Finish development, not test

2017-04-25
    1) Fixed 'step 2' issue
    2) Finished, tested.
    3) Did not copy '<sampleName>.step2.Log.final.out' to 'Report/Statistic'

2017-04-27
    1) Copy '*.step2.Log.final.out' to 'Report', but I haven't done it

2017-05-02
    1) Add new function 'finish marker', for finish checking, did not test

2017-05-03
    1) Revised printing Info on the screen

___________________________________________________________________________________
"""
