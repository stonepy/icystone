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



import time
import multiprocessing as MP

class main:

    def __init__(self, config_dict):

        # Start Note
        note_start = """

                              ***************************************
                              *                                     *
                              *  Start mapping with STAR programme  *
                              *                                     *
                              ***************************************


        %s
        """ % time.ctime()
        print(note_start)


        from packages import settings


        # Get necessery Info from 'config.ini' and 'settings.py'
        fastq_dir   = config_dict["section_1"]["4_"].split(" ")[-1]     # Split out the fastq_dir value
        output_dir  = config_dict["section_1"]["5_"].split(" ")[-1]     # Split out the output_dir value
        report_dir  = config_dict["section_1"]["6_"].split(" ")[-1]     # Split out the report_dir value
        Species     = config_dict["section_2"]["2_"].split(" ")[-1]     # Split out the Species value

        STAR_path   = settings.software_dict["STAR"]
        GenomeSTAR  = settings.species_dict[Species]["GenomeSTAR"]
        GTF         = settings.species_dict[Species]["GTF"]

        Threshold   = settings.software_dict["Mapping"]
        nRun        = config_dict["section_4"]["2_samples"].split("\n")[0:-1]   # Convert sample string to sample list
        tab         = ""

        count = 0
        i     = 0






















        # Finish Note
        note_finish = """

                              ****************************************
                              *                                      *
                              *  Finish mapping with STAR programme  *
                              *                                      *
                              ****************************************


        %s
        """ % time.ctime()
        print(note_finish)















"""
_ Log _____________________________________________________________________________

2017-04-17
    1) Import 'settings.py' and get 'congfig_dict' form 'Main_SNP_mRNA'

___________________________________________________________________________________

"""
