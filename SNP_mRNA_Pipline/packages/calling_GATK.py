Info = """

_ Information ____________________________________________________________________

    Name         : Calling_GATK_SNP_mRNA
    Description  : Find SNP/INDEL with GATK programme
    Author       : Hwx
    Version      : V0
    Dev Env      : Red Hat 4.8.5_11/Ubuntu16.04 LTS;Python3.5.3,virtualenv15.1.0
    Finish Date  : 2017_05_03
__________________________________________________________________________________


"""


from packages.process_manager import call_func
from packages.process_manager import multiP_1
from packages.checking        import branchDIR_check
from packages                 import settings
import time



class main:

    def __init__(self, config_dict):

        # Start Note ___________________________________________________________________________________________________
        note_start = """

  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  |                                         |
  |  Start SNP calling with GATK programme  |
  |                                         |
  ===========================================

  %s\n
        """ % time.ctime()
        print(note_start)

        # _ Parameter preparation ______________________________________________________________________________________

        # Get necessery Info from 'config.ini' and 'settings.py'
        self.OutputDir  = config_dict["section_1"]["5_"].split(" ")[-1]     # Split out the OutputDir value
        self.ReportDir  = config_dict["section_1"]["6_"].split(" ")[-1]     # Split out the ReportDir value
        self.Species    = config_dict["section_2"]["2_"].split(" ")[-1]     # Split out the Species value
        self.Samples    = config_dict["section_4"]["2_samples"].split("\n")[0:-1]   # Convert sample string to sample list

        # Get parameters from 'setting.py'
        self.Genome     = settings.species_dict[self.Species]['Genome']         # Genome fasta file
        self.JAVA       = settings.software_dict["JAVA"]         #
        self.GATK       = settings.software_dict["GATK"]         #
        self.Threshold  = settings.software_dict["Calling"]      # Maybe this time it's also no use

        # If "dbSNP" exists, it will be used, only human and mouse for the temporary
        if "dbSNP" in settings.species_dict[self.Species]:
            knownDBsnpGATK = "-D:dbsnp,vcf " + settings.species_dict[self.Species]["dbSNP"]
        else:
            knownDBsnpGATK = ""

        # Use for passing parameters to 'process_manager.py'
        self.para_dict = {
            "Samples"  : self.Samples,
            "nProcess" : len(self.Samples),
            "nThread"  : self.Threshold,
            "CMDs"     : []
        }

        # Make sure the directory for '*.vcf' files exists
        CallingDir = self.OutputDir + "/3_Calling"
        branchDIR_check(CallingDir)     # Directory check

        Step1 = \
            """\n_ Step1 GATK SNP calling _____________________________________________________________________________________\n """

        for sample in self.Samples:

            DIR = "{CallingingDir}/{sample}".format(CallingingDir=CallingDir, sample=sample)
            branchDIR_check(DIR)     # Directory check
            bamFinal_path = "{OutputDir}/{DataPre}/{sample}/{sample}_final.bam".format(OutputDir=self.OutputDir, DataPre="2_DataPre", sample=sample)
            cmd = "{JAVA} -jar {GATK} -T HaplotypeCaller -I {bam} -R {Genome} -nct 10 -o {CallingDir}/{sample}.vcf {knownDBsnpGATK}".format(JAVA=self.JAVA, GATK=self.GATK, bam=bamFinal_path, Genome=self.Genome, CallingDir=CallingDir, sample=sample, knownDBsnpGATK=knownDBsnpGATK)

            self.para_dict["CMDs"].append(cmd)
            print("\n%s\n>>> Executing command:\n" % Step1)
            # print(cmd+"\n")    # for testing

        # Assign GATK tasks
        multiP_1(self.para_dict, call_func)

        """ Copy results to Report Dir """
        # ReportDir = self.ReportDir + "/2_DataPre"

        # Finish Note __________________________________________________________________________________________________
        note_finish = """

  ============================================
  |                                          |
  |  Finish SNP calling with GATK programme  |
  |                                          |
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  %s\n
        """ % time.ctime()
        print(note_finish)





"""
_ Log _____________________________________________________________________________

2017-05-02
    1) Finished 'GATK' coding, tested on Server #6, everything is OK except results
    were empty, maybe becasuse the anmount of sample reads were too small.

2017-05-02
    1) Finished testing on Server #6, everything is OK except results
    were empty, maybe becasuse the anmount of sample reads were too small.
    2) Did not develop 'Varscan' part

___________________________________________________________________________________
"""
