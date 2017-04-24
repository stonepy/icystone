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
from packages.process_manager import multiP
from packages.checking        import branchDIR_check
from packages                 import settings
import time


class main:

    def __init__(self, config_dict):

        # Start Note
        note_start = """

                              =======================================
                              |                                     |
                              |  Start mapping with STAR programme  |
                              |                                     |
                              =======================================


        %s
        """ % time.ctime()
        print(note_start)


        # Get necessery Info from 'config.ini' and 'settings.py'
        FastqDir    = config_dict["section_1"]["4_"].split(" ")[-1]     # Split out the FastqDir value
        OutputDir   = config_dict["section_1"]["5_"].split(" ")[-1]     # Split out the OutputDir value
        ReportDir   = config_dict["section_1"]["6_"].split(" ")[-1]     # Split out the ReportDir value
        Species     = config_dict["section_2"]["2_"].split(" ")[-1]     # Split out the Species value
        Samples     = config_dict["section_4"]["2_samples"].split("\n")[0:-1]   # Convert sample string to sample list


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


        # _ STAR alignment step 1 _____________________________________________________________________________________
        for sample in Samples:

            DIR = "{OutputDir}/{sample}".format(OutputDir=OutputDir, sample=sample)
            branchDIR_check(DIR)

            tab += " {OutputDir}/{sample}/{sample}.step1.SJ.out.tab ".format(OutputDir=OutputDir, sample=sample)     # Very vital, for step 2

            cmd = "{STAR_path} --runThreadN {Threshold} --genomeDir {GenomeSTAR} --readFilesIn {FastqDir}/{sample}_R1.fastq.gz {FastqDir}/{sample}_R2.fastq.gz --readFilesCommand zcat --sjdbGTFfile {GTF} --sjdbOverhang 149 --outFileNamePrefix {OutputDir}/{sample}/{sample}.step1.".format(STAR_path=STAR_path, Threshold=Threshold, GenomeSTAR=GenomeSTAR, FastqDir=FastqDir, sample=sample, GTF=GTF, OutputDir=OutputDir)

            para_dict["CMDs"].append(cmd)
        # multiP(para_dict, call_func)


        # _ STAR alignment step 2 _____________________________________________________________________________________
        for sample in Samples:

            DIR = "{OutputDir}/{sample}".format(OutputDir=OutputDir, sample=sample)
            branchDIR_check(DIR)

            cmd = "{STAR_path} --runThreadN {Threshold} --genomeDir {GenomeSTAR} --readFilesIn {FastqDir}/{sample}_R1.fastq.gz {FastqDir}/{sample}_R2.fastq.gz --readFilesCommand zcat --sjdbGTFfile {GTF} --sjdbFileChrStartEnd {tab} --sjdbOverhang 149 --outFileNamePrefix {OutputDir}/{sample}/{sample}.step1.".format(STAR_path=STAR_path, Threshold=Threshold, GenomeSTAR=GenomeSTAR, FastqDir=FastqDir, sample=sample, GTF=GTF, tab=tab, OutputDir=OutputDir)

            para_dict["CMDs"].append(cmd)
        multiP(para_dict, call_func)



        # Finish Note
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

2017-04-24
    1
___________________________________________________________________________________
"""
